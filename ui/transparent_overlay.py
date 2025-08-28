import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QSizePolicy, QScrollArea
)
from PyQt5.QtCore import Qt, QTimer


class ChatOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat Overlay")
        self.resize(400, 400)  # Resizable window with title bar

        # Set solid green background (for OBS chroma key)
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(0, 255, 0);  /* OBS will key out this green */
            }
        """)

        # Layout for chat messages
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setLayout(self.layout)
        container.setStyleSheet("background: transparent;")

        scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        self.message_widgets = []
        self.max_messages = 10

    def add_message(self, platform: str, user: str, message: str):
        if platform.lower() == "youtube":
            color = "#FF4444"
        elif platform.lower() == "twitch":
            color = "#9146FF"
        else:
            color = "#FFFFFF"

        label = QLabel()
        label.setText(
            f"<b style='color:{color}'>[{platform.title()}]</b> "
            f"<span style='color:white'>{user}:</span> "
            f"<span style='color:white'>{message}</span>"
        )
        label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 130);  /* semi-transparent message bubbles */
                padding: 6px;
                border-radius: 8px;
                font-size: 16px;
            }
        """)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label.setWordWrap(True)

        self.layout.addWidget(label)
        self.message_widgets.append(label)

        if len(self.message_widgets) > self.max_messages:
            old_label = self.message_widgets.pop(0)
            old_label.deleteLater()

    def test_messages(self):
        self.add_message("youtube", "Sakura", "こんにちは！これはテストです 🗾")
        self.add_message("twitch", "EpicGamer", "Let's gooo 🎮🔥")
        self.add_message("youtube", "Aki", "123 numbers become 一二三 😲")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = ChatOverlay()
    overlay.show()
    QTimer.singleShot(1000, overlay.test_messages)
    sys.exit(app.exec_())
