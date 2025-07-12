from telethon.sync import TelegramClient

api_id = 21447109
api_hash = 'fd29bf548f7484cb35925187b61d56b5'

with TelegramClient('session', api_id, api_hash) as client:
    for dialog in client.iter_dialogs():
        print(f"{dialog.id} - {dialog.title}")
