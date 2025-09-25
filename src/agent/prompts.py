from pathlib import Path
SYSTEM = Path("prompts/system_therapist.md").read_text()

def build_prompt(sensor_ctx: str, user_msg: str, history: list[str]):
    h = "".join(history[-6:])
    return (
        f"<|system|>\n{SYSTEM}\n"
        f"<|user|>\n{sensor_ctx}\n\nUser: {user_msg}\n"
        f"<|history|>\n{h}\n"
        f"<|assistant|>"
    )