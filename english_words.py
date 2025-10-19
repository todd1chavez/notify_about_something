from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
import os
import time
import asyncio
import re
import json
from json.decoder import JSONDecodeError
import subprocess

from services import Notification
from services import BaseClass, Services



def send_notification(notification: Notification) -> None:
    """ Отправляем уведомление """

    subprocess.run([
        'notify-send',
        '-t', '0',
        notification.title,
        notification.content,
    ])


class EnglishWords(BaseClass):
    """ Повторяем английские слова """

    def __init__(self):
        self.module_name: str = 'english_words'
        self.project_path: str = self.get_project_path()
        self.path_to_db: str = f'{self.project_path}/db/english_words.json'


    def save_word(self, all_words_from_file: List[str]) -> None:
        """ Сохраняем слово """

        if os.path.getsize(self.path_to_db) == 0:
            db: Dict = {
                'words': {}
            }
        else:
            with open(self.path_to_db) as file:
                db: Dict = json.loads(file.read())


        for line in all_words_from_file:

            if line in [word.get('line') for word in db['words'].values() if db['words']]:
                """
                subprocess.run([
                    'notify-send',
                    '-t', '0',
                    'Word to repeat',
                    f'The word has already been added - {line}'
                ])
                """
                continue

            current_time: int = round(time.time())
            russian_word, english_word = line.split(':')

            data: Dict = {
                'time': current_time,
                'line': line,
                'russian_word': russian_word,
                'english_word': english_word,
            }
            db['words'][current_time] = data
            time.sleep(0.5)

        with open(self.path_to_db, 'w') as file:
            json.dump(db, file)


    def get_all_words_from_file(self) -> List:
        """ Получаем все слова из файла """

        all_words_from_file: List[str] = []
        path_to_file: str = f'{self.project_path}/list_of_english_words.txt'
        if not os.path.exists(path_to_file):
            text: str = 'Отсутствует файл list_of_english_words.txt'
            notification: Notification = Notification(
                title='Word to repeat',
                content=text
            )
            send_notification(notification)
            exit()

        if os.path.getsize(path_to_file) == 0:
            text: str = f'\nФайл пустой - {path_to_file}\n'
            notification: Notification = Notification(
                title='Word to repeat',
                content=text
            )
            send_notification(notification)
            exit()

        with open(path_to_file) as file:
            if file.read().strip() == '':
                text: str = f'\nФайл пустой - {path_to_file}\n'
                notification: Notification = Notification(
                    title='Word to repeat',
                    content=text
                )
                send_notification(notification)
                exit()

        with open(path_to_file) as file:
            for line in file:
                line: str = line.strip()

                if re.findall(r'^#[а-я]+?\:[a-z]+$', line) or re.findall(r'^# [а-я]+?\:[a-z]+$', line) :
                    continue

                if re.findall(r'^[а-я]+?\:[a-z]+$', line):
                    all_words_from_file.append(line)
                elif re.findall(r'^[a-z]+?\:[а-я]+$', line):
                    all_words_from_file.append(line)
                else:
                    text: str = f'\nСлово записано неправильно - {line}\n'
                    notification: Notification = Notification(
                        title='Word to repeat',
                        content=text
                    )
                    send_notification(notification)
                    exit()


        if not all_words_from_file:
            text: str = f'Нет слов для повторения'
            notification: Notification = Notification(
                title='Word to repeat',
                content=text
            )
            send_notification(notification)
            exit()

        return all_words_from_file


    def get_all_words_from_db(self) -> List[str]:
        """ Получаем все слова из базы данных """
        
        result: List[str] = []

        with open(self.path_to_db) as file:
            content = file.read()
            db = json.loads(content)

        for object_of_word in db['words'].values():
            line = object_of_word['line']
            result.append(line)

        return result


    def get_word_to_repeat(self, all_words_from_file: List[str]) -> str:
        """ Получаем слово для повторения """

        with open(self.path_to_db) as file:
            content = file.read()
            db = json.loads(content)

        last_word_number: int | None = db.get('last_word_number')



        if last_word_number is not None and len(all_words_from_file) == 1:
            line: str = all_words_from_file[0]
            word: str = line.split(':')[0]
            new_last_word_number = 0


        if last_word_number is not None and str(last_word_number):
            last_word_number: int = int(last_word_number) + 1
            if last_word_number == len(all_words_from_file):
                last_word_number: int = 0
                new_last_word_number = -1
            try:
                line: str = all_words_from_file[last_word_number]
                word: str = line.split(':')[0]
                new_last_word_number = last_word_number
            except IndexError:
                line: str = all_words_from_file[0]
                word: str = line.split(':')[0]
                new_last_word_number = 0
        else:
            line: str = all_words_from_file[0]
            word: str = line.split(':')[0]
            new_last_word_number = 0

        db['last_word_number'] = new_last_word_number

        with open(self.path_to_db, 'w') as file:
            json.dump(db, file)

        return word


    def get_translation_of_word(self, arguments: Tuple, all_words_from_file: List[str]) -> str:
        """ Получаем перевод слова """

        word_to_translate: str = arguments.arguments[0]

        for words in all_words_from_file:
            result = re.findall(':' + word_to_translate + '$', words)
            if result: return words.split(':')[0]

        text: str = f'Перевод для "{word_to_translate}" не найден'
        return text


    def get_information_for_notification(self, arguments: Tuple | None) -> Notification:
        """ Получаем информацию для уведомления """

        if arguments and arguments.module_name == self.module_name:
            all_words_from_file: List[str] = self.get_all_words_from_db()
            word = self.get_translation_of_word(arguments, all_words_from_file)
            information_for_notification: Notification = Notification(
                title='Word to repeat',
                content=word
            )
        else:
            all_words_from_file: List[str] = self.get_all_words_from_file()
            self.save_word(all_words_from_file)
            word: str = self.get_word_to_repeat(all_words_from_file)
            information_for_notification: Notification = Notification(
                title='Word to repeat',
                content=word
            )

        return information_for_notification
