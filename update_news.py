import asyncio
from telethon import TelegramClient
import csv
from datetime import datetime
import re

api_id = 21447109
api_hash = 'fd29bf548f7484cb35925187b61d56b5'
channel_ids = [-1001989491822, -1001147552061, -1002253053676]

bad_phrases = [
    "** •┈┈┈┈┈┈┈┈┈┈┈• ✈️@Nabuls_News",
    "** ••┈┈┈┈┈┈┈┈┈┈┈•• 🩵",
    "**❗ •┈┈┈┈┈┈┈┈┈┈┈• ✈️@Nabuls_News",
    " •┈┈┈┈┈┈┈┈┈┈┈• ****✈️****@Nabuls_News**",
    "**•┈┈┈┈┈┈┈┈┈┈┈• ✈️@Nabuls_News",
    "•┈┈┈┈┈┈┈┈┈┈┈• ✈️@Nabuls_News",
    "@News_Nablus1"
]

client = TelegramClient('session_name', api_id, api_hash)

def clean_text(text):
    original_text = text

    for phrase in bad_phrases:
        text = text.replace(phrase, "")

    url_pattern = r'(https?://[^\s]+|www\.[^\s]+|t\.me/[^\s]+|@[^\s]+)'
    text = re.sub(url_pattern, '', text)

    text = re.sub(r'\s+', ' ', text).strip()

    if original_text != text:
    print("🧹 نص مختلف، بنعمل شيء هنا")  # أو أي أكشن بدك إياه

async def update_news():
    # هنا منعنا الطلب يدوي للرقم
    await client.start()

    while True:
        all_messages = []
        # هنا تكمل كودك جوه while
        # مثال:
        print("✅ البوت شغال وبحدث الأخبار...")
        break  # بس عشان ما تصير لوب لا نهائي أثناء التجربة


    while True:
        all_messages = []
        for channel_id in channel_ids:
            print(f"📡 بجيب من القناة: {channel_id}")
            async for message in client.iter_messages(channel_id, limit=50):
                if message.text:
                    date_obj = message.date
                    text = clean_text(message.text)
                    all_messages.append({'date': date_obj, 'message': text})

        all_messages.sort(key=lambda x: x['date'], reverse=True)

        with open('news.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'message'])
            for msg in all_messages:
                date_str = msg['date'].strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([date_str, msg['message']])

        print("✅ تم تحديث الملف بدون روابط ولا يوزرات 👌")
        await asyncio.sleep(1)

asyncio.run(update_news())
