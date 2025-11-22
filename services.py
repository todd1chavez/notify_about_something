from typing import List, Tuple
from abc import ABC, abstractmethod
import os
import time
import subprocess
from dataclasses import dataclass
from collections import namedtuple
import sys



@dataclass
class Notification:
    title: str
    content: str


@dataclass
class Rule:
    added: int = 0
    id: int = 0
    question: str = ''
    answer: str = ''


class Services:

    def __init__(self) -> None:
        self.perform_necessary_checks()

    def perform_necessary_checks(self) -> None:

        def check_presence_of_all_folders() -> None:
            pass


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        check_presence_of_all_folders()


    def get_project_path(self) -> str:
        """ Получаем путь к проекту """

        project_path: str = os.path.abspath(                 
            os.path.join(os.path.dirname(__file__)) 
        )                                                    
        return project_path


    @classmethod
    def get_arguments(cls) -> Tuple:
        """ Получаем аргументы, переданные в скрипт """
        
        def check_module() -> None:
            nonlocal list_of_arguments
            if not (len(list_of_arguments) > 1): return

            module_name: str = list_of_arguments[1]
            if not (module_name in available_modules):
                text: str = f'Такого модуля нет - {module_name}'
                print(text)
                print('Доступные -', ', '.join(list(available_modules)))
                exit()


        # ВЫШЕ ОПРЕДЕЛЕНИЕ ФУНКЦИЙ

        available_modules: Tuple = ('english_words', 'math_tasks', 'english_rules', 'english_phrases')

        Arguments = namedtuple('Arguments', ['module_name', 'arguments'])
        list_of_arguments: List[str] = sys.argv
        check_module()

        if len(list_of_arguments) >= 4:
            text: str = 'Такое количество аргументов не обрабатывается'
            print(text)
            exit()
        elif len(list_of_arguments) > 2:
            module_name: str = list_of_arguments[1]
            arguments: List[str] = list_of_arguments[2:]
            arguments: Arguments = Arguments(
                module_name=module_name,
                arguments=arguments
            )
            return arguments
        elif len(list_of_arguments) == 2:
            text: str = 'Не было передано аргументов'
            print(text)
            exit()
        else:
            pass



class BaseClass(Services, ABC):

    @abstractmethod
    def get_information_for_notification(self):
        # Этот метод должен возвращать информацию для уведомления
        # Словарь с двумя полями - заголовок, описание
        raise ValueError('Обязательный класс для реализации')
