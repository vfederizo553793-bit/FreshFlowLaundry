import sys
from PyQt6 import QtWidgets
from user_login import LoginUI
from user_signup import SignupUI
from customer_DB import CustomerDashboardUI
from admin_DB import AdminDashboardUI


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

    def show_login(self):
        self._hide_all_windows()
        self.login_window.show()

    def show_signup(self):
        self._hide_all_windows()
        self.signup_window.show()

    def show_customer_dashboard(self, user_id):
        self._hide_all_windows()
        self.customer_window = QtWidgets.QWidget()
        self.customer_ui = CustomerDashboardUI()
        self.customer_ui.setupUi(self.customer_window, self, user_id)
        self.customer_window.show()

    def show_admin_dashboard(self, user_id):
        self._hide_all_windows()
        self.admin_window = QtWidgets.QMainWindow()
        self.admin_ui = AdminDashboardUI()
        self.admin_ui.setupUi(self.admin_window, self, user_id)
        self.admin_window.show()

    def _hide_all_windows(self):
        for window in [
            self.login_window,
            self.signup_window,
            self.customer_window,
            self.admin_window,
        ]:
            if window:
                window.hide()

    def run(self):
        self.show_login()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    main_app = FreshFlow()
    main_app.run()
