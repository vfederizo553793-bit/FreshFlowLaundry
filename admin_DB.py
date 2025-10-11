from PyQt6 import QtCore, QtGui, QtWidgets

class AdminDashboardUI:
    def setupUi(self, MainWindow, main_app=None):
        self.main_app = main_app
        self.MainWindow = MainWindow
        MainWindow.resize(1200, 750)
        MainWindow.setWindowTitle("🧺 Fresh Flow Laundry System — Admin Dashboard")
        MainWindow.setStyleSheet("background-color: #f4faff; font: 11pt 'Times New Roman';")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        self.label_header = QtWidgets.QLabel("🧺 FRESH FLOW LAUNDRY SYSTEM — ADMIN DASHBOARD", parent=self.centralwidget)
        self.label_header.setGeometry(QtCore.QRect(300, 20, 650, 40))
        self.label_header.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_header.setFont(QtGui.QFont("Times New Roman", 16, QtGui.QFont.Weight.Bold))

        self.btn_logout = QtWidgets.QPushButton("🚪 Logout", parent=self.centralwidget)
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

        self.summary_box = QtWidgets.QGroupBox("📊 System Overview", parent=self.centralwidget)
        self.summary_box.setGeometry(QtCore.QRect(50, 80, 1100, 150))
        self.summary_box.setStyleSheet("QGroupBox { background-color: #e8f4ff; border-radius: 10px; }")

        stats = [
            ("👥 Total Customers", "124"),
            ("🧺 Active Orders", "32"),
            ("✅ Completed Orders", "598"),
            ("💰 Total Revenue", "₱142,350")
        ]

        for i, (title, value) in enumerate(stats):
            title_label = QtWidgets.QLabel(title, parent=self.summary_box)
            title_label.setGeometry(QtCore.QRect(50 + (i * 260), 40, 180, 25))
            title_label.setFont(QtGui.QFont("Times New Roman", 11, QtGui.QFont.Weight.Bold))

            value_label = QtWidgets.QLabel(value, parent=self.summary_box)
            value_label.setGeometry(QtCore.QRect(50 + (i * 260), 70, 180, 25))
            value_label.setFont(QtGui.QFont("Times New Roman", 13))

        self.customers_box = QtWidgets.QGroupBox("👥 Manage Customers", parent=self.centralwidget)
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

        self.btn_refresh_customers = QtWidgets.QPushButton("🔄 Refresh", parent=self.customers_box)
        self.btn_refresh_customers.setGeometry(QtCore.QRect(190, 160, 120, 25))
        self.btn_refresh_customers.clicked.connect(self.refresh_customers)

        self.orders_box = QtWidgets.QGroupBox("📦 Manage Orders", parent=self.centralwidget)
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

        self.order_info = QtWidgets.QLabel("Current: Pending | Total: ₱250", parent=self.orders_box)
        self.order_info.setGeometry(QtCore.QRect(20, 70, 530, 40))
        self.order_info.setStyleSheet("background-color: white; border-radius: 5px; padding: 5px;")

        self.btn_update_order = QtWidgets.QPushButton("✅ Update Status", parent=self.orders_box)
        self.btn_update_order.setGeometry(QtCore.QRect(220, 150, 150, 30))
        self.btn_update_order.clicked.connect(self.update_order_status)

        self.reports_box = QtWidgets.QGroupBox("📈 Reports & Analytics", parent=self.centralwidget)
        self.reports_box.setGeometry(QtCore.QRect(50, 470, 500, 230))
        self.reports_box.setStyleSheet("QGroupBox { background-color: #e8f4ff; border-radius: 10px; }")

        self.report_text = QtWidgets.QTextEdit(parent=self.reports_box)
        self.report_text.setGeometry(QtCore.QRect(20, 40, 460, 140))
        self.report_text.setReadOnly(True)
        self.report_text.setPlainText(
            "📅 Monthly Overview:\n"
            "• Total Revenue: ₱142,350 (+8%)\n"
            "• New Customers: 15\n"
            "• Completed Orders: 598\n"
            "• Pending Orders: 32\n"
            "• Complaints Received: 3\n"
            "• Customer Satisfaction: 94%\n"
        )

        self.btn_generate_report = QtWidgets.QPushButton("📊 Generate Report", parent=self.reports_box)
        self.btn_generate_report.setGeometry(QtCore.QRect(180, 190, 150, 30))
        self.btn_generate_report.clicked.connect(self.generate_report)

        self.msg_box = QtWidgets.QGroupBox("💬 Customer Messages", parent=self.centralwidget)
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

        self.btn_reply = QtWidgets.QPushButton("📨 Send Reply", parent=self.msg_box)
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
            "O001": ("Pending", "₱250"),
            "O002": ("Completed", "₱320"),
            "O003": ("In Progress", "₱180")
        }
        status, total = order_info.get(order, ("Pending", "₱0"))
        self.order_info.setText(f"Current: {status} | Total: {total}")
        self.status_dropdown.setCurrentText(status)

    def update_order_status(self):
        status = self.status_dropdown.currentText()
        QtWidgets.QMessageBox.information(None, "Order Updated", f"Order status changed to '{status}'.")

    def generate_report(self):
        QtWidgets.QMessageBox.information(None, "Report", "📈 New system report generated successfully!")

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
            if self.main_app:
                self.MainWindow.close()
                self.main_app.show_login()
            else:
                QtWidgets.QMessageBox.information(None, "Logout", "Logged out successfully!")
                self.MainWindow.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = AdminDashboardUI()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())
