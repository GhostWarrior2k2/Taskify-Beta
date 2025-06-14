# Copyright 2025 Pikes Development
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QLabel, QMessageBox, QSystemTrayIcon, QMenu, QAction, QCheckBox, QComboBox, QRadioButton, QButtonGroup, QTextEdit, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QDateTime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import time
from email.mime.base import MIMEBase
from email import encoders

class Collaboration:
    def __init__(self, parent):
        self.parent = parent
        self.share_button = QPushButton('Share Board')
        self.share_button.clicked.connect(self.share_board)
        self.open_colab_button = QPushButton('Open Colab')
        self.open_colab_button.clicked.connect(self.open_colab)
        from dotenv import load_dotenv
        load_dotenv()
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.password = os.getenv('SENDER_PASSWORD')

    def share_board(self):
        board_name = self.parent.board_list.currentItem().text()
        if board_name:
            user_email = QInputDialog.getText(self.parent, 'Share Board', 'Enter user email:')
            if user_email[1]:
                board_data = self.get_board_data(board_name)
                self.send_board_via_email(user_email[0], board_data)
                QMessageBox.information(self.parent, 'Board Shared', f'Board "{board_name}" shared with {user_email[0]}')
        else:
            QMessageBox.warning(self.parent, 'Error', 'Please select a board')

    def get_board_data(self, board_name):
        for board in self.parent.boards['boards']:
            if board['name'] == board_name:
                return board
        return None

    def send_board_via_email(self, recipient_email, board_data):
        sender_email = os.getenv('SENDER_EMAIL')
        password = os.getenv('SENDER_PASSWORD')
        # sender_email = "taskifyv1@gmail.com"
        # password = "xdsm cfce uhst vzhv"

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = 'Shared Board'

        board_name = board_data['name']
        file_name = f"{board_name}.json"

        with open(file_name, 'w') as f:
            json.dump(board_data, f)

        attachment = MIMEApplication(open(file_name, 'rb').read())
        attachment.add_header('Content-Disposition', f'attachment; filename= {file_name}')
        msg.attach(attachment)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.sender_email, self.password)
        text = msg.as_string()
        server.sendmail(self.sender_email, receiver_email, text)
        server.quit()

        os.remove(file_name)

    def open_colab(self):
        file_name, _ = QFileDialog.getOpenFileName(self.parent, 'Open Shared Board', '', 'JSON Files (*.json)')

        if file_name:
            with open(file_name, 'r') as f:
                shared_board_data = json.load(f)

            self.shared_taskify_app = TaskifyApp()
            self.shared_taskify_app.boards['boards'] = [shared_board_data]
            self.shared_taskify_app.load_board_list()
            self.shared_taskify_app.show()





class ContactForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        from dotenv import load_dotenv
        load_dotenv()
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.password = os.getenv('SENDER_PASSWORD')
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Contact Us')
        self.apply_dark_theme()

        layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Name')
        layout.addWidget(self.name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('Phone Number')
        layout.addWidget(self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email')
        layout.addWidget(self.email_input)

        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText('Message')
        layout.addWidget(self.message_input)

        send_button = QPushButton('Send')
        send_button.clicked.connect(self.send_email)
        layout.addWidget(send_button)

        self.setLayout(layout)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2f343f;
                color: #ffffff;
            }

            QLabel {
                background-color: transparent;
            }

            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QLineEdit {
                background-color: #4f545c;
                color: #ffffff;
                border: 1px solid #3498db;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }

            QTextEdit {
                background-color: #4f545c;
                color: #ffffff;
                border: 1px solid #3498db;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
        """)

    def send_email(self):
        try:
            receiver_email = self.email_input.text()

            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = receiver_email
            msg['Subject'] = 'Contact Form Submission'

            name = self.name_input.text()
            phone = self.phone_input.text()
            email = self.email_input.text()
            message = self.message_input.toPlainText()

            body = f"Name: {name}\nPhone: {phone}\nEmail: {email}\n\nMessage:\n{message}"
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.password)
            text = msg.as_string()
            server.sendmail(self.sender_email, receiver_email, text)
            server.quit()

            QMessageBox.information(self, 'Email Sent', 'Your message has been sent successfully')
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to send email: {str(e)}')

class ClickableListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            item = self.itemAt(event.pos())
            if item:
                if item.isSelected():
                    self.clearSelection()
                else:
                    self.setCurrentItem(item)
        super().mousePressEvent(event)


class TaskifyApp(QWidget):
    def __init__(self, shared_board_data=None):
        super().__init__()
        self.boards = self.load_boards()
        self.initUI()

        self.collaboration = Collaboration(self)
        self.task_layout.addWidget(self.collaboration.share_button)
        self.task_layout.addWidget(self.collaboration.open_colab_button)

        if shared_board_data:
            self.boards = {'boards': [shared_board_data]}
        else:
            self.boards = self.load_boards()

        self.notification_timer = QTimer()
        self.notification_timer.timeout.connect(self.check_notifications)
        self.notification_timer.start(60000)

        self.display_statistics()


        self.oldPos = self.pos()
    def mousePressEvent(self, event):
        if event.y() < 50:  # adjust this value to match the height of your title bar
            self.oldPos = event.globalPos()
  

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.y() < 50:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()



    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.apply_dark_theme()

        self.title_bar = QHBoxLayout()
        self.title_label = QLabel("Taskify (Beta)")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.minimize_button = QPushButton("-")
        self.minimize_button.setFixedSize(30, 30)
        self.minimize_button.clicked.connect(self.showMinimized)
        self.fullscreen_button = QPushButton("FS")
        self.fullscreen_button.setFixedSize(30, 30)
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)
        self.help_button = QPushButton("?")
        self.help_button.setFixedSize(60, 30)
        self.help_button.clicked.connect(self.open_help)
        self.theme_switch = QCheckBox("Light Mode")
        self.theme_switch.setFixedSize(100, 30)
        self.theme_switch.setChecked(False)
        self.theme_switch.stateChanged.connect(self.toggle_theme)
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(30, 30)
        self.close_button.clicked.connect(self.close_window)
        self.title_bar.addWidget(self.title_label)
        self.title_bar.addStretch()
        self.title_bar.addWidget(self.help_button)
        self.title_bar.addWidget(self.theme_switch)
        self.title_bar.addWidget(self.minimize_button)
        self.title_bar.addWidget(self.fullscreen_button)
        self.title_bar.addWidget(self.close_button)

        self.board_list = ClickableListWidget()
        self.board_list.setMinimumWidth(200)
        self.board_name_input = QLineEdit()
        self.board_name_input.setFixedWidth(200)
        self.add_board_button = QPushButton('Add Board')
        self.add_board_button.setFixedSize(120, 30)
        self.remove_board_button = QPushButton('Remove Board')
        self.remove_board_button.setFixedSize(120, 30)

        self.card_list = ClickableListWidget()
        self.card_list.setMinimumWidth(200)
        self.card_name_input = QLineEdit()
        self.card_name_input.setFixedWidth(200)
        self.add_card_button = QPushButton('Add Card')
        self.add_card_button.setFixedSize(120, 30)
        self.remove_card_button = QPushButton('Remove Card')
        self.remove_card_button.setFixedSize(120, 30)

        self.task_list = QListWidget()
        self.task_list.setMinimumWidth(400)
        self.task_name_input = QLineEdit()
        self.task_name_input.setFixedWidth(200)
        self.remove_task_button = QPushButton('Remove Task')
        self.remove_task_button.setFixedSize(120, 30)
        self.add_task_button = QPushButton('Add Task')
        self.add_task_button.setFixedSize(120, 30)

        self.priority_group = QButtonGroup()
        self.priority_low = QRadioButton('Low')
        self.priority_medium = QRadioButton('Medium')
        self.priority_high = QRadioButton('High')
        self.priority_group.addButton(self.priority_low)
        self.priority_group.addButton(self.priority_medium)
        self.priority_group.addButton(self.priority_high)
        self.priority_medium.setChecked(True)

        self.repeat_group = QButtonGroup()
        self.repeat_none = QRadioButton('None')
        self.repeat_daily = QRadioButton('Daily')
        self.repeat_weekly = QRadioButton('Weekly')
        self.repeat_monthly = QRadioButton('Monthly')
        self.repeat_group.addButton(self.repeat_none)
        self.repeat_group.addButton(self.repeat_daily)
        self.repeat_group.addButton(self.repeat_weekly)
        self.repeat_group.addButton(self.repeat_monthly)
        self.repeat_none.setChecked(True)

        self.task_dependency_input = QLineEdit()
        self.task_dependency_input.setPlaceholderText("Depends on")

        self.statistics_label = QLabel()

        self.delete_data_button = QPushButton('Delete All Data')
        self.delete_data_button.setFixedHeight(30)
        self.delete_data_button.clicked.connect(self.delete_data)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.title_bar)

        self.content_layout = QHBoxLayout()
        self.board_card_layout = QVBoxLayout()
        self.board_card_layout.addWidget(QLabel('Boards'))
        self.board_card_layout.addWidget(self.board_list)
        self.board_card_layout.addWidget(self.board_name_input)
        board_button_layout = QHBoxLayout()
        board_button_layout.addWidget(self.add_board_button)
        self.edit_board_button = QPushButton('Edit Board')
        self.edit_board_button.setFixedSize(120, 30)
        self.edit_board_button.clicked.connect(self.edit_board)
        board_button_layout.addWidget(self.edit_board_button)
        board_button_layout.addWidget(self.remove_board_button)
        self.board_card_layout.addLayout(board_button_layout)
        self.board_card_layout.addWidget(QLabel('Cards'))
        self.board_card_layout.addWidget(self.card_list)
        self.board_card_layout.addWidget(self.card_name_input)
        card_button_layout = QHBoxLayout()
        card_button_layout.addWidget(self.add_card_button)
        self.edit_card_button = QPushButton('Edit Card')
        self.edit_card_button.setFixedSize(120, 30)
        self.edit_card_button.clicked.connect(self.edit_card)
        card_button_layout.addWidget(self.edit_card_button)
        card_button_layout.addWidget(self.remove_card_button)
        self.board_card_layout.addLayout(card_button_layout)
        self.content_layout.addLayout(self.board_card_layout)

        self.task_layout = QVBoxLayout()
        self.task_layout.addWidget(QLabel('Tasks'))
        self.task_layout.addWidget(self.task_list)
        self.task_layout.addWidget(self.task_name_input)
        self.task_layout.addWidget(QLabel('Priority'))
        priority_layout = QHBoxLayout()
        priority_layout.addWidget(self.priority_low)
        priority_layout.addWidget(self.priority_medium)
        priority_layout.addWidget(self.priority_high)
        self.task_layout.addLayout(priority_layout)

        self.task_layout.addWidget(QLabel('Repeat'))
        repeat_layout = QHBoxLayout()
        repeat_layout.addWidget(self.repeat_none)
        repeat_layout.addWidget(self.repeat_daily)
        repeat_layout.addWidget(self.repeat_weekly)
        repeat_layout.addWidget(self.repeat_monthly)
        self.task_layout.addLayout(repeat_layout)

        self.task_time_input = QLineEdit()
        self.task_time_input.setPlaceholderText("HH:MM")
        self.task_layout.addWidget(self.task_time_input)
        self.task_layout.addWidget(self.task_dependency_input)
        task_button_layout = QHBoxLayout()
        task_button_layout.addWidget(self.add_task_button)
        self.edit_task_button = QPushButton('Edit Task')
        self.edit_task_button.setFixedSize(120, 30)
        self.edit_task_button.clicked.connect(self.edit_task)
        task_button_layout.addWidget(self.edit_task_button)
        task_button_layout.addWidget(self.remove_task_button)
        self.task_layout.addLayout(task_button_layout)

        button_layout = QHBoxLayout()
        self.email_report_button = QPushButton('Contact Us')
        self.email_report_button.setFixedHeight(30)
        self.email_report_button.clicked.connect(self.open_contact_form)
        button_layout.addWidget(self.email_report_button, stretch=1)
        button_layout.addWidget(self.delete_data_button, stretch=1)
        self.task_layout.addLayout(button_layout)

        self.task_layout.addWidget(self.statistics_label)
        self.content_layout.addLayout(self.task_layout)

        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)

        self.board_list.itemSelectionChanged.connect(self.board_selected)
        self.card_list.itemSelectionChanged.connect(self.card_selected)
        self.add_board_button.clicked.connect(self.add_board)
        self.add_card_button.clicked.connect(self.add_card)
        self.remove_board_button.clicked.connect(self.remove_board)
        self.remove_card_button.clicked.connect(self.remove_card)
        self.remove_task_button.clicked.connect(self.remove_task)
        self.add_task_button.clicked.connect(self.add_task)
        self.task_list.itemChanged.connect(self.task_checked)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('favicon.ico'))
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.tray_menu = QMenu()
        self.show_action = QAction('Show Taskify', self)
        self.show_action.triggered.connect(self.show)
        self.tray_menu.addAction(self.show_action)

        self.exit_action = QAction('Exit', self)
        self.exit_action.triggered.connect(self.close_app)
        self.tray_menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

        self.load_board_list()
        self.about_button = QPushButton('About')
        self.about_button.clicked.connect(self.show_about)
        self.title_bar.addWidget(self.about_button)
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def close_window(self):
        self.hide()
        self.tray_icon.showMessage('Taskify', 'Taskify is still running in the background.')

    def close_app(self):
        self.tray_icon.show()
        self.close()

    def delete_data(self):
        reply = QMessageBox.question(self, 'Delete Data', 'Are you sure you want to delete all data?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.remove('boards.json')
            except FileNotFoundError:
                pass
            self.boards = {'boards': []}
            self.load_board_list()
            self.card_list.clear()
            self.task_list.clear()
            self.display_statistics()

    def load_boards(self):
        try:
            with open('boards.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'boards': []}

    def save_boards(self):
        with open('boards.json', 'w') as f:
            json.dump(self.boards, f)

    def load_board_list(self):
        self.board_list.clear()
        for board in self.boards['boards']:
            item = QListWidgetItem(board['name'])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
            item.setCheckState(Qt.Unchecked)
            self.board_list.addItem(item)

    def load_card_list(self):
        self.card_list.clear()
        if self.board_list.currentItem():
            board_name = self.board_list.currentItem().text()
            for board in self.boards['boards']:
                if board['name'] == board_name:
                    for card in board.get('cards', []):
                        item = QListWidgetItem(card['name'])
                        item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable)
                        item.setCheckState(Qt.Unchecked)
                        self.card_list.addItem(item)

    def load_task_list(self):
        self.task_list.clear()
        if self.card_list.currentItem():
            card_name = self.card_list.currentItem().text()
            board_name = self.board_list.currentItem().text()
            for board in self.boards['boards']:
                if board['name'] == board_name:
                    for card in board.get('cards', []):
                        if card['name'] == card_name:
                            for task in card.get('tasks', []):
                                task_text = task['name']
                                if 'time' in task:
                                    task_text += f" - {task['time'].split(' ')[1]}"
                                item = QListWidgetItem(task_text)
                                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                                item.setCheckState(Qt.Unchecked if not task['completed'] else Qt.Checked)
                                if task.get('priority') == 'High':
                                    item.setForeground(Qt.red)
                                elif task.get('priority') == 'Medium':
                                    item.setForeground(Qt.yellow)
                                elif task.get('priority') == 'Low':
                                    item.setForeground(Qt.green)
                                self.task_list.addItem(item)

    def board_selected(self):
        self.load_card_list()
        self.card_list.clearSelection()
        self.task_list.clear()

    def card_selected(self):
        self.load_task_list()

    def add_board(self):
        board_name = self.board_name_input.text()
        self.boards['boards'].append({'name': board_name, 'cards': []})
        self.save_boards()
        self.load_board_list()
        self.board_name_input.clear()

    def add_card(self):
        if self.board_list.currentItem():
            board_name = self.board_list.currentItem().text()
            card_name = self.card_name_input.text()
            for board in self.boards['boards']:
                if board['name'] == board_name:
                    board['cards'].append({'name': card_name, 'tasks': []})
            self.save_boards()
            self.load_card_list()
            self.card_name_input.clear()

    def show_about(self):
        QMessageBox.about(self, 'About', 'Copyright 2025 Pikes Development. All rights reserved.')

    def remove_board(self):
        if self.board_list.currentItem():
            board_name = self.board_list.currentItem().text()
            for board in self.boards['boards']:
                if board['name'] == board_name:
                    self.boards['boards'].remove(board)
                    self.save_boards()
                    self.load_board_list()
                    self.card_list.clear()
                    self.task_list.clear()
                    self.display_statistics()
                    break

    def remove_card(self):
        if self.board_list.currentItem() and self.card_list.currentItem():
            board_name = self.board_list.currentItem().text()
            card_name = self.card_list.currentItem().text()
            for board in self.boards['boards']:
                if board['name'] == board_name:
                    for card in board.get('cards', []):
                        if card['name'] == card_name:
                            board['cards'].remove(card)
                            self.save_boards()
                            self.load_card_list()
                            self.task_list.clear()
                            self.display_statistics()
                            break
                    break

    def remove_task(self):
        if self.board_list.currentItem() and self.card_list.currentItem() and self.task_list.currentItem():
            board_name = self.board_list.currentItem().text()
            card_name = self.card_list.currentItem().text()
            task_name = self.task_list.currentItem().text().split(' - ')[0]
            for board in self.boards['boards']:
                if board['name'] == board_name:
                    for card in board.get('cards', []):
                        if card['name'] == card_name:
                            card['tasks'] = [task for task in card.get('tasks', []) if task['name'] != task_name]
                            self.save_boards()
                            self.load_task_list()
                            self.display_statistics()
                            break
                    break

    def open_contact_form(self):
        self.contact_form = ContactForm()
        self.contact_form.show()


    def add_task(self):
        if self.board_list.currentItem() and self.card_list.currentItem():
            board_name = self.board_list.currentItem().text()
            card_name = self.card_list.currentItem().text()
            task_name = self.task_name_input.text()
            task_time = self.task_time_input.text()

            task_priority = None
            if self.priority_low.isChecked():
                task_priority = 'Low'
            elif self.priority_medium.isChecked():
                task_priority = 'Medium'
            elif self.priority_high.isChecked():
                task_priority = 'High'

            task_repeat = None
            if self.repeat_none.isChecked():
                task_repeat = 'None'
            elif self.repeat_daily.isChecked():
                task_repeat = 'Daily'
            elif self.repeat_weekly.isChecked():
                task_repeat = 'Weekly'
            elif self.repeat_monthly.isChecked():
                task_repeat = 'Monthly'

            task_dependency = self.task_dependency_input.text()
            if task_name:
                for board in self.boards['boards']:
                    if board['name'] == board_name:
                        for card in board.get('cards', []):
                            if card['name'] == card_name:
                                task = {'name': task_name, 'completed': False, 'priority': task_priority, 'repeat': task_repeat, 'depends_on': task_dependency}
                                if task_time:
                                    try:
                                        from datetime import datetime
                                        current_date = datetime.now().strftime("%Y-%m-%d")
                                        task_datetime = f"{current_date} {task_time}"
                                        from PyQt5.QtCore import QDateTime
                                        QDateTime.fromString(task_datetime, "yyyy-MM-dd HH:mm")
                                        task['time'] = task_datetime
                                    except ValueError:
                                        QMessageBox.critical(self, 'Error', 'Invalid time format. Please use HH:MM.')
                                        return
                                card.setdefault('tasks', []).append(task)
                                self.save_boards()
                                self.load_task_list()
                                self.task_name_input.clear()
                                self.task_time_input.clear()
                                self.display_statistics()
                                break
                        break

    def task_checked(self, item):
        board_name = self.board_list.currentItem().text()
        card_name = self.card_list.currentItem().text()
        task_name = item.text().split(' - ')[0]
        for board in self.boards['boards']:
            if board['name'] == board_name:
                for card in board.get('cards', []):
                    if card['name'] == card_name:
                        for task in card.get('tasks', []):
                            if task['name'] == task_name:
                                if item.checkState() == Qt.Checked:
                                    depends_on = task.get('depends_on')
                                    if depends_on:
                                        dependent_task = self.find_task(depends_on, board_name, card_name)
                                        if dependent_task and not dependent_task['completed']:
                                            QMessageBox.warning(self, 'Dependency not met', f'Task "{task_name}" depends on "{depends_on}" which is not completed.')
                                            item.setCheckState(Qt.Unchecked)
                                            return
                                task['completed'] = item.checkState() == Qt.Checked
                                self.save_boards()
                                self.display_statistics()
                                break
                        break
                break

    def find_task(self, task_name, board_name, card_name):
        for board in self.boards['boards']:
            if board['name'] == board_name:
                for card in board.get('cards', []):
                    if card['name'] == card_name:
                        for task in card.get('tasks', []):
                            if task['name'] == task_name:
                                return task
        return None


    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def check_notifications(self):
        current_time = QDateTime.currentDateTime()
        for board in self.boards['boards']:
            for card in board.get('cards', []):
                for task in card.get('tasks', []):
                    if 'time' in task:
                        task_time = QDateTime.fromString(task.get('time', ''), "yyyy-MM-dd HH:mm")
                        if task_time.isValid() and current_time.secsTo(task_time) <= 300 and not task.get('notified', False):
                            import winsound
                            winsound.Beep(2500, 1000)  # Play default system sound
                            self.tray_icon.showMessage('Taskify', f"Task '{task['name']}' starts in 5 minutes.")
                            task['notified'] = True
                            self.save_boards()

    def display_statistics(self):
        completed_tasks = 0
        total_tasks = 0
        for board in self.boards['boards']:
            for card in board.get('cards', []):
                for task in card.get('tasks', []):
                    total_tasks += 1
                    if task['completed']:
                        completed_tasks += 1
        if total_tasks > 0:
            completion_rate = completed_tasks / total_tasks * 100
            self.statistics_label.setText(f"Completion Rate: {round(completion_rate,2)}%")
        else:
            self.statistics_label.setText("No tasks")

    def open_help(self):
        try:
            os.startfile('README.txt')
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'README.txt file not found.')

    def toggle_theme(self):
        if self.theme_switch.isChecked():
            self.apply_light_theme()
        else:
            self.apply_dark_theme()

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2f343f;
                color: #ffffff;
            }

            QLabel {
                background-color: transparent;
            }

            QPushButton {
                background-color: #3498db;
                color: #ffffff;
                border: none;
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #2980b9;
            }

            QLineEdit {
                background-color: #4f545c;
                color: #ffffff;
                border: 1px solid #3498db;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }

            QListWidget {
                background-color: #4f545c;
                color: #ffffff;
                border: 1px solid #3498db;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }

            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3498db;
            }

            QListWidget::item:selected {
                background-color: #2980b9;
                color: #ffffff;
            }
        """)

    def edit_board(self):
        if self.board_list.currentItem():
            board_name = self.board_list.currentItem().text()
            new_board_name, ok = QInputDialog.getText(self, 'Edit Board', 'Enter new board name:', text=board_name)
            if ok and new_board_name:
                for board in self.boards['boards']:
                    if board['name'] == board_name:
                        board['name'] = new_board_name
                        self.save_boards()
                        self.load_board_list()
                        break

    def edit_card(self):
        if self.board_list.currentItem() and self.card_list.currentItem():
            board_name = self.board_list.currentItem().text()
            card_name = self.card_list.currentItem().text()
            new_card_name, ok = QInputDialog.getText(self, 'Edit Card', 'Enter new card name:', text=card_name)
            if ok and new_card_name:
                for board in self.boards['boards']:
                    if board['name'] == board_name:
                        for card in board.get('cards', []):
                            if card['name'] == card_name:
                                card['name'] = new_card_name
                                self.save_boards()
                                self.load_card_list()
                                break
                        break

    def edit_task(self):
        if self.board_list.currentItem() and self.card_list.currentItem() and self.task_list.currentItem():
            board_name = self.board_list.currentItem().text()
            card_name = self.card_list.currentItem().text()
            task_name = self.task_list.currentItem().text().split(' - ')[0]
            new_task_name, ok = QInputDialog.getText(self, 'Edit Task', 'Enter new task name:', text=task_name)
            if ok and new_task_name:
                for board in self.boards['boards']:
                    if board['name'] == board_name:
                        for card in board.get('cards', []):
                            if card['name'] == card_name:
                                for task in card.get('tasks', []):
                                    if task['name'] == task_name:
                                        task['name'] = new_task_name
                                        self.save_boards()
                                        self.load_task_list()
                                        break
                                break
                        break

    def apply_light_theme(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #f7f7f7;
            color: #333333;
        }

        QLabel {
            background-color: transparent;
        }

        QPushButton {
            background-color: #4CAF50;
            color: #ffffff;
            border: none;
            padding: 10px 20px;
            font-size: 12px;
            font-weight: bold;
            border-radius: 5px;
        }

        QPushButton:hover {
            background-color: #3e8e41;
        }

        QLineEdit {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #4CAF50;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
        }

        QListWidget {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #4CAF50;
            padding: 10px;
            font-size: 16px;
            border-radius: 5px;
        }

        QListWidget::item {
            padding: 10px;
            border-bottom: 1px solid #4CAF50;
        }

        QListWidget::item:selected {
            background-color: #8BC34A;
            color: #ffffff;
        }
    """)

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    app = QApplication(sys.argv)
    taskify_app = TaskifyApp()
    taskify_app.show()
    sys.exit(app.exec_())