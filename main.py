from typing import List, Tuple, Dict
import subprocess

from english_words import EnglishWords
from services import Services, Notification



notification_topics: List = [
    EnglishWords(),
]


def main(arguments: Tuple | None) -> None:
    """ Точка входа """

    for notification_topic in notification_topics:
        information_for_notification: Notification = notification_topic.get_information_for_notification(arguments)
        subprocess.run([
            'notify-send',
            '-t', '0',
            information_for_notification.title,
            information_for_notification.content,
        ])


if __name__ == '__main__':
    arguments: Tuple | None = Services.get_arguments()
    main(arguments)
