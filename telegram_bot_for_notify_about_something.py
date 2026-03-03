from typing import Dict
import os
import asyncio
import json

from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_ADMIN_ID, TELEGRAM_BOT_TOKEN



NEW_VALUE_FOR_VERB_PAST: int = 1
NEW_VALUE_FOR_WORD_PAST: int = 2

def change_index_for_verbs_past():
    """ Уменьшаем индекс для verbs_past """
    
    project_path: str = os.path.abspath(                 
        os.path.join(os.path.dirname(__file__)) 
    )                                                    
    path_to_db: str = f'{project_path}/db/english_verbs.json'
    with open(path_to_db) as file:
        content: str = file.read()
        db: Dict = json.loads(content)

    last_word_verb_past_number: int = int(db['last_word_verb_past_number'])

    if last_word_verb_past_number != 0:
        new_value: int = last_word_verb_past_number - NEW_VALUE_FOR_VERB_PAST
    else:
        new_value: int = 0

    db['last_word_verb_past_number'] = new_value

    with open(path_to_db, 'w') as file:
        json.dump(db, file)


def change_index_for_words_past():
    """ Уменьшаем индекс для words_past """
    
    project_path: str = os.path.abspath(                 
        os.path.join(os.path.dirname(__file__)) 
    )                                                    
    path_to_db: str = f'{project_path}/db/english_words.json'
    with open(path_to_db) as file:
        content: str = file.read()
        db: Dict = json.loads(content)

    last_word_verb_past_number: int = int(db['last_word_past_number'])

    if last_word_verb_past_number != 0:
        new_value: int = last_word_verb_past_number - NEW_VALUE_FOR_WORD_PAST
    else:
        new_value: int = 0

    db['last_word_past_number'] = new_value

    with open(path_to_db, 'w') as file:
        json.dump(db, file)


def change_index_for_following_words():
    """ Уменьшаем индекс у каждых слов из повторяемых ранее, чтобы повторить их еще раз """

    change_index_for_verbs_past()
    change_index_for_words_past()


async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    @dp.callback_query(F.data == 'again')
    async def handle_again(callback: types.CallbackQuery):
        change_index_for_following_words()
        await callback.message.answer('Index changed successfully')


    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())
