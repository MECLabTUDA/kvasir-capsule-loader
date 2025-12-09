import json
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent

CONFIG_PATHS = [
    PROJECT_PATH / "config.json",
    Path("~").expanduser() / ".kvasircapsuleloader.json",
]
CONFIG = {}
for path in CONFIG_PATHS:
    if not path.exists():
        continue
    with open(path, "r") as f:
        CONFIG.update(json.load(f))

KVASIR_CAPSULE_PATH = Path(CONFIG["kvasir-capsule-path"]).expanduser()
KVASIR_CAPSULE_PATH.mkdir(exist_ok=True, parents=True)
DEFAULT_RANDOM_SEED = CONFIG.get("random-seed", 1337)
