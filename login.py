from telethon import TelegramClient

api_id = 38326898
api_hash = "9570441b95e80737f726440c9b148530"

client = TelegramClient(
    "session",
    api_id,
    api_hash
)

client.start()

print("SUCCESS")