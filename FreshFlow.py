import sys
import random
import mysql.connector
from mysql.connector import Error
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox


def mydb():
    """
    Create and return a MySQL database connection.
    Returns None on failure.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="squeezo",
            charset="utf8mb4"
        )
        return connection
    except Error as e:
        print(f"[DB ERROR] Database connection failed: {e}")
        return None


class LoginUI:
    def setupUi(self, Dialog, main_app):
        """
        Setup the login dialog UI. `main_app` is passed so the UI can call
        methods to switch windows (show_signup, show_customer_dashboard, show_admin_dashboard).
        """
        self.main_app = main_app
        self.Dialog = Dialog
        Dialog.setObjectName("LoginDialog")
        Dialog.resize(480, 400)
        Dialog.setStyleSheet("background-color: lightblue;")

        self.label_logo = QtWidgets.QLabel(Dialog)
        self.label_logo.setGeometry(QtCore.QRect(45, 25, 60, 60))
        try:
            self.label_logo.setPixmap(QtGui.QPixmap("logo.png"))
            self.label_logo.setScaledContents(True)
        except Exception:
            self.label_logo.setText("ðŸ§º")
            self.label_logo.setFont(QtGui.QFont("Arial", 40))
            self.label_logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.label_title = QtWidgets.QLabel(Dialog)
        self.label_title.setGeometry(QtCore.QRect(115, 35, 340, 45))
        font_title = QtGui.QFont("Times New Roman", 16, QtGui.QFont.Weight.Bold)
        self.label_title.setFont(font_title)
        self.label_title.setStyleSheet("color: #01579b;")
        self.label_title.setText("FRESH FLOW LAUNDRY SYSTEM")

        self.username_label = QtWidgets.QLabel("Username :", parent=Dialog)
        self.username_label.setGeometry(QtCore.QRect(80, 120, 100, 24))
        self.username_label.setFont(QtGui.QFont("Times New Roman", 11))
        self.username_label.setStyleSheet("color: #004d40;")

        self.lineEdit_username = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_username.setGeometry(QtCore.QRect(190, 120, 200, 28))
        self.lineEdit_username.setStyleSheet("background-color:white; border-radius:5px; padding:3px;")
        self.lineEdit_username.setPlaceholderText("Enter username")

        self.password_label = QtWidgets.QLabel("Password :", parent=Dialog)
        self.password_label.setGeometry(QtCore.QRect(80, 165, 100, 24))
        self.password_label.setFont(QtGui.QFont("Times New Roman", 11))
        self.password_label.setStyleSheet("color: #004d40;")

        self.lineEdit_password = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_password.setGeometry(QtCore.QRect(190, 165, 200, 28))
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setStyleSheet("background-color:white; border-radius:5px; padding:3px;")
        self.lineEdit_password.setPlaceholderText("Enter password")
        self.lineEdit_password.returnPressed.connect(self.login_user)

        self.radio_customer = QtWidgets.QRadioButton("Customer", parent=Dialog)
        self.radio_customer.setGeometry(QtCore.QRect(150, 215, 100, 22))
        self.radio_customer.setChecked(True)
        self.radio_customer.setFont(QtGui.QFont("Times New Roman", 11))
        self.radio_customer.setStyleSheet("color:#01579b;")

        self.radio_admin = QtWidgets.QRadioButton("Admin", parent=Dialog)
        self.radio_admin.setGeometry(QtCore.QRect(260, 215, 100, 22))
        self.radio_admin.setFont(QtGui.QFont("Times New Roman", 11))
        self.radio_admin.setStyleSheet("color:#01579b;")

        self.btn_login = QtWidgets.QPushButton("Login", parent=Dialog)
        self.btn_login.setGeometry(QtCore.QRect(160, 260, 161, 30))
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #0288d1; 
                color: white; 
                font: 12pt 'Times New Roman'; 
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0277bd;
            }
        """)
        self.btn_login.clicked.connect(self.login_user)

        self.label_signup = QtWidgets.QLabel("Don't have an account?", parent=Dialog)
        self.label_signup.setGeometry(QtCore.QRect(110, 320, 151, 21))
        self.label_signup.setFont(QtGui.QFont("Times New Roman", 9))
        self.label_signup.setStyleSheet("color:#004d40;")

        self.btn_signup = QtWidgets.QPushButton("Sign up Here", parent=Dialog)
        self.btn_signup.setGeometry(QtCore.QRect(230, 318, 111, 24))
        self.btn_signup.setFont(QtGui.QFont("Times New Roman", 10))
        self.btn_signup.setStyleSheet("""
            QPushButton {
                background-color:white; 
                border:1px solid #0288d1;
                border-radius:6px;
                color:#01579b;
            }
            QPushButton:hover {
                background-color:#b3e5fc;
            }
        """)
        self.btn_signup.clicked.connect(lambda: main_app.show_signup())

    def login_user(self):
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()
        role = "admin" if self.radio_admin.isChecked() else "customer"

        if not username or not password:
            QtWidgets.QMessageBox.warning(None, "Error", "âš ï¸ Please enter both username and password.")
            return

        connection = mydb()
        if connection is None:
            QtWidgets.QMessageBox.critical(None, "Error", "âŒ Database connection failed.")
            return

        cursor = None
        try:
            cursor = connection.cursor()
            query = "SELECT user_id, full_name, role FROM users WHERE username=%s AND password=%s AND role=%s"
            cursor.execute(query, (username, password, role))
            result = cursor.fetchone()

            if result:
                user_id, full_name, db_role = result
                QtWidgets.QMessageBox.information(None, "Success", f"âœ… Welcome, {full_name}!")
                self.lineEdit_password.clear()
                if db_role == "admin":
                    if self.main_app:
                        self.main_app.show_admin_dashboard(user_id)
                else:
                    if self.main_app:
                        self.main_app.show_customer_dashboard(user_id)
            else:
                QtWidgets.QMessageBox.warning(None, "Login Failed", "âŒ Invalid username, password, or role.")
                self.lineEdit_password.clear()
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"âŒ Database error: {str(e)}")
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            try:
                connection.close()
            except Exception:
                pass


class SignupUI:
    def setupUi(self, Dialog, main_app):
        self.main_app = main_app
        self.Dialog = Dialog

        Dialog.setObjectName("SignupDialog")
        Dialog.resize(480, 400)
        Dialog.setStyleSheet("background-color: lightblue;")

        self.label_title = QtWidgets.QLabel(Dialog)
        self.label_title.setGeometry(QtCore.QRect(60, 30, 360, 50))
        font_title = QtGui.QFont("Times New Roman", 18, QtGui.QFont.Weight.Bold)
        self.label_title.setFont(font_title)
        self.label_title.setStyleSheet("color: #01579b;")
        self.label_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_title.setText("CREATE ACCOUNT")

        font_label = QtGui.QFont("Times New Roman", 11)
        font_input = QtGui.QFont("Times New Roman", 11)

        self.fullname_label = QtWidgets.QLabel("Full Name:", parent=Dialog)
        self.fullname_label.setGeometry(QtCore.QRect(80, 110, 100, 24))
        self.fullname_label.setFont(font_label)

        self.username_label = QtWidgets.QLabel("Username:", parent=Dialog)
        self.username_label.setGeometry(QtCore.QRect(80, 150, 100, 24))
        self.username_label.setFont(font_label)

        self.password_label = QtWidgets.QLabel("Password:", parent=Dialog)
        self.password_label.setGeometry(QtCore.QRect(80, 190, 100, 24))
        self.password_label.setFont(font_label)

        self.confirm_label = QtWidgets.QLabel("Confirm Password:", parent=Dialog)
        self.confirm_label.setGeometry(QtCore.QRect(80, 230, 130, 24))
        self.confirm_label.setFont(font_label)

        input_style = """
            QLineEdit {
                background-color: white;
                border-radius: 5px;
                padding: 3px;
                border: 1px solid #81d4fa;
            }
            QLineEdit:focus {
                border: 1px solid #0288d1;
                background-color: #e1f5fe;
            }
        """

        self.lineEdit_fullname = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_fullname.setGeometry(QtCore.QRect(220, 110, 200, 28))
        self.lineEdit_fullname.setFont(font_input)
        self.lineEdit_fullname.setStyleSheet(input_style)

        self.lineEdit_username = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_username.setGeometry(QtCore.QRect(220, 150, 200, 28))
        self.lineEdit_username.setFont(font_input)
        self.lineEdit_username.setStyleSheet(input_style)

        self.lineEdit_password = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_password.setGeometry(QtCore.QRect(220, 190, 200, 28))
        self.lineEdit_password.setFont(font_input)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_password.setStyleSheet(input_style)

        self.lineEdit_confirm = QtWidgets.QLineEdit(parent=Dialog)
        self.lineEdit_confirm.setGeometry(QtCore.QRect(220, 230, 200, 28))
        self.lineEdit_confirm.setFont(font_input)
        self.lineEdit_confirm.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_confirm.setStyleSheet(input_style)

        self.radio_customer = QtWidgets.QRadioButton("Customer", parent=Dialog)
        self.radio_customer.setGeometry(QtCore.QRect(160, 270, 100, 22))
        self.radio_customer.setChecked(True)
        self.radio_customer.setFont(font_label)
        self.radio_customer.setStyleSheet("color:#01579b;")

        self.radio_admin = QtWidgets.QRadioButton("Admin", parent=Dialog)
        self.radio_admin.setGeometry(QtCore.QRect(270, 270, 100, 22))
        self.radio_admin.setFont(font_label)
        self.radio_admin.setStyleSheet("color:#01579b;")

        self.btn_back = QtWidgets.QPushButton("Back to Login", parent=Dialog)
        self.btn_back.setGeometry(QtCore.QRect(100, 320, 130, 32))
        self.btn_back.setFont(font_label)
        self.btn_back.setStyleSheet("""
            QPushButton {
                background-color: #0288d1;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #0277bd;
            }
        """)
        self.btn_back.clicked.connect(lambda: main_app.show_login())

        self.btn_register = QtWidgets.QPushButton("Register", parent=Dialog)
        self.btn_register.setGeometry(QtCore.QRect(260, 320, 130, 32))
        self.btn_register.setFont(font_label)
        self.btn_register.setStyleSheet("""
            QPushButton {
                background-color: #00796b;
                color: white;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #00695c;
            }
        """)
        self.btn_register.clicked.connect(self.register_user)

    def register_user(self):
        fullname = self.lineEdit_fullname.text().strip()
        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()
        confirm = self.lineEdit_confirm.text().strip()
        role = "customer" if self.radio_customer.isChecked() else "admin"

        if not (fullname and username and password and confirm):
            QtWidgets.QMessageBox.warning(None, "Error", "âš ï¸ Please fill out all fields.")
            return

        if password != confirm:
            QtWidgets.QMessageBox.warning(None, "Error", "âš ï¸ Passwords do not match.")
            self.lineEdit_confirm.clear()
            return

        connection = mydb()
        if connection is None:
            QtWidgets.QMessageBox.critical(None, "Error", "âŒ Database connection failed.")
            return

        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                QtWidgets.QMessageBox.warning(None, "Error", "âš ï¸ Username already exists.")
                return

            query = "INSERT INTO users (full_name, username, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (fullname, username, password, role))
            connection.commit()

            QtWidgets.QMessageBox.information(None, "Success", "âœ… Signup successful! Redirecting to login...")

            self.lineEdit_fullname.clear()
            self.lineEdit_username.clear()
            self.lineEdit_password.clear()
            self.lineEdit_confirm.clear()

            try:
                self.Dialog.hide()
            except Exception:
                pass

            if self.main_app:
                self.main_app.show_login()

        except Error as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", f"âŒ {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"âŒ Unexpected error: {e}")
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            try:
                connection.close()
            except Exception:
                pass


class AdminDashboardUI:
    def setupUi(self, MainWindow, main_app=None, user_id=None):
        self.main_app = main_app
        self.MainWindow = MainWindow
        MainWindow.resize(1200, 750)
        MainWindow.setWindowTitle("ðŸ§º Fresh Flow Laundry System â€” Admin Dashboard")
        MainWindow.setStyleSheet("background-color: #f4faff; font: 11pt 'Times New Roman';")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.label_header = QtWidgets.QLabel("ðŸ§º FRESH FLOW LAUNDRY SYSTEM â€” ADMIN DASHBOARD", parent=self.centralwidget)
        self.label_header.setGeometry(QtCore.QRect(300, 20, 650, 40))
        self.label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_header.setFont(QtGui.QFont("Times New Roman", 16, QtGui.QFont.Weight.Bold))

        self.btn_logout = QtWidgets.QPushButton("ðŸšª Logout", parent=self.centralwidget)
        self.btn_logout.setGeometry(QtCore.QRect(1050, 25, 100, 35))
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: white;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0f2ff;
            }
        """)
        self.btn_logout.clicked.connect(self.logout)

        self.summary_box = QtWidgets.QGroupBox("ðŸ“Š System Overview", parent=self.centralwidget)
        self.summary_box.setGeometry(QtCore.QRect(50, 80, 1100, 150))
        self.summary_box.setStyleSheet("QGroupBox { background-color: #e8f4ff; border-radius: 10px; }")

        stats = [
            ("ðŸ‘¥ Total Customers", "124"),
            ("ðŸ§º Active Orders", "32"),
            ("âœ… Completed Orders", "598"),
            ("ðŸ’° Total Revenue", "â‚±142,350")
        ]

        for i, (title, value) in enumerate(stats):
            title_label = QtWidgets.QLabel(title, parent=self.summary_box)
            title_label.setGeometry(QtCore.QRect(50 + (i * 260), 40, 180, 25))
            title_label.setFont(QtGui.QFont("Times New Roman", 11, QtGui.QFont.Weight.Bold))

            value_label = QtWidgets.QLabel(value, parent=self.summary_box)
            value_label.setGeometry(QtCore.QRect(50 + (i * 260), 70, 180, 25))
            value_label.setFont(QtGui.QFont("Times New Roman", 13))

        self.customers_box = QtWidgets.QGroupBox("ðŸ‘¥ Manage Customers", parent=self.centralwidget)
        self.customers_box.setGeometry(QtCore.QRect(50, 250, 500, 200))
        self.customers_box.setStyleSheet("QGroupBox { background-color: #e8f4ff; border-radius: 10px; }")

        QtWidgets.QLabel("Select Active Customer:", parent=self.customers_box).setGeometry(QtCore.QRect(20, 35, 200, 25))
        self.customer_dropdown = QtWidgets.QComboBox(parent=self.customers_box)
        self.customer_dropdown.setGeometry(QtCore.QRect(190, 35, 250, 25))
        self.customer_dropdown.addItems(["Rendell Alfanta", "Erica Mundiz", "Charina Hibaya"])
        self.customer_dropdown.currentTextChanged.connect(self.display_customer_info)

        self.info_label = QtWidgets.QLabel(
            "Customer ID: CUST-101\nContact: 09123456789\nAddress: Brgy. Matina Pangi\nActive Orders: 2",
            parent=self.customers_box
        )
        self.info_label.setGeometry(QtCore.QRect(20, 70, 460, 80))
        self.info_label.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")

        self.btn_refresh_customers = QtWidgets.QPushButton("ðŸ”„ Refresh", parent=self.customers_box)
        self.btn_refresh_customers.setGeometry(QtCore.QRect(190, 160, 120, 25))
        self.btn_refresh_customers.clicked.connect(self.refresh_customers)

        self.orders_box = QtWidgets.QGroupBox("ðŸ“¦ Manage Orders", parent=self.centralwidget)
        self.orders_box.setGeometry(QtCore.QRect(580, 250, 570, 200))
        self.orders_box.setStyleSheet("QGroupBox { background-color: #e8f4ff; border-radius: 10px; }")

        QtWidgets.QLabel("Select Order:", parent=self.orders_box).setGeometry(QtCore.QRect(20, 35, 120, 25))
        self.order_dropdown = QtWidgets.QComboBox(parent=self.orders_box)
        self.order_dropdown.setGeometry(QtCore.QRect(130, 35, 180, 25))
        self.order_dropdown.addItems(["O001 - Rendell Alfanta", "O002 - Erica Mundiz", "O003 - Charina Hibaya"])
        self.order_dropdown.currentTextChanged.connect(self.display_order_status)

        QtWidgets.QLabel("Update Status:", parent=self.orders_box).setGeometry(QtCore.QRect(320, 35, 120, 25))
        self.status_dropdown = QtWidgets.QComboBox(parent=self.orders_box)
        self.status_dropdown.setGeometry(QtCore.QRect(430, 35, 120, 25))
        self.status_dropdown.addItems(["Pending", "In Progress", "Completed"])

        self.order_info = QtWidgets.QLabel("Current: Pending | Total: â‚±250", parent=self.orders_box)
        self.order_info.setGeometry(QtCore.QRect(20, 70, 530, 40))
        self.order_info.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")

        self.btn_update_order = QtWidgets.QPushButton("âœ… Update Status", parent=self.orders_box)
        self.btn_update_order.setGeometry(QtCore.QRect(220, 150, 150, 30))
        self.btn_update_order.clicked.connect(self.update_order_status)

        self.reports_box = QtWidgets.QGroupBox("ðŸ“ˆ Reports & Analytics", parent=self.centralwidget)
        self.reports_box.setGeometry(QtCore.QRect(50, 470, 500, 230))
        self.reports_box.setStyleSheet("QGroupBox { background-color: #e8f4ff; border-radius: 10px; }")

        self.report_text = QtWidgets.QTextEdit(parent=self.reports_box)
        self.report_text.setGeometry(QtCore.QRect(20, 40, 460, 140))
        self.report_text.setReadOnly(True)
        self.report_text.setPlainText(
            "ðŸ“… Monthly Overview:\n"
            "â€¢ Total Revenue: â‚±142,350 (+8%)\n"
            "â€¢ New Customers: 15\n"
            "â€¢ Completed Orders: 598\n"
            "â€¢ Pending Orders: 32\n"
            "â€¢ Complaints Received: 3\n"
            "â€¢ Customer Satisfaction: 94%\n"
        )

        self.btn_generate_report = QtWidgets.QPushButton("ðŸ“Š Generate Report", parent=self.reports_box)
        self.btn_generate_report.setGeometry(QtCore.QRect(180, 190, 150, 30))
        self.btn_generate_report.clicked.connect(self.generate_report)

        self.msg_box = QtWidgets.QGroupBox("ðŸ’¬ Customer Messages", parent=self.centralwidget)
        self.msg_box.setGeometry(QtCore.QRect(580, 470, 570, 230))
        self.msg_box.setStyleSheet("QGroupBox { background-color: #e8f4ff; border-radius: 10px; }")

        QtWidgets.QLabel("Select Customer:", parent=self.msg_box).setGeometry(QtCore.QRect(20, 40, 130, 25))
        self.msg_customer_dropdown = QtWidgets.QComboBox(parent=self.msg_box)
        self.msg_customer_dropdown.setGeometry(QtCore.QRect(150, 40, 180, 25))
        self.msg_customer_dropdown.addItems(["Rendell Alfanta", "Erica Mundiz", "Charina Hibaya"])
        self.msg_customer_dropdown.currentTextChanged.connect(self.display_customer_message)

        self.message_display = QtWidgets.QLabel("Message: Please speed up my laundry.", parent=self.msg_box)
        self.message_display.setGeometry(QtCore.QRect(20, 80, 530, 50))
        self.message_display.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")

        self.reply_input = QtWidgets.QLineEdit(parent=self.msg_box)
        self.reply_input.setGeometry(QtCore.QRect(20, 140, 430, 30))
        self.reply_input.setPlaceholderText("Type your reply here...")

        self.btn_reply = QtWidgets.QPushButton("ðŸ“¨ Send Reply", parent=self.msg_box)
        self.btn_reply.setGeometry(QtCore.QRect(460, 140, 100, 30))
        self.btn_reply.clicked.connect(self.reply_message)

    def display_customer_info(self):
        name = self.customer_dropdown.currentText()
        info_map = {
            "Rendell Alfanta": "Customer ID: CUST-101\nContact: 09123456789\nAddress: Brgy. Matina Pangi\nActive Orders: 2",
            "Erica Mundiz": "Customer ID: CUST-102\nContact: 09987654321\nAddress: Brgy. Dona Pilar\nActive Orders: 1",
            "Charina Hibaya": "Customer ID: CUST-103\nContact: 09112223344\nAddress: Brgy. Bago Aplaya\nActive Orders: 3"
        }
        self.info_label.setText(info_map.get(name, ""))

    def refresh_customers(self):
        QtWidgets.QMessageBox.information(None, "Refreshed", "Customer data updated successfully!")

    def display_order_status(self):
        order = self.order_dropdown.currentText().split(" - ")[0]
        order_info = {
            "O001": ("Pending", "â‚±250"),
            "O002": ("Completed", "â‚±320"),
            "O003": ("In Progress", "â‚±180")
        }
        status, total = order_info.get(order, ("Pending", "â‚±0"))
        self.order_info.setText(f"Current: {status} | Total: {total}")
        try:
            self.status_dropdown.setCurrentText(status)
        except Exception:
            pass

    def update_order_status(self):
        status = self.status_dropdown.currentText()
        QtWidgets.QMessageBox.information(None, "Order Updated", f"Order status changed to '{status}'.")

    def generate_report(self):
        QtWidgets.QMessageBox.information(None, "Report", "ðŸ“ˆ New system report generated successfully!")

    def display_customer_message(self):
        name = self.msg_customer_dropdown.currentText()
        msg_map = {
            "Rendell Alfanta": "Please speed up my laundry.",
            "Erica Mundiz": "Thank you for the service!",
            "Charina Hibaya": "Is my order ready?"
        }
        self.message_display.setText(f"Message: {msg_map.get(name, '')}")

    def reply_message(self):
        reply_text = self.reply_input.text()
        if not reply_text.strip():
            QtWidgets.QMessageBox.warning(None, "Empty", "Please type a reply before sending.")
            return
        customer = self.msg_customer_dropdown.currentText()
        QtWidgets.QMessageBox.information(None, "Reply Sent", f"Reply sent to {customer}:\n\n{reply_text}")
        self.reply_input.clear()

    def logout(self):
        confirm = QtWidgets.QMessageBox.question(
            None, "Confirm Logout", "Are you sure you want to logout?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                self.MainWindow.close()
            except Exception:
                pass
            if self.main_app:
                self.main_app.show_login()


class CustomerDashboardUI:
    def setupUi(self, CustomerDashboard, main_app=None, user_id=None):
        self.main_app = main_app
        self.CustomerDashboard = CustomerDashboard
        self.CustomerDashboard.setObjectName("CustomerDashboard")
        self.CustomerDashboard.resize(1280, 900)
        self.CustomerDashboard.setWindowTitle("ðŸ§º Fresh Flow Laundry System - Customer Dashboard")
        self.CustomerDashboard.setStyleSheet("""
            QWidget { background-color: #f4faff; font: 11pt 'Times New Roman'; }
            QGroupBox { 
                background-color: #e8f4ff; 
                border-radius: 12px; 
                font-weight: bold;
                margin-top: 12px;
                padding-top: 10px;
            }
            QPushButton {
                background-color: white; 
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #d0e8ff;
            }
        """)

        # Use a root widget layout to host components when CustomerDashboard is a QWidget
        root_layout = QtWidgets.QVBoxLayout(self.CustomerDashboard)

        header_layout = QtWidgets.QHBoxLayout()
        self.header_label = QtWidgets.QLabel("ðŸ§º FRESH FLOW LAUNDRY SYSTEM - CUSTOMER DASHBOARD")
        self.header_label.setFont(QtGui.QFont("Times New Roman", 18, QtGui.QFont.Weight.Bold))
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.btn_logout = QtWidgets.QPushButton("ðŸšª Logout")
        self.btn_logout.setFixedWidth(100)
        self.btn_logout.clicked.connect(self.logout)
        header_layout.addWidget(self.header_label)
        header_layout.addWidget(self.btn_logout)
        root_layout.addLayout(header_layout)

        top_layout = QtWidgets.QHBoxLayout()

        self.profile_box = QtWidgets.QGroupBox("ðŸ‘¤ Profile Information")
        self.profile_box.setFixedWidth(360)
        profile_layout = QtWidgets.QVBoxLayout()
        labels = ["Customer ID:", "Full Name:", "Address:", "Email:", "Mobile:"]
        self.profile_fields = {}
        for text in labels:
            row_layout = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel(text)
            line_edit = QtWidgets.QLineEdit()
            line_edit.setStyleSheet("background-color: white; border-radius: 5px;")
            row_layout.addWidget(label)
            row_layout.addWidget(line_edit)
            profile_layout.addLayout(row_layout)
            self.profile_fields[text] = line_edit
        generated_id = f"CUST-{random.randint(100, 999)}"
        self.profile_fields["Customer ID:"].setText(generated_id)
        self.profile_fields["Customer ID:"].setReadOnly(True)
        self.profile_fields["Customer ID:"].setStyleSheet("background-color: #f0f0f0; border-radius: 5px;")
        self.btn_save_profile = QtWidgets.QPushButton("ðŸ’¾ Save Details")
        self.btn_save_profile.clicked.connect(self.save_profile)
        profile_layout.addWidget(self.btn_save_profile)
        self.profile_box.setLayout(profile_layout)

        self.order_box = QtWidgets.QGroupBox("ðŸ§¼ Place New Order")
        order_layout = QtWidgets.QVBoxLayout()

        row1 = QtWidgets.QHBoxLayout()
        self.combo_item = QtWidgets.QComboBox()
        self.combo_item.addItems([
            "Shirt - â‚±25", "Pants - â‚±35", "Jacket - â‚±50",
            "Bedsheet - â‚±70", "Towel - â‚±30", "Curtain - â‚±90"
        ])
        self.spin_qty = QtWidgets.QSpinBox()
        self.spin_qty.setRange(1, 50)
        self.btn_add_item = QtWidgets.QPushButton("âž• Add Item")
        self.btn_add_item.clicked.connect(self.add_item)
        row1.addWidget(QtWidgets.QLabel("Laundry Item:"))
        row1.addWidget(self.combo_item)
        row1.addWidget(QtWidgets.QLabel("Quantity:"))
        row1.addWidget(self.spin_qty)
        row1.addWidget(self.btn_add_item)
        order_layout.addLayout(row1)

        self.table_items = QtWidgets.QTableWidget()
        self.table_items.setColumnCount(3)
        self.table_items.setHorizontalHeaderLabels(["Item", "Quantity", "Price (â‚±)"])
        self.table_items.horizontalHeader().setStretchLastSection(True)
        order_layout.addWidget(self.table_items)

        self.btn_delete_item = QtWidgets.QPushButton("ðŸ—‘ï¸ Delete Selected")
        self.btn_delete_item.clicked.connect(self.delete_item)
        order_layout.addWidget(self.btn_delete_item)

        row2 = QtWidgets.QHBoxLayout()
        self.combo_service = QtWidgets.QComboBox()
        self.combo_service.addItems(["Normal - â‚±15", "Delicate - â‚±25", "Dry Clean - â‚±40"])
        self.combo_detergent = QtWidgets.QComboBox()
        self.combo_detergent.addItems(["Regular - â‚±10", "Hypo Allergenic - â‚±20"])
        self.combo_discount = QtWidgets.QComboBox()
        self.combo_discount.addItems(["None", "Student - 10%", "Senior Citizen - 20%"])
        row2.addWidget(QtWidgets.QLabel("Service Type:"))
        row2.addWidget(self.combo_service)
        row2.addWidget(QtWidgets.QLabel("Detergent:"))
        row2.addWidget(self.combo_detergent)
        row2.addWidget(QtWidgets.QLabel("Discount:"))
        row2.addWidget(self.combo_discount)
        order_layout.addLayout(row2)

        self.btn_submit_order = QtWidgets.QPushButton("âœ… Submit Order")
        self.btn_submit_order.clicked.connect(self.submit_order)
        order_layout.addWidget(self.btn_submit_order)

        self.order_box.setLayout(order_layout)

        top_layout.addWidget(self.profile_box)
        top_layout.addWidget(self.order_box)
        root_layout.addLayout(top_layout)

        middle_layout = QtWidgets.QHBoxLayout()

        self.status_box = QtWidgets.QGroupBox("ðŸ“¦ Laundry Status")
        status_layout = QtWidgets.QVBoxLayout()
        self.status_text = QtWidgets.QLabel("No active orders.")
        self.btn_refresh_status = QtWidgets.QPushButton("ðŸ”„ Refresh")
        self.btn_refresh_status.clicked.connect(self.refresh_status)
        status_layout.addWidget(self.status_text)
        status_layout.addWidget(self.btn_refresh_status)
        self.status_box.setLayout(status_layout)

        self.payment_box = QtWidgets.QGroupBox("ðŸ’³ Payment Details")
        payment_layout = QtWidgets.QVBoxLayout()
        self.input_amount = QtWidgets.QLineEdit()
        self.combo_payment = QtWidgets.QComboBox()
        self.combo_payment.addItems(["Cash", "Credit Card", "GCash"])
        self.btn_confirm_payment = QtWidgets.QPushButton("ðŸ’° Confirm Payment")
        self.btn_confirm_payment.clicked.connect(self.confirm_payment)
        payment_layout.addWidget(QtWidgets.QLabel("Amount:"))
        payment_layout.addWidget(self.input_amount)
        payment_layout.addWidget(self.combo_payment)
        payment_layout.addWidget(self.btn_confirm_payment)
        self.payment_box.setLayout(payment_layout)

        self.summary_box = QtWidgets.QGroupBox("ðŸ“„ Order Summary")
        summary_layout = QtWidgets.QVBoxLayout()
        self.summary_text = QtWidgets.QTextEdit()
        self.summary_text.setReadOnly(True)
        self.btn_save_receipt = QtWidgets.QPushButton("ðŸ’¾ Save Receipt")
        self.btn_save_receipt.clicked.connect(self.save_receipt)
        summary_layout.addWidget(self.summary_text)
        summary_layout.addWidget(self.btn_save_receipt)
        self.summary_box.setLayout(summary_layout)

        self.rating_box = QtWidgets.QGroupBox("â­ Rate Our Service")
        rating_layout = QtWidgets.QHBoxLayout()
        self.combo_rating = QtWidgets.QComboBox()
        self.combo_rating.addItems(["1", "2", "3", "4", "5"])
        self.btn_submit_rating = QtWidgets.QPushButton("ðŸ“¤ Submit Rating")
        self.btn_submit_rating.clicked.connect(self.submit_rating)
        rating_layout.addWidget(QtWidgets.QLabel("Rating (1-5):"))
        rating_layout.addWidget(self.combo_rating)
        rating_layout.addWidget(self.btn_submit_rating)
        self.rating_box.setLayout(rating_layout)

        middle_layout.addWidget(self.status_box)
        middle_layout.addWidget(self.payment_box)
        middle_layout.addWidget(self.summary_box)
        middle_layout.addWidget(self.rating_box)

        root_layout.addLayout(middle_layout)

        self.feedback_box = QtWidgets.QGroupBox("ðŸ“ Feedback to Service")
        feedback_layout = QtWidgets.QVBoxLayout()
        self.input_feedback = QtWidgets.QTextEdit()
        self.input_feedback.setPlaceholderText("Write your feedback here...")
        self.btn_submit_feedback = QtWidgets.QPushButton("ðŸ“¤ Submit Feedback")
        self.btn_submit_feedback.clicked.connect(self.submit_feedback)
        feedback_layout.addWidget(self.input_feedback)
        feedback_layout.addWidget(self.btn_submit_feedback)
        self.feedback_box.setLayout(feedback_layout)
        root_layout.addWidget(self.feedback_box)

        bottom_layout = QtWidgets.QHBoxLayout()

        self.msg_box = QtWidgets.QGroupBox("ðŸ’¬ Message Provider")
        msg_layout = QtWidgets.QVBoxLayout()
        self.input_msg = QtWidgets.QTextEdit()
        self.btn_send_msg = QtWidgets.QPushButton("ðŸ“¨ Send")
        self.btn_send_msg.clicked.connect(self.send_message)
        msg_layout.addWidget(self.input_msg)
        msg_layout.addWidget(self.btn_send_msg)
        self.msg_box.setLayout(msg_layout)

        self.notification_box = QtWidgets.QGroupBox("ðŸ”” Notifications")
        notif_layout = QtWidgets.QVBoxLayout()
        self.notification_text = QtWidgets.QTextEdit()
        self.notification_text.setReadOnly(True)
        self.btn_refresh_notif = QtWidgets.QPushButton("ðŸ”„ Refresh")
        self.btn_refresh_notif.clicked.connect(self.refresh_notifications)
        notif_layout.addWidget(self.notification_text)
        notif_layout.addWidget(self.btn_refresh_notif)
        self.notification_box.setLayout(notif_layout)

        bottom_layout.addWidget(self.msg_box)
        bottom_layout.addWidget(self.notification_box)
        root_layout.addLayout(bottom_layout)

        self.total_amount = 0.0
        self.order_items = []

    def logout(self):
        reply = QMessageBox.question(self.CustomerDashboard, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.CustomerDashboard.close()
            except Exception:
                pass
            if hasattr(self, "main_app") and self.main_app:
                self.main_app.show_login()

    def save_profile(self):
        QMessageBox.information(self.CustomerDashboard, "Profile Saved", "Your profile details have been saved.")

    def add_item(self):
        item_text = self.combo_item.currentText()
        qty = self.spin_qty.value()
        try:
            price_per_item = float(item_text.split("â‚±")[1])
        except Exception:
            price_per_item = 0.0
        item_name = item_text.split(" - ")[0]
        total_price = price_per_item * qty

        self.order_items.append((item_name, qty, total_price))
        self.update_table()
        self.update_summary()

    def delete_item(self):
        selected_rows = sorted({idx.row() for idx in self.table_items.selectedIndexes()}, reverse=True)
        if not selected_rows:
            QMessageBox.warning(self.CustomerDashboard, "No Selection", "Please select a row to delete.")
            return
        for row in selected_rows:
            if 0 <= row < len(self.order_items):
                del self.order_items[row]
        self.update_table()
        self.update_summary()

    def update_table(self):
        self.table_items.setRowCount(len(self.order_items))
        for row, (item, qty, price) in enumerate(self.order_items):
            self.table_items.setItem(row, 0, QtWidgets.QTableWidgetItem(item))
            self.table_items.setItem(row, 1, QtWidgets.QTableWidgetItem(str(qty)))
            self.table_items.setItem(row, 2, QtWidgets.QTableWidgetItem(f"{price:.2f}"))

    def update_summary(self):
        self.total_amount = sum(price for _, _, price in self.order_items)
        try:
            service_price = float(self.combo_service.currentText().split("â‚±")[1])
        except Exception:
            service_price = 0.0
        try:
            detergent_price = float(self.combo_detergent.currentText().split("â‚±")[1])
        except Exception:
            detergent_price = 0.0

        discount_text = self.combo_discount.currentText()
        discount_rate = 0
        if "Student" in discount_text:
            discount_rate = 0.10
        elif "Senior" in discount_text:
            discount_rate = 0.20

        subtotal = self.total_amount + service_price + detergent_price
        total_after_discount = subtotal * (1 - discount_rate)
        self.total_amount = total_after_discount

        summary_lines = [f"{item} x {qty} = â‚±{price:.2f}" for item, qty, price in self.order_items]
        summary_lines.append(f"Service: {self.combo_service.currentText()}")
        summary_lines.append(f"Detergent: {self.combo_detergent.currentText()}")
        summary_lines.append(f"Discount: {self.combo_discount.currentText()}")
        summary_lines.append(f"Total Amount: â‚±{self.total_amount:.2f}")
        self.summary_text.setText("\n".join(summary_lines))
        self.input_amount.setText(f"{self.total_amount:.2f}")

    def submit_order(self):
        if not self.order_items:
            QMessageBox.warning(self.CustomerDashboard, "No Items", "Please add items before submitting an order.")
            return
        QMessageBox.information(self.CustomerDashboard, "Order Submitted", "Your order has been submitted successfully.")
        self.status_text.setText("Order submitted. Waiting for processing...")
        self.order_items.clear()
        self.update_table()
        self.update_summary()

    def refresh_status(self):
        self.status_text.setText("No active orders." if not self.order_items else "Processing order...")

    def confirm_payment(self):
        try:
            amount = float(self.input_amount.text())
            if amount < self.total_amount:
                QMessageBox.warning(self.CustomerDashboard, "Payment Error", "Amount is less than total!")
                return
        except ValueError:
            QMessageBox.warning(self.CustomerDashboard, "Payment Error", "Invalid amount entered!")
            return
        QMessageBox.information(self.CustomerDashboard, "Payment Confirmed",
                                f"Payment of â‚±{amount:.2f} received via {self.combo_payment.currentText()}.")

    def save_receipt(self):
        try:
            with open("receipt.txt", "w", encoding="utf-8") as f:
                f.write(self.summary_text.toPlainText())
            QMessageBox.information(self.CustomerDashboard, "Saved", "Receipt saved as receipt.txt")
        except Exception as e:
            QMessageBox.critical(self.CustomerDashboard, "Error", f"Could not save receipt: {e}")

    def send_message(self):
        msg = self.input_msg.toPlainText().strip()
        if not msg:
            QMessageBox.warning(self.CustomerDashboard, "Empty Message", "Please type a message to send.")
            return
        QMessageBox.information(self.CustomerDashboard, "Message Sent", "Your message has been sent to admin.")
        self.input_msg.clear()

    def refresh_notifications(self):
        self.notification_text.setText("No new notifications.")

    def submit_rating(self):
        rating = self.combo_rating.currentText()
        QMessageBox.information(self.CustomerDashboard, "Rating Submitted", f"Thank you for rating us {rating}/5!")

    def submit_feedback(self):
        feedback_text = self.input_feedback.toPlainText().strip()
        if not feedback_text:
            QMessageBox.warning(self.CustomerDashboard, "Empty Feedback", "Please write something before submitting.")
            return
        QMessageBox.information(self.CustomerDashboard, "Feedback Submitted", "Your feedback has been sent to the admin.")
        self.input_feedback.clear()


class FreshFlow:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setApplicationName("Fresh Flow Laundry System")

        self.login_window = None
        self.signup_window = None
        self.customer_window = None
        self.admin_window = None

        self.login_ui = None
        self.signup_ui = None
        self.customer_ui = None
        self.admin_ui = None

        # prepare windows
        self.setup_login_window()
        self.setup_signup_window()

    def setup_login_window(self):
        self.login_window = QtWidgets.QDialog()
        self.login_ui = LoginUI()
        self.login_ui.setupUi(self.login_window, self)

    def setup_signup_window(self):
        self.signup_window = QtWidgets.QDialog()
        self.signup_ui = SignupUI()
        self.signup_ui.setupUi(self.signup_window, self)

    def _hide_all_windows(self):
        for window in [
            self.login_window,
            self.signup_window,
            self.customer_window,
            self.admin_window,
        ]:
            if window:
                try:
                    window.hide()
                except Exception:
                    pass

    def show_login(self):
        self._hide_all_windows()
        if not self.login_window:
            self.setup_login_window()
        self.login_window.show()

    def show_signup(self):
        self._hide_all_windows()
        if not self.signup_window:
            self.setup_signup_window()
        self.signup_window.show()

    def show_customer_dashboard(self, user_id=None):
        self._hide_all_windows()
        self.customer_window = QtWidgets.QWidget()
        self.customer_ui = CustomerDashboardUI()
        self.customer_ui.setupUi(self.customer_window, self, user_id)
        self.customer_window.show()

    def show_admin_dashboard(self, user_id=None):
        self._hide_all_windows()
        self.admin_window = QtWidgets.QMainWindow()
        self.admin_ui = AdminDashboardUI()
        self.admin_ui.setupUi(self.admin_window, self, user_id)
        self.admin_window.show()

    def run(self):
        self.show_login()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    main_app = FreshFlow()
    main_app.run()