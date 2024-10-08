#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QListWidget, QStackedWidget, QHBoxLayout,QLabel, QVBoxLayout, QLineEdit, QMessageBox, QWidget

# Created on 2024年8月10日
# author: Untuitivist
# site: https://pyqt5.com , https://github.com/untuitivist
# email: 2724386553@qq.com
# file: SMRTS
# description:
__author__ = """By: Untuitivist
QQ: 2724386553
Email: 2724386553@qq.com"""
__copyright__ = 'Copyright (c) 2024 Untuitivist'
__version__ = 1.0

# 导入自定义模块
from AddTab import addTab_arg
from SegmentationWidget import SegmentationWidget
from LoginWidget import LoginWidget
from DataLoader import DataLoaderWidget

# 用户名和密码列表, 后续可以接入数据库
password_list = [["admin", "password"], ["", ""]]


# 超导材料快速无损检测系统功能模块
class SMRTS(QWidget):

    def __init__(self, *args, **kwargs):
        super(SMRTS, self).__init__(*args, **kwargs)
        self.resize(1960, 1080)
        layout = QHBoxLayout(self, spacing=0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle("超导材料快速无损检测系统")
        self.listWidget = QListWidget(self)
        layout.addWidget(self.listWidget)
        self.stackedWidget = QStackedWidget(self)
        layout.addWidget(self.stackedWidget)

        # 初始化登录状态
        self.login = False

        # 添加选项卡
        self.initUi()
        self.userManagement()
        self.highSpectralImageProcessing()
        self.sensorSignalProcessing()
        self.modelBuilding()
        self.resultOutput()

    def initUi(self):
        self.listWidget.currentRowChanged.connect(self.showPage)
        self.listWidget.setFrameShape(QListWidget.NoFrame)
        self.listWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.updateSidebar()

    @addTab_arg("用户管理")
    def userManagement(self):

        # 创建控件
        loginWidget = LoginWidget(self)

        # 获取控件
        self.loginWidget = loginWidget

        # 功能接入
        self.loginWidget.loginButton.clicked.connect(self.loginUser)

        # 设置样式
        loginWidget.setFixedSize(600, 600)
        loginWidget.setStyleSheet('background: white; margin: auto; border-radius: 10px;')
        self.loginWidget.resultLabel.setStyleSheet("font-family: 'Microsoft YaHei'; font-size: 40px; color: black; background: transparent;")
        self.loginWidget.usernameInput.setStyleSheet("font-size: 30px; border: 2px solid gray; border-radius: 5px; padding: 5px;")
        self.loginWidget.passwordInput.setStyleSheet("font-size: 30px; border: 2px solid gray; border-radius: 5px; padding: 5px;")
        labelStyleSheet = "font-family: 'Microsoft YaHei'; font-size: 35px; color: black;"
        self.loginWidget.accountLabel.setStyleSheet(labelStyleSheet)
        self.loginWidget.passwordLabel.setStyleSheet(labelStyleSheet)
        self.loginWidget.registerButton.setStyleSheet("font-size: 20px; border: 2px solid gray; border-radius: 5px; padding: 12px;")
        self.loginWidget.loginButton.setStyleSheet("font-size: 20px; border: 2px solid gray; border-radius: 5px; padding: 12px;")


        # 布局
        containerWidget = QWidget(self)
        containerLayout = QVBoxLayout(containerWidget)
        containerLayout.addStretch(1)
        containerLayout.addWidget(loginWidget, alignment=Qt.AlignCenter)
        containerLayout.addStretch(1)
        self.stackedWidget.addWidget(containerWidget)

    def loginUser(self):
        username = self.loginWidget.usernameInput.text()
        password = self.loginWidget.passwordInput.text()

        # 示例验证逻辑
        if [username, password] in password_list:
            self.login = True
            self.loginWidget.resultLabel.setText("登录成功")
            self.loginWidget.resultLabel.setText("欢迎，" + username)
            # QMessageBox.information(self, "登录成功", "登录成功！")
            self.loginWidget.usernameInput.clear()
            self.loginWidget.passwordInput.clear()
        else:
            self.login = False
            self.loginWidget.resultLabel.setText("登录失败")
            # QMessageBox.warning(self, "登录失败", "用户名或密码错误。")

        self.updateSidebar()  # 更新侧边栏功能

    def updateSidebar(self):
        # 根据登录状态更新侧边栏功能
        if self.login:
            self.listWidget.setEnabled(True)
        else:
            self.listWidget.setEnabled(False)
            self.stackedWidget.setCurrentWidget(self.stackedWidget.widget(0))  # 显示登录界面

    def showPage(self, index):
        # 根据登录状态决定是否允许访问
        if self.login or index == 0:
            self.stackedWidget.setCurrentIndex(index)
        else:
            QMessageBox.warning(self, "权限警告", "请先登录才能访问此功能。")

    @addTab_arg("高光谱图像处理")
    def highSpectralImageProcessing(self):

        # 创建控件: 数据加载器, 高光谱矫正, 阈值分割, 光谱曲线显示
        HSIP_dataloader = DataLoaderWidget("数据加载:", "directory")
        HSIP_correction = SegmentationWidget("高光谱矫正:", ["黑白校正", "畸变校正"])
        HSIP_correction_sample = SegmentationWidget("样本选择:", ifplotly=False)
        HSIP_threshold = SegmentationWidget("阈值分割:", ["Otsu", "二值分割"])
        HSIP_threshold_sample = SegmentationWidget("样本选择:", ifplotly=False)
        HSIP_curve = SegmentationWidget("数据可视化:", ["图像显示", "光谱曲线显示"])
        HSIP_curve_sample = SegmentationWidget("样本选择:", ifplotly=False)

        # 获取控件
        self.HSIP_dataloader = HSIP_dataloader
        self.HSIP_correction = HSIP_correction
        self.HSIP_correction_sample = HSIP_correction_sample
        self.HSIP_threshold = HSIP_threshold
        self.HSIP_threshold_sample = HSIP_threshold_sample
        self.HSIP_curve = HSIP_curve
        self.HSIP_curve_sample = HSIP_curve_sample

        # 功能接入
        self.HSIP_dataloader.pathLineEdit.textChanged.connect(self.HSIP_dataload)

        self.HSIP_correction_sample.showButton.clicked.connect(self.HSIP_correction_dataim)
        self.HSIP_threshold_sample.showButton.clicked.connect(self.HSIP_threshold_dataim)
        self.HSIP_curve_sample.showButton.clicked.connect(self.HSIP_curve_dataim)

        self.HSIP_correction.append_function("黑白校正", self.HSIP_blackWhiteCorrection)
        self.HSIP_correction.append_function("畸变校正", self.HSIP_distortionCorrection)

        self.HSIP_threshold.append_function("Otsu", self.HSIP_otsuThresholding)
        self.HSIP_threshold.append_function("二值分割", self.HSIP_binaryThresholding)

        self.HSIP_curve.append_function("图像显示", self.HSIP_imageDisplay)
        self.HSIP_curve.append_function("光谱曲线显示", self.HSIP_spectrumCurveDisplay)

        # 设置样式

        SW_StyleSheet_label = 'font-family: "Microsoft YaHei"; font-size: 30px; color: black;'
        self.HSIP_dataloader.label.setStyleSheet(SW_StyleSheet_label)
        self.HSIP_correction.label.setStyleSheet(SW_StyleSheet_label)
        self.HSIP_correction_sample.label.setStyleSheet(SW_StyleSheet_label)
        self.HSIP_threshold.label.setStyleSheet(SW_StyleSheet_label)
        self.HSIP_threshold_sample.label.setStyleSheet(SW_StyleSheet_label)
        self.HSIP_curve.label.setStyleSheet(SW_StyleSheet_label)
        self.HSIP_curve_sample.label.setStyleSheet(SW_StyleSheet_label)

        SW_StyleSheet_combobox = 'font-family: "Microsoft YaHei"; font-size: 25px; color: black;'
        self.HSIP_dataloader.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        self.HSIP_correction.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.HSIP_correction_sample.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.HSIP_threshold.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.HSIP_threshold_sample.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.HSIP_curve.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.HSIP_curve_sample.comboBox.setStyleSheet(SW_StyleSheet_combobox)

        SW_StyleSheet_showbutton = 'font-family: "Microsoft YaHei"; font-size: 25px; color: black; padding: 5px;'
        self.HSIP_dataloader.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_dataloader.chooseButton.setMinimumWidth(100)
        self.HSIP_correction.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_correction.plotlyWidgetButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_correction_sample.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_correction_sample.showButton.setText("确认")
        self.HSIP_threshold.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_threshold.plotlyWidgetButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_threshold_sample.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_threshold_sample.showButton.setText("确认")
        self.HSIP_curve.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_curve.plotlyWidgetButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_curve_sample.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.HSIP_curve_sample.showButton.setText("确认")

        self.HSIP_correction_sample.setMaximumHeight(80)
        self.HSIP_threshold_sample.setMaximumHeight(80)
        self.HSIP_curve_sample.setMaximumHeight(80)

        # 设置布局
        fromLayout = QHBoxLayout()
        dataloaderLayout = QVBoxLayout()
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # 添加边距和间距
        leftLayout.setContentsMargins(10, 10, 10, 10)
        rightLayout.setContentsMargins(10, 10, 10, 10)
        leftLayout.setSpacing(10)
        rightLayout.setSpacing(10)

        # 添加控件到布局, 设置伸缩因子
        dataloaderLayout.addWidget(HSIP_dataloader, 2)
        leftLayout.addLayout(dataloaderLayout, 2)
        leftLayout.addWidget(HSIP_correction_sample, 2)
        leftLayout.addWidget(HSIP_correction, 13)

        rightLayout.addWidget(HSIP_threshold_sample)
        rightLayout.addWidget(HSIP_threshold)
        rightLayout.addWidget(HSIP_curve_sample)
        rightLayout.addWidget(HSIP_curve)
        
        fromLayout.addLayout(leftLayout, 1)  # 1 表示左侧布局占据 1 份空间
        fromLayout.addLayout(rightLayout, 1)  # 1 表示右侧布局占据 1 份空间

        # 创建容器控件并设置布局
        containerWidget = QWidget()
        containerWidget.setLayout(fromLayout)
        self.stackedWidget.addWidget(containerWidget)
    
    # 功能函数
    def HSIP_blackWhiteCorrection(self):
        # TODO: 实现黑白校正功能
        self.HSIP_correction.plotlyViewer.show_local(self.HSIP_correction_file)

    def HSIP_distortionCorrection(self):
        # TODO: 实现畸变校正功能
        self.HSIP_correction.plotlyViewer.show_local(self.HSIP_correction_file)

    def HSIP_otsuThresholding(self):
        # TODO: 实现Otsu分割功能
        self.HSIP_threshold.plotlyViewer.show_local(self.HSIP_threshold_file)

    def HSIP_binaryThresholding(self):
        # TODO: 实现二值分割功能
        self.HSIP_threshold.plotlyViewer.show_local(self.HSIP_threshold_file)

    def HSIP_imageDisplay(self):
        # TODO: 实现图像显示功能
        self.HSIP_threshold.plotlyViewer.show_local(self.HSIP_threshold_file)

    def HSIP_spectrumCurveDisplay(self):
        # TODO: 实现数据可视化功能
        self.HSIP_curve.plotlyViewer.show_local(self.HSIP_curve_file)

    def HSIP_dataload(self):
        # TODO: 将数据加载到样本选择中
        # print("高光谱图像处理: 数据列表加载")
        self.HSIP_dir_path = self.HSIP_dataloader.dir_path
        for file_name in os.listdir(self.HSIP_dir_path):
            self.HSIP_correction_sample.append_function(file_name, self.HSIP_correction_dataim)
            self.HSIP_threshold_sample.append_function(file_name, self.HSIP_threshold_dataim)
            self.HSIP_curve_sample.append_function(file_name, self.HSIP_curve_dataim)
    def HSIP_correction_dataim(self):
        # TODO: 保存选项的样本数据文件地址
        self.HSIP_correction_file = os.path.join(self.HSIP_dir_path, self.HSIP_correction_sample.comboBox.currentText())
    def HSIP_threshold_dataim(self):
        # TODO: 保存选项的样本数据文件地址
        self.HSIP_threshold_file = os.path.join(self.HSIP_dir_path, self.HSIP_threshold_sample.comboBox.currentText())
    def HSIP_curve_dataim(self):
        # TODO: 保存选项的样本数据文件地址
        self.HSIP_curve_file = os.path.join(self.HSIP_dir_path, self.HSIP_curve_sample.comboBox.currentText())

    @addTab_arg("传感器信号处理")
    def sensorSignalProcessing(self):
        # 创建控件: 数据加载器, 预处理方法选择, 信号可视化
        SSP_dataloader = DataLoaderWidget("数据加载器:", "directory")
        SSP_correction = SegmentationWidget("预处理方法选择:", ["S-G smoothing"], ifplotly=False)
        SSP_threshold = SegmentationWidget("信号可视化:")

        # 获取控件
        self.SSP_dataloader = SSP_dataloader
        self.SSP_correction = SSP_correction
        self.SSP_threshold = SSP_threshold

        # 功能设置
        self.SSP_correction.append_function("S-G smoothing", self.SSP_SGsmoothing)
        self.SSP_dataloader.pathLineEdit.textChanged.connect(self.SSP_dataload)
        self.SSP_threshold.showButton.clicked.connect(self.SSP_imageDisplay)

        # 设置样式
        SW_StyleSheet_label = 'font-family: "Microsoft YaHei"; font-size: 30px; color: black;'
        self.SSP_dataloader.label.setStyleSheet(SW_StyleSheet_label)
        self.SSP_correction.label.setStyleSheet(SW_StyleSheet_label)
        self.SSP_threshold.label.setStyleSheet(SW_StyleSheet_label)

        SW_StyleSheet_combobox = 'font-family: "Microsoft YaHei"; font-size: 25px; color: black;'
        self.SSP_dataloader.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        self.SSP_correction.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.SSP_threshold.comboBox.setStyleSheet(SW_StyleSheet_combobox)

        SW_StyleSheet_showbutton = 'font-family: "Microsoft YaHei"; font-size: 25px; color: black; padding: 5px;'
        self.SSP_dataloader.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.SSP_dataloader.chooseButton.setMinimumWidth(400)
        self.SSP_dataloader.chooseButton.setMaximumWidth(400)
        self.SSP_correction.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.SSP_correction.showButton.setMinimumWidth(400)
        self.SSP_correction.showButton.setMaximumWidth(400)
        self.SSP_correction.showButton.setText("确认")
        self.SSP_threshold.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.SSP_threshold.showButton.setMinimumWidth(195)
        self.SSP_threshold.showButton.setMaximumWidth(195)
        self.SSP_threshold.plotlyWidgetButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.SSP_threshold.plotlyWidgetButton.setMinimumWidth(195)
        self.SSP_threshold.plotlyWidgetButton.setMaximumWidth(195)

        # 设置布局
        fromLayout = QVBoxLayout()

        # 添加边距和间距
        fromLayout.setContentsMargins(20, 20, 20, 20)
        fromLayout.setSpacing(20)
        
        # 添加控件到布局, 设置伸缩因子
        fromLayout.addWidget(SSP_dataloader, 1)
        fromLayout.addWidget(SSP_correction, 1)
        fromLayout.addWidget(SSP_threshold, 6)
        self.setLayout(fromLayout)


        # 创建容器控件并设置布局
        containerWidget = QWidget()
        containerWidget.setLayout(fromLayout)
        self.stackedWidget.addWidget(containerWidget)

    def SSP_SGsmoothing(self):
        # TODO: 实现SGsmoothing功能
        pass
    def SSP_dataload(self):
        # TODO: 实现dataload功能
        print("传感器信号处理: 数据列表加载")
        self.SSP_dir_path = self.SSP_dataloader.dir_path
        for file_name in os.listdir(self.SSP_dir_path):
            self.SSP_threshold.append_function(file_name, self.SSP_threshold_dataim)
    def SSP_threshold_dataim(self):
        # TODO: 实现threshold_dataim功能
        self.SSP_threshold_file = os.path.join(self.SSP_dir_path, self.SSP_threshold.comboBox.currentText())
    def SSP_imageDisplay(self):
        # TODO: 实现imageDisplay功能
        self.SSP_threshold.plotlyViewer.show_local(self.SSP_threshold_file)


    @addTab_arg("模型构建")
    def modelBuilding(self):
        # 创建控件
        # 氧化程度定量模型: 标题, 高光谱数据加载, 氧化指标数据加载, 特征选择, 模型选择训练
        QMDO_title = QLabel("氧化程度定量模型", self)
        QMDO_dataloader_H = DataLoaderWidget("高光谱数据加载:", "directory")
        QMDO_dataloader_O = DataLoaderWidget("氧化指标数据加载:", "single")
        QMDO_feature_selection = SegmentationWidget("特征选择:", ["2D-COS"])
        QMDO_model_selection = SegmentationWidget("模型选择:", ["3D-Mobilnet"], ifplotly=False)
        
        # 导电指数定量模型: 标题, 传感器信号数据加载, 导电指标数据加载, 模型选择训练
        QMCI_title = QLabel("导电指数定量模型", self)
        QMCI_dataloader_S = DataLoaderWidget("传感器信号数据加载:", "directory")
        QMCI_dataloader_C = DataLoaderWidget("导电指标数据加载:", "single")
        QMCI_model_selection = SegmentationWidget("模型选择:", ["MTCN-SA"], ifplotly=False)

        # 等级分类模型: 标题, 标签数据加载, 模型选择训练
        QMCL_title = QLabel("等级分类模型", self)
        CMH_dataloader_L = DataLoaderWidget("标签数据加载:", "single")
        CMH_model_selection = SegmentationWidget("模型选择:", ["HFA-Net"], ifplotly=False)

        # 功能设置
        QMDO_feature_selection.append_function("2D-COS", self.QMDO_2D_COS)
        QMDO_model_selection.append_function("3D-Mobilnet", self.QMDO_3D_Mobilenet)
        QMCI_model_selection.append_function("MTCN-SA", self.QMCI_MTCN_SA)
        CMH_model_selection.append_function("HFA-Net", self.CMH_HFA_Net)

        # 获取控件
        self.QMDO_title = QMDO_title
        self.QMDO_dataloader_H = QMDO_dataloader_H
        self.QMDO_dataloader_O = QMDO_dataloader_O
        self.QMDO_feature_selection = QMDO_feature_selection
        self.QMDO_model_selection = QMDO_model_selection

        self.QMCI_title = QMCI_title
        self.QMCI_dataloader_S = QMCI_dataloader_S
        self.QMCI_dataloader_C = QMCI_dataloader_C
        self.QMCI_model_selection = QMCI_model_selection

        self.QMCL_title = QMCL_title
        self.CMH_dataloader_L = CMH_dataloader_L
        self.CMH_model_selection = CMH_model_selection


        # 功能接入

        # 设置样式

        StyleSheet_title = 'font-family: "Microsoft YaHei"; font-size: 40px; color: black; background-color: #87CEEB; border-radius: 10px; padding: 10px;'
        self.QMDO_title.setStyleSheet(StyleSheet_title)
        self.QMDO_title.setMaximumHeight(80)
        self.QMDO_title.setMinimumHeight(80)
        self.QMCI_title.setStyleSheet(StyleSheet_title)
        self.QMCI_title.setMaximumHeight(80)
        self.QMCI_title.setMinimumHeight(80)
        self.QMCL_title.setStyleSheet(StyleSheet_title)
        self.QMCL_title.setMaximumHeight(80)
        self.QMCL_title.setMinimumHeight(80)


        SW_StyleSheet_label = 'font-family: "Microsoft YaHei"; font-size: 30px; color: black;'
        self.QMDO_dataloader_H.label.setStyleSheet(SW_StyleSheet_label)
        self.QMDO_dataloader_O.label.setStyleSheet(SW_StyleSheet_label)
        self.QMDO_feature_selection.label.setStyleSheet(SW_StyleSheet_label)
        self.QMDO_model_selection.label.setStyleSheet(SW_StyleSheet_label)
        self.QMCI_dataloader_S.label.setStyleSheet(SW_StyleSheet_label)
        self.QMCI_dataloader_C.label.setStyleSheet(SW_StyleSheet_label)
        self.QMCI_model_selection.label.setStyleSheet(SW_StyleSheet_label)
        self.CMH_dataloader_L.label.setStyleSheet(SW_StyleSheet_label)
        self.CMH_model_selection.label.setStyleSheet(SW_StyleSheet_label)

        SW_StyleSheet_combobox = 'font-family: "Microsoft YaHei"; font-size: 25px; color: black;'
        self.QMDO_dataloader_H.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        self.QMDO_dataloader_O.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        self.QMDO_feature_selection.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.QMDO_model_selection.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.QMCI_dataloader_S.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        self.QMCI_dataloader_C.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        self.QMCI_model_selection.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        self.CMH_dataloader_L.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        self.CMH_model_selection.comboBox.setStyleSheet(SW_StyleSheet_combobox)

        SW_StyleSheet_showbutton = 'font-family: "Microsoft YaHei"; font-size: 25px; color: black; padding: 5px;'
        self.QMDO_dataloader_H.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.QMDO_dataloader_O.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.QMDO_feature_selection.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.QMDO_feature_selection.plotlyWidgetButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.QMDO_model_selection.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.QMCI_dataloader_S.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.QMCI_dataloader_C.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.QMCI_model_selection.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.CMH_dataloader_L.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        self.CMH_model_selection.showButton.setStyleSheet(SW_StyleSheet_showbutton)

        self.QMDO_model_selection.showButton.setText("训练")
        self.QMCI_model_selection.showButton.setText("训练")
        self.CMH_model_selection.showButton.setText("训练")

        # 设置布局
        fromLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        rightLayout = QVBoxLayout()

        # 添加边距和间距
        leftLayout.setContentsMargins(10, 10, 10, 10)
        rightLayout.setContentsMargins(10, 10, 10, 10)
        leftLayout.setSpacing(10)
        rightLayout.setSpacing(10)

        # 添加控件到布局
        leftLayout.addWidget(QMDO_title, 1)
        leftLayout.addWidget(QMDO_dataloader_H, 2)
        leftLayout.addWidget(QMDO_dataloader_O, 2)
        leftLayout.addWidget(QMDO_feature_selection, 8)
        leftLayout.addWidget(QMDO_model_selection, 1)

        rightLayout.addWidget(QMCI_title, 2)
        rightLayout.addWidget(QMCI_dataloader_S, 4)
        rightLayout.addWidget(QMCI_dataloader_C, 4)
        rightLayout.addWidget(QMCI_model_selection, 2)
        

        rightLayout.addWidget(QMCL_title, 2)
        rightLayout.addWidget(CMH_dataloader_L, 4)
        rightLayout.addWidget(CMH_model_selection, 2)
        rightLayout.addWidget(QLabel(), 7)

        # 设置伸缩因子
        fromLayout.addLayout(leftLayout, 1)  # 1 表示左侧布局占据 1 份空间
        fromLayout.addLayout(rightLayout, 1)  # 1 表示右侧布局占据 1 份空间

        # 创建容器控件并设置布局
        containerWidget = QWidget()
        containerWidget.setLayout(fromLayout)
        self.stackedWidget.addWidget(containerWidget)

    def QMDO_2D_COS(self):
        # TODO: 添加2D-COS功能
        pass
    def QMDO_3D_Mobilenet(self):
        # TODO: 添加3D-Mobilenet功能
        pass
    def QMCI_MTCN_SA(self):
        # TODO: 添加MTCN-SA功能
        pass
    def CMH_HFA_Net(self):
        # TODO: 添加HFA-Net功能
        pass

    @addTab_arg("检测结果输出")
    def resultOutput(self):
        # 创建控件: 数据加载器1, 数据加载器2, 数据可视化, 模型选择, 预测结果
        RQ_dataloader_1 = DataLoaderWidget("待检测样本数据1加载:", "single")
        RQ_dataloader_2 = DataLoaderWidget("待检测样本数据2加载:", "single")
        RQ_dataVisualization = SegmentationWidget("数据可视化:", ["光谱曲线", "传感器信号"])
        RQ_model_selection = SegmentationWidget("模型选择:", ["3D-Mobilnet", "MTCN-SA", "HFA-Net"], ifplotly=False)
        # 预测结果: 氧化程度, 导电指数, 分级
        RQ_predict = QLabel("预测结果:  ")
        RQ_predict_O_title = QLabel("氧化程度:")
        RQ_predict_O = QLineEdit()
        RQ_predict_O .setReadOnly(True)
        RQ_predict_C_title = QLabel("导电指数:")
        RQ_predict_C = QLineEdit()
        RQ_predict_C .setReadOnly(True)
        RQ_predict_L_title = QLabel("分级:")
        RQ_predict_L = QLineEdit()
        RQ_predict_L .setReadOnly(True)

        # 功能设置
        RQ_dataVisualization.append_function("光谱曲线", self.RQ_show_spectra)
        RQ_dataVisualization.append_function("传感器信号", self.RQ_show_signal)

        RQ_model_selection.append_function("3D-Mobilnet", self.RQ_show_3D_Mobilnet)
        RQ_model_selection.append_function("MTCN-SA", self.RQ_show_MTCN_SA)
        RQ_model_selection.append_function("HFA-Net", self.RQ_show_HFA_Net)


        # 获取控件
        self.RQ_dataloader_1 = RQ_dataloader_1
        self.RQ_dataloader_2 = RQ_dataloader_2
        self.RQ_dataVisualization = RQ_dataVisualization
        self.RQ_model_selection = RQ_model_selection
        self.RQ_predict = RQ_predict
        self.RQ_predict_O = RQ_predict_O
        self.RQ_predict_C = RQ_predict_C
        self.RQ_predict_L = RQ_predict_L


        # 功能接入

        # 设置样式
        SW_StyleSheet_label = 'font-family: "Microsoft YaHei"; font-size: 30px; color: black;'
        RQ_dataloader_1.label.setStyleSheet(SW_StyleSheet_label)
        RQ_dataloader_2.label.setStyleSheet(SW_StyleSheet_label)
        RQ_dataVisualization.label.setStyleSheet(SW_StyleSheet_label)
        RQ_model_selection.label.setStyleSheet(SW_StyleSheet_label)
        RQ_predict.setStyleSheet(SW_StyleSheet_label)
        RQ_predict_O_title.setStyleSheet(SW_StyleSheet_label)
        RQ_predict_C_title.setStyleSheet(SW_StyleSheet_label)
        RQ_predict_L_title.setStyleSheet(SW_StyleSheet_label)

        SW_StyleSheet_combobox = 'font-family: "Microsoft YaHei"; font-size: 25px; color: black;'
        RQ_dataloader_1.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        RQ_dataloader_2.pathLineEdit.setStyleSheet(SW_StyleSheet_combobox)
        RQ_dataVisualization.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        RQ_model_selection.comboBox.setStyleSheet(SW_StyleSheet_combobox)
        RQ_predict_O.setStyleSheet(SW_StyleSheet_combobox)
        RQ_predict_C.setStyleSheet(SW_StyleSheet_combobox)
        RQ_predict_L.setStyleSheet(SW_StyleSheet_combobox)



        SW_StyleSheet_showbutton = 'font-family: "Microsoft YaHei"; font-size: 25px; color: black; padding: 5px;'
        RQ_dataloader_1.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        RQ_dataloader_2.chooseButton.setStyleSheet(SW_StyleSheet_showbutton)
        RQ_dataVisualization.plotlyWidgetButton.setStyleSheet(SW_StyleSheet_showbutton)
        RQ_dataVisualization.showButton.setStyleSheet(SW_StyleSheet_showbutton)
        RQ_model_selection.showButton.setStyleSheet(SW_StyleSheet_showbutton)

        RQ_dataloader_1.chooseButton.setMinimumWidth(100)
        RQ_dataloader_2.chooseButton.setMinimumWidth(100)
        RQ_dataVisualization.plotlyWidgetButton.setMinimumWidth(100)
        RQ_model_selection.comboBox.setMinimumWidth(300)

        # 设置布局
        fromLayout = QVBoxLayout()
        dataloaderLayout = QHBoxLayout()
        predictLayout = QHBoxLayout()
        predictoutputLayout = QHBoxLayout()
        model_predLayout = QHBoxLayout()

        # 添加边距和间距
        fromLayout.setContentsMargins(100, 10, 100, 10)
        predictLayout.setContentsMargins(10, 0, 10, 0)
        model_predLayout.setContentsMargins(0, 0, 0, 50)


        # 数据加载
        dataloaderLayout.addWidget(RQ_dataloader_1, 1)
        dataloaderLayout.addWidget(RQ_dataloader_2, 1)


        # 预测结果
        predictoutputLayout.addWidget(RQ_predict_O_title, 1)
        predictoutputLayout.addWidget(RQ_predict_O, 1)
        predictoutputLayout.addWidget(RQ_predict_C_title, 1)
        predictoutputLayout.addWidget(RQ_predict_C, 1)
        predictoutputLayout.addWidget(RQ_predict_L_title, 1)
        predictoutputLayout.addWidget(RQ_predict_L, 1)
        predictLayout.addWidget(RQ_predict, 1)
        predictLayout.addLayout(predictoutputLayout, 1)
        
        
        # 添加控件到布局
        model_predLayout.addWidget(RQ_model_selection, 1)
        model_predLayout.addLayout(predictLayout, 1)
        fromLayout.addLayout(dataloaderLayout, 1)
        fromLayout.addWidget(RQ_dataVisualization, 4)
        fromLayout.addLayout(model_predLayout, 1)


        # 创建容器控件并设置布局
        containerWidget = QWidget()
        containerWidget.setLayout(fromLayout)
        self.stackedWidget.addWidget(containerWidget)
    
    def RQ_show_spectra(self):
        # TODO: 实现显示光谱曲线的功能
        pass
    def RQ_show_signal(self):
        # TODO: 实现显示传感器信号的功能
        pass
    def RQ_show_3D_Mobilnet(self):
        # TODO: 实现显示3D-Mobilnet的功能
        pass
    def RQ_show_MTCN_SA(self):
        # TODO: 实现显示MTCN-SA的功能
        pass
    def RQ_show_HFA_Net(self):
        # TODO: 实现显示HFA-Net的功能
        pass



