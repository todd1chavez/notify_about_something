from abc import ABC, abstractmethod
import os
import time
import subprocess
from dataclasses import dataclass



@dataclass
class Notification:
    title: str
    content: str


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



class BaseClass(Services, ABC):

    @abstractmethod
    def get_information_for_notification(self):
        # Этот метод должен возвращать информацию для уведомления
        # Словарь с двумя полями - заголовок, описание
        pass
