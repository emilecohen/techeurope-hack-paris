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
    def __init__(self, instructions: str = None, greet: str = None) -> None:
        super().__init__(
            instructions=(
                "You are a helpful voice AI assistant that speaks english."
                if instructions is None
                else instructions
            )
        )
        self.greet = (
            "Greet the user and ask how you can help them." if greet is None else greet
        )

    @function_tool()
    async def do_a_query(context: RunContext, query: str) -> dict[str]:
        """
        Retrieve relevant news articles from the vector database.

        This function accepts a natural language query and searches
        across stored financial news articles. It returns a dictionary
        containing the most relevant results, which may include titles,
        summaries, media sources, categories, and publication details.
        """
        client = Client("https://techeurope-hack-pari-6f861422.alpic.live/")
        async with client:
            result = await client.call_tool(
                "get_articles_with_config", {"query": query}
            )

        system_instructions, articles = result.content[0].text.split("=" * 50)

        return (
            Assistant(
                instructions=system_instructions,
                greet=f"When you start you will summarize the news that i will send you {articles}",
            ),
            "Transferring to news agent",
        )

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=self.greet)


async def entrypoint(ctx: JobContext, avatar_id: Optional[str]) -> None:
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="alloy",
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
            entrypoint_fnc=partial(entrypoint, avatar_id=args.avatar_id),
            worker_type=WorkerType.ROOM,
        )
    )
