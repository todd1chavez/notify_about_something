from typing import List, Tuple, Dict
import subprocess
from plyer import notification as pn
import platform

from math_tasks import MathTasks
from english_words import EnglishWords
from english_rules import EnglishRules
from english_phrases import EnglishPhrases
from services import Services, Notification
from notification import NotificationTkinter



notification_topics: List = [
    # MathTasks(),
    EnglishWords(),
    EnglishPhrases(),
    EnglishRules(),
]


def add_notification_to_list(list_of_notifications: List[Notification], information_for_notification: List[Notification]) -> None:
    """ Добавляем уведомление в список """

    for notification in information_for_notification:
        list_of_notifications.append(notification)



def main(arguments: Tuple | None) -> None:
    """ Точка входа """

    list_of_notifications: List[Notification] = []

    for notification_topic in notification_topics:
        if arguments and arguments.module_name == 'english_rules' and not isinstance(notification_topic, EnglishRules): continue
        if arguments and arguments.module_name == 'english_words' and not isinstance(notification_topic, EnglishWords): continue
        if arguments and arguments.module_name == 'english_phrases' and not isinstance(notification_topic, EnglishPhrases): continue

        information_for_notification: List[Notification] = notification_topic.get_information_for_notification(arguments)
        add_notification_to_list(list_of_notifications, information_for_notification)

    NotificationTkinter().show_all_notifications(list_of_notifications)



if __name__ == '__main__':
    arguments: Tuple | None = Services.get_arguments()
    main(arguments)
