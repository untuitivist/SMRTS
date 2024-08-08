
# 超导材料快速无损检测系统(SMRTS)

## 简介
SMRTS 是一个基于 PyQt5 的桌面应用程序，具有美观的用户界面和丰富的功能。此项目包含多个主要的 Python 文件，用于不同的功能模块。

## 文件结构
```
/SMRTS
│-- app.py
│-- AddTab.py
│-- DataLoader.py
│-- LoginWidget.py
│-- SegmentationWidget.py
│-- SMRTS.py
│-- README.md
│-- requirements.txt
```

## 安装

1. 下载代码到本地：

2. 进入项目目录：
    ```sh
    cd SMRTS
    ```

3. 安装所需的依赖包：
    ```sh
    pip install -r requirements.txt
    ```

## 运行

在终端中运行以下命令启动应用程序：
```sh
python app.py
```

## 代码说明

### app.py
`app.py` 是应用程序的入口文件，包含应用程序的总体样式表定义和应用程序的启动代码。

### AddTab.py
`AddTab.py` 文件定义了用于添加新选项卡的功能。

### DataLoader.py
`DataLoader.py` 文件包含数据加载器类和函数，用于加载和处理数据。

### LoginWidget.py
`LoginWidget.py` 文件定义了登录小部件类，包括用户登录界面的布局和功能。

### SegmentationWidget.py
`SegmentationWidget.py` 文件定义了图像显示小部件类，用于图像显示和数据分析任务。

### SMRTS.py
`SMRTS.py` 文件包含 `SMRTS` 类，定义了应用程序的主要功能和用户界面。

## 样式表
应用程序使用了自定义的美化样式表，以提供更好的用户体验。以下是主窗口的样式定义：
```css
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
```
各个部件的样式表美化在`SMRTS.py`中
