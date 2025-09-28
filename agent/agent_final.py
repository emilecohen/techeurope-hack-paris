import argparse
import sys
from functools import partial
from typing import Optional

from dotenv import load_dotenv

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

from openai.types.beta.realtime.session import TurnDetection
from livekit.agents import mcp

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")

    async def on_enter(self) -> None:
        await self.session.generate_reply(
            instructions="Greet the user and ask how you can help them."
        )

    @function_tool()
    async def lookup_weather(
        self,
        context: RunContext,
        location: str,
    ) -> dict[str]:
        """Look up weather information for a given location.

        Args:
            location: The location to look up weather information for.
        """

        return {"weather": "sunny", "temperature_f": 70}


async def entrypoint(ctx: JobContext, avatar_id: Optional[str]) -> None:
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    local_agent_session = AgentSession(
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
    await bey_avatar_session.start(local_agent_session, room=ctx.room)

    await local_agent_session.start(
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
