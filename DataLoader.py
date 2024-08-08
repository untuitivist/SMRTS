from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit
import sys
import os

class DataLoaderWidget(QLabel):
    def __init__(self, title: str, choose: str, parent: QLabel = None) -> None:
        """
        初始化 DataLoaderWidget 部件

        :param title: 部件的标题
        :param choose: 选择类型，可以是 'single'（单个文件）、'multiple'（多个文件）或 'directory'（目录）
        :param parent: 父部件
        """
        super().__init__(parent)
        self.choose = choose

        # 创建布局
        layout = QVBoxLayout(self)
        topLayout = QHBoxLayout()
        bottomLayout = QHBoxLayout()

        # 添加标签、文本框和选择按钮
        self.label = QLabel(title, self)
        self.pathLineEdit = QLineEdit(self)  # 文本框显示路径
        self.pathLineEdit.setReadOnly(True)  # 设置文本框为只读
        self.pathLineEdit.setText("Choose...")  # 设置文本框默认文本
        self.chooseButton = QPushButton("选择", self)
        self.chooseButton.setMaximumWidth(100)  # 设置按钮最大宽度

        # 将标签添加到顶部布局，文本框和按钮添加到底部布局
        topLayout.addWidget(self.label)
        bottomLayout.addWidget(self.pathLineEdit)
        bottomLayout.addWidget(self.chooseButton)

        # 将顶部布局和底部布局添加到主布局
        layout.addLayout(topLayout)
        layout.addLayout(bottomLayout)
        self.setLayout(layout)

        # 连接按钮点击信号到槽函数
        if choose == 'single':
            self.chooseButton.clicked.connect(self.select_single_file)
        elif choose == 'multiple':
            self.chooseButton.clicked.connect(self.select_multiple_files)
        elif choose == 'directory':
            self.chooseButton.clicked.connect(self.select_single_directory)
        else:
            raise ValueError("choose 参数必须是 'single'、'multiple' 或 'directory'")

    def select_single_file(self) -> None:
        """选择单个文件, csv, excel"""
        self.file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "CSV Files (*.csv);;Excel Files (*.xlsx *.xls)")
        if self.file_path:
            self.pathLineEdit.setText(self.file_path)

    def select_multiple_files(self) -> None:
        """选择多个文件"""
        self.file_paths, _ = QFileDialog.getOpenFileNames(self, "选择文件", "", "All Files (*)")
        if self.file_paths:
            self.pathLineEdit.setText('\n'.join(self.file_paths))  # 显示多个文件路径，每个路径换行

    def select_single_directory(self) -> None:
        """选择单个目录"""
        self.dir_path = QFileDialog.getExistingDirectory(self, "选择目录", "", QFileDialog.ShowDirsOnly)
        if self.dir_path:
            self.pathLineEdit.setText(self.dir_path)

    def get_path(self) -> list:
        """
        获取选择的路径

        :return: 返回选择的路径列表
        """
        if self.pathLineEdit.text() == "Choose...":
            return []
        elif self.choose == 'single':
            return [self.pathLineEdit.text()]
        elif self.choose == 'multiple':
            return self.pathLineEdit.text().split('\n')
        elif self.choose == 'directory':
            return [os.path.join(self.pathLineEdit.text(), file_name) for file_name in os.listdir(self.pathLineEdit.text())]
        else:
            raise ValueError("choose 参数必须是 'single'、'multiple' 或 'directory'")

if __name__ == '__main__':
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("数据加载器")
            self.setGeometry(100, 100, 600, 400)

            # 创建主布局
            mainLayout = QVBoxLayout()

            # 创建多个 DataLoaderWidget 实例
            self.fileLoaderWidget = DataLoaderWidget("选择单个文件:", 'single', self)
            self.filesLoaderWidget = DataLoaderWidget("选择多个文件:", 'multiple', self)
            self.directoryLoaderWidget = DataLoaderWidget("选择目录:", 'directory', self)

            # 将 DataLoaderWidget 实例添加到主布局
            mainLayout.addWidget(self.fileLoaderWidget)
            mainLayout.addWidget(self.filesLoaderWidget)
            mainLayout.addWidget(self.directoryLoaderWidget)

            # 创建主窗口的中央小部件
            centralWidget = QWidget(self)
            centralWidget.setLayout(mainLayout)
            self.setCentralWidget(centralWidget)

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
