from typing import Tuple, List
import re
import random

from services import Notification
from services import BaseClass



class MathTasks(BaseClass):
    """ Математические задачи """

    def __init__(self):
        self.module_name: str = 'math_tasks'


    def get_math_expr_without_first_operand(self) -> str:
        """ Получаем математическое выражение без первого операнда """
        
        sign = random.choice(['+', '-'])
        first_number: int = random.randint(2, 100)
        second_number: int = random.randint(2, 100)

        if sign == '-':
            first_number = max([first_number, second_number])
            second_number = min([first_number, second_number])

        result_of_math_expr = eval(f'{first_number} {sign} {second_number}')

        if sign == '-':
            right_answer: str = result_of_math_expr + second_number
        else:
            right_answer: str = result_of_math_expr - second_number

        result: str = f'\n||{right_answer}|| \\{sign} {second_number} \\= {result_of_math_expr}'
        return result


    def get_math_expr_without_second_operand(self) -> str:
        """ Получаем математическое выражение без второго операнда """
        
        sign = random.choice(['+', '-'])
        first_number: int = random.randint(2, 100)
        second_number: int = random.randint(2, 100)

        if sign == '-':
            first_number = max([first_number, second_number])
            second_number = min([first_number, second_number])

        result_of_math_expr = eval(f'{first_number} {sign} {second_number}')

        if sign == '-':
            right_answer: str = first_number - result_of_math_expr
        else:
            right_answer: str = result_of_math_expr - first_number

        result: str = f'\n{first_number} \\{sign} ||{right_answer}|| \\= {result_of_math_expr}'
        return result


    def get_simple_math_expr(self) -> str:
        """ Получаем простое математическое выражение """

        sign = random.choice(['+', '-'])
        first_number: int = random.randint(2, 100)
        second_number: int = random.randint(2, 100)
        result_of_expression = eval(f'{first_number} {sign} {second_number}')

        result: str = f'\n{first_number} \\{sign} {second_number} \\= ||{result_of_expression}||'
        return result


    def get_information_for_notification(self, arguments: Tuple | None) -> List[Notification]:
        """ Получаем информацию для уведомления """

        if arguments and arguments.module_name == self.module_name:
            text: str = 'Не определена логика для этого случая'
            print(text)
            exit()

        methods = [
            self.get_simple_math_expr,
            self.get_math_expr_without_first_operand,
            self.get_math_expr_without_second_operand,
        ]
        math_expr: str = random.choice(methods)()

        information_for_notification: Notification = Notification(
            subject='math_expr',
            title='math_expr',
            content=math_expr
        )
        return [information_for_notification]
