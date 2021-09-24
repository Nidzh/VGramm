#!/environments/vgramm/venv/bin python

from telethon import TelegramClient, events

import re

api_id = 8687001
api_hash = 'd243535550a3b97eae1bc6fa54b26857'

client = TelegramClient('VGramm', api_id, api_hash)
keywords = ['ui', 'ux', 'ui/ux', 'дизайнер', 'ищу дизайнера']


@client.on(events.NewMessage)
async def my_event_handler(event):

    raw_text = event.raw_text.lower()
    text = re.sub('\W', ' ', event.raw_text.lower())

    if raw_text == '/help':
        await client.send_message('+79067836944', f'Доступные команды:\n\n'
                                                  f'**/help** - `Подсказка`\n\n'
                                                  f'**/all** - `Показать все активные ключевые слова`\n\n'
                                                  f'**/add keyword1, keyword2, key word3** - `Добавить ключевые слова в списке. Через запятую, в любом регистре`\n\n'
                                                  f'**/del keyword1, keyword2, key word3** - `Удалить ключевые слова в списке. Через запятую, в любом регистре`')

        await client.send_message('+79104778970', f'Доступные команды:\n\n'
                                                  f'**/help** - `Подсказка`\n\n'
                                                  f'**/all** - `Показать все активные ключевые слова`\n\n'
                                                  f'**/add keyword1, keyword2, key word3** - `Добавить ключевые слова в списке. Через запятую, в любом регистре`\n\n'
                                                  f'**/del keyword1, keyword2, key word3** - `Удалить ключевые слова в списке. Через запятую, в любом регистре`')


    if raw_text == '/all':
        await client.send_message('+79067836944', f'Использумые ключевые слова: **{keywords}**')
        await client.send_message('+79104778970', f'Использумые ключевые слова: **{keywords}**')


    elif raw_text.startswith('/add'):
        add_keywords = event.raw_text.lower().replace('/add', '').split(',')
        if add_keywords[0]:
            for keyword in add_keywords:
                keywords.append(keyword.strip())
                await client.send_message('+79067836944',
                                      f'Ключевое слово **{keyword.strip()}** ДОБАВЛЕНО. Все использумые ключевые слова: {keywords}')
                await client.send_message('+79104778970',
                                      f'Ключевое слово **{keyword.strip()}** ДОБАВЛЕНО. Все использумые ключевые слова: {keywords}')
        else:
            await client.send_message('+79067836944',
                                      f'Попробуйте ещё раз, но с ключевым словом.')
            await client.send_message('+79104778970',
                                      f'Попробуйте ещё раз, но с ключевым словом.')

    elif raw_text.startswith('/del'):
        del_keywords = event.raw_text.lower().replace('/del', '').split(',')
        if del_keywords[0]:
            for keyword in del_keywords:
                print(keyword)
                if keyword.strip() in keywords:
                    keywords.remove(keyword.strip())
                    await client.send_message('+79067836944',
                                              f'Ключевое слово **{keyword.strip()}** УДАЛЕНО. Все использумые ключевые слова: {keywords}')
                    await client.send_message('+79104778970',
                                              f'Ключевое слово **{keyword.strip()}** УДАЛЕНО. Все использумые ключевые слова: {keywords}')
                else:
                    await client.send_message('+79067836944',
                                              f'Ключевого слова **{keyword.strip()}** нет в списке')
                    await client.send_message('+79104778970',
                                              f'Ключевого слова **{keyword.strip()} **нет в списке')
        else:
            await client.send_message('+79067836944',
                                      f'Попробуйте ещё раз, но с ключевым словом.')
            await client.send_message('+79104778970',
                                      f'Попробуйте ещё раз, но с ключевым словом.')

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
