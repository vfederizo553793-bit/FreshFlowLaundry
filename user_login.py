from PyQt6 import QtCore, QtGui, QtWidgets
from DATABASE import mydb


class LoginUI:
    def setupUi(self, Dialog, main_app):
        self.main_app = main_app
        Dialog.setObjectName("LoginDialog")
        Dialog.resize(480, 400)
        Dialog.setStyleSheet("background-color: lightblue;")

        self.label_logo = QtWidgets.QLabel(Dialog)
        self.label_logo.setGeometry(QtCore.QRect(45, 25, 60, 60))
        try:
            self.label_logo.setPixmap(QtGui.QPixmap("logo.png"))
            self.label_logo.setScaledContents(True)
        except:
            self.label_logo.setText("🧺")
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
            QtWidgets.QMessageBox.warning(None, "Error", "⚠️ Please enter both username and password.")
            return

        connection = mydb()
        if connection is None:
            QtWidgets.QMessageBox.critical(None, "Error", "❌ Database connection failed.")
            return

        try:
            cursor = connection.cursor()
            query = "SELECT user_id, full_name, role FROM users WHERE username=%s AND password=%s AND role=%s"
            cursor.execute(query, (username, password, role))
            result = cursor.fetchone()

            if result:
                user_id, full_name, db_role = result
                QtWidgets.QMessageBox.information(None, "Success", f"✅ Welcome, {full_name}!")

                self.lineEdit_password.clear()

                if db_role == "admin":
                    self.main_app.show_admin_dashboard(user_id)
                else:
                    self.main_app.show_customer_dashboard(user_id)
            else:
                QtWidgets.QMessageBox.warning(None, "Login Failed", "❌ Invalid username, password, or role.")
                self.lineEdit_password.clear()
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"❌ Database error: {str(e)}")
        finally:
            cursor.close()
            connection.close()