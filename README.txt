

list_of_english_words.txt - файл модуля english_words.py. Английские слова, по которым идет
  повторение в текущий момент.

list_of_english_rules.txt - файл модуля english_rules.py. Правила по английскому, по которым идет
  повторение в текущий момент.

list_of_english_phrases.txt - файл модуля english_words.py. Часто используемые английские фразы, по которым идет
  повторение в текущий момент.


db - папка где хранятся все данные проекта. Каждый файл папки должен быть формата json.

db/english_words.json - файл модуля english_words.py. Используется для хранения английских
  слов, которые повторялись когда-то.

db/english_phrases.json - файл модуля english_words.py. Используется для хранения часто используемых фраз английского
  языка, которые повторялись когда-то.


check_english_word.sh - файл модуля english_words.py. Используется для проверки перевода указанного слова.
  Команда для создания символьной ссылки - sudo ln -s /home/me/foo/utility/notify_about_something/check_english_word.sh /usr/bin/cew

check_english_rule.sh - файл модуля english_rules.py. Используется для проверки ответа на показанный вопрос
  Команда для создания символьной ссылки - sudo ln -s /home/me/foo/utility/notify_about_something/check_english_rule.sh /usr/bin/cer

check_english_phrase.sh - файл модуля english_words.py. Используется для проверки перевода указанной фразы.
  Команда для создания символьной ссылки - sudo ln -s /home/me/foo/utility/notify_about_something/check_english_phrase.sh /usr/bin/cep

ew.sh - файл через который запускается весь скрипт. Чтобы он начал работать автоматически, в crontab -e нужно добавить такую строку:
*/30 * * * * /home/me/foo/utility/notify_about_something/ew.sh >> /tmp/cron_log.log 2>&1


в ~/.zshrc добавить алиас, чтобы быстро открывать - alias rew="nv /home/me/foo/utility/notify_about_something/list_of_english_words.txt"
в ~/.zshrc добавить алиас, чтобы быстро открывать - alias rer="nv /home/me/foo/utility/notify_about_something/list_of_english_rules.txt"
в ~/.zshrc добавить алиас, чтобы быстро открывать - alias rep="nv /home/me/foo/utility/notify_about_something/list_of_english_phrases.txt"

export DISPLAY="`grep nameserver /etc/resolv.conf | sed 's/nameserver //'`:0"

#!/bin/bash

# Запустить cron, если не запущен
if ! pgrep -x "cron" > /dev/null; then
  sudo service cron start
fi

ps aux | grep cron
