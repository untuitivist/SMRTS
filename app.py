import sys
from PyQt5.QtWidgets import QApplication
from SMRTS import SMRTS


# 总体美化样式表
Stylesheet = """
QListWidget, QListView, QTreeWidget, QTreeView {
    outline: 0px;
}
QListWidget {
    min-width: 240px;
    max-width: 240px;
    font-size: 25px;
    color: white;
    background: #4682B4;
}
QListWidget::item:selected {
    background: #DCD0F3;
    border-left: 8px solid rgb(153, 204, 255);
    border-radius: 5px;
}
HistoryPanel::item:hover {
    background: rgb(52, 52, 52);
}
QStackedWidget {
    background: #B0E0E6;
}
QLabel {
    color: white;
}
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Stylesheet)
    w = SMRTS()
    w.show()
    sys.exit(app.exec_())
