from dotenv import load_dotenv

from livekit import agents
from livekit.agents import (
    AgentSession,
    Agent,
    RoomInputOptions,
    function_tool,
    RunContext,
)
from livekit.plugins import (
    openai,
    noise_cancellation,
)
from livekit.agents import mcp
from fastmcp import Client


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
            "Greet the user and ask how you can help them and what news he/she wants to find."
            if greet is None
            else greet
        )

    @function_tool()
    async def do_a_query(context: RunContext, query: str) -> dict[str]:
        """
        Retrieve relevant news articles from the vector database.

        Use this function whenever the user asks to look up or search for news,
        financial updates, or information on a specific topic, company, or event.
        Typical trigger phrases include (but are not limited to):
            - "Search for news about <topic>"
            - "Find articles on <company/event>"
            - "Get the latest updates on <subject>"
            - "Look up financial news regarding <keyword>"

        This function accepts a natural language query and searches across stored
        financial news articles. It returns a dictionary containing the most relevant
        results, which may include titles, summaries, media sources, categories, and
        publication details.
        """
        client = Client("https://techeurope-hack-pari-6f861422.alpic.live/")
        async with client:
            result = await client.call_tool(
                "get_articles_with_config", {"query": query}
            )

        return result

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=self.greet)


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(voice="coral"),
        # mcp_servers=[mcp.MCPServerHTTP("http://localhost:8000/mcp")],
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
