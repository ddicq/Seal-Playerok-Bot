"""
Render entrypoint for Seal Playerok Bot.

Render Background Worker has no interactive terminal. This launcher prepares
bot_settings/config.json from environment variables, then starts the original
bot.py without changing its feature code.
"""
import copy
import json
import os
import re
import sys

# On Render, mount a Persistent Disk at /var/data and set SEAL_DATA_DIR=/var/data.
os.environ.setdefault("SEAL_DATA_DIR", "/var/data")

import paths
paths.ensure_dirs()

# Import the project's own default configuration template.
from settings import CONFIG

CONFIG_PATH = paths.CONFIG_FILE

def env(name: str) -> str:
    return os.environ.get(name, "").strip()

def main() -> None:
    activation_code = env("SEAL_ACTIVATION_CODE").upper()
    if not re.fullmatch(r"[A-Z0-9][RB][A-Z0-9]{5}[47]", activation_code):
        raise SystemExit(
            "Render setup incomplete: set SEAL_ACTIVATION_CODE to the valid "
            "8-character activation code issued by @SealPlayerokBot."
        )

    telegram_token = env("TELEGRAM_BOT_TOKEN")
    telegram_password = env("TELEGRAM_BOT_PASSWORD")
    if not telegram_token or not telegram_password:
        raise SystemExit(
            "Render setup incomplete: set TELEGRAM_BOT_TOKEN and "
            "TELEGRAM_BOT_PASSWORD in the Render Environment settings."
        )

    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
        except (OSError, json.JSONDecodeError):
            config = copy.deepcopy(CONFIG.default)
    else:
        config = copy.deepcopy(CONFIG.default)

    # Restore any newly introduced settings keys without discarding user data.
    def restore_missing(current, defaults):
        for key, value in defaults.items():
            if key not in current or type(current[key]) is not type(value):
                current[key] = copy.deepcopy(value)
            elif isinstance(value, dict):
                restore_missing(current[key], value)

    restore_missing(config, CONFIG.default)

    config["activation_code"] = activation_code
    config["telegram"]["api"]["token"] = telegram_token
    config["telegram"]["bot"]["password"] = telegram_password

    # Optional Playerok credentials. If omitted, they can be configured later
    # through the bot's existing Telegram interface.
    optional_fields = (
        ("PLAYEROK_API_TOKEN", "playerok", "api", "token"),
        ("PLAYEROK_COOKIES", "playerok", "api", "cookies"),
        ("PLAYEROK_USER_AGENT", "playerok", "api", "user_agent"),
        ("PLAYEROK_PROXY", "playerok", "api", "proxy"),
        ("TELEGRAM_API_MODE", "telegram", "api", "mode"),
        ("TELEGRAM_PROXY", "telegram", "api", "proxy"),
        ("TELEGRAM_CUSTOM_API_URL", "telegram", "api", "custom_api_url"),
    )
    for env_name, *keys in optional_fields:
        value = env(env_name)
        if value:
            target = config
            for key in keys[:-1]:
                target = target[key]
            target[keys[-1]] = value

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    temp_path = CONFIG_PATH + ".render-tmp"
    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp_path, CONFIG_PATH)

    print("[Render] Persistent data directory:", os.environ["SEAL_DATA_DIR"])
    print("[Render] Configuration prepared. Starting original bot.py...", flush=True)

    # Keep the original bot entrypoint and all original features.
    import runpy
    runpy.run_path(os.path.join(paths.ROOT_DIR, "bot.py"), run_name="__main__")


if __name__ == "__main__":
    main()
