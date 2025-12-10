import json
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent

# Create user config if not available yet
USER_CONFIG_PATH = Path("~").expanduser() / ".kvasircapsuleloader.json"
if not USER_CONFIG_PATH.exists():
    with open(USER_CONFIG_PATH, "w") as f:
        json.dump({}, f)

# Config hierarchy, bottom overwrites top
CONFIG_PATHS = [
    PROJECT_PATH / "config.json",
    USER_CONFIG_PATH,
]

# Load config
CONFIG = {}
for path in CONFIG_PATHS:
    if not path.exists():
        continue
    with open(path, "r") as f:
        CONFIG.update(json.load(f))

# Load and process config values
KVASIR_CAPSULE_PATH = Path(CONFIG["kvasir-capsule-path"]).expanduser()
KVASIR_CAPSULE_PATH.mkdir(exist_ok=True, parents=True)
DEFAULT_RANDOM_SEED = CONFIG.get("random-seed", 1337)
