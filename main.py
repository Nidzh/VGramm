import re

from telethon import TelegramClient, events
from loguru import logger

logger.add('debug.log', format='{time} {level} {message}', encoding='UTF-8')

api_id = "API_ID"
api_hash = "API_HASH"

client = TelegramClient('VGramm', api_id, api_hash)
keywords = ['ui', 'ui/ux', 'дизайнер', 'ищу дизайнера', 'wordpress', 'вордпресс', 'вордпрес', 'редизайн',
            'разработать сайт на тильде', 'разработать сайт на тильда', 'разработать сайт на tilda',
            'создать сайт на tilda', 'создать сайта на тильде', 'создать сайта на тильда', 'дизайнер на tilda',
            'дизайнер на тильде', 'дизайнер на тильду', 'дизайнер', 'ищу дизайнера', 'подрядчика на дизайн',
            'нужен дизайн', 'веб-дизайн', 'веб-дизайнер', 'вебдизайн', 'вебдизайнер', 'дизайнеры', 'ux/ui-дизайн']

bad_keywords = ['#помощь']


@logger.catch()
@client.on(events.NewMessage)
async def my_event_handler(event):
    raw_text = event.raw_text.lower()
    text = re.sub('\W', ' ', event.raw_text.lower())
    logger.debug(f'event: {event}\n'
                 f'format_text: {text}')

    if raw_text == '/help':
        await client.send_message('me', f'Доступные команды:\n\n'
                                                  f'**/help** - `Подсказка`\n\n'
                                                  f'**/all** - `Показать все активные ключевые слова`\n\n'
                                                  f'**/all_bad** - `Показать все активные исключаемые слова`\n\n'
                                                  f'**/add keyword1, keyword2, key word3** - `Добавить ключевые слова в списке. Через запятую, в любом регистре`\n\n'
                                                  f'**/del keyword1, keyword2, key word3** - `Удалить ключевые слова в списке. Через запятую, в любом регистре`\n\n'
                                                  f'**/add_bad keyword1, keyword2, key word3** - `Добавить исключающие слова в списке. Через запятую, в любом регистре`\n\n'
                                                  f'**/del_bad keyword1, keyword2, key word3** - `Удалить исключающие слова в списке. Через запятую, в любом регистре`')


    elif raw_text == '/all':
        await client.send_message('me', f'Использумые ключевые слова: **{keywords}**')

    elif raw_text == '/all_bad':
        await client.send_message('me', f'Использумые исключающие слова: **{bad_keywords}**')

    elif raw_text.startswith('/add_bad'):
        add_keywords = event.raw_text.lower().replace('/add_bad', '').split(',')
        logger.info(f'add_bad_keywords: {add_keywords}')
        if add_keywords[0]:
            for keyword in add_keywords:
                bad_keywords.append(keyword.strip())
                await client.send_message('me',
                                          f'Исключающее слово **{keyword.strip()}** ДОБАВЛЕНО. Все использумые исключающие ключевые слова: {bad_keywords}')
        else:
            await client.send_message('me',
                                      f'Попробуйте ещё раз, но с исключающим словом.')

    elif raw_text.startswith('/del_bad'):
        del_keywords = event.raw_text.lower().replace('/del_bad', '').split(',')
        logger.info(f'del_bad_keywords: {del_keywords}')
        if del_keywords[0]:
            for keyword in del_keywords:
                if keyword.strip() in bad_keywords:
                    bad_keywords.remove(keyword.strip())
                    await client.send_message('me',
                                              f'Исключающее слово **{keyword.strip()}** УДАЛЕНО. Все использумые исключающие слова: {bad_keywords}')
                else:
                    await client.send_message('me',
                                              f'Исключающего слова **{keyword.strip()}** нет в списке')

    elif raw_text.startswith('/add'):
        add_keywords = event.raw_text.lower().replace('/add', '').split(',')
        logger.info(f'add_keywords: {add_keywords}')
        if add_keywords[0]:
            for keyword in add_keywords:
                keywords.append(keyword.strip())
                await client.send_message('me',
                                          f'Ключевое слово **{keyword.strip()}** ДОБАВЛЕНО. Все использумые ключевые слова: {keywords}')
        else:
            await client.send_message('me',
                                      f'Попробуйте ещё раз, но с ключевым словом.')

    elif raw_text.startswith('/del'):
        del_keywords = event.raw_text.lower().replace('/del', '').split(',')
        logger.info(f'del_keywords: {del_keywords}')
        if del_keywords[0]:
            for keyword in del_keywords:
                print(keyword)
                if keyword.strip() in keywords:
                    keywords.remove(keyword.strip())
                    await client.send_message('me',
                                              f'Ключевое слово **{keyword.strip()}** УДАЛЕНО. Все использумые ключевые слова: {keywords}')
                else:
                    await client.send_message('me',
                                              f'Ключевого слова **{keyword.strip()}** нет в списке')  
        else:
            await client.send_message('me',
                                      f'Попробуйте ещё раз, но с исключающим словом.')

    else:
        text_is_bad = False
        for bad_keyword in bad_keywords:
            if bad_keyword in event.raw_text.lower():
                text_is_bad = True
                break
        logger.info(f'text_is_bad: {text_is_bad}')

        for keyword in keywords:
            if len(keyword.split()) == 1:
                if keyword in text.split() and text_is_bad == False:
                    try:
                        await client.forward_messages('me', event.message)
                    except Exception as e:
                        logger.error(f'Exception: {e}')
                        await client.send_message('me', f'Пользовател запретил пересылку своих сообщений.'
                                                                  f'Текст: {event.raw_text}'
                                                                  f'Отправитель: {event.get_sender()}'
                                                                  f'Ищи в чате: {event.get_chat()}')

                    break
            
            elif len(keyword.split()) > 1:
                if keyword in text and text_is_bad == False:
                    await client.forward_messages('me', event.message)
                    break

client.start()
client.run_until_disconnected()
