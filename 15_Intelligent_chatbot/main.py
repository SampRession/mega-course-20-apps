import sys
import threading

from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
)

from backend import ChatBot

# NOTE: DON'T WANT TO GIVE MY PHONE NUMBER TO GET AN API KEY
# NOTE: SO, IT DOESN'T WORK !


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chatbot = ChatBot()

        self.setWindowTitle("Homemade ChatBot")
        window_min_width = 700
        self.setMinimumSize(window_min_width, 400)

        # Chat area widget
        self.chat_area = QTextEdit(self)
        self.chat_area.setGeometry(15, 15, (window_min_width - 30), 320)
        self.chat_area.setReadOnly(True)

        # Input field widget
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(15, 350, 550, 35)
        self.input_field.returnPressed.connect(self.send_prompt)

        # Send button widget
        self.send_button = QPushButton("Send", self)
        self.send_button.setGeometry(580, 350, 105, 35)
        self.send_button.clicked.connect(self.send_prompt)

        # self.show()

    def send_prompt(self):
        user_input = self.input_field.text()
        self.chat_area.append(f"<p style='color:#333333'>Me: {user_input}</p>")
        self.input_field.clear()

        thread = threading.Thread(
            target=self.get_bot_response, args=(user_input,)
        )
        thread.start()

    def get_bot_response(self, user_input):
        self.response = self.chatbot.get_response(user_input)
        self.show_response()

    def show_response(self):
        self.chat_area.append(
            f"<p style='color:#333333;"
            f"background-color:#E9E9E9'>"
            f"Bot: {self.response}</p>"
        )


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
