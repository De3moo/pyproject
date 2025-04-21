from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel, QStackedWidget, QStyle
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
import sys


class IconButton(QPushButton):
    """Custom button to hold an icon and optional text"""
    def __init__(self, icon, text, parent=None):
        super().__init__(text, parent)
        self.full_text = text
        self.setIcon(icon)
        self.setIconSize(QSize(24, 24))
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #7A5FD2;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 8px;
                font-size: 16px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #9276E6;
            }
        """)

    def update_text_visibility(self, show_text):
        self.setText(self.full_text if show_text else "")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Helpdesk Ticketing System")
        self.setGeometry(100, 100, 900, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar_widget = QWidget()
        self.sidebar_expanded_width = 200
        self.sidebar_collapsed_width = 60
        self.sidebar_widget.setFixedWidth(self.sidebar_expanded_width)
        self.sidebar_widget.setStyleSheet("background-color: #5D3FD3;")

        self.sidebar_layout = QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_layout.setContentsMargins(10, 20, 10, 20)
        self.sidebar_layout.setSpacing(15)

        self.burger_button = QPushButton("☰")
        self.burger_button.setFixedHeight(40)
        self.burger_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 24px;
                border: none;
                text-align: left;
                padding-left: 5px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        self.burger_button.setCursor(Qt.PointingHandCursor)
        self.burger_button.clicked.connect(self.toggle_sidebar)
        self.sidebar_layout.addWidget(self.burger_button)

        self.nav_buttons = []

        self.btn_page1 = IconButton(self.style().standardIcon(getattr(QStyle, "SP_ComputerIcon")), "Home")
        self.btn_page2 = IconButton(self.style().standardIcon(getattr(QStyle, "SP_FileIcon")), "Documents")
        self.btn_page3 = IconButton(self.style().standardIcon(getattr(QStyle, "SP_FileDialogDetailedView")), "Settings")

        self.nav_buttons.extend([self.btn_page1, self.btn_page2, self.btn_page3])

        for btn in self.nav_buttons:
            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()

        self.stack = QStackedWidget()
        self.page1 = self.create_home_page()
        self.page2 = self.create_page("📄 Welcome to Documents Page")
        self.page3 = self.create_page("⚙️ You are viewing Settings Page")

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)

        self.btn_page1.clicked.connect(lambda: self.stack.setCurrentWidget(self.page1))
        self.btn_page2.clicked.connect(lambda: self.stack.setCurrentWidget(self.page2))
        self.btn_page3.clicked.connect(lambda: self.stack.setCurrentWidget(self.page3))

        main_layout.addWidget(self.sidebar_widget)
        main_layout.addWidget(self.stack)

        self.sidebar_expanded = True

    def toggle_sidebar(self):
        start_width = self.sidebar_widget.width()
        end_width = self.sidebar_collapsed_width if self.sidebar_expanded else self.sidebar_expanded_width

        self.animation = QPropertyAnimation(self.sidebar_widget, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.setEasingCurve(QEasingCurve.InOutCubic)
        self.animation.start()

        for btn in self.nav_buttons:
            btn.update_text_visibility(not self.sidebar_expanded)

        self.sidebar_expanded = not self.sidebar_expanded

    def create_page(self, text):
        page = QWidget()
        layout = QVBoxLayout(page)
        label = QLabel(text)
        label.setStyleSheet("font-size: 24px;")
        layout.addWidget(label, alignment=Qt.AlignCenter)
        return page

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        title = QLabel("\U0001F3AB Helpdesk Ticketing System")
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        subtitle = QLabel("Welcome back! Manage complaints, track progress, and resolve issues efficiently.")
        subtitle.setStyleSheet("font-size: 16px; color: gray;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        stats = QWidget()
        stats_layout = QHBoxLayout(stats)
        stats_layout.setSpacing(20)

        def make_stat_box(title, value, color):
            box = QWidget()
            box.setStyleSheet(f"""
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
            """)
            box_layout = QVBoxLayout(box)
            box_title = QLabel(title)
            box_title.setStyleSheet("color: white; font-size: 14px;")
            box_value = QLabel(str(value))
            box_value.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
            box_layout.addWidget(box_title)
            box_layout.addWidget(box_value)
            return box

        stats_layout.addWidget(make_stat_box("Open Tickets", 8, "#FF8C42"))
        stats_layout.addWidget(make_stat_box("Resolved", 23, "#4CAF50"))
        stats_layout.addWidget(make_stat_box("Pending", 5, "#FFC107"))

        layout.addWidget(stats)

        new_ticket_btn = QPushButton("\u2795 New Ticket")
        new_ticket_btn.setStyleSheet("""
            QPushButton {
                background-color: #5D3FD3;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #7A5FD2;
            }
        """)
        new_ticket_btn.setCursor(Qt.PointingHandCursor)
        layout.addWidget(new_ticket_btn, alignment=Qt.AlignLeft)

        recent_label = QLabel("\U0001F4CB Recent Activity")
        recent_label.setStyleSheet("font-size: 18px; margin-top: 20px;")
        layout.addWidget(recent_label)

        recent_placeholder = QLabel("No recent tickets.")
        recent_placeholder.setStyleSheet("font-size: 14px; color: gray;")
        layout.addWidget(recent_placeholder)

        return page


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
