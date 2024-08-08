from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

# 定义一个登录小部件，继承自QLabel
class LoginWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建表单布局
        formLayout = QFormLayout()
        formLayout.setContentsMargins(10, 0, 10, 0)

        # 创建结果标签，并设置其对齐方式和最小高度
        self.resultLabel = QLabel("请先登录", self)
        self.resultLabel.setAlignment(Qt.AlignCenter)
        self.resultLabel.setMinimumHeight(20)

        # 创建用户名输入框和密码输入框，并设置提示文本
        self.usernameInput = QLineEdit(self)
        self.usernameInput.setPlaceholderText("请输入账号...")

        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.passwordInput.setPlaceholderText("请输入密码...")

        # 设置标签的对齐方式
        formLayout.setLabelAlignment(Qt.AlignRight)

        # 创建账号和密码标签
        self.accountLabel = QLabel("账号:", self)
        self.passwordLabel = QLabel("密码:", self)

        # 创建注册和登录按钮
        self.registerButton = QPushButton("注册", self)
        self.loginButton = QPushButton("登录", self)

        # 创建按钮布局，并添加按钮
        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.registerButton)
        buttonsLayout.addWidget(self.loginButton)
        buttonsLayout.setAlignment(Qt.AlignCenter)

        # 将控件添加到表单布局中
        formLayout.addRow(self.resultLabel)
        formLayout.addRow(self.accountLabel, self.usernameInput)
        formLayout.addRow(self.passwordLabel, self.passwordInput)
        formLayout.addRow(buttonsLayout)

        # 设置主布局
        self.setLayout(formLayout)

# 主程序入口
if __name__ == "__main__":
    # 定义一个登录窗口，继承自QMainWindow
    class LoginWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("登录")
            self.setGeometry(100, 100, 400, 300)
            self.setCentralWidget(LoginWidget(self))
            self.show()

    # 创建应用程序实例
    app = QApplication(sys.argv)
    # 创建并显示主窗口
    window = LoginWindow()
    # 运行应用程序主循环
    sys.exit(app.exec_())
