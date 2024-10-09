import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextEdit, QLabel, QScrollArea, QFrame)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


class ChatBotUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Friendly Chatbot")
        self.setFixedSize(400, 700)  # Size similar to the design

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Background frame with a black color
        background_frame = QFrame(self)
        background_frame.setStyleSheet("background-color: black")  # Black background
        main_layout.addWidget(background_frame)

        # Chat area (scrollable)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_widget.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.chat_widget)
        self.scroll_area.setStyleSheet("background-color: #F4C2C2; border: none;")
        main_layout.addWidget(self.scroll_area)

        # Input field and send button
        input_layout = QHBoxLayout()
        self.text_input = QTextEdit(self)
        self.text_input.setFixedHeight(60)
        self.text_input.setStyleSheet("""
            background-color: #FFFFFF;
            border-radius: 25px;
            padding: 15px;
            font-size: 16px;
        """)
        send_button = QPushButton("Send", self)
        send_button.setStyleSheet("""
            background-color: #F76363;
            color: white;
            border-radius: 25px;
            padding: 18px;
            font-size: 16px;
        """)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.text_input)
        input_layout.addWidget(send_button)
        main_layout.addLayout(input_layout)

        # Start the bot's motivational messages as soon as the window appears
        QTimer.singleShot(1000, self.start_motivational_messages)

    def send_message(self):
        user_message = self.text_input.toPlainText().strip()
        if user_message:
            self.add_chat_bubble(user_message, "user")
            self.text_input.clear()
            self.process_bot_message(user_message)

    def process_bot_message(self, user_message):
        # Handle user's response after the motivational messages
        bot_message = self.chatbot_response(user_message)
        self.add_chat_bubble(bot_message, "bot")

    def start_motivational_messages(self):
        # The series of motivational messages to be sent
        messages = [
            "Hey there! 👋 I just popped in because I sensed something in the air... ✨",
            "Sometimes life throws negativity your way, but guess what? You’re way stronger than that! 💪",
            "You’re amazing, and no hater can change that. 💖",
            "Here’s the deal: You should always remember you’re AWESOME. 🌟",
            "Negativity? Pfft. It’s got nothing on you. 💥",
            "Let’s spread good vibes only! 🎉",
            "Now, do you want more advice or maybe just to chat? 😎"
        ]
        self.delayed_bot_response(messages)

    def delayed_bot_response(self, messages):
        # Send messages one by one with a delay
        for i, msg in enumerate(messages):
            QTimer.singleShot(i * 2000, lambda m=msg: self.add_chat_bubble(m, "bot"))

        # Ask for further advice after the last message
        QTimer.singleShot(len(messages) * 2000, self.ask_for_further_advice)

    def ask_for_further_advice(self):
        self.wait_for_user_response()

    def wait_for_user_response(self):
        # Temporarily enabling input for user response
        self.text_input.setEnabled(True)
        self.text_input.setPlaceholderText("Type your response here...")

    def chatbot_response(self, message):
        response = message.lower()
        if "no" in response or "okay" in response or "fine" in response:
            self.add_chat_bubble("Okay, I'll leave for now... 😌", "bot")
            QTimer.singleShot(2000, lambda: self.add_chat_bubble("But remember, always stay happy! 😊", "bot"))
            QTimer.singleShot(4000, self.close_application)
        else:
            self.add_chat_bubble("Join our site, and we can talk more! 💻", "bot")
            QTimer.singleShot(2000, self.close_application)

    def close_application(self):
        QApplication.quit()

    def add_chat_bubble(self, message, sender):
        # Create a layout for the message bubble
        bubble_layout = QHBoxLayout()
        bubble_layout.setAlignment(Qt.AlignLeft if sender == "bot" else Qt.AlignRight)

        # Add user or bot icon
        icon_label = QLabel(self)
        if sender == "bot":
            icon_label.setPixmap(QPixmap("botg.png").scaled(40, 40, Qt.KeepAspectRatio))  # Bot icon
        else:
            icon_label.setPixmap(QPixmap("user.png").scaled(40, 40, Qt.KeepAspectRatio))  # User icon

        # Add text bubble with updated style for single-line horizontal expansion
        text_label = QLabel(message)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(f"""
            background-color: {"#FF5C5C" if sender == "user" else "#E3A1A1"};  /* Red for user, Grayish pink for bot */
            color: white;
            border-radius: 15px;
            padding: 10px 20px;
            max-width: 500px;  /* Increased width for longer single lines */
            font-size: 16px;
            margin-bottom: 20px;  /* Space between messages */
        """)

        # Add icon and text bubble to the layout
        if sender == "bot":
            bubble_layout.addWidget(icon_label)
            bubble_layout.addWidget(text_label)
        else:
            bubble_layout.addWidget(text_label)
            bubble_layout.addWidget(icon_label)

        # Add the bubble layout to the chat layout
        self.chat_layout.addLayout(bubble_layout)
        self.chat_widget.adjustSize()
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatbot = ChatBotUI()
    chatbot.show()
    sys.exit(app.exec_())
