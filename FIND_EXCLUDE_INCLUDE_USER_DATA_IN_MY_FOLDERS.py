from telethon import TelegramClient, functions, types
import socks
import asyncio

api_id = 1
api_hash = 'adasdasd'
proxy = (socks.SOCKS5, '127.0.0.1', 2080)
session_name = 'my_telegram_session'

# Enhanced peer resolver
async def resolve_peers(client, peers):
    results = []
    for peer in peers:
        try:
            entity = await client.get_entity(peer)
            base_info = {
                'id': getattr(entity, 'id', None),
                'type': type(entity).__name__,
            }

            if isinstance(entity, types.User):
                # Extract detailed user info
                user_info = {
                    'first_name': entity.first_name,
                    'last_name': entity.last_name,
                    'username': entity.username,
                    'phone': entity.phone,
                    'is_contact': entity.contact,
                    'is_mutual_contact': entity.mutual_contact,
                    'deleted': entity.deleted,
                    'bot': entity.bot,
                    'verified': entity.verified,
                    'restricted': entity.restricted,
                    'access_hash': entity.access_hash,
                    'lang_code': getattr(entity, 'lang_code', None)
                }
                base_info.update(user_info)
            elif hasattr(entity, 'title'):
                # It's a group, channel, etc.
                base_info['title'] = entity.title
                base_info['username'] = getattr(entity, 'username', None)

            results.append(base_info)
        except Exception as e:
            results.append({'id': None, 'error': str(e)})
    return results

async def main():
    async with TelegramClient(session_name, api_id, api_hash, proxy=proxy) as client:
        try:
            result = await client(functions.messages.GetDialogFiltersRequest())
            for dialog_filter in result.filters:
                if isinstance(dialog_filter, types.DialogFilter):
                    print(f"\n📁 Folder Name: {dialog_filter.title.text}")

                    # ░ Included ░
                    print(f"\n✅ Included:\n")
                    included = await resolve_peers(client, dialog_filter.include_peers)
                    for chat in included:
                        for k, v in chat.items():
                            print(f"  {k}: {v}")
                        print(" " + "-"*40)

                    # ░ Excluded ░
                    print(f"\n❌ Excluded:\n")
                    excluded = await resolve_peers(client, dialog_filter.exclude_peers)
                    for chat in excluded:
                        for k, v in chat.items():
                            print(f"  {k}: {v}")
                        print(" " + "-"*40)

                    # ░ Pinned ░
                    print(f"\n📌 Pinned:\n")
                    pinned = await resolve_peers(client, dialog_filter.pinned_peers)
                    for chat in pinned:
                        for k, v in chat.items():
                            print(f"  {k}: {v}")
                        print(" " + "-"*40)

                    print("=" * 60)
        except Exception as e:
            print(f"⚠️ Error: {e}")

# Run it
if __name__ == '__main__':
    asyncio.run(main())