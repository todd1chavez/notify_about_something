from typing import List, Tuple, Dict
import asyncio

from math_tasks import MathTasks
from english_words import EnglishWords
from english_verbs_past import EnglishVerbsPast
from english_rules import EnglishRules
from english_phrases import EnglishPhrases
from english_verbs import EnglishVerbs
from english_words_past import EnglishWordsPast
from services import Services, Notification
from notification import NotificationTelegram
import telegram_bot_for_notify_about_something



notification_topics: List = [
    EnglishWords(),
    EnglishVerbsPast(),

    MathTasks(),
    # EnglishPhrases(),
    EnglishRules(),

    EnglishWordsPast(),
    EnglishVerbs(),
]


def add_notification_to_list(list_of_notifications: List[Notification], information_for_notification: List[Notification]) -> None:
    """ Добавляем уведомление в список """

    for notification in information_for_notification:
        list_of_notifications.append(notification)


def split_notification_by_topics(list_of_notifications: List[Notification]) -> Dict:
    
    all_notification_topics: Dict = {}

    for notification in list_of_notifications:
        if all_notification_topics.get(notification.subject, None):
            all_notification_topics[notification.subject].append(notification)
        else:
            all_notification_topics[notification.subject] = [notification]
            print(all_notification_topics)

    return all_notification_topics



def main(arguments: Tuple | None) -> None:
    """ Точка входа """

    list_of_notifications: List[Notification] = []

    for notification_topic in notification_topics:
        if arguments and arguments.module_name == 'english_rules' and not isinstance(notification_topic, EnglishRules): continue
        if arguments and arguments.module_name == 'english_words' and not isinstance(notification_topic, EnglishWords): continue
        if arguments and arguments.module_name == 'english_verbs' and not isinstance(notification_topic, EnglishVerbsPast): continue
        # if arguments and arguments.module_name == 'english_phrases' and not isinstance(notification_topic, EnglishPhrases): continue
        # if arguments and arguments.module_name == 'english_verbs' and not isinstance(notification_topic, EnglishVerbs): continue
        if arguments and arguments.module_name == 'english_words_past' and not isinstance(notification_topic, EnglishWordsPast): continue

        information_for_notification: List[Notification] = notification_topic.get_information_for_notification(arguments)
        print(information_for_notification)
        add_notification_to_list(list_of_notifications, information_for_notification)

    list_of_notifications: Dict = split_notification_by_topics(list_of_notifications)
    NotificationTelegram().show_all_notifications(list_of_notifications)



if __name__ == '__main__':
    arguments: Tuple | None = Services.get_arguments()
    main(arguments)

