import sys
import io
import csv  # عشان نخزن البيانات في ملف CSV

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from telethon import TelegramClient  # type: ignore

api_id = 21447109  # api_id تبعك
api_hash = 'fd29bf548f7484cb35925187b61d56b5'  # api_hash تبعك

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start()
    channel_ids = [-1001989491822, -1001147552061,-1002253053676 ]  # أرقام القنوات

    # نفتح ملف CSV جديد ونكتب البيانات فيه
    with open('news.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['message'])  # اسم العمود

        for channel_id in channel_ids:
            async for message in client.iter_messages(channel_id, limit=10):  # ✅ صح هون!
                if message.text:
                    text = message.text.replace('\n', ' ')
                    writer.writerow([text])

    print("✅ تم حفظ الرسائل في news.csv بنجاح!")

client.loop.run_until_complete(main())

print(f"🔵 بحمّل من القناة: {channel_id}")

