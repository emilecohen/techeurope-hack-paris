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


@function_tool()
async def set_up_times_agent(context: RunContext) -> dict[str]:
    """Transfer the call to the New York Times Agent, whenever the user mention something can"""
    client = Client("https://techeurope-hack-pari-6f861422.alpic.live/")
    async with client:
        result = await client.call_tool(
            "get_config_instructions",
        )

    return (
        Assistant(
            instructions=result.content[0].text, greet="Times", agentType="Times"
        ),
        "Transferring to The New York Times support",
    )


@function_tool()
async def revert_to_base_agent(context: RunContext) -> dict[str]:
    """Revert the agent call to original settings"""
    return (
        Assistant(),
        "Transferring to Base Agent",
    )


class Assistant(Agent):
    def __init__(
        self, instructions: str = None, greet: str = None, agentType: str = None
    ) -> None:
        super().__init__(
            instructions=(
                "You are a helpful voice AI assistant that speaks english."
                if instructions is None
                else instructions
            ),
            tools=[set_up_times_agent] if agentType is None else [revert_to_base_agent],
        )
        self.greet = (
            "Greet the user and ask how you can help them."
            if greet is None
            else "Introduce yourself as a The New York Times specialist and ask how you can help with their account always mention what tools you have avalible."
        )

    async def on_enter(self) -> None:
        await self.session.generate_reply(instructions=self.greet)


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(voice="coral"),
        mcp_servers=[mcp.MCPServerHTTP("http://localhost:8000/mcp")],
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
