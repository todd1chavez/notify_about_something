from typing import List
import time

import tkinter as tk
import ctypes
from plyer import notification as pn
import requests

from services import Notification
from config import TELEGRAM_ADMIN_ID, TELEGRAM_BOT_TOKEN



class NotificationTkinter:
    """ Показываем уведомление через tkinter """

    def get_content(self, content: str) -> None:
        """ Разделяем вопрос с ответом, если это вопрос и там есть ответ """

        if ':::::' in content:
            return content.split(':::::')
        elif ':' in content:
            return content.split(':')
        else:
            return content



    def create_notify(self, notification: Notification, number_of_notifications: int, notification_number: int) -> None:

        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Мое окно")
        self.root.maxsize(500, 200)
        self.root.overrideredirect(True)  # Убираем рамки окна
        self.root.attributes("-topmost", True)  # Поверх всех окон

        # Настраиваем содержимое
        frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.RIDGE)
        frame.pack(fill=tk.BOTH, expand=True)

        result = self.get_content(notification.content)
        if len(result) == 1:
            message: str = result
            label = tk.Label(frame, text=f'{message}', bg="white", wraplength=350)
        elif len(result) > 1:
            question, answer = result
            label = tk.Label(frame, text=f'{question}', bg="white", wraplength=350)
        else:
            text: str = f'Такой ответ не обрабатывается - {result}'
            raise ValueError(text)

        label.pack(padx=10, pady=(10, 0))


        # Поле ввода
        entry = tk.Entry(frame, width=30)
        entry.pack(padx=10, pady=5, fill="x", expand=True)

        # Обработка нажатия на кнопку "Ок"
        def on_ok():
            entered_text = entry.get()
            # Здесь можно добавить ваш код для обработки текста

            if 'answer' in locals():
                if not entered_text.strip() and len(result) == 3:
                    pn.notify(
                        title=question[:50],
                        message=answer[:50],
                        app_name='time to repeat',
                        timeout=10000
                    )
                    self.root.destroy()
                if not entered_text.strip():
                    pn.notify(
                        title=question[:50],
                        message=answer[:50],
                        app_name='time to repeat',
                        timeout=10000
                    )
                    self.root.destroy()
                if entered_text.strip() == answer: self.root.destroy()
            else:
                self.root.destroy()


        # Кнопки
        button_frame = tk.Frame(frame, bg="white")
        button_frame.pack(pady=5)

        ok_button = tk.Button(button_frame, text="Проверить", command=on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)

        # Получаем размеры окна
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Расчет положения: правый нижний угол с небольшим отступом
        x = screen_width - width - 30
        y = screen_height - height - 45

        # Перемещаем окно в нужную позицию
        self.root.geometry(f"+{x}+{y}")

        # Гарантируем, что окно поверх всех
        ctypes.windll.user32.SetWindowPos(
            ctypes.windll.user32.GetForegroundWindow(),
            -1,  # HWND_TOPMOST
            x,
            y,
            width,
            height,
            0x0001  # SWP_NOSIZE
        )

        self.root.mainloop()



    def show_all_notifications(self, list_of_notifications: List[Notification]) -> None:
        """ Показываем все уведомления """
        
        for count, notification in enumerate(list_of_notifications, 1):
            self.create_notify(notification, number_of_notifications=len(list_of_notifications), notification_number=count)



class NotificationTelegram:
    """ Показываем уведомление через telegram """

    def get_content(self, content: str) -> None:
        """ Разделяем вопрос с ответом, если это вопрос и там есть ответ """

        if ':::::' in content:
            return content.split(':::::')
        elif ':' in content:
            return content.split(':')
        else:
            return content


    def send_message(self, notification: Notification) -> None:
        """ Отправляем сообщение с уведомлением """

        result = self.get_content(notification.content)
        print('result - ', result)
        if len(result) == 1:
            text: str = result
        elif len(result) > 1:
            text, answer = result
        else:
            text: str = f'Такой аргумент не обрабатывается - {result}'
            raise ValueError(text)

        url: str = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
        payload = {
            'chat_id': TELEGRAM_ADMIN_ID,
            'text': text
        }
        requests.post(url, data=payload)


    def show_all_notifications(self, list_of_notifications: List[Notification]) -> None:
        """ Показываем все уведомления """

        for notification in list_of_notifications:
            self.send_message(notification)
            time.sleep(1)
