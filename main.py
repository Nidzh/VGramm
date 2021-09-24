from telethon import TelegramClient, events
import re

# Use your own values from my.telegram.org
api_id = 8687001
api_hash = 'd243535550a3b97eae1bc6fa54b26857'

client = TelegramClient('VGramm', api_id, api_hash)
keywords = ['ui', 'ux', 'ui/ux', '#ui', '#ux', '#ui/ux', 'дизайнер', 'ищу дизайнера']


@client.on(events.NewMessage)
async def my_event_handler(event):

    text = re.sub('\W', ' ', event.raw_text.lower())

    if '.all' in event.raw_text.lower():
        await client.send_message('+79067836944', f'Использумые ключевые слова: {keywords}')
        await client.send_message('+79104778970', f'Использумые ключевые слова: {keywords}')


    elif '.add' in event.raw_text.lower():
        add_keywords = event.raw_text.lower().replace('.add ', '').split(',')
        for keyword in add_keywords:
            keywords.append(keyword.strip())
        await client.send_message('+79067836944',
                                  f'Ключевые слова ДОБАВЛЕНЫ. Все использумые ключевые слова: {keywords}')
        await client.send_message('+79104778970',
                                  f'Ключевые слова ДОБАВЛЕНЫ. Все использумые ключевые слова: {keywords}')

    elif '.del' in event.raw_text.lower():
        del_keywords = event.raw_text.lower().replace('.del ', '').split(',')
        for keyword in del_keywords:
            print(keyword)
            if keyword.strip() in keywords:
                keywords.remove(keyword.strip())
                await client.send_message('+79067836944',
                                          f'Ключевые слова УДАЛЕНЫ. Все использумые ключевые слова: {keywords}')
                await client.send_message('+79104778970',
                                          f'Ключевые слова УДАЛЕНЫ. Все использумые ключевые слова: {keywords}')
            else:
                await client.send_message('+79067836944',
                                          f'Ключевое слово {keyword} нет в списке')
                await client.send_message('+79104778970',
                                          f'Ключевое слово {keyword} нет в списке')


    else:
        for keyword in keywords:
            if len(keyword.split()) == 1:
                if keyword in text.split():
                    await client.forward_messages('+79067836944', event.message)
                    await client.forward_messages('+79104778970', event.message)
                    break
            elif len(keyword.split()) > 1:
                if keyword in text:
                    await client.forward_messages('+79067836944', event.message)
                    await client.forward_messages('+79104778970', event.message)
                    break


client.start()
client.run_until_disconnected()
