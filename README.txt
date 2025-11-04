

list_of_english_words.txt - файл модуля english_words.py. Английские слова, по которым идет
  повторение в текущий момент.

list_of_english_rules.txt - файл модуля english_rules.py. Правила по английскому, по которым идет
  повторение в текущий момент.


db - папка где хранятся все данные проекта. Каждый файл папки должен быть формата json.

db/english_words.json - файл модуля english_words.py. Используется для хранения английских
  слов, которые повторялись когда-то.

db/english_rules.json - файл модуля english_rules.py. Используется для хранения правил английского
  языка, которые повторялись когда-то. Сейчас там есть только параметр last_rule_number


check_english_word.sh - файл модуля english_words.py. Используется для проверки перевода указанного слова.
  Команда для создания символьной ссылки - sudo ln -s /home/me/foo/utility/notify_about_something/check_english_word.sh /usr/bin/cew

check_english_rule.sh - файл модуля english_rules.py. Используется для проверки ответа на показанный вопрос
  Команда для создания символьной ссылки - sudo ln -s /home/me/foo/utility/notify_about_something/check_english_rule.sh /usr/bin/cer


ew.sh - файл через который запускается весь скрипт. Чтобы он начал работать автоматически, в crontab -e нужно добавить такую строку:
*/30 * * * * /home/me/foo/utility/notify_about_something/ew.sh >> /tmp/cron_log.log 2>&1


в ~/.zshrc добавить алиас, чтобы быстро открывать - alias rew="nv /home/me/foo/utility/notify_about_something/list_of_english_words.txt"
в ~/.zshrc добавить алиас, чтобы быстро открывать - alias rer="nv /home/me/foo/utility/notify_about_something/list_of_english_rules.txt"
