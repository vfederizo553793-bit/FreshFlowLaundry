import random
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMessageBox

class CustomerDashboardUI:
    def setupUi(self, CustomerDashboard, main_app=None):
        self.main_app = main_app

        self.CustomerDashboard = CustomerDashboard
        self.CustomerDashboard.setObjectName("CustomerDashboard")
        self.CustomerDashboard.resize(1280, 900)
        self.CustomerDashboard.setWindowTitle("🧺 Fresh Flow Laundry System - Customer Dashboard")
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

        main_layout = QtWidgets.QVBoxLayout(self.CustomerDashboard)

        header_layout = QtWidgets.QHBoxLayout()
        self.header_label = QtWidgets.QLabel("🧺 FRESH FLOW LAUNDRY SYSTEM - CUSTOMER DASHBOARD")
        self.header_label.setFont(QtGui.QFont("Times New Roman", 18, QtGui.QFont.Weight.Bold))
        self.header_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.btn_logout = QtWidgets.QPushButton("🚪 Logout")
        self.btn_logout.setFixedWidth(100)
        self.btn_logout.clicked.connect(self.logout)
        header_layout.addWidget(self.header_label)
        header_layout.addWidget(self.btn_logout)
        main_layout.addLayout(header_layout)

        top_layout = QtWidgets.QHBoxLayout()

        self.profile_box = QtWidgets.QGroupBox("👤 Profile Information")
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
        self.btn_save_profile = QtWidgets.QPushButton("💾 Save Details")
        self.btn_save_profile.clicked.connect(self.save_profile)
        profile_layout.addWidget(self.btn_save_profile)
        self.profile_box.setLayout(profile_layout)

        self.order_box = QtWidgets.QGroupBox("🧼 Place New Order")
        order_layout = QtWidgets.QVBoxLayout()

        row1 = QtWidgets.QHBoxLayout()
        self.combo_item = QtWidgets.QComboBox()
        self.combo_item.addItems([
            "Shirt - ₱25", "Pants - ₱35", "Jacket - ₱50",
            "Bedsheet - ₱70", "Towel - ₱30", "Curtain - ₱90"
        ])
        self.spin_qty = QtWidgets.QSpinBox()
        self.spin_qty.setRange(1, 50)
        self.btn_add_item = QtWidgets.QPushButton("➕ Add Item")
        self.btn_add_item.clicked.connect(self.add_item)
        row1.addWidget(QtWidgets.QLabel("Laundry Item:"))
        row1.addWidget(self.combo_item)
        row1.addWidget(QtWidgets.QLabel("Quantity:"))
        row1.addWidget(self.spin_qty)
        row1.addWidget(self.btn_add_item)
        order_layout.addLayout(row1)

        self.table_items = QtWidgets.QTableWidget()
        self.table_items.setColumnCount(3)
        self.table_items.setHorizontalHeaderLabels(["Item", "Quantity", "Price (₱)"])
        self.table_items.horizontalHeader().setStretchLastSection(True)
        order_layout.addWidget(self.table_items)

        self.btn_delete_item = QtWidgets.QPushButton("🗑️ Delete Selected")
        self.btn_delete_item.clicked.connect(self.delete_item)
        order_layout.addWidget(self.btn_delete_item)

        row2 = QtWidgets.QHBoxLayout()
        self.combo_service = QtWidgets.QComboBox()
        self.combo_service.addItems(["Normal - ₱15", "Delicate - ₱25", "Dry Clean - ₱40"])
        self.combo_detergent = QtWidgets.QComboBox()
        self.combo_detergent.addItems(["Regular - ₱10", "Hypo Allergenic - ₱20"])
        self.combo_discount = QtWidgets.QComboBox()
        self.combo_discount.addItems(["None", "Student - 10%", "Senior Citizen - 20%"])
        row2.addWidget(QtWidgets.QLabel("Service Type:"))
        row2.addWidget(self.combo_service)
        row2.addWidget(QtWidgets.QLabel("Detergent:"))
        row2.addWidget(self.combo_detergent)
        row2.addWidget(QtWidgets.QLabel("Discount:"))
        row2.addWidget(self.combo_discount)
        order_layout.addLayout(row2)

        self.btn_submit_order = QtWidgets.QPushButton("✅ Submit Order")
        self.btn_submit_order.clicked.connect(self.submit_order)
        order_layout.addWidget(self.btn_submit_order)

        self.order_box.setLayout(order_layout)

        top_layout.addWidget(self.profile_box)
        top_layout.addWidget(self.order_box)
        main_layout.addLayout(top_layout)

        middle_layout = QtWidgets.QHBoxLayout()

        self.status_box = QtWidgets.QGroupBox("📦 Laundry Status")
        status_layout = QtWidgets.QVBoxLayout()
        self.status_text = QtWidgets.QLabel("No active orders.")
        self.btn_refresh_status = QtWidgets.QPushButton("🔄 Refresh")
        self.btn_refresh_status.clicked.connect(self.refresh_status)
        status_layout.addWidget(self.status_text)
        status_layout.addWidget(self.btn_refresh_status)
        self.status_box.setLayout(status_layout)

        self.payment_box = QtWidgets.QGroupBox("💳 Payment Details")
        payment_layout = QtWidgets.QVBoxLayout()
        self.input_amount = QtWidgets.QLineEdit()
        self.combo_payment = QtWidgets.QComboBox()
        self.combo_payment.addItems(["Cash", "Credit Card", "GCash"])
        self.btn_confirm_payment = QtWidgets.QPushButton("💰 Confirm Payment")
        self.btn_confirm_payment.clicked.connect(self.confirm_payment)
        payment_layout.addWidget(QtWidgets.QLabel("Amount:"))
        payment_layout.addWidget(self.input_amount)
        payment_layout.addWidget(self.combo_payment)
        payment_layout.addWidget(self.btn_confirm_payment)
        self.payment_box.setLayout(payment_layout)

        self.summary_box = QtWidgets.QGroupBox("📄 Order Summary")
        summary_layout = QtWidgets.QVBoxLayout()
        self.summary_text = QtWidgets.QTextEdit()
        self.summary_text.setReadOnly(True)
        self.btn_save_receipt = QtWidgets.QPushButton("💾 Save Receipt")
        self.btn_save_receipt.clicked.connect(self.save_receipt)
        summary_layout.addWidget(self.summary_text)
        summary_layout.addWidget(self.btn_save_receipt)
        self.summary_box.setLayout(summary_layout)

        self.rating_box = QtWidgets.QGroupBox("⭐ Rate Our Service")
        rating_layout = QtWidgets.QHBoxLayout()
        self.combo_rating = QtWidgets.QComboBox()
        self.combo_rating.addItems(["1", "2", "3", "4", "5"])
        self.btn_submit_rating = QtWidgets.QPushButton("📤 Submit Rating")
        self.btn_submit_rating.clicked.connect(self.submit_rating)
        rating_layout.addWidget(QtWidgets.QLabel("Rating (1-5):"))
        rating_layout.addWidget(self.combo_rating)
        rating_layout.addWidget(self.btn_submit_rating)
        self.rating_box.setLayout(rating_layout)

        middle_layout.addWidget(self.status_box)
        middle_layout.addWidget(self.payment_box)
        middle_layout.addWidget(self.summary_box)
        middle_layout.addWidget(self.rating_box)

        main_layout.addLayout(middle_layout)

        self.feedback_box = QtWidgets.QGroupBox("📝 Feedback to Service")
        feedback_layout = QtWidgets.QVBoxLayout()
        self.input_feedback = QtWidgets.QTextEdit()
        self.input_feedback.setPlaceholderText("Write your feedback here...")
        self.btn_submit_feedback = QtWidgets.QPushButton("📤 Submit Feedback")
        self.btn_submit_feedback.clicked.connect(self.submit_feedback)
        feedback_layout.addWidget(self.input_feedback)
        feedback_layout.addWidget(self.btn_submit_feedback)
        self.feedback_box.setLayout(feedback_layout)
        main_layout.addWidget(self.feedback_box)

        bottom_layout = QtWidgets.QHBoxLayout()

        self.msg_box = QtWidgets.QGroupBox("💬 Message Provider")
        msg_layout = QtWidgets.QVBoxLayout()
        self.input_msg = QtWidgets.QTextEdit()
        self.btn_send_msg = QtWidgets.QPushButton("📨 Send")
        self.btn_send_msg.clicked.connect(self.send_message)
        msg_layout.addWidget(self.input_msg)
        msg_layout.addWidget(self.btn_send_msg)
        self.msg_box.setLayout(msg_layout)

        self.notification_box = QtWidgets.QGroupBox("🔔 Notifications")
        notif_layout = QtWidgets.QVBoxLayout()
        self.notification_text = QtWidgets.QTextEdit()
        self.notification_text.setReadOnly(True)
        self.btn_refresh_notif = QtWidgets.QPushButton("🔄 Refresh")
        self.btn_refresh_notif.clicked.connect(self.refresh_notifications)
        notif_layout.addWidget(self.notification_text)
        notif_layout.addWidget(self.btn_refresh_notif)
        self.notification_box.setLayout(notif_layout)

        bottom_layout.addWidget(self.msg_box)
        bottom_layout.addWidget(self.notification_box)
        main_layout.addLayout(bottom_layout)

        self.total_amount = 0.0
        self.order_items = []

    def logout(self):
        reply = QMessageBox.question(self.CustomerDashboard, "Logout", "Are you sure you want to logout?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if hasattr(self, "main_app") and self.main_app:
                self.CustomerDashboard.close()
                self.main_app.show_login()
            else:
                self.CustomerDashboard.close()

    def save_profile(self):
        QMessageBox.information(self.CustomerDashboard, "Profile Saved", "Your profile details have been saved.")

    def add_item(self):
        item_text = self.combo_item.currentText()
        qty = self.spin_qty.value()
        try:
            price_per_item = float(item_text.split("₱")[1])
        except:
            price_per_item = 0.0
        item_name = item_text.split(" - ")[0]
        total_price = price_per_item * qty

        self.order_items.append((item_name, qty, total_price))
        self.update_table()
        self.update_summary()

    def delete_item(self):
        selected_rows = set(idx.row() for idx in self.table_items.selectedIndexes())
        if not selected_rows:
            QMessageBox.warning(self.CustomerDashboard, "No Selection", "Please select a row to delete.")
            return
        for row in sorted(selected_rows, reverse=True):
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
            service_price = float(self.combo_service.currentText().split("₱")[1])
        except:
            service_price = 0.0
        try:
            detergent_price = float(self.combo_detergent.currentText().split("₱")[1])
        except:
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

        summary_lines = [f"{item} x {qty} = ₱{price:.2f}" for item, qty, price in self.order_items]
        summary_lines.append(f"Service: {self.combo_service.currentText()}")
        summary_lines.append(f"Detergent: {self.combo_detergent.currentText()}")
        summary_lines.append(f"Discount: {self.combo_discount.currentText()}")
        summary_lines.append(f"Total Amount: ₱{self.total_amount:.2f}")
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
                                f"Payment of ₱{amount:.2f} received via {self.combo_payment.currentText()}.")

    def save_receipt(self):
        with open("receipt.txt", "w") as f:
            f.write(self.summary_text.toPlainText())
        QMessageBox.information(self.CustomerDashboard, "Saved", "Receipt saved as receipt.txt")

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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = CustomerDashboardUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
