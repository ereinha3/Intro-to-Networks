import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / "routers.env"

# Try to load variables from routers.env first; fall back to default .env semantics.
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
else:
    load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def _resolve_input_dir(raw_path: str) -> Path:
    candidate = Path(raw_path)
    if not candidate.is_absolute():
        candidate = (PROJECT_ROOT / candidate).resolve()
    return candidate


HOST = os.getenv("HOST", "127.0.0.1")

PORT_R2 = int(_require_env("PORT_R2"))
PORT_R3 = int(_require_env("PORT_R3"))
PORT_R4 = int(_require_env("PORT_R4"))
PORT_R5 = int(_require_env("PORT_R5"))
PORT_R6 = int(_require_env("PORT_R6"))

INPUT_DIR = _resolve_input_dir(os.getenv("INPUT_DIR", "./input"))


