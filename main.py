from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

api_id = 29624898
api_hash = '5b4a9c274b2d7bc48847d527b2721330'

source_channel = -1001220837618
target_channel = -1002771892101

client = TelegramClient('forwarder_session', api_id, api_hash)

KEYWORDS = ['tp1', 'tp2', 'tp3', 'sl']

# store the last SIGNAL ALERT msg id from the source and the forwarded id
latest_signal_map = {}

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    global latest_signal_map

    msg = event.message
    if not msg.text:
        return

    text = msg.text.lower()

    # 🚨 If it's a SIGNAL ALERT
    if 'signal alert' in text:
        sent = await client.send_message(target_channel, msg.text)
        latest_signal_map[msg.id] = sent.id
        print(f"✅ SIGNAL ALERT forwarded (text only) — id {msg.id}")
        return

    # 📌 If it's a reply with TP/SL
    if any(k in text for k in KEYWORDS) and msg.reply_to_msg_id:
        original_id = msg.reply_to_msg_id
        if original_id in latest_signal_map:
            forwarded_reply_to = latest_signal_map[original_id]

            if msg.media and isinstance(msg.media, (MessageMediaPhoto, MessageMediaDocument)):
                await client.send_file(
                    target_channel,
                    msg.media,
                    caption=msg.text or "",
                    reply_to=forwarded_reply_to
                )
                print(f"📷 Forwarded reply with media — id {msg.id}")
            else:
                await client.send_message(
                    target_channel,
                    msg.text,
                    reply_to=forwarded_reply_to
                )
                print(f"↪️ Forwarded reply (text only) — id {msg.id}")

# ✅ Start bot
client.start()
print("✅ Bot is running...")
client.run_until_disconnected()
