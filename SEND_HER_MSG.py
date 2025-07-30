from telethon import TelegramClient, types
import asyncio
import socks

# Your Telegram developer credentials
api_id = 1
api_hash = 'DASD'
session_name = 'my_telegram_session'
proxy = (socks.SOCKS5, '127.0.0.1', 2080)

# Bahar's user_id and access_hash
user_id = 2
access_hash = 312323  # Must be int, not a string
message_text = "Hell This is a test message from my Telethon script 😊"

async def main():
    async with TelegramClient(session_name, api_id, api_hash, proxy=proxy) as client:
        try:
            # Create an InputPeerUser (target to receive message)
            user = types.InputPeerUser(user_id=user_id, access_hash=access_hash)

            # Send the message
            await client.send_message(user, message_text)

            print("✅ Message sent to user!")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())