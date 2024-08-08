import os
import sys
import tempfile
from plotly.io import to_html
import plotly.graph_objs as go
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox, QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QApplication

class PlotlyViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, fig=None):
        super().__init__()
        self.page().profile().downloadRequested.connect(self.on_downloadRequested)

        self.settings().setAttribute(self.settings().ShowScrollBars, False)
        self.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.WebGLEnabled, True)

        self.temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding='utf-8')
        self.figure = fig  # 保存 figure
        self.set_figure(fig)

        self.setWindowTitle("绘图")

    def set_figure(self, fig=None):
        self.temp_file.seek(0)
        if fig is None:
            fig = go.Figure()
        fig.update_xaxes(showspikes=True)
        fig.update_yaxes(showspikes=True)
        html = to_html(fig, config={"responsive": True, 'scrollZoom': True})
        html += "\n<style>body{margin: 0; overflow: hidden;}" \
                "\n.plot-container,.main-svg,.svg-container{width:100% !important; height:100% !important;}</style>"

        self.temp_file.write(html)
        self.temp_file.truncate()
        self.temp_file.seek(0)
        self.load(QtCore.QUrl.fromLocalFile(self.temp_file.name))

        self.figure = fig  # 更新 figure

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.temp_file.close()
        os.unlink(self.temp_file.name)
        super().closeEvent(event)

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(400, 400)

    def on_downloadRequested(self, download):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setDefaultSuffix(".png")
        path, _ = dialog.getSaveFileName(self, "Save File", os.path.join(os.getcwd(), "newplot.png"), "*.png")
        if path:
            download.setPath(path)
            download.accept()


class PlotlyViewerDialog(QtWidgets.QDialog):
    def __init__(self, plotly_viewer):
        super().__init__()
        self.setWindowTitle("Plotly Viewer")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinMaxButtonsHint)  # 添加标题栏按钮
        self.setLayout(QtWidgets.QVBoxLayout())

        # 复制 PlotlyViewer 实例
        self.plotly_viewer = plotly_viewer

        # 创建一个新的 PlotlyViewer 实例
        self.plotly_viewer_copy = PlotlyViewer()
        # 使用原 PlotlyViewer 的 HTML 内容更新新的 PlotlyViewer
        self.plotly_viewer_copy.set_figure(self.plotly_viewer.figure)

        self.layout().addWidget(self.plotly_viewer_copy)
        self.resize(800, 600)  # 设置对话框初始大小


class SegmentationWidget(QWidget):
    def __init__(self, title: str, items: list = [], ifplotly: bool = True, parent: QWidget = None):
        super().__init__(parent)

        # 创建布局
        layout = QVBoxLayout(self)

        # 创建顶部布局
        topLayout = QHBoxLayout()

        # 添加下拉框, 显示按钮和plotlyViewer全屏按钮
        self.label = QLabel(title, self)
        self.comboBox = QComboBox(self)
        self.comboBox.addItem("Choose...")
        for item in items:
            self.comboBox.addItem(item)
        self.showButton = QPushButton("显示", self)

        # 将控件添加到顶部布局
        topLayout.addWidget(self.label)
        topLayout.addWidget(self.comboBox)
        topLayout.addWidget(self.showButton)
        

        # 将顶部布局和 PlotlyViewer 添加到主布局
        layout.addLayout(topLayout)
        
        if ifplotly:
            self.plotlyWidgetButton = QPushButton("全屏", self)
            self.plotlyWidgetButton.setMaximumWidth(100)
            self.plotlyWidgetButton.setMinimumWidth(100)
            topLayout.addWidget(self.plotlyWidgetButton)
            # 创建 PlotlyViewer 用于图像显示
            self.plotlyViewer = PlotlyViewer()
            layout.addWidget(self.plotlyViewer)
            # 连接按钮点击信号到槽函数
            self.showButton.clicked.connect(self.showButtonClicked)
            self.plotlyWidgetButton.clicked.connect(self.showpoltlyVieweronly)


        # 设置布局
        self.setLayout(layout)

        # 初始化功能字典
        self.functions_dict = {item: None for item in items}

    def showButtonClicked(self):
        selected_item = self.comboBox.currentText()
        if selected_item != "Choose...":
            if self.functions_dict.get(selected_item):
                self.functions_dict[selected_item]()
            else:
                self.display_default_figure(f"No function defined for {selected_item}")
        else:
            self.display_default_figure("请选择一个选项")

    def append_function(self, item, function):
        if item in self.functions_dict:
            self.functions_dict[item] = function
        else:
            print(f"Item {item} not found in the list of options.")

    def setStyles(self, label_style=None, comboBox_style=None, button_style=None, window_style=None):
        if label_style:
            self.label.setStyleSheet(label_style)
        if comboBox_style:
            self.comboBox.setStyleSheet(comboBox_style)
        if button_style:
            self.showButton.setStyleSheet(button_style)
        if window_style:
            self.setStyleSheet(window_style)

    def display_default_figure(self, text):
        fig = go.Figure()
        fig.add_annotation(text=text, xref="paper", yref="paper", showarrow=False, font=dict(size=20))
        self.plotlyViewer.set_figure(fig)

    def showpoltlyVieweronly(self):
        dialog = PlotlyViewerDialog(self.plotlyViewer)
        dialog.exec_()

if __name__ == "__main__":
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Segmentation Widget Example")

            self.segmentation_widget = SegmentationWidget("阈值分割:", ["Item1", "Item2", "Item3"], ifplotly=1)

            self.segmentation_widget.append_function("Item1", self.function_for_item1)
            self.segmentation_widget.append_function("Item2", self.function_for_item2)
            self.segmentation_widget.append_function("Item3", self.function_for_item3)

            label_style = "color: blue; font-size: 18px;"
            comboBox_style = "background-color: lightgray; font-size: 14px;"
            button_style = "background-color: lightgreen; font-size: 14px;"
            window_style = "background-color: #f0f0f0;"

            self.segmentation_widget.setStyles(label_style, comboBox_style, button_style, window_style)

            central_widget = QWidget()
            central_layout = QVBoxLayout(central_widget)
            central_layout.addWidget(self.segmentation_widget)
            self.setCentralWidget(central_widget)

        def function_for_item1(self):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))
            fig.update_layout(xaxis=dict(domain=[0.1, 0.9]), yaxis=dict(title="Item1 y-axis title"))
            self.segmentation_widget.plotlyViewer.set_figure(fig)

        def function_for_item2(self):
            fig = go.Figure()
            fig.add_trace(go.Bar(x=["A", "B", "C"], y=[7, 8, 9]))
            fig.update_layout(xaxis=dict(title="Item2 x-axis title"), yaxis=dict(title="Item2 y-axis title"))
            self.segmentation_widget.plotlyViewer.set_figure(fig)

        def function_for_item3(self):
            fig = go.Figure()
            fig.add_trace(go.Pie(labels=["Apple", "Banana", "Cherry"], values=[10, 20, 30]))
            fig.update_layout(title="Item3 Pie Chart")
            self.segmentation_widget.plotlyViewer.set_figure(fig)
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
