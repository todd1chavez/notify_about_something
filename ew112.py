minutes_to_wait: int = 45

def execute_script() -> None:
    pass


with open('/home/me01/foo/utility/notify_about_something/temporary_data_for_script') as file:
    content: str = file.read().strip()


if not content:
    value_to_write: int = 0
    execute_script()
elif int(content) < minutes_to_wait:
    value_to_write: int = int(content) + 15
elif int(content) == minutes_to_wait:
    value_to_write: int = 0
    execute_script()


with open('/home/me01/foo/utility/notify_about_something/temporary_data_for_script', 'w') as file:
    file.write(str(value_to_write))
