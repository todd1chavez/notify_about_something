from typing import Dict, List, Tuple
from abc import ABC, abstractmethod
import os
import time
import asyncio
import re
import json
from json.decoder import JSONDecodeError
import subprocess
import xml.etree.ElementTree as ET
import platform
from plyer import notification as pn

from services import Notification, Rule
from services import BaseClass, Services



def send_notification(title: str, content: str, quit: bool = False) -> None:
    """ Отправляем уведомление """

    notification: Notification = Notification(
        title=title,
        content=content
    )

    if platform.system() == 'Windows':
        pn.notify(
            title=notification.title,
            message=notification.content,
            app_name='time to repeat',
            timeout=10000
        )
    else:
        subprocess.run([
            'notify-send',
            '-t', '0',
            notification.title,
            notification.content,
        ])

    if quit: exit()


class EnglishRules(BaseClass):
    """ Повторяем английские правила """

    def __init__(self):
        self.module_name: str = 'english_rules'
        self.project_path: str = self.get_project_path()
        self.path_to_db: str = f'{self.project_path}/db/english_rules.json'


    def save_rules(self, all_rules_from_file: List[Rule]) -> None:
        """ Сохраняем правила """

        if not os.path.exists(self.path_to_db):
            text: str = f'Файл для сохранения правил отсутствует - english_rules.json'
            send_notification('English rule to repeat', text, quit=True)


        if os.path.getsize(self.path_to_db) == 0:
            db: Dict = {
                'rules': {}
            }
        else:
            with open(self.path_to_db, encoding='utf-8') as file:
                db: Dict = json.loads(file.read())


        rules_for_saving: List[Rule] = []

        for rule in all_rules_from_file:

            if rule.question in [rule.get('question') for rule in db['rules'].values()]:
                text: str = f'Попытка повторного добавления - {rule.question}'
                send_notification('English rule to repeat', text, quit=True)

            current_time: int = round(time.time())

            data: Dict = {
                'added': current_time,
                'id': rule.id,
                'question': rule.question,
                'answer': rule.answer
            }
            rules_for_saving.append(data)


        if not rules_for_saving: return

        for rule in rules_for_saving:
            id: int = rule['id']
            db['rules'][id] = rule
            time.sleep(0.5)

        with open(self.path_to_db, 'w') as file:
            json.dump(db, file)


    def check_duplicate_ids(self, list_of_qa_id: List[int]) -> None:
        """ Проверяем есть ли в файле правила с одинаковыми id """

        previous_qa_id: int = 0

        for qa_id in list_of_qa_id:

            if previous_qa_id != 0 and (qa_id - 1) != previous_qa_id:
                text: str = f'Порядок id нарушен - {qa_id}'
                send_notification('English rule to repeat', text, quit=True)

            if qa_id == previous_qa_id:
                text: str = f'Правило с id {qa_id} уже существует'
                send_notification('English rule to repeat', text, quit=True)

            previous_qa_id = qa_id


    def check_id_sequence(self, list_of_qa_id: List[int]) -> None:
        """ Проверяем порядок qa_id """

        if sorted(list_of_qa_id) != list_of_qa_id:
            text: str = f'Нарушена последовательность id'
            send_notification('English rule to repeat', text, quit=True)

        if list_of_qa_id[0] != 1:
            text: str = f'id первого правила должно быть 1'
            send_notification('English rule to repeat', text, quit=True)


    def get_all_rules_from_file(self) -> List[Rule]:
        """ Получаем все правила из файла """

        all_rules_from_file: List[Rule] = []
        path_to_file: str = f'{self.project_path}/list_of_english_rules.txt'

        if not os.path.exists(path_to_file):
            text: str = 'Отсутствует файл list_of_english_rules.txt'
            send_notification('English rule to repeat', text, quit=True)

        if os.path.getsize(path_to_file) == 0:
            text: str = f'\nФайл пустой - {path_to_file}\n'
            send_notification('English rule to repeat', text, quit=True)

        try:
            tree = ET.parse(path_to_file)
            root = tree.getroot()
        except Exception:
            text: str = f'Не удалось открыть файл {path_to_file}'
            send_notification('English rule to repeat', text, quit=True)


        list_of_qa_id: List[int] = []

        for qa in root.findall('qa'):
            qa_id: str = qa.get('id')

            if re.sub(r'\d+', '', qa_id):
                text: str = f'Некорректный id - {qa_id}'
                send_notification('English rule to repeat', text, quit=True)

            list_of_qa_id.append(int(qa_id))

            qa_content: str = qa.text.strip()
            if '#---' in qa_content: continue
            if '# ---' in qa_content: continue

            if not ('---' in qa_content):
                text: str = f'Правило под id {qa_id} добавлено некорректно'
                send_notification('English rule to repeat', text, quit=True)

            qa_content: List = qa_content.split('---')

            if len(qa_content) != 2:
                text: str = f'Правило под id {qa_id} добавлено некорректно'
                send_notification('English rule to repeat', text, quit=True)

            question, answer = [item.strip() for item in qa_content]
            rule: Rule = Rule(id=qa_id, question=question, answer=answer)
            all_rules_from_file.append(rule)

        if not all_rules_from_file:
            text: str = f'Нет правил для повторения'
            send_notification('English rule to repeat', text, quit=True)

        self.check_id_sequence(list_of_qa_id)
        self.check_duplicate_ids(list_of_qa_id)

        return all_rules_from_file


    def add_new_rule_for_repeat(self, all_rules_from_file: List[Rule], rules_to_repeat) -> None:
        """ Добавляем новое правило для повторения """

        with open(self.path_to_db, encoding='utf-8') as file:
            content = file.read()
            db = json.loads(content)

        last_rule_number: int | None = db.get('last_rule_number')


        if last_rule_number is not None and len(all_rules_from_file) == 1:
            rule: Rule = all_rules_from_file[0]
            rule: Tuple = (rule.id, rule.question)
            new_last_rule_number = 0


        if last_rule_number is not None and str(last_rule_number):
            last_rule_number: int = int(last_rule_number) + 1
            if last_rule_number == len(all_rules_from_file):
                last_rule_number: int = 0
                new_last_rule_number = -1
            try:
                rule: Rule = all_rules_from_file[last_rule_number]
                rule: Tuple = (rule.id, rule.question)
                new_last_rule_number = last_rule_number
            except IndexError:
                rule: Rule = all_rules_from_file[0]
                rule: Tuple = (rule.id, rule.question)
                new_last_rule_number = 0
        else:
            rule: Rule = all_rules_from_file[0]
            rule: Tuple = (rule.id, rule.question)
            new_last_rule_number = 0

        db['last_rule_number'] = new_last_rule_number

        with open(self.path_to_db, 'w') as file:
            json.dump(db, file)

        rules_to_repeat.append(rule)


    def add_permanent_words(self, all_words_from_file: List[str], words_to_repeat) -> None:
        """ Добавляем постоянные слова """
        
        for word in all_words_from_file:
            if not re.findall(r'^-', word): continue
            word = word.split(':')[0].strip()
            words_to_repeat.append(word)


    def get_rules_to_repeat(self, all_rules_from_file: List[Rule]) -> List[Tuple]:
        """ Получаем правила для для повторения """

        rules_to_repeat: List[Tuple] = []

        self.add_new_rule_for_repeat(all_rules_from_file, rules_to_repeat) # Добавляем первое правило

        # self.add_permanent_words(all_words_from_file, words_to_repeat)

        return rules_to_repeat


    def get_answer_to_question(self, arguments: Tuple, all_rules_from_file: List[Rule]) -> str:
        """ Получаем ответ к вопросу """

        question_id: str = arguments.arguments[0]

        for rule in all_rules_from_file:
            if rule.id == question_id:
                return rule.answer

        text: str = f'Вопрос не был найден по id {question_id}'
        return text


    def generate_result(self, rules: List[Tuple]) -> List[Notification]:
        """ Формируем результат """

        result: List[Notification] = []

        for rule in rules:

            information_for_notification: Notification = Notification(
                title=f'English rule to repeat ({rule[0]})',
                content=rule[1]
            )
            result.append(information_for_notification)

        return result


    def get_information_for_notification(self, arguments: Tuple | None) -> List[Notification]:
        """ Получаем информацию для уведомления """

        if arguments and arguments.module_name == self.module_name:
            all_rules_from_file: List[Rule] = self.get_all_rules_from_file()
            answer: str = self.get_answer_to_question(arguments, all_rules_from_file)
            information_for_notification: Notification = Notification(
                title='Right answer',
                content=answer
            )
            result = [information_for_notification]
        else:
            all_rules_from_file: List[Rule] = self.get_all_rules_from_file()
            # self.save_rules(all_rules_from_file)
            rules: List[Tuple] = self.get_rules_to_repeat(all_rules_from_file)
            result: List[Notification] = self.generate_result(rules)

        return result
