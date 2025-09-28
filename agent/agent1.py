import argparse
import sys
from functools import partial
from typing import Optional
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    WorkerType,
    cli,
    AgentSession,
    Agent,
    RoomInputOptions,
    function_tool,
    RunContext,
)
from livekit.plugins import (
    bey,
    openai,
    noise_cancellation,
)
from fastmcp import Client
from openai.types.beta.realtime.session import TurnDetection


load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(
        self, instructions: str | None = None, greet: str | None = None
    ) -> None:
        super().__init__(
            instructions=(
                instructions
                if instructions is not None
                else (
                    "You are a helpful voice AI assistant. "
                    "You must always speak clearly in English, and only in English."
                )
            )
        )
        self.greet = (
            greet
            if greet is not None
            else "Hello! How can I help you today? (Please note: I only speak English.)"
        )

    @function_tool()
    async def do_a_query(context: RunContext, query: str) -> dict[str]:
        """
        Retrieve relevant news articles from the vector database using the 'get_articles_with_config' tool.

        Purpose:
            - Always use this function whenever the user asks to look up or search for news,
              financial updates, or information on a specific topic, company, or event.
            - Do NOT search the open internet; rely only on our curated, reliable sources.

        Trigger phrases include (but are not limited to):
            - "Search for news about <topic>"
            - "Find articles on <company/event>"
            - "Get the latest updates on <subject>"
            - "Look up financial news regarding <keyword>"

        Input:
            query (str): A natural language query describing the topic, company, or event.

        Output:
            dict[str]: The most relevant results retrieved from the vector database,
            which may include titles, summaries, media sources, categories, and publication details.

        Notes:
            - Ensure the response adheres to the newsroom style and voice defined in templates.
            - Begin responses with "Welcome to The New York Times" and provide context and nuance.
            - Offer to go deeper: "Would you like a more detailed analysis or related perspectives?"
        """
        client = Client("https://techeurope-hack-pari-6f861422.alpic.live/")
        async with client:
            result = await client.call_tool(
                "get_articles_with_config", {"query": query}
            )

        return result.content[0].text

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=self.greet)


async def entrypoint(ctx: JobContext, avatar_id: Optional[str]) -> None:
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="coral",
            model="gpt-realtime",
            turn_detection=TurnDetection(
                type="server_vad",
                threshold=0.5,
                prefix_padding_ms=300,
                silence_duration_ms=500,
                create_response=True,
                interrupt_response=True,
            ),
        ),
        # mcp_servers=[mcp.MCPServerHTTP("http://localhost:8000/mcp")],
    )

    if avatar_id is not None:
        bey_avatar_session = bey.AvatarSession(avatar_id=avatar_id)
    else:
        bey_avatar_session = bey.AvatarSession()
    await bey_avatar_session.start(session, room=ctx.room)

    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` instead for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description="Run a LiveKit agent with Bey avatar.")
    parser.add_argument("--avatar-id", type=str, help="Avatar ID to use.")
    args = parser.parse_args()

    sys.argv = [sys.argv[0], "dev"]  # overwrite args for the LiveKit CLI
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=partial(
                entrypoint, avatar_id="b5bebaf9-ae80-4e43-b97f-4506136ed926"
            ),
            worker_type=WorkerType.ROOM,
        )
    )
