from random import randint
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

def addTab_arg(functionality=None):
    """
    装饰器工厂函数，用于向 QListWidget 添加带图标的项目。

    :param functionality: 要显示的功能名称
    :return: 装饰器函数
    """
    def addTab(func):
        """
        装饰器函数，实际执行添加项目的操作。

        :param func: 被装饰的方法
        :return: 包装后的方法
        """
        def wrapper(self, *args, **kwargs):
            """
            包装函数，添加带图标的项目到 QListWidget，并调用被装饰的方法。

            :param self: 方法所属的实例
            :param args: 方法的参数
            :param kwargs: 方法的关键字参数
            """
            # 创建带随机图标和功能名称的 QListWidgetItem
            item = QListWidgetItem(
                QIcon('Data/0%d.ico' % randint(1, 8)), functionality, self.listWidget)
            # 设置项目大小
            item.setSizeHint(QSize(16777215, 80))
            # 设置项目文本居中对齐
            item.setTextAlignment(Qt.AlignCenter)
            # 调用被装饰的方法
            func(self, *args, **kwargs)
        return wrapper
    return addTab
