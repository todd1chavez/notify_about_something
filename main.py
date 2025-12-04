from typing import List, Tuple, Dict
import subprocess
from plyer import notification as pn
import platform

from math_tasks import MathTasks
from english_words import EnglishWords
from english_rules import EnglishRules
from english_phrases import EnglishPhrases
from services import Services, Notification



notification_topics: List = [
    # MathTasks(),
    EnglishWords(),
    EnglishPhrases(),
    EnglishRules(),
]


def show_notification(information_for_notification: List[Notification]) -> None:
    """ Показываем уведомление """

    for notification in information_for_notification:

        if platform.system() == 'Windows':
            pn.notify(
               title=notification.title,
                message=notification.content,
                app_name='Мое приложение',
                timeout=10  # время отображения в секундах
            )
        else:
            subprocess.run([
                'notify-send',
                '-t', '0',
                notification.title,
                notification.content,
            ])


def main(arguments: Tuple | None) -> None:
    """ Точка входа """

    for notification_topic in notification_topics:

        if arguments and arguments.module_name == 'english_rules' and not isinstance(notification_topic, EnglishRules): continue
        if arguments and arguments.module_name == 'english_words' and not isinstance(notification_topic, EnglishWords): continue
        if arguments and arguments.module_name == 'english_phrases' and not isinstance(notification_topic, EnglishPhrases): continue

        information_for_notification: List[Notification] = notification_topic.get_information_for_notification(arguments)
        show_notification(information_for_notification)



if __name__ == '__main__':
    arguments: Tuple | None = Services.get_arguments()
    main(arguments)
