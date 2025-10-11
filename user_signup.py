from PyQt6 import QtWidgets, QtCore, QtGui
import mysql.connector
from DATABASE import mydb

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
            QtWidgets.QMessageBox.warning(None, "Error", "⚠️ Please fill out all fields.")
            return

        if password != confirm:
            QtWidgets.QMessageBox.warning(None, "Error", "⚠️ Passwords do not match.")
            self.lineEdit_confirm.clear()
            return

        connection = mydb()
        if connection is None:
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                QtWidgets.QMessageBox.warning(None, "Error", "⚠️ Username already exists.")
                return

            query = "INSERT INTO users (full_name, username, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (fullname, username, password, role))
            connection.commit()

            QtWidgets.QMessageBox.information(None, "Success", "✅ Signup successful! Redirecting to login...")

            self.lineEdit_fullname.clear()
            self.lineEdit_username.clear()
            self.lineEdit_password.clear()
            self.lineEdit_confirm.clear()

            self.Dialog.hide()
            self.main_app.show_login()

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", f"❌ {e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"❌ Unexpected error: {e}")
        finally:
            cursor.close()
            connection.close()
