from telethon import TelegramClient, events
import os
import asyncio

api_id = 29624898
api_hash = '5b4a9c274b2d7bc48847d527b2721330'

source_channel = -1001220837618
target_channel = -1002771892101

session_name = os.getenv("SESSION_NAME", "default_session")
client = TelegramClient(session_name, api_id, api_hash)

KEYWORDS = ['tp1', 'tp2', 'tp3', 'sl']

# store the last SIGNAL ALERT msg id from the source and the forwarded id
latest_signal_map = {}

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    global latest_signal_map

    msg = event.message
    text = msg.message
    if not text:
        return

    lowered = text.lower()

    # 🚨 If it's a SIGNAL ALERT
    if 'signal alert' in lowered:
        sent = await client.send_message(target_channel, text)
        latest_signal_map[msg.id] = sent.id
        print(f"✅ SIGNAL ALERT forwarded (text only) — id {msg.id}")
        return

    # 📌 If it's a reply with TP/SL
    if any(k in lowered for k in KEYWORDS) and msg.reply_to_msg_id:
        original_id = msg.reply_to_msg_id
        if original_id in latest_signal_map:
            forwarded_reply_to = latest_signal_map[original_id]

            await client.send_message(
                target_channel,
                text,
                reply_to=forwarded_reply_to
            )
            print(f"↪️ Forwarded reply (text only) — id {msg.id}")

# ✅ Start bot
async def main():
    await client.connect()
    await client.start()  # triggers phone number + code login if needed
    print(f"✅ Logged in — session saved as: {session_name}")
    print(f"✅ Bot is running using session: {session_name}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
