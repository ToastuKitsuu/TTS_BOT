import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QSizePolicy, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont


class ChatOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat Overlay")
        self.resize(400, 400)  # You can resize it now!

        # Set solid green background for OBS chroma key
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(0, 255, 0);  /* OBS will key this out */
            }
        """)

        # Layout for chat messages
        self.layout = QVBoxLayout()
        self.layout.setSpacing(5)

        # Scrollable chat area
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        # Chat container inside scroll area
        container = QWidget()
        container.setLayout(self.layout)
        container.setStyleSheet("background: transparent;")

        scroll.setWidget(container)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        self.message_widgets = []
        self.max_messages = 10

    def add_message(self, platform: str, user: str, message: str):
        # Platform color
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

        # Apply better contrast and bold font
        label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 220);
                padding: 6px;
                border-radius: 8px;
                font-size: 16px;
                color: white;
            }
        """)
        font = QFont("Arial", 12)
        font.setBold(True)
        label.setFont(font)

        # Add drop shadow to improve visibility
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setOffset(1, 1)
        shadow.setColor(Qt.black)
        label.setGraphicsEffect(shadow)

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
