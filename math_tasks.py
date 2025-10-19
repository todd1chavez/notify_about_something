from typing import Tuple
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
        result: str = f'? {sign} {second_number} = {result_of_math_expr}'
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
        result: str = f'{first_number} {sign} ? = {result_of_math_expr}'
        return result


    def get_simple_math_expr(self) -> str:
        """ Получаем простое математическое выражение """

        sign = random.choice(['+', '-'])
        first_number: int = random.randint(2, 100)
        second_number: int = random.randint(2, 100)


        result: str = f'{first_number} {sign} {second_number} = ?'
        return result


    def get_information_for_notification(self, arguments: Tuple | None) -> Notification:
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
            title='Solve the mathematical expression',
            content=math_expr
        )
        return information_for_notification
