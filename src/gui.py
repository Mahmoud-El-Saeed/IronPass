import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QStackedWidget, QLabel, QLineEdit, QPushButton,
                            QFrame, QSpacerItem, QSizePolicy, QFormLayout, QTableWidgetItem,
                            QHeaderView, QAbstractItemView, QTableWidget, QMessageBox , QDesktopWidget)
from PyQt5.QtCore import Qt , QSize, QTimer
from PyQt5.QtGui import QFont, QIcon
import re
from .cli import PASSWORD_PATTERN
from .crypto_utils import Generate_Password



class FirstTimeScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #2c3e50;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        content_frame = QFrame()
        # content_frame.setFixedWidth(700)
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 15px;
            }
        """)

        frame_layout = QVBoxLayout(content_frame)
        frame_layout.setContentsMargins(40, 40, 40, 40)
        frame_layout.setSpacing(15)

        title_label = QLabel("Welcome to Ironpass")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; margin-bottom: 10px;")

        create_pass_label = QLabel("Create a Master Password:")
        create_pass_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")

        self.create_password_input = QLineEdit()
        self.create_password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        script_dir = os.path.dirname(__file__)
        self.view_icon = QIcon(os.path.join(script_dir, '..', 'images', 'view.png'))
        self.hide_icon = QIcon(os.path.join(script_dir, '..', 'images', 'hide.png'))

        create_pass_layout = self._create_password_layout(self.create_password_input)
        confirm_pass_layout = self._create_password_layout(self.confirm_password_input)

        self.create_vault_button = QPushButton("Create Vault")

        line_edit_style = """
            QLineEdit {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #34495e;
                border-radius: 5px;
                padding: 12px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
        """
        self.create_password_input.setStyleSheet(line_edit_style)
        self.confirm_password_input.setStyleSheet(line_edit_style)

        self.create_vault_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)

        frame_layout.addWidget(title_label)
        frame_layout.addWidget(create_pass_label)
        frame_layout.addLayout(create_pass_layout)
        confirm_pass_label = QLabel("Confirm Master Password:")
        confirm_pass_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        frame_layout.addWidget(confirm_pass_label)
        frame_layout.addLayout(confirm_pass_layout)
        frame_layout.addWidget(self.create_vault_button)

        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(content_frame)
        h_layout.addStretch()
        main_layout.addLayout(h_layout)
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def _create_password_layout(self, line_edit):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        toggle_button = QPushButton()
        toggle_button.setIcon(self.view_icon)
        toggle_button.setIconSize(QSize(24, 24))
        toggle_button.setStyleSheet("background-color: transparent; border: none;")
        toggle_button.clicked.connect(lambda: self._toggle_password_visibility(line_edit, toggle_button))
        layout.addWidget(line_edit)
        layout.addWidget(toggle_button, alignment=Qt.AlignCenter)
        return layout

    def _toggle_password_visibility(self, line_edit, button):
        if line_edit.echoMode() == QLineEdit.Password:
            line_edit.setEchoMode(QLineEdit.Normal)
            button.setIcon(self.hide_icon)
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            button.setIcon(self.view_icon)
    


class ReturningUserScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #2c3e50;")

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(top_spacer)

        login_frame = QFrame()
        login_frame.setFixedWidth(450)
        login_frame.setStyleSheet("QFrame { background-color: #34495e; border-radius: 10px; }")
        
        frame_layout = QVBoxLayout(login_frame)
        frame_layout.setContentsMargins(40, 40, 40, 40)
        frame_layout.setSpacing(20)

        title_label = QLabel("Welcome back to Ironpass")
        title_font = QFont(); title_font.setPointSize(22); title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")
        title_label.setWordWrap(True)
        
        password_label = QLabel("Enter Master Password:")
        password_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        password_layout = QHBoxLayout()
        password_layout.setSpacing(10) # إضافة مسافة
        
        script_dir = os.path.dirname(__file__)
        icon_path_view = os.path.join(script_dir, '..', 'images', 'view.png')
        icon_path_hide = os.path.join(script_dir, '..', 'images', 'hide.png')
        self.view_icon = QIcon(icon_path_view)
        self.hide_icon = QIcon(icon_path_hide)

        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(self.view_icon)
        
        self.toggle_button.setIconSize(QSize(24, 24))

        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.toggle_button, alignment=Qt.AlignCenter) 

        self.toggle_button.clicked.connect(self.toggle_password_visibility)
        
        self.unlock_button = QPushButton("Unlock")
        
        self.password_input.setStyleSheet("""
            QLineEdit { background-color: #2c3e50; color: white; border: 1px solid #34495e; 
                        border-radius: 5px; padding: 12px; font-size: 16px; }
            QLineEdit:focus { border: 1px solid #3498db; }
        """)

        self.toggle_button.setStyleSheet("background-color: transparent; border: none;")
        
        self.unlock_button.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; border: none; border-radius: 5px;
                        padding: 12px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #2980b9; }
        """)

        frame_layout.addWidget(title_label)
        frame_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
        frame_layout.addWidget(password_label)
        frame_layout.addLayout(password_layout)
        frame_layout.addWidget(self.unlock_button)
        
        h_layout = QHBoxLayout(); h_layout.addStretch(); h_layout.addWidget(login_frame); h_layout.addStretch()
        main_layout.addLayout(h_layout)
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(bottom_spacer)

    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setIcon(self.hide_icon)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_button.setIcon(self.view_icon)
            

class OptionsMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #2c3e50;")

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(top_spacer)

        menu_frame = QFrame()
        menu_frame.setFixedWidth(400)
        menu_frame.setStyleSheet("QFrame { background-color: #34495e; border-radius: 10px; }")
        
        frame_layout = QVBoxLayout(menu_frame)
        frame_layout.setContentsMargins(40, 40, 40, 40)
        frame_layout.setSpacing(25)

        title_label = QLabel("Main Menu")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; margin-bottom: 15px;")
        
        self.show_button = QPushButton("Show Passwords")
        self.add_button = QPushButton("Add New Password")
        self.delete_button = QPushButton("Delete Password")

        buttons = [self.show_button, self.add_button, self.delete_button]

        for button in buttons:
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)

        frame_layout.addWidget(title_label)
        frame_layout.addWidget(self.show_button)
        frame_layout.addWidget(self.add_button)
        frame_layout.addWidget(self.delete_button)
        
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(menu_frame)
        h_layout.addStretch()
        main_layout.addLayout(h_layout)

        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(bottom_spacer)


class AddScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #2c3e50;")

        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(top_spacer)

        content_frame = QFrame()
        content_frame.setFixedWidth(500)
        content_frame.setStyleSheet("QFrame { background-color: #34495e; border-radius: 10px; }")
        
        frame_layout = QVBoxLayout(content_frame)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        frame_layout.setSpacing(20)

        title_label = QLabel("Add New Password")
        title_font = QFont(); title_font.setPointSize(22); title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; margin-bottom: 10px;")

        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        self.site_name_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        password_hbox = QHBoxLayout()
        password_hbox.setSpacing(10)
        password_hbox.addWidget(self.password_input)
        
        self.generate_pass_button = QPushButton("Generate")
        
        script_dir = os.path.dirname(__file__)
        icon_path_view = os.path.join(script_dir, '..', 'images', 'view.png')
        icon_path_hide = os.path.join(script_dir, '..', 'images', 'hide.png')
        self.view_icon = QIcon(icon_path_view)
        self.hide_icon = QIcon(icon_path_hide)
        
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(self.view_icon)
        self.toggle_button.setIconSize(QSize(24, 24))
        self.toggle_button.setStyleSheet("background-color: transparent; border: none;")
        self.toggle_button.clicked.connect(self.toggle_password_visibility)

        password_hbox.addWidget(self.generate_pass_button)
        password_hbox.addWidget(self.toggle_button, alignment=Qt.AlignCenter)
        
        form_layout.addRow(QLabel("Site Name:"), self.site_name_input)
        form_layout.addRow(QLabel("Username/Email:"), self.username_input)
        form_layout.addRow(QLabel("Password:"), password_hbox)
        
        label_style = "color: #ecf0f1; font-size: 14px;"
        for i in range(form_layout.rowCount()):
            label_item = form_layout.itemAt(i, QFormLayout.LabelRole)
            if label_item:
                label_item.widget().setStyleSheet(label_style)

        for widget in [self.site_name_input, self.username_input, self.password_input]:
            widget.setStyleSheet("""
                QLineEdit { background-color: #2c3e50; color: white; border: 1px solid #34495e; 
                            border-radius: 5px; padding: 10px; font-size: 14px; }
                QLineEdit:focus { border: 1px solid #3498db; }
            """)
        
        self.generate_pass_button.setFixedWidth(80)
        self.generate_pass_button.setStyleSheet("""
            QPushButton { background-color: #566573; color: white; border: none; 
                        border-radius: 5px; padding: 8px; font-size: 12px; }
            QPushButton:hover { background-color: #808b96; }
        """)

        buttons_hbox = QHBoxLayout()
        buttons_hbox.setSpacing(10)
        
        self.back_button = QPushButton("Back")
        self.store_button = QPushButton("Store")
        
        buttons_hbox.addWidget(self.back_button)
        buttons_hbox.addStretch()
        buttons_hbox.addWidget(self.store_button)
        
        self.back_button.setStyleSheet("""
            QPushButton { background-color: #7f8c8d; color: white; border: none; border-radius: 5px;
                        padding: 12px 25px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #95a5a6; }
        """)
        self.store_button.setStyleSheet("""
            QPushButton { background-color: #27ae60; color: white; border: none; border-radius: 5px;
                        padding: 12px 25px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #2ecc71; }
        """)

        frame_layout.addWidget(title_label)
        frame_layout.addLayout(form_layout)
        frame_layout.addSpacerItem(QSpacerItem(1, 20))
        frame_layout.addLayout(buttons_hbox)

        h_layout = QHBoxLayout()
        h_layout.addStretch(); h_layout.addWidget(content_frame); h_layout.addStretch()
        main_layout.addLayout(h_layout)

        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(bottom_spacer)
    
    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_button.setIcon(self.hide_icon)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_button.setIcon(self.view_icon)


class ShowScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        self.setStyleSheet("background-color: #2c3e50;")

        title_label = QLabel("Saved Passwords")
        title_font = QFont(); title_font.setPointSize(22); title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by site or username...")
        self.search_input.setStyleSheet("""
            QLineEdit { background-color: #34495e; color: white; border: 1px solid #34495e; 
                        border-radius: 5px; padding: 10px; font-size: 14px; }
            QLineEdit:focus { border: 1px solid #3498db; }
        """)
        
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Site Name", "Username/Email", "Password", "Actions"])
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(False)
        
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Interactive)
        header.resizeSection(3, 130)
        
        self.table_widget.setStyleSheet("""
            QTableWidget { background-color: #34495e; color: #ecf0f1; border: none; font-size: 14px; }
            QHeaderView::section { background-color: #566573; color: white; padding: 10px; border: none;
                                   font-size: 14px; font-weight: bold; }
            QTableWidget::item { padding-left: 10px; padding-right: 10px; }
        """)

        self.back_button = QPushButton("Back to Menu")
        self.back_button.setFixedWidth(150)
        self.back_button.setStyleSheet("""
            QPushButton { background-color: #7f8c8d; color: white; border: none; border-radius: 5px;
                          padding: 12px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #95a5a6; }
        """)
        
        main_layout.addWidget(title_label, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.table_widget)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        
        script_dir = os.path.dirname(__file__)
        self.view_icon = QIcon(os.path.join(script_dir, '..', 'images', 'view.png'))
        self.hide_icon = QIcon(os.path.join(script_dir, '..', 'images', 'hide.png'))
        
        self.search_input.textChanged.connect(self.filter_table)

    def load_real_data(self, engine):
        self.table_widget.setRowCount(0)
        all_entries = engine.show_All_passwords()

        for row, item in enumerate(all_entries):
            db_id, site, user, password = item
            
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(site))
            self.table_widget.setItem(row, 1, QTableWidgetItem(user))
            
            password_item = QTableWidgetItem("••••••••••")
            password_item.setData(Qt.UserRole, password)
            self.table_widget.setItem(row, 2, password_item)
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            actions_layout.setSpacing(10)
            
            copy_btn = QPushButton("Copy")
            toggle_vis_btn = QPushButton()
            toggle_vis_btn.setIcon(self.view_icon)
            
            for btn in [copy_btn, toggle_vis_btn]:
                btn.setCursor(Qt.PointingHandCursor)
            
            copy_btn.setStyleSheet("""
                QPushButton {
                    background-color: #566573;
                    color: white;
                    border-radius: 3px;
                    padding: 3px 5px;
                    font-size: 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #808b96;
                }
                QPushButton:pressed {
                    background-color: #c0392b;
                }
            """)
            toggle_vis_btn.setIconSize(QSize(20,20))

            actions_layout.addWidget(copy_btn)
            actions_layout.addWidget(toggle_vis_btn)
            actions_layout.addStretch()

            copy_btn.clicked.connect(lambda state, p=password, btn=copy_btn: self.copy_to_clipboard(p, btn))
            toggle_vis_btn.clicked.connect(lambda state, r=row, btn=toggle_vis_btn: self.toggle_row_password_visibility(r, btn))

            self.table_widget.setCellWidget(row, 3, actions_widget)
            self.table_widget.setRowHeight(row, 50)

    def copy_to_clipboard(self, text, button):
        QApplication.clipboard().setText(text)
        original_text = button.text()
        button.setText("Copied!")
        QTimer.singleShot(1500, lambda: button.setText(original_text))

    def toggle_row_password_visibility(self, row, button):
        password_item = self.table_widget.item(row, 2)
        if password_item.text() == "••••••••••":
            real_password = password_item.data(Qt.UserRole)
            password_item.setText(real_password)
            button.setIcon(self.hide_icon)
        else:
            password_item.setText("••••••••••")
            button.setIcon(self.view_icon)

    def filter_table(self, text):
        for row in range(self.table_widget.rowCount()):
            site_item = self.table_widget.item(row, 0)
            username_item = self.table_widget.item(row, 1)
            
            site_match = text.lower() in site_item.text().lower()
            user_match = text.lower() in username_item.text().lower()
            
            if site_match or user_match:
                self.table_widget.setRowHidden(row, False)
            else:
                self.table_widget.setRowHidden(row, True)


class DeleteScreen(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        self.setStyleSheet("background-color: #2c3e50;")

        title_label = QLabel("Delete a Password")
        title_font = QFont(); title_font.setPointSize(22); title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter by site or username to find the entry to delete...")
        self.search_input.setStyleSheet("""
            QLineEdit { background-color: #34495e; color: white; border: 1px solid #34495e; 
                        border-radius: 5px; padding: 10px; font-size: 14px; }
            QLineEdit:focus { border: 1px solid #3498db; }
        """)
        
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Site Name", "Username/Email", "Action"])
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(False)
        
        header = self.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.table_widget.setStyleSheet("""
            QTableWidget { background-color: #34495e; color: #ecf0f1; border: none; font-size: 14px; }
            QHeaderView::section { background-color: #566573; color: white; padding: 10px; border: none;
                                   font-size: 14px; font-weight: bold; }
            QTableWidget::item { padding-left: 10px; padding-right: 10px; }
            QTableWidget::item:selected { background-color: #3498db; }
        """)

        self.back_button = QPushButton("Back to Menu")
        self.back_button.setFixedWidth(150)
        self.back_button.setStyleSheet("""
            QPushButton { background-color: #7f8c8d; color: white; border: none; border-radius: 5px;
                          padding: 12px; font-size: 16px; font-weight: bold; }
            QPushButton:hover { background-color: #95a5a6; }
        """)
        
        main_layout.addWidget(title_label, alignment=Qt.AlignLeft)
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.table_widget)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)
        
        self.search_input.textChanged.connect(self.filter_table)

    def load_real_data(self):
        self.table_widget.setRowCount(0)
        all_entries = self.engine.show_All_passwords()

        for row, item in enumerate(all_entries):
            db_id, site, user, password = item
            
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(site))
            self.table_widget.setItem(row, 1, QTableWidgetItem(user))
            
            delete_button = QPushButton("Delete")
            delete_button.setCursor(Qt.PointingHandCursor)
            delete_button.setStyleSheet("""
                QPushButton { background-color: #c0392b; color: white; border: none; 
                            border-radius: 3px; padding: 8px; font-size: 12px; font-weight: bold; min-width: 80px;}
                QPushButton:hover { background-color: #e74c3c; }
            """)
            
            delete_button.clicked.connect(lambda state, r=row, s=site, u=user: self._confirm_delete(r, s, u))
            
            self.table_widget.setCellWidget(row, 2, delete_button)
            self.table_widget.setRowHeight(row, 50)

    def _confirm_delete(self, row_number, site, user):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Confirm Deletion")
        msg_box.setText(f"Are you sure you want to permanently delete the entry?\n\nSite: {site}\nUsername: {user}")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        ret = msg_box.exec_()
        
        if ret == QMessageBox.Yes:
            success = self.engine.delete_password(site, user)
            if success:
                self.table_widget.removeRow(row_number)
                print(f"Entry for {site} - {user} deleted successfully.")
            else:
                QMessageBox.critical(self, "Error", "Failed to delete the entry from the database.")

    def filter_table(self, text):
        for row in range(self.table_widget.rowCount()):
            site_item = self.table_widget.item(row, 0)
            username_item = self.table_widget.item(row, 1)
            
            site_match = text.lower() in site_item.text().lower()
            user_match = text.lower() in username_item.text().lower()
            
            if site_match or user_match:
                self.table_widget.setRowHidden(row, False)
            else:
                self.table_widget.setRowHidden(row, True)



class MainWindowIRON(QMainWindow):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

        self.setWindowTitle("Ironpass Password Manager")
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.7)

        self.resize(window_width, window_height)

        self._center_on_screen()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.first_time_screen = FirstTimeScreen()
        self.returning_user_screen = ReturningUserScreen()
        self.options_menu = OptionsMenu()
        self.add_screen = AddScreen()
        self.show_screen = ShowScreen()
        self.delete_screen = DeleteScreen(self.engine)

        self.stacked_widget.addWidget(self.first_time_screen)
        self.stacked_widget.addWidget(self.returning_user_screen)
        self.stacked_widget.addWidget(self.options_menu)
        self.stacked_widget.addWidget(self.add_screen)
        self.stacked_widget.addWidget(self.show_screen)
        self.stacked_widget.addWidget(self.delete_screen)

        self.options_menu.add_button.clicked.connect(self.show_add_screen)
        self.options_menu.show_button.clicked.connect(self.show_show_screen)
        self.options_menu.delete_button.clicked.connect(self.show_delete_screen)

        self.add_screen.back_button.clicked.connect(self.show_options_menu)
        self.show_screen.back_button.clicked.connect(self.show_options_menu)
        self.delete_screen.back_button.clicked.connect(self.show_options_menu)

        self.first_time_screen.create_vault_button.clicked.connect(self.handle_create_vault)
        self.returning_user_screen.unlock_button.clicked.connect(self.handle_unlock_vault)

        self.add_screen.store_button.clicked.connect(self.handle_store_password)
        self.add_screen.generate_pass_button.clicked.connect(self.handle_generate_password)

    def _center_on_screen(self):
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def handle_create_vault(self):
        password = self.first_time_screen.create_password_input.text()
        confirm = self.first_time_screen.confirm_password_input.text()
        if not password or password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match or are empty.")
            return
        if not re.match(PASSWORD_PATTERN, password):
            QMessageBox.warning(self, "Weak Password", "Password must be at least 9 characters long and contain uppercase, lowercase, digits, and special characters.")
            return
        success = self.engine.setup_first_time(password)
        if success:
            QMessageBox.information(self, "Success", "Vault created successfully!")
            self.show_options_menu()

    def handle_unlock_vault(self):
        password = self.returning_user_screen.password_input.text()
        if not password:
            QMessageBox.warning(self, "Input Error", "Master Password cannot be empty.")
            return
        success = self.engine.unlock_app(password)
        if success:
            self.show_options_menu()
        else:
            QMessageBox.warning(self, "Error", "Incorrect Master Password.")
            self.returning_user_screen.password_input.clear()

    def handle_store_password(self):
        site = self.add_screen.site_name_input.text().strip()
        username = self.add_screen.username_input.text().strip()
        password = self.add_screen.password_input.text().strip()
        if not all([site, username, password]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return
        success = self.engine.add_password(site, username, password)
        if success:
            QMessageBox.information(self, "Success", "Password stored successfully!")
            self.add_screen.site_name_input.clear()
            self.add_screen.username_input.clear()
            self.add_screen.password_input.clear()
        else:
            QMessageBox.critical(self, "Database Error", "This site/username combination already exists.")

    def handle_generate_password(self):
        generated_password = Generate_Password()
        self.add_screen.password_input.setText(generated_password)

    def show_first_time_screen(self):
        self.stacked_widget.setCurrentWidget(self.first_time_screen)

    def show_returning_user_screen(self):
        self.stacked_widget.setCurrentWidget(self.returning_user_screen)

    def show_options_menu(self):
        self.stacked_widget.setCurrentWidget(self.options_menu)

    def show_add_screen(self):
        self.add_screen.site_name_input.clear()
        self.add_screen.username_input.clear()
        self.add_screen.password_input.clear()
        self.stacked_widget.setCurrentWidget(self.add_screen)

    def show_show_screen(self):
        self.show_screen.load_real_data(self.engine)
        self.stacked_widget.setCurrentWidget(self.show_screen)

    def show_delete_screen(self):
        self.delete_screen.load_real_data()
        self.stacked_widget.setCurrentWidget(self.delete_screen)

