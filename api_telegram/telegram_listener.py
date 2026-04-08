from telethon import TelegramClient
import asyncio
import os
from pathlib import Path
from datetime import timezone, timedelta, datetime
from database.database import init_user_table, insert_user_message, clear_table


def _load_env_file():
    env_path = Path(__file__).resolve().parents[1] / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_file()

api_id_raw = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
session_name = os.getenv("TELEGRAM_SESSION_NAME", "session_default")

if not api_id_raw or not api_hash:
    raise RuntimeError("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH in environment.")

try:
    api_id = int(api_id_raw)
except ValueError as exc:
    raise RuntimeError("TELEGRAM_API_ID must be an integer.") from exc

client=TelegramClient(session_name, api_id, api_hash)
async def main():
    await client.connect()
    if not await client.is_user_authorized():
        raise RuntimeError("Telegram session is not authorized. Run login flow first.")
    user_id_map = {}  # Add name and user id's
    #The following function fetches all user id's
    async for dialog in client.iter_dialogs():
        entity = dialog.entity
        if dialog.is_user:
            name=entity.first_name
            user_id_map[name]=entity.id
    #The following code fetches messages and displays them
    since = datetime.now(timezone.utc) - timedelta(days=1)
    for username, userid in user_id_map.items():
        init_user_table(userid)
        clear_table(userid) ##Clears table before adding messages
        try:
            async for message in client.iter_messages(userid):
                if message.date < since:
                    break
                message_id=message.id
                user_id=message.sender_id
                text=message.text or ""
                timestamp=message.date.isoformat()
                from_me=message.out
                insert_user_message(userid, message_id, user_id, text, timestamp, from_me) #Adds messages in table
        except Exception as e:
             print(f"No chats available or error: {e}")
    return

def run_api():
    asyncio.run(main())