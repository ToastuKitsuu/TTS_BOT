import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor

class ChatOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(600, 400)
        self.setStyleSheet("background: transparent;")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)

        # Scrollable area
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
        self.max_messages = 10  # keep it clean

    def add_message(self, platform: str, user: str, message: str):
        # Determine color
        if platform.lower() == "youtube":
            color = "#FF4444"  # Red
        elif platform.lower() == "twitch":
            color = "#9146FF"  # Purple
        else:
            color = "#FFFFFF"  # Default white

        label = QLabel()
        label.setText(f"<b style='color:{color}'>[{platform.title()}]</b> <span style='color:white'>{user}:</span> <span style='color:white'>{message}</span>")
        label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 130);
                padding: 6px;
                border-radius: 8px;
                font-size: 16px;
            }
        """)
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        label.setWordWrap(True)

        self.layout.addWidget(label)
        self.message_widgets.append(label)

        # Remove old messages
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

    # Example: Add test messages on timer
    QTimer.singleShot(1000, overlay.test_messages)

    sys.exit(app.exec_())
# ui/transparent_overlay.py