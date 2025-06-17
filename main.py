from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

api_id = 29624898
api_hash = '5b4a9c274b2d7bc48847d527b2721330'

source_channel = -1001220837618
target_channel = -1002771892101

client = TelegramClient('forwarder_session', api_id, api_hash)

KEYWORDS = ['tp1', 'tp2', 'tp3', 'sl']
latest_signal_map = {}

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    global latest_signal_map

    msg = event.message
    if not msg.text:
        return

    text = msg.text.lower()

    # 🚨 1. Forward SIGNAL ALERT (text + image)
    if 'signal alert' in text:
        sent = await client.send_file(
            target_channel,
            '/mnt/data/NEWSIGNALQS.png',
            caption=msg.text
        )
        latest_signal_map[msg.id] = sent.id
        print(f"✅ Forwarded SIGNAL ALERT w/ image — id {msg.id}")
        return

    # 📌 2. Forward replies (TP/SL) as reply to SIGNAL ALERT
    if any(k in text for k in KEYWORDS) and msg.reply_to_msg_id:
        original_id = msg.reply_to_msg_id
        if original_id in latest_signal_map:
            reply_to = latest_signal_map[original_id]

            if msg.media and isinstance(msg.media, (MessageMediaPhoto, MessageMediaDocument)):
                await client.send_file(
                    target_channel,
                    msg.media,
                    caption=msg.text or "",
                    reply_to=reply_to
                )
                print(f"📷 Reply w/ media → SIGNAL ALERT — id {msg.id}")
            else:
                await client.send_message(
                    target_channel,
                    msg.text,
                    reply_to=reply_to
                )
                print(f"↪️ Reply (text only) → SIGNAL ALERT — id {msg.id}")
        return

    print(f"⛔ Skipped — id {msg.id}")

async def start_bot():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ Not authorized — run locally to generate session first")
        return
    print("✅ Bot is live and listening...")
    await client.run_until_disconnected()

client.loop.run_until_complete(start_bot())
