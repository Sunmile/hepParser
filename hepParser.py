"""
author:houmeijie
author2: wanghui
"""
## This version is used for high resolution image shotting only
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from matplotlib.backend_bases import *
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from candidate_dialog import QmyDialogSize, QAnalyseBar, pbar_str
from spectra_tools_fix import *
from Hp_opt import get_fit_pk, get_comp_pk, save_file, get_filter_MZ
from PIL import Image
from mzML_parser import getPeaksById
from draw_3D import *

# import pymzml
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import platform
import mplcursors
import time
import xlwt

qstr = """
        QWidget {
            background:white;
            font-size:16px;
            color:#3265f6}
        QPushButton {
            border-radius: 4px;
            padding: 5px 12px;
            background-color: #3265f6;
            color: white;
        }
        QPushButton:hover {
            background-color: #538bf7;
        }
        QPushButton:pressed {
            background-color: #538bf7;
        }
        QWidget#left26{
            margin-left:20px;
        }
        QLineEdit{
            background-color: white;
            border:1px solid #dddddd;
            border-radius: 2px;
            padding: 6px 6px;
        }
        QMessageBox {
            font-size: 14px;
            padding: 10px;
        }
        QLabel#font8{
            font-size: 12px;
        }
        QLineEdit#font_gray{
            color:gray;
        }
        """
# 滚动条样式
scroll_str = """
            QScrollBar:vertical{
                width:6px;
                background:#dddddd;
                margin:0px,0px,0px,0px;
            }
            QScrollBar:horizontal{
                height:6px;
                background:#dddddd;
                margin:0px,0px,0px,0px;
            }
            QScrollBar::handle:vertical
            {
                width:6px;
                background:#bbbbbb; 
                border-radius:3px;   
                min-height:20;
            }
            QScrollBar::handle:horizontal
            {
                height:6px;
                background:#bbbbbb; 
                border-radius:3px;   
                min-width:20;
            }
            QScrollBar::handle:vertical:hover
            {
                width:6px;
                background:#aaaaaa;   
                border-radius:3px;
                min-height:20;
            }
            QScrollBar::handle:horizontal:hover
            {
                height:6px;
                background:#aaaaaa;   
                border-radius:3px;
                border-radius:3px;
                min-width:20;
            }
            QScrollBar::add-page:vertical,QScrollBar::sub-page:vertical,QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal
            {
                background:#eeeeee;
                border-radius:4px;
            }
            """
# 导航条的样式
navi_str = """
            QWidget {
                border: none;
                background: #f5f5f5;
                color:#3265f6;
                padding:4px;
                font-size:14px} 
            QWidget:hover {
                background-color: #dddddd;
            }
            QWidget:pressed {
                background-color: #dddddd;
            }
            """
if platform.system() != "Windows":
    # 分析界面左侧按钮
    label_btn_str = """QPushButton {
                        background-color: #7b94b1;
                        color :white;
                        padding: 1px 1px;
                        border-radius:10px;
                        margin: 0px;
                    }
                    """
    # 分析界面左侧按钮被按下时
    push_label_btn_str = """QPushButton {
                            background-color: #7b94b1;
                            color :blue;
                            padding: 1px 1px;
                            border-radius:10px;
                            margin: 0px;
                        }
                        """
    # 原始谱界面的 scan编号样式 被按下的样式
    push_scan_label_str = """
                            QPushButton{ 
                                border-radius: 16px;
                                background-color:#3265f6;
                                border:2px solid #3265f6;
                                color: white;
                            }
                            """
    # tic图界面左侧的scan的样式
    tmp_scan_label_str = """
                        QPushButton{
                            border-radius: 16px;
                            padding: 5px 12px;
                            background-color: white;
                            color: #3265f6;
                            border:2px solid #3265f6;
                        }
                        QPushButton:hover {
                            background-color: #3265f6;
                            color:white;
                        }
                        QPushButton:pressed {
                            background-color: #3265f6;
                            color:white;
                        }
                        """
else:
    label_btn_str = """QPushButton {
                            background-color: #7b94b1;
                            color :white;
                            padding: 1px 1px;
                            border-radius:9px;
                            margin: 0px;
                        }
                        """
    # 分析界面左侧按钮被按下时
    push_label_btn_str = """QPushButton {
                                background-color: #7b94b1;
                                color :blue;
                                padding: 1px 1px;
                                border-radius:9px;
                                margin: 0px;
                            }
                            """
    # 原始谱界面的 scan编号样式 被按下的样式
    push_scan_label_str = """
                            QPushButton{ 
                                border-radius: 15px;
                                background-color:#3265f6;
                                border:2px solid #3265f6;
                                color: white;
                            }
                            """
    tmp_scan_label_str = """
                            QPushButton{
                                border-radius: 15px;
                                padding: 5px 12px;
                                background-color: white;
                                color: #3265f6;
                                border:2px solid #3265f6;
                            }
                            QPushButton:hover {
                                background-color: #3265f6;
                                color:white;
                            }
                            QPushButton:pressed {
                                background-color: #3265f6;
                                color:white;
                            }
                            """

# label的分子式的样式
label_struct_str = """QPushButton {
                        background-color:none;
                        color :black;
                        text-align:left;
                        padding: 1px 0px;
                        margin: 0px;
                    }
                    """
# label的分子式的样式被选中的样式
push_label_struct_str = """QPushButton {
                            background-color:none;
                            color :blue;
                            text-align:left;
                            padding: 1px 0px;
                            margin: 0px;
                        }
                        """

# 原始谱界面的 scan编号右侧的图标按钮
scan_icon_str = """
                QPushButton {
                    border-radius: 5px;
                    padding: 5px 5px;
                    background-color:none;
                    border-image:url(icon/QT1.png);
                    color: gray;
                }
                """

push_scan_icon_str = """
                QPushButton {
                    border-radius: 5px;
                    padding: 5px 5px;
                    background-color:none;
                    border-image:url(icon/QT.png);
                    color: gray;
                }
                QPushButton:hover {
                    border-image:url(icon/QT2.png);
                    
                }
                QPushButton:pressed {
                     border-image:url(icon/QT2.png);
                }
                """
# 原始谱界面的 scan编号右侧的减号按钮被按下去时
scan_btn_str = """
                QPushButton {
                    border-radius: 4px;
                    padding: 5px 12px;
                    background-color: #eaeaea;
                    color: gray;
                }
                QPushButton:hover {
                    background-color: #dddddd;
                }
                QPushButton:pressed {
                    background-color: #dddddd;
                }
                """


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self._init_config()

        self._init_data()

        self._init_ui()

    def _init_config(self):
        self.spectrumIDList = []
        self.xmlFinished = False
        self.init_finish = False
        self.inited_tic = False
        self.isRaw = False
        self.figFlag = 0  # tic：1  labels:2  famliy:3
        self.spectrumIndex = 0
        self.candidate_num = 0
        self.ppm = 20
        self.bound_th = 0.001
        self.bound_intensity = 300
        self.x_percentage_value = 0
        self.y_percentage_value = 0
        self.x_space = 12
        self.y_space = 20
        self.anno_text_size = 14
        self.opacity = [False, False, False, False]
        self.peaks_flag = [True, False, False, False, True]
        self.peaks_family_flag = [True, True]
        self.bound = ['', '', '', '']
        self.bound_family = ['', '', '', '']
        self.scan_plot = {}
        self.scan_widget = {}
        self.scan_com_button = {}
        self.chk_list = []
        # self.lose_ion = ["HSO_3", 'NH_2', 'NH_{2}SO_3', 'COOH']
        self.lose_ion = ["SO_3", 'NH', 'NHSO_3', 'COO']
        if platform.system() != "Windows":
            self.x_space = 15
            self.y_space = 36
            self.anno_text_size = 13
            print("OS", platform.system())

    def _init_data(self):
        s = time.time()
        self.DATA0 = 'data/plot0_005_tic.pk'
        self.ori_mass_range = [0, 1200]
        self.ori_scan_range = [0, 1400]
        self.fit_list = get_fit_pk('data/Isotope_dist_fit.pk')
        self.the_HP = get_comp_pk('data/HP_20.pk')  # 枚举的理论肝素结构
        self.peak_dict = {}  # 保存实验谱mz->absolute intensity

        e = time.time()
        print("load pk:", e - s)

    def _init_ui(self):

        # 获取总的屏幕大小
        screen = QDesktopWidget().screenGeometry()
        self.setWindowTitle("hepParser")
        self.window().setObjectName("window")
        self.resize(screen.width() * 0.9, screen.height() * 0.9)

        # 设置窗体在屏幕中间
        windowSize = self.geometry()
        self.move((screen.width() - windowSize.width()) / 2, (screen.height() - windowSize.height()) / 8)
        self.setWindowIcon(QIcon('icon/analysing.svg'))

        # 设置外观属性
        mpl.rcParams['font.sans-serif'] = ['SimHei', 'STSong', 'STHeiti', 'Songti SC', 'PingFang HK']  # 汉字字体
        mpl.rcParams['font.size'] = 14  # 字体大小
        mpl.rcParams['axes.unicode_minus'] = False  # 正常显示符号

        # 窗体主要内容
        self._initcentralWidget()

        # 菜单栏
        self._initMenu()

        # 工具栏
        self._initToolBar()

        # 状态栏
        self._initStatusBar()

        # 右键
        self.createContextMenu()

    def _initcentralWidget(self):

        # 左侧第1页
        self.centralWidget = QWidget(self)
        self.left_box = QToolBox(self.centralWidget)
        self.left_box.setGeometry(QRect(5, 5, 356, 551))
        self.left_box.setFrameShape(QFrame.NoFrame)

        """左侧边栏的子面板1"""

        _translate = QCoreApplication.translate

        """1的面板"""
        self.page_tic = QWidget()
        self.page_tic.setGeometry(QRect(0, 0, 356, 401))

        self.verticalLayout_1 = QVBoxLayout(self.page_tic)
        self.verticalLayout_1.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_1.setSpacing(2)
        self.scrollArea_1 = QScrollArea(self.page_tic)
        self.scrollArea_1.setFrameShape(QFrame.Panel)
        self.scrollArea_1.setFrameShadow(QFrame.Raised)
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollArea_1.verticalScrollBar().setStyleSheet(scroll_str)
        self.scrollArea_1.horizontalScrollBar().setStyleSheet(scroll_str)
        self.scrollAreaWidgetContents_1 = QWidget()
        self.scrollAreaWidgetContents_1.setGeometry(QRect(0, 0, 348, 393))

        self.verticalLayout_10 = QVBoxLayout(self.scrollAreaWidgetContents_1)
        self.verticalLayout_10.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName("verticalLayout_20")

        """1.1"""
        self.scan_context = QWidget(self.scrollAreaWidgetContents_1)
        self.scan_context_verticalLayout = QVBoxLayout(self.scan_context)

        self.scan_context_verticalLayout.setSpacing(0)
        # self.scan_context.setObjectName("left26")

        self.add_scan_region = QWidget()
        self.add_scan_horizontalLayout = QHBoxLayout(self.add_scan_region)
        self.add_scan_region.setFixedWidth(160)
        self.add_scan_label = QLineEdit()
        self.add_scan_label.setText("Scan Id")
        self.add_scan_label.setFixedWidth(90)
        # self.add_scan_label.setFixedHeight(60)
        self.add_scan_btn = QPushButton("+")
        self.add_scan_btn.clicked.connect(self.add_scan)
        self.add_scan_btn.setFixedWidth(34)
        # self.add_scan_btn.setFixedHeight(60)
        self.add_scan_horizontalLayout.addWidget(self.add_scan_label)
        self.add_scan_horizontalLayout.addWidget(self.add_scan_btn)
        # self.scan_context_verticalLayout.addWidget(self.add_scan_region)

        # self.tic_btn = QPushButton("解析质谱")
        # self.tic_btn.clicked.connect(self.dataProcess_case)
        # self.tic_btn.setObjectName("left26")
        # self.tic_btn.setFixedWidth(158)

        self.verticalLayout_10.addWidget(self.scan_context)
        # self.verticalLayout_10.addWidget(self.tic_btn)
        self.verticalLayout_10.addStretch()
        self.verticalLayout_10.setSpacing(0)

        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents_1)
        self.verticalLayout_1.addWidget(self.scrollArea_1)

        # 左侧第2页
        self.right_label_page = QWidget()
        self.right_label_page.setGeometry(QRect(0, 0, 356, 401))
        self.right_verticalLayout_2 = QVBoxLayout(self.right_label_page)
        self.right_verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.right_verticalLayout_2.setSpacing(2)

        # 上半部分
        self.right_function_region = QWidget()

        self.right_function_verticalLayout_21 = QVBoxLayout(self.right_function_region)
        self.right_function_verticalLayout_21.setContentsMargins(3, 3, 3, 3)
        self.right_function_verticalLayout_21.setSpacing(2)
        self.right_function_scrollArea_21 = QScrollArea(self.right_function_region)
        self.right_function_scrollArea_21.setFrameShape(QFrame.Panel)
        self.right_function_scrollArea_21.setFrameShadow(QFrame.Raised)
        self.right_function_scrollArea_21.setWidgetResizable(True)
        self.right_function_scrollArea_21.verticalScrollBar().setStyleSheet(scroll_str)
        self.right_function_scrollArea_21.horizontalScrollBar().setStyleSheet(scroll_str)
        self.right_function_scrollAreaWidgetContents_21 = QWidget()
        self.right_function_scrollAreaWidgetContents_21.setGeometry(QRect(0, 0, 348, 393))

        self.right_function_verticalLayout = QVBoxLayout(self.right_function_scrollAreaWidgetContents_21)

        self.right_tic = QWidget()
        self.right_tic_verticalLayout = QVBoxLayout(self.right_tic)
        self.right_tic_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.right_tic_verticalLayout.setSpacing(10)
        self.right_config = QWidget()
        self.right_config_verticalLayout = QVBoxLayout(self.right_config)
        self.right_config_verticalLayout.setSpacing(2)

        self.ppm_region = QWidget()
        self.ppm_region_horizontalLayout = QHBoxLayout(self.ppm_region)
        self.ppm_region_horizontalLayout.setSpacing(8)
        self.ppm_region.setFixedWidth(180)
        # self.ppm_region.setObjectName("left26")
        self.ppm_info = QLabel()
        self.ppm_info.setText(_translate("MainWindow", "ppm:"))
        self.ppm_info.setStyleSheet("QLabel{background:none}")
        self.ppm_info.setFixedWidth(40)
        self.edit_ppm = QLineEdit()
        self.edit_ppm.setStyleSheet("QLabel{background:none}")
        self.edit_ppm.setPlaceholderText(str(self.ppm))
        self.edit_ppm.textEdited.connect(self.ppm_text_changed)
        self.edit_ppm.setObjectName("font_gray")
        self.edit_ppm.setFixedWidth(50)
        self.right_anylyse = QPushButton("Apply")
        self.right_anylyse.clicked.connect(self.apply_ppm)
        self.right_anylyse.setFixedWidth(68)
        self.right_anylyse.setStyleSheet(scan_btn_str)
        self.ppm_region_horizontalLayout.addWidget(self.ppm_info)
        self.ppm_region_horizontalLayout.addWidget(self.edit_ppm)
        self.ppm_region_horizontalLayout.addWidget(self.right_anylyse)

        self.check_region = QWidget()
        self.check_region_verticalLayout = QVBoxLayout(self.check_region)
        self.check_region_verticalLayout.setSpacing(8)
        self.check_region.setFixedWidth(200)
        self.chb_dA = QCheckBox('No dA')
        self.chb_dA.setChecked(False)
        self.chb_aG = QCheckBox('No aG')
        self.chb_aG.setChecked(False)
        self.chb_aM = QCheckBox('No aM')
        self.chb_aM.setChecked(False)
        self.check_region_verticalLayout.addWidget(self.chb_dA)
        self.check_region_verticalLayout.addWidget(self.chb_aG)
        self.check_region_verticalLayout.addWidget(self.chb_aM)

        self.dp_region1 = QWidget()
        self.dp_region1_horizontalLayout = QHBoxLayout(self.dp_region1)
        self.dp_region1_horizontalLayout.setSpacing(8)
        self.dp_region1.setFixedWidth(180)
        self.dp_info = QLabel()
        self.dp_info.setText(_translate("MainWindow", "Min dp:"))
        self.dp_info.setStyleSheet("QLabel{background:none}")
        self.dp_info.setFixedWidth(60)
        self.dp_min = QLineEdit()
        self.dp_min.setStyleSheet("QLabel{background:none}")
        self.dp_min.setPlaceholderText(str(0))
        self.dp_min.setObjectName("font_gray")
        self.dp_min.setFixedWidth(60)
        self.dp_region2 = QWidget()
        self.dp_region2_horizontalLayout = QHBoxLayout(self.dp_region2)
        self.dp_region2_horizontalLayout.setSpacing(8)
        self.dp_region2.setFixedWidth(180)
        self.dp_info2 = QLabel()
        self.dp_info2.setText(_translate("MainWindow", "Max dp:"))
        self.dp_info2.setStyleSheet("QLabel{background:none}")
        self.dp_info2.setFixedWidth(60)
        self.dp_max = QLineEdit()
        self.dp_max.setStyleSheet("QLabel{background:none}")
        self.dp_max.setPlaceholderText(str(20))
        self.dp_max.setObjectName("font_gray")
        self.dp_max.setFixedWidth(60)
        self.dp_region1_horizontalLayout.addWidget(self.dp_info)
        self.dp_region1_horizontalLayout.addWidget(self.dp_min)
        self.dp_region2_horizontalLayout.addWidget(self.dp_info2)
        self.dp_region2_horizontalLayout.addWidget(self.dp_max)

        self.right_config_verticalLayout.addWidget(self.right_tic)
        self.right_config_verticalLayout.addWidget(self.ppm_region)
        self.right_config_verticalLayout.addWidget(self.check_region)
        self.right_config_verticalLayout.addWidget(self.dp_region1)
        self.right_config_verticalLayout.addWidget(self.dp_region2)


        self.right_function_verticalLayout.addWidget(self.right_config)
        # self.right_function_verticalLayout.addWidget(self.right_anylyse)
        self.right_function_verticalLayout.addStretch()
        self.right_function_scrollArea_21.setWidget(self.right_function_scrollAreaWidgetContents_21)
        self.right_function_verticalLayout_21.addWidget(self.right_function_scrollArea_21)

        self.right_center = QWidget()
        self.right_center_horizontalLayout = QVBoxLayout(self.right_center)
        self.right_center_horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.right_center_horizontalLayout.setSpacing(2)
        self.right_center_horizontalLayout.setAlignment(Qt.AlignHCenter)
        # 下半部分
        self.right_struct_info = QWidget()

        self.right_verticalLayout_21 = QVBoxLayout(self.right_struct_info)
        self.right_verticalLayout_21.setContentsMargins(3, 3, 3, 3)
        self.right_verticalLayout_21.setSpacing(2)
        self.right_scrollArea_21 = QScrollArea(self.right_struct_info)
        self.right_scrollArea_21.setFrameShape(QFrame.Panel)
        self.right_scrollArea_21.setFrameShadow(QFrame.Raised)
        self.right_scrollArea_21.setWidgetResizable(True)
        self.right_scrollArea_21.horizontalScrollBar().setStyleSheet(scroll_str)
        self.right_scrollArea_21.verticalScrollBar().setStyleSheet(scroll_str)
        self.right_scrollAreaWidgetContents_21 = QWidget()
        self.right_scrollAreaWidgetContents_21.setGeometry(QRect(0, 0, 348, 393))

        self.right_verticalLayout_211 = QVBoxLayout(self.right_scrollAreaWidgetContents_21)
        # self.right_verticalLayout_211.setContentsMargins(1,1,1,1)
        self.right_verticalLayout_211.setSpacing(2)
        self.right_verticalLayout_211.setObjectName("right_verticalLayout_20")

        self.struct_title_region = QWidget()
        self.struct_title_region_horizontalLayout = QHBoxLayout(self.struct_title_region)

        self.struct_title_num = QLabel()
        self.struct_title_info = QLabel()
        self.struct_title_score = QLabel()
        self.struct_title_padj = QLabel()
        self.struct_title_region_horizontalLayout.addWidget(self.struct_title_num)
        self.struct_title_region_horizontalLayout.addWidget(self.struct_title_info)
        self.struct_title_region_horizontalLayout.addWidget(self.struct_title_score)
        self.struct_title_region_horizontalLayout.addWidget(self.struct_title_padj)


        # self.struct_title_info_2 = QLabel()
        # self.struct_title_info_2.setObjectName("font8")

        self.right_comp_region = QWidget()
        self.right_label_horizontalLayout = QHBoxLayout(self.right_comp_region)
        self.right_label_horizontalLayout.setSpacing(2)

        self.right_struct_btn_region = QWidget()
        self.right_struct_btn_verticalLayout = QVBoxLayout(self.right_struct_btn_region)
        self.right_struct_region = QWidget()
        self.right_struct_region_verticalLayout = QVBoxLayout(self.right_struct_region)
        self.right_struct_score = QWidget()
        self.right_struct_score_verticalLayout = QVBoxLayout(self.right_struct_score)
        self.right_struct_padj = QWidget()
        self.right_struct_padj_verticalLayout = QVBoxLayout(self.right_struct_padj)
        self.right_struct_btn_verticalLayout.setSpacing(2)
        self.right_struct_region_verticalLayout.setSpacing(2)
        self.right_struct_score_verticalLayout.setSpacing(2)
        self.right_struct_padj_verticalLayout.setSpacing(2)
        self.right_label_horizontalLayout.addWidget(self.right_struct_btn_region)
        self.right_label_horizontalLayout.addWidget(self.right_struct_region)
        self.right_label_horizontalLayout.addWidget(self.right_struct_score)
        self.right_label_horizontalLayout.addWidget(self.right_struct_padj)

        self.right_verticalLayout_211.addWidget(self.struct_title_region)
        # self.right_verticalLayout_211.addWidget(self.struct_title_info_2)
        self.right_verticalLayout_211.addWidget(self.right_comp_region)

        # spacerItem = QSpacerItem(20,40,1,4)
        # self.right_verticalLayout_211.addItem(spacerItem)
        self.right_verticalLayout_211.addStretch()

        self.right_scrollArea_21.setWidget(self.right_scrollAreaWidgetContents_21)
        self.right_verticalLayout_21.addWidget(self.right_scrollArea_21)

        sub_splitter = QSplitter(self)
        sub_splitter.setOrientation(Qt.Vertical)
        sub_splitter.addWidget(self.right_function_region)
        sub_splitter.addWidget(self.right_center)
        sub_splitter.addWidget(self.right_struct_info)  # 右侧FigureCanvas对象

        sub_splitter.setStretchFactor(0, 40)
        sub_splitter.setStretchFactor(1, 10)
        sub_splitter.setStretchFactor(2, 50)
        sub_splitter.setHandleWidth(1)
        self.right_verticalLayout_2.addWidget(sub_splitter)

        # 左侧面板
        self.left_box.addItem(self.page_tic, "TIC spectra select")
        self.left_box.addItem(self.right_label_page, "Parameters")
        self.left_box.setStyleSheet(qstr)
        # self.left_box.setFixedWidth(240)

        # 中间图表面板
        self._fig = mpl.figure.Figure(figsize=(8, 5), dpi=88)  # 单位英寸
        self._fig.subplots_adjust(left=0.09, bottom=0.09, right=0.95, top=0.9, wspace=0.3, hspace=0.3)
        self.figCanvas = FigureCanvas(self._fig)  # 创建FigureCanvas对象，必须传递一个Figure对象
        self.figCanvas.setCursor(Qt.PointingHandCursor)
        self._cid1 = self.figCanvas.mpl_connect("pick_event", self.pick_event)
        self.figCanvas.setStyleSheet("QWidget{border:none}")

        self._drawInit()

        # 设置左侧边栏和右侧图表面板
        # self.splitter = QSplitter(self)
        # self.splitter.setOrientation(Qt.Horizontal)
        # self.splitter.addWidget(self.figCanvas)
        # self.splitter.addWidget(self.left_box)
        # self.splitter.addWidget(self.figCanvas)
        # leftWidth = int(400 * 100.0 / (QDesktopWidget().screenGeometry().width()))
        # self.splitter.setStretchFactor(0, leftWidth)
        # self.splitter.setStretchFactor(1, 100 - leftWidth)
        # self.splitter.setHandleWidth(0)
        # self.splitter.setStyleSheet("QSplitter::handle { background-color:white}")
        self.setCentralWidget(self.figCanvas)

    def _initMenu(self):

        # 菜单栏的action
        openMzFileAct = QAction('Open .mzML', self)
        openMzFileAct.setStatusTip('Open .mzML')
        openMzFileAct.triggered.connect(self.openTICByMzML)

        openRawFileAct = QAction('Open .raw', self)
        openRawFileAct.setStatusTip('Open .raw')
        openRawFileAct.triggered.connect(self.openTICByRawFile)

        openDirAct = QAction('Open raw dir', self)
        openDirAct.setStatusTip('Open raw directory')
        openDirAct.triggered.connect(self.openTICByRawDir)

        showTICAct = QAction('show TIC', self)
        showTICAct.triggered.connect(self.showTIC)

        showTableAct = QAction('show table', self)
        showTableAct.triggered.connect(self._drawTable)

        downloadAct = QAction('download table', self)
        downloadAct.setStatusTip('download table')
        downloadAct.triggered.connect(self.downloadTabel)

        aboutAct = QAction('about hepParser', self)
        aboutAct.setStatusTip('about hepParser')
        aboutAct.triggered.connect(self.aboutUs)

        exitMenuAct = QAction('Exit', self)
        exitMenuAct.setStatusTip('Exit application')
        exitMenuAct.triggered.connect(self.close)

        # 菜单栏
        menubar = self.menuBar()

        fileMenu = menubar.addMenu('File')  # File还是&File
        fileMenu.addAction(openMzFileAct)
        fileMenu.addAction(openRawFileAct)
        fileMenu.addAction(openDirAct)

        viewMenu = menubar.addMenu('View')
        viewMenu.addAction(showTICAct)
        viewMenu.addAction(showTableAct)

        toolMenu = menubar.addMenu('Tools')
        toolMenu.addAction(downloadAct)

        aboutMenu = menubar.addMenu('about')
        aboutMenu.addAction(aboutAct)

        exitMenu = menubar.addMenu('Exit')
        exitMenu.addAction(exitMenuAct)

    def _initToolBar(self):
        # 自定义的工具栏工具
        self.openDirActIcon = QAction(QIcon('icon/folder-open-regular.svg'), "Open Dir", self)
        self.openDirActIcon.setStatusTip('Open raw directory')
        self.openDirActIcon.triggered.connect(self.openTICByRawDir)
        self.openDirActIcon.setObjectName("blue")

        self.openFileActIcon = QAction(QIcon('icon/text-file-svgrepo-com.svg'), "Open file", self)
        self.openFileActIcon.setStatusTip('Open .mzml')
        self.openFileActIcon.triggered.connect(self.openTICByMzML)

        self.showTICAction = QAction(QIcon('icon/text.svg'), 'TIC', self)
        self.showTICAction.setStatusTip('TIC')
        self.showTICAction.triggered.connect(self.showTIC)

        # labelAction = QAction(QIcon('icon/chart-bar-regular.svg'), '解析质谱', self)
        # labelAction.setStatusTip('解析质谱')
        # labelAction.triggered.connect(self.load_origin_peaks_case)

        self.changeAction = QAction(QIcon('icon/statistics.svg'), 'Component', self)
        self.changeAction.setStatusTip('Component')
        self.changeAction.triggered.connect(self.change_comp)

        self.tableAction = QAction(QIcon('icon/table-svgrepo-com.svg'), 'Table', self)
        self.tableAction.setStatusTip('Show table')
        self.tableAction.triggered.connect(self._drawTable)

        self.downloadAction = QAction(QIcon('icon/download-svgrepo-com.svg'), 'Download', self)
        self.downloadAction.setStatusTip('Download')
        self.downloadAction.triggered.connect(self.downloadTabel)

        # 设置工具栏的语言
        self.naviToolbar = NavigationToolbar(self.figCanvas, self)  # 创建工具栏
        self.naviToolbar.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)  # ToolButtonTextUnderIcon,ToolButtonTextBesideIcon
        actList = self.naviToolbar.actions()

        actList = self.naviToolbar.actions()  # 关联的Action列表
        actList[0].setText("Reset")  # Home
        actList[0].setToolTip("Reset the view")  # Reset original view
        actList[0].setIcon(QIcon('icon/home-run.svg'))

        actList[1].setText("Back")  # Back
        actList[1].setToolTip("Back to previous view")  # Back to previous view
        actList[1].setIcon(QIcon('icon/left-arrow.svg'))

        actList[2].setText("Forward")  # Forward
        actList[2].setToolTip("Forward to next view")  # Forward to next view
        actList[2].setIcon(QIcon('icon/next.svg'))

        actList[4].setText("Pan")  # Pan
        actList[4].setToolTip("Pan axes with left mouse, zoom with right")  # Pan axes with left mouse, zoom with right
        actList[4].setIcon(QIcon('icon/move.svg'))

        actList[5].setText("Zoom")  # Zoom
        actList[5].setToolTip("Zoom to rectangle")  # Zoom to rectangle
        actList[5].setIcon(QIcon('icon/zoom.svg'))

        actList[6].setText("Subplots")  # Subplots
        actList[6].setToolTip("Configure subplots")  # Configure subplots
        actList[6].setIcon(QIcon('icon/desktop.svg'))

        actList[7].setText("Customize")  # Customize
        actList[7].setToolTip("Edit axis, curve and image parameters")  # Edit axis, curve and image parameters
        actList[7].setIcon(QIcon('icon/config.svg'))

        actList[9].setText("Save")  # Save
        actList[9].setToolTip("Save the figure")  # Save the figure
        actList[9].setIcon(QIcon('icon/save.svg'))

        # 设置初始透明度:
        self.setOpacity()

        self.naviToolbar.insertAction(actList[0], self.openDirActIcon)
        self.naviToolbar.insertAction(actList[0], self.openFileActIcon)
        self.naviToolbar.insertAction(actList[0], self.showTICAction)
        self.naviToolbar.insertAction(actList[0], self.changeAction)
        self.naviToolbar.insertAction(actList[0], self.tableAction)
        self.naviToolbar.insertAction(actList[0], actList[8])

        self.naviToolbar.removeAction(actList[6])
        self.naviToolbar.removeAction(actList[7])

        count = len(actList)  # Action的个数
        lastAction = actList[count - 1]  # 最后一个Action
        self.naviToolbar.insertAction(lastAction, self.downloadAction)

        self.naviToolbar.setStyleSheet(navi_str)

        self.addToolBar(self.naviToolbar)  # 添加matplotlib自带的工具栏到主窗口

    def _initStatusBar(self):
        self.info_label = QLabel()
        self.info_label.setMinimumWidth(200)

    def _drawInit(self):
        img = Image.open('icon/background.png')
        ax1 = self._fig.add_subplot(1, 1, 1)
        ax1.imshow(img)
        ax1.axis("off")
        self._fig.canvas.draw_idle()

    def _draw3D(self):
        self._fig = self.draw_3d_plot(self.DATA0, self.ori_mass_range, self.ori_scan_range)

    def _drawTIC(self):
        self.figFlag = 1
        self.ppm = 20
        self.page_tic.setDisabled(False)
        self.left_box.setCurrentWidget(self.page_tic)

        if self.isRaw:
            self.dlgProgress.close()

        self._fig.clear()
        self.ticAx = self._fig.add_subplot(1, 1, 1)

        tic_line = self.ticAx.plot(self.xmlInfo[0], self.xmlInfo[1], c='black', linewidth=0.3, picker=True)
        self.ticAx.fill_between(self.xmlInfo[0], 0, self.xmlInfo[1], facecolor='#E6ECF5')

        mplcursors.cursor(tic_line, hover=True,
                          annotation_kwargs=dict(
                              bbox=dict(boxstyle="round,pad=.6",
                                        fc="#e3e3e3",
                                        alpha=.2,
                                        ec="#0670DB", lw=2),
                              arrowprops=dict(
                                  arrowstyle="->",
                                  connectionstyle="arc3",
                                  shrinkB=3,
                                  ec="#0325A6",
                              )))

        if not self.init_finish:
            # 设置左侧边栏和右侧图表面板
            self.splitter = QSplitter(self)
            self.splitter.setOrientation(Qt.Horizontal)
            # self.splitter.addWidget(self.figCanvas)
            self.splitter.addWidget(self.left_box)
            self.splitter.addWidget(self.figCanvas)
            # if platform.system() != "Windows":
            #     leftWidth = int(660 * 100.0 / (QDesktopWidget().screenGeometry().width()))
            # else:
            #     leftWidth = int(840 * 100.0 / (QDesktopWidget().screenGeometry().width()))
            # self.splitter.setStretchFactor(0, leftWidth)
            # self.splitter.setStretchFactor(1, 100 - leftWidth)
            self.splitter.setHandleWidth(0)
            self.splitter.setStyleSheet("QSplitter::handle { background-color:white}")
            self.setCentralWidget(self.splitter)
            self.init_finish = True

        if not self.inited_tic:
            self.inited_tic = True
            self.add_scan(self.spectrumID)
        else:
            tmp_list = self.spectrumIDList
            self.spectrumIDList = []
            for i in range(0, self.scan_context_verticalLayout.count()):
                self.scan_context_verticalLayout.itemAt(i).widget().deleteLater()
            for i in range(len(tmp_list)):
                self.add_scan(tmp_list[i])

        self.ticAx.set_title("TIC")  # 子图标题
        self.ticAx.set_xlabel('Time', fontsize=18)
        self.ticAx.set_ylabel('Total Intensity', fontsize=18)
        self.ticAx.set_xlim(left=0, auto=False)
        self.ticAx.set_ylim(bottom=0, auto=False)
        self.ticAx.spines['top'].set_visible(False)
        self.ticAx.spines['right'].set_visible(False)
        self.ticAx.spines['left'].set_linewidth(1.5)
        self.ticAx.spines['bottom'].set_linewidth(1.5)
        self._fig.canvas.draw_idle()

        self.opacity = [True, False, False, False]
        self.setOpacity()

    def generate_left_side(self):  # 在左侧增加按钮
        for i in range(0, self.right_tic_verticalLayout.count()):
            self.right_tic_verticalLayout.itemAt(i).widget().deleteLater()
        for i in range(0, len(self.spectrumIDList)):
            tmp_region = QWidget()
            tmp_region.setFixedWidth(180)
            tmp_hor = QHBoxLayout(tmp_region)
            tmp_hor.setContentsMargins(1, 1, 1, 1)
            tmp_hor.setSpacing(8)

            tmp_id = self.spectrumIDList[i]

            tmp_btn_1 = QPushButton(str(tmp_id))
            tmp_btn_1.clicked.connect(lambda: self._change_spectrum(self.sender().text()))
            tmp_btn_1.setStyleSheet(tmp_scan_label_str)
            tmp_btn_1.setFixedWidth(80)

            tmp_btn_2 = QPushButton(" ")
            tmp_btn_2.clicked.connect(lambda: self.dataProcess(self.sender()))
            tmp_btn_2.setDisabled(True)
            tmp_btn_2.setStyleSheet(scan_icon_str)
            tmp_btn_2.setFixedWidth(30)

            tmp_btn_3 = QPushButton("-")
            tmp_btn_3.clicked.connect(lambda: self.sub_scan_origin_fig(self.sender()))
            tmp_btn_3.setStyleSheet(scan_btn_str)
            tmp_btn_3.setFixedWidth(30)

            tmp_hor.addWidget(tmp_btn_1)
            tmp_hor.addWidget(tmp_btn_2)
            tmp_hor.addWidget(tmp_btn_3)
            self.right_tic_verticalLayout.addWidget(tmp_region)

            self.scan_com_button[self.spectrumIDList[i]] = tmp_region

    def load_origin_peaks(self):
        # run = pymzml.run.Reader(self.mzmlFileName)
        # self.spectrum = run[self.spectrumID]
        self.spectrum, self.maxIntensity = getPeaksById(self.mzmlFileName, self.spectrumID)
        # self.maxIntensity = self.spectrum.peaks("centroided").max()
        # save_file(self.spectrum.peaks("centroided"), "938.mgf")
        self.peaks, self.maxIntensity, self.total_int, self.exp_isp, self.the_spectra, self.dict_list = get_filter_MZ(
            # origin_MZ=self.spectrum.peaks("centroided"),
            origin_MZ=self.spectrum,
            max_int=self.maxIntensity,
            fit_list=self.fit_list,
            the_HP=self.the_HP,
            ppm=self.ppm,
            bound_th=self.bound_th,
            bound_intensity=self.bound_intensity)
        for peak in self.peaks:
            self.peak_dict[peak[0]] = peak[1]
        self.origin_xs, self.origin_ys = format_peaks(self.peaks)

    def plot_origin_peaks(self, xs, ys):  # 获取原始峰
        self.scan_com_button[self.spectrumID].layout().itemAt(0).widget().setStyleSheet(push_scan_label_str)
        self.scan_com_button[self.spectrumID].layout().itemAt(1).widget().setStyleSheet(push_scan_icon_str)
        self.scan_com_button[self.spectrumID].layout().itemAt(1).widget().setDisabled(False)
        self.orgAx.plot(xs, ys, linewidth=1, c='gray', zorder=1)
        self.orgAx.set_ybound(lower=0, upper=1.1 * max(ys))
        self.orgAx.set_xlabel('m/z', fontsize=14)
        self.orgAx.set_ylabel('intensity', fontsize=14)
        self.orgAx.spines['top'].set_visible(False)
        self.orgAx.spines['right'].set_visible(False)
        self.orgAx.spines['left'].set_linewidth(1.5)
        self.orgAx.spines['bottom'].set_linewidth(1.5)
        self.orgAx.set_title("$MS^1(scan=" + str(self.spectrumID) + ")$", fontsize=14)  # 子图标题
        self._fig.canvas.draw_idle()

        self.opacity = [True, False, False, False]
        self.setOpacity()

    def _analyse_Composition(self):

        # 获取全部组成
        self.dataDlgProcess.close()
        self.all_right_struct, self.all_key_with_order = get_all_struct(self.label_info)
        self.chk_list = []
        self.change_comp()

    def _draw_composition(self):
        # 标注分析
        self.figFlag = 3
        self.load_label()
        self.mass_anotation = {}

        self._fig.clear()
        self.orgAx = self._fig.add_subplot(1, 1, 1)

        # 删除按钮
        for i in range(self.right_center_horizontalLayout.count()):
            self.right_center_horizontalLayout.itemAt(i).widget().deleteLater()
        for i in range(self.right_struct_btn_verticalLayout.count()):
            self.right_struct_btn_verticalLayout.itemAt(i).widget().deleteLater()
            self.right_struct_region_verticalLayout.itemAt(i).widget().deleteLater()
            self.right_struct_score_verticalLayout.itemAt(i).widget().deleteLater()
            self.right_struct_padj_verticalLayout.itemAt(i).widget().deleteLater()

        # 重新添加按钮
        change_btn = QPushButton("Activate one label")
        change_info_region = QWidget()
        change_info_region_hori = QVBoxLayout(change_info_region)
        change_info_region_hori.setAlignment(Qt.AlignHCenter)
        change_info_region_hori.setContentsMargins(0, 0, 0, 0)
        change_info = QLabel()
        change_info.setText("Click to select a component to interpret the spectrum")
        change_info.setStyleSheet("QLabel{font-size:8px;}")
        change_info_region_hori.addWidget(change_info)
        # change_btn.setStyleSheet(all_btn_str)
        change_btn.clicked.connect(self._label)
        change_btn.setFixedWidth(200)
        self.right_center_horizontalLayout.addWidget(change_btn)
        self.right_center_horizontalLayout.addWidget(change_info_region)
        # self.right_verticalLayout_22
        # self.struct_title_num.setText("&nbsp;序号<sup></sup>")
        # self.struct_title_info.setText("&nbsp;&nbsp;&nbsp;分子组成<sup>a</sup>")
        # # self.struct_title_info_2.setText("&nbsp;&nbsp;&nbsp;&nbsp;<sup>a</sup>[HexA,GlcA,GlcN,Ac,SO3,Levoglucosan,Man]")
        # self.struct_title_score.setText("<sup></sup>&nbsp;&nbsp;&nbsp;&nbsp;单分子解释度")
        self.struct_title_num.setText("&nbsp;No.<sup></sup>")
        self.struct_title_info.setText("&nbsp;Component<sup></sup>")
        # self.struct_title_info_2.setText("<sup>a</sup>")
        self.struct_title_score.setText("<sup></sup>&nbsp;Score")
        self.struct_title_padj.setText("<sup></sup>&nbsp;-log<sub>10</sub>p<sub>adj</sub>")
        right_is, right_structs, right_scores,right_p = [], [], [],[]
        for i in range(len(self.right_struct)):
            label_btn = QPushButton(str(i + 1))
            label_btn.setStyleSheet(
                label_btn_str[:-1] + "QPushButton{background-color:" + self.colors_str[self.right_struct[i][3]] + "}")

            label_btn.setFixedWidth(21)

            label_struct = QPushButton(self.right_struct[i][0])
            label_struct.setStyleSheet(label_struct_str)

            label_score = QPushButton(str(self.right_struct[i][1]))
            label_score.setStyleSheet(label_struct_str)

            label_padj = QPushButton(str(self.right_struct[i][2]))
            label_padj.setStyleSheet(label_struct_str)

            label_btn.clicked.connect(lambda: self._labelFamilyPeak(self.sender().text()))
            label_struct.clicked.connect(lambda: self._labelFamilyPeak(self.struct_id[self.sender().text()]))

            self.right_struct_btn_verticalLayout.addWidget(label_btn)
            self.right_struct_region_verticalLayout.addWidget(label_struct)
            self.right_struct_score_verticalLayout.addWidget(label_score)
            self.right_struct_padj_verticalLayout.addWidget(label_padj)

            right_is.append(i + 1)
            right_structs.append(self.right_struct[i][0])
            right_scores.append(self.right_struct[i][1])
            right_p.append(self.right_struct[i][2])
        self.struct_df = pd.DataFrame({"id": right_is, "composition": right_structs, "score": right_scores, "log_p_adj":right_p})
        for i in range(self.right_struct_btn_verticalLayout.count()):
            self.right_struct_btn_verticalLayout.itemAt(i).widget().setDisabled(True)
            self.right_struct_region_verticalLayout.itemAt(i).widget().setDisabled(True)
            self.right_struct_score_verticalLayout.itemAt(i).widget().setDisabled(True)
            self.right_struct_padj_verticalLayout.itemAt(i).widget().setDisabled(True)
        self.massToStructs = {}
        self.massToStructsScore = {}
        self.massToStructsChks = {}
        t1 = time.time()
        # print(self.spectrumID, self.xy)
        for key in self.xy:
            label_list = self.mass_labels[key]
            a_list = []

            for j in range(len(label_list)):
                if label_list[j][4] != 1:
                    self.orgAx.annotate(s="+" + str(label_list[j][4] - 1), xy=key,
                                        xytext=(-(self.x_space), +(10 + self.y_space * j + self.y_space * 0.5)),
                                        textcoords='offset pixels',
                                        color='black', ha='center', va='bottom',
                                        fontsize=8, fontweight='extra bold')

                a = self.orgAx.annotate(s=str(label_list[j][-2]), xy=key,
                                        xytext=(+0, +(10 + self.y_space * j)),
                                        textcoords='offset pixels',
                                        color='white', ha='center', va='bottom',
                                        fontsize=self.anno_text_size, fontweight='extra bold',
                                        bbox=dict(boxstyle='circle,pad=0.1',
                                                  fc=self.colors[label_list[j][-2]],
                                                  ec=self.colors[label_list[j][-2]],
                                                  lw=1))
                self.orgAx.annotate(s=str(label_list[j][2]) + "-", xy=key,
                                    xytext=(+(self.x_space), +(10 + self.y_space * j + self.y_space * 0.5)),
                                    textcoords='offset pixels',
                                    color='black', ha='center', va='bottom',
                                    fontsize=8, fontweight='extra bold')
                a_list.append(a)
            self.mass_anotation[key] = a_list
        # 画原始结构
        artists = []
        for i in range(len(self.label_xs)):
            a = self.orgAx.plot(self.label_xs[i], self.label_ys[i],
                                label=self.mass_struct_tips[(self.label_xs[i][1], self.label_ys[i][1])],
                                linewidth=1, color='blue', picker='True', zorder=2)
            artists.append(a)
        mplcursors.cursor(pickables=self.orgAx, hover=True,
                          annotation_kwargs=dict(
                              bbox=dict(boxstyle="round,pad=.7",
                                        fc="#e3e3e3",
                                        alpha=.2,
                                        ec="#7b94b1"),
                              arrowprops=dict(
                                  arrowstyle="->",
                                  connectionstyle="arc3",
                                  shrinkB=3,
                                  ec="#7b94b1",
                              ))).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))
        self.orgAx.plot(self.origin_xs, self.origin_ys, linewidth=1, c='gray', zorder=1)
        self.figFlag = 3

        # print(self.spectrumID, max(self.origin_ys))
        self.orgAx.set_ybound(lower=0)
        self.orgAx.set_xlabel('m/z', fontsize=14)
        self.orgAx.set_ylabel('intensity', fontsize=14)
        self.orgAx.spines['top'].set_visible(False)
        self.orgAx.spines['right'].set_visible(False)
        self.orgAx.spines['left'].set_linewidth(1.5)
        self.orgAx.spines['bottom'].set_linewidth(1.5)
        self.orgAx.set_title("$MS^1(scan=" + str(self.spectrumID) + ")$", fontsize=10,
                             fontproperties='Times New Roman')  # 子图标题
        self._fig.canvas.draw_idle()

        self.opacity = [True, True, True, True]
        self.setOpacity()
        self.tableAction.setText("Show table")
        self.tableAction.setIcon(QIcon('icon/table-svgrepo-com.svg'))
        self.tableAction.triggered.disconnect()
        self.tableAction.triggered.connect(self._drawTable)
        self.right_anylyse.setStyleSheet(scan_btn_str)

    def _drawTable(self):
        if self.figFlag < 3:
            QMessageBox.information(self, "Message", "Please loading spectra data first")
        else:
            self._fig.clear()
            ax2 = self._fig.add_subplot(1, 1, 1)
            rowLabel = ['M/Z', 'Charge', 'Isotopic peak', 'Component', 'Loss']

            table = ax2.table(cellText=self.labels[0:20], colLabels=rowLabel, rowLoc='center',
                              loc='center', cellLoc='center', fontsize=60, edges='open')
            for (row, col), cell in table.get_celld().items():
                if row == 0:
                    cell.visible_edges = "BT"
                if row == 20:
                    cell.visible_edges = 'B'
            # ax2.annotate('目前只显示前18行数据，更多数据请点击"下载分子式"下载后查看', xy=(0.6, 0), color='black', va='bottom', fontsize=10)
            ax2.set_title(
                'Here show the first 20 row data. Please download for the complete data\n'
                'Components:[HexA,GlcA,GlcN,Ac,SO3,Levoglucosan,Dehydrated Mannitol],Loss:[$HSO_3$, $NH_2$, $NH_{2}SO_3$, $COOH$]')
            ax2.axis("off")
            table.scale(1, 2.3)

        self._fig.canvas.draw_idle()
        self.tableAction.setText("Back")
        self.tableAction.setIcon(QIcon('icon/back.svg'))
        self.tableAction.triggered.disconnect()
        self.tableAction.triggered.connect(self._draw_composition)

    def _label(self):
        if self.figFlag < 3:
            QMessageBox.information(self, "Message", "Please loading spectra data first")
        else:
            self.figFlag = 4
            self.left_box.setCurrentWidget(self.right_label_page)
            self._labelFamilyPeak(1)
            # 重新添加按钮
            for i in range(self.right_center_horizontalLayout.count()):
                self.right_center_horizontalLayout.itemAt(i).widget().deleteLater()
            self.struct_title_num.setText("&nbsp;No.<sup></sup>")
            self.struct_title_info.setText("&nbsp;Components<sup></sup>")
            # self.struct_title_info_2.setText("<sup>a</sup>")
            self.struct_title_score.setText("<sup></sup>&nbsp;Score")


            change_btn = QPushButton("Deactivate one label")  # 启动单分子标注
            change_info_region = QWidget()
            change_info_region_hori = QVBoxLayout(change_info_region)
            change_info_region_hori.setAlignment(Qt.AlignHCenter)
            change_info_region_hori.setContentsMargins(0, 0, 0, 0)
            change_info = QLabel()
            change_info.setText("Back")
            change_info.setStyleSheet("QLabel{font-size:8px;}")
            change_info_region_hori.addWidget(change_info)

            change_btn.setFixedWidth(200)
            change_btn.clicked.connect(self._draw_composition)
            self.right_center_horizontalLayout.addWidget(change_btn)
            self.right_center_horizontalLayout.addWidget(change_info_region)
            for i in range(self.right_struct_btn_verticalLayout.count()):
                self.right_struct_btn_verticalLayout.itemAt(i).widget().setDisabled(False)
                self.right_struct_region_verticalLayout.itemAt(i).widget().setDisabled(False)
                self.right_struct_score_verticalLayout.itemAt(i).widget().setDisabled(False)

    def _labelFamilyPeak(self, index):
        for i in range(self.right_struct_btn_verticalLayout.count()):
            self.right_struct_btn_verticalLayout.itemAt(i).widget().setStyleSheet(
                label_btn_str[:-1] + "QPushButton{background-color:" + self.colors_str[self.right_struct[i][3]] + "}")
            self.right_struct_btn_verticalLayout.itemAt(i).widget().setFixedWidth(21)
            self.right_struct_region_verticalLayout.itemAt(i).widget().setStyleSheet(label_struct_str)
            self.right_struct_score_verticalLayout.itemAt(i).widget().setStyleSheet(label_struct_str)

        index = int(index) - 1
        self.right_struct_btn_verticalLayout.itemAt(index).widget().setStyleSheet(push_label_btn_str)
        self.right_struct_region_verticalLayout.itemAt(index).widget().setStyleSheet(push_label_struct_str)
        self.right_struct_score_verticalLayout.itemAt(index).widget().setStyleSheet(push_label_struct_str)

        self._fig.clear()
        self.ax1 = self._fig.add_subplot(1, 1, 1)

        self.ax1.plot(self.origin_xs, self.origin_ys, linewidth=1, c='gray')  # 用折线图画柱体

        # 标注出衍生峰和基团损失

        mz_list, inten_list, comp_list, lose_list, z_list, score_list = self.mass_family[self.key_with_order[index]]
        xs, ys = format_peaks_2_dim(mzs=mz_list, intens=inten_list)
        self.ax1.plot(xs, ys, linewidth=1, c='blue', label=self.right_struct[index][0])

        for i in range(len(mz_list)):
            lose_info = format_loss(lose_list[i], self.lose_ion)
            if lose_info == "$$":
                lose_info = format_comp(comp_list[i], z_list[i])
            self.ax1.annotate(s=lose_info, xy=(mz_list[i], inten_list[i]), xytext=(+0, +20),
                              color='blue', textcoords='offset pixels', rotation=90, ha='center', va='bottom',
                              fontsize=11)

        self.ax1.set_ybound(lower=0)
        self.ax1.set_xlabel('m/z', fontsize=14)
        self.ax1.set_ylabel('intensity', fontsize=14)
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        self.ax1.spines['left'].set_linewidth(1.5)
        self.ax1.spines['bottom'].set_linewidth(1.5)
        self.ax1.set_title(("$MS^1(scan=" + str(self.spectrumID) + ")$"), fontsize=14)
        self.ax1.legend()
        self._fig.canvas.draw_idle()

        self.opacity = [True, False, False, True]
        self.setOpacity()

    def load_label(self):  # 转换标注数据

        # 3.标注匹配上结构，红色
        print(self.spectrumID, "family", len(self.label_info[3]))
        #  self.labels = format_labels = self.label_info[0]

        self.xy, self.mass_labels, self.mass_struct_tips, self.right_struct, self.struct_id, self.label_message, self.labels \
            = get_labels(self.label_info, self.peak_dict, self.lose_ion, self.key_with_order)

        self.label_xs, self.label_ys = format_peaks_alone(self.xy)

        # 4.衍生峰里的
        self.mass_family = get_family(self.label_info, self.peak_dict)

        # 5.用于表格下载
        self.df = pd.DataFrame({
            'M/Z': self.label_message[0],
            'Charge': self.label_message[1],
            'Isotopic Peak ': self.label_message[2],
            'Components': self.label_message[3],
            'Loss': self.label_message[4]
        })

        # 颜色生成器
        colors = mpl.cm.get_cmap("YlOrRd")  # 'viridis', 'inferno', 'plasma', 'magma'
        digit = list(map(str, range(10))) + list("ABCDEF")
        self.colors = colors(np.linspace(0, 1, len(self.right_struct) + 2))
        self.colors_str = []
        for color in self.colors:
            string = '#'
            for i in range(0, 3):
                a1 = int(color[i] * 255) // 16
                a2 = int(color[i] * 255) % 16
                string += digit[a1] + digit[a2]
            self.colors_str.append(string)
        self.colors = self.colors.tolist()
        self.colors.reverse()
        self.colors_str.reverse()

    def set_xmlInfo(self, xmlInfo):
        self.spectrumID = xmlInfo[3]
        self.xmlInfo = xmlInfo

    def updateConvertProcessBar(self, preMess):
        curr, total = preMess.split('/')
        QApplication.processEvents()  # 实时刷新界面
        self.dlgProgress.setValue(int(float(curr) * 100.0 / float(total)))
        QApplication.processEvents()  # 实时刷新界面
        self.dlgProgress.setLabelText("Transforming spectrum" + preMess)
        QApplication.processEvents()  # 实时刷新界面

    def updateDataProcessBar(self, ID):
        QApplication.processEvents()  # 实时刷新界面
        self.dataDlgProcess.setValue(int(ID * 100.0 / 6167))
        QApplication.processEvents()  # 实时刷新界面
        self.dataDlgProcess.setLabelText("Has finished " + str(ID) + "/6167       ")
        QApplication.processEvents()  # 实时刷新界面

    def infoParseProcess(self, data_info):
        self.match_result, self.label_info, self.candidate_max_num, self.candi_score = data_info

    def mxmlParseProcess(self):
        self.mzThread = mzMLWorker(xmlFileName=self.mzmlFileName)
        self.mzThread.sinXml.connect(self.set_xmlInfo)
        self.mzThread.finished.connect(self._drawTIC)
        # self.mzThread.finished.connect(self._draw3D)
        self.mzThread.start()

    def getConvertProcess(self):  # msconvert 转换文件的进度条
        self.isRaw = True
        self.dlgProgress = QProgressDialog("Transforming spectrum format...", "", 1, 100, self)
        self.dlgProgress_hori = QVBoxLayout(self.dlgProgress)

        self.dlgProgress.setWindowTitle("Transforming spectrum")
        self.dlgProgress.setWindowModality(Qt.WindowModal)  # 模态对话框
        self.dlgProgress.setCancelButton(None)  # 隐藏取消按钮
        self.dlgProgress.setAutoReset(True)  # calls reset() as soon as value() equals maximum()
        self.dlgProgress.setAutoClose(True)  # whether the dialog gets hidden by reset()
        self.dlgProgress.setMinimumDuration(0)
        self.dlgProgress.setFixedSize(280, 110)
        self.dlgProgress.setStyleSheet(pbar_str)
        self.dlgProgress.open()

        self.thread = ConvertWorker(curPath=self.curPath, rawFileName=self.rawFileName)
        self.thread.sinOut.connect(self.updateConvertProcessBar)
        self.thread.finished.connect(self.mxmlParseProcess)
        self.thread.start()

    def load_special_spectrum(self, scan_id):
        print("debug", scan_id)
        self.figFlag = 2
        self.spectrumIndex = 0
        self.spectrumID = int(scan_id)
        self.spectrumID_old = self.spectrumID
        self.right_label_page.setDisabled(False)
        self.left_box.setCurrentWidget(self.right_label_page)
        # 生成左侧按钮
        self.generate_left_side()
        # 加载数据
        # self.load_origin_peaks()

        self.spectrum, self.maxIntensity = getPeaksById(self.mzmlFileName, self.spectrumID)
        # run = pymzml.run.Reader(self.mzmlFileName)
        # self.spectrum = run[self.spectrumID]
        # 画出原始图
        self._fig.clear()
        self.orgAx = self._fig.add_subplot(1, 1, 1)
        # xs, ys = format_peaks_350(self.spectrum.peaks("centroided"))
        xs, ys = format_peaks(self.spectrum)
        self.plot_origin_peaks(xs, ys)

    def _change_spectrum(self, scan_id):
        self.spectrumID_old = self.spectrumID
        self.spectrumID = int(scan_id)
        for i in range(len(self.spectrumIDList)):
            self.scan_com_button[self.spectrumIDList[i]].layout().itemAt(0).widget().setStyleSheet(tmp_scan_label_str)
            self.scan_com_button[self.spectrumIDList[i]].layout().itemAt(1).widget().setStyleSheet(scan_icon_str)
            self.scan_com_button[self.spectrumIDList[i]].layout().itemAt(1).widget().setDisabled(True)
        self.scan_com_button[self.spectrumID].layout().itemAt(0).widget().setStyleSheet(push_scan_label_str)
        self.scan_com_button[self.spectrumID].layout().itemAt(1).widget().setDisabled(False)
        self.scan_com_button[self.spectrumID].layout().itemAt(1).widget().setStyleSheet(push_scan_icon_str)
        # 加载数据
        # self.load_origin_peaks()
        # run = pymzml.run.Reader(self.mzmlFileName)
        # self.spectrum = run[self.spectrumID]
        self.spectrum, self.maxIntensity = getPeaksById(self.mzmlFileName, self.spectrumID)
        # 画出原始图
        self._fig.clear()
        self.orgAx = self._fig.add_subplot(1, 1, 1)
        # xs, ys = format_peaks_350(self.spectrum.peaks("centroided"))
        xs, ys = format_peaks(self.spectrum)
        self.plot_origin_peaks(xs, ys)

    def dataProcess(self, wid):  # 为数据处理部分添加进度条
        for i in range(0, self.right_tic_verticalLayout.count()):
            if self.right_tic_verticalLayout.itemAt(i).widget().layout().itemAt(1).widget() == wid:
                scan_id = int(self.right_tic_verticalLayout.itemAt(i).widget().layout().itemAt(0).widget().text())
                if scan_id == self.spectrumID:
                    # QMessageBox.information(self, "Message", "请先打开原始谱，再进行下一步分析")
                    # else:
                    self.figFlag = 3
                    # self.ppm = int(self.edit_ppm.text())
                    self.load_origin_peaks()
                    self.dataDlgProcess = QAnalyseBar()
                    self.dataDlgProcess.show()
                    # save_file(spectrum.peaks("centroided"), 'data/' + str(self.spectrumID) + ".mgf")
                    self.dataThread = DataWorker(peaks = self.peaks, exp_isp=self.exp_isp, max_int=self.maxIntensity,
                                                 total_int=self.total_int, the_spectra=self.the_spectra,
                                                 dict_list=self.dict_list, the_HP=self.the_HP,
                                                 ppm=self.ppm, bound_th=self.bound_th,
                                                 bound_intensity=self.bound_intensity,
                                                 chb_dA=self.chb_dA.isChecked(),
                                                 chb_aM=self.chb_aM.isChecked(),
                                                 chb_aG=self.chb_aG.isChecked(),
                                                 min_dp=int(self.dp_min.text()),
                                                 max_dp=int(self.dp_max.text()))
                    self.dataThread.sinID.connect(self.updateDataProcessBar)
                    self.dataThread.sinDataInfo.connect(self.infoParseProcess)
                    self.dataThread.finished.connect(self._analyse_Composition)
                    self.dataThread.start()

    def add_scan(self, scan_id=None):
        if not scan_id:
            scan_id = self.add_scan_label.text()
        if scan_id != "" and int(scan_id) not in self.spectrumIDList:
            scan_id = int(scan_id)
            # tic画图
            x = self.xmlInfo[0][scan_id - 1]
            y = self.xmlInfo[1][scan_id - 1]
            xs = [x, x, x]
            ys = [0, y, 0]
            a = self.ticAx.scatter([x], [y], c='#134bb9', s=14, label='scan')
            b = self.ticAx.plot(xs, ys, c='#134bb9', linewidth=1, label="maxIso")
            c = self.ticAx.annotate(s=str(scan_id), xy=(x, y), xytext=(+0, +4),
                                    color='#0325A6', textcoords='offset points', ha='center', label='scan',
                                    fontsize=12, fontweight='bold')
            self.scan_plot[scan_id] = [a, b, c]

            # 左侧添加按钮
            self._fig.canvas.draw()

            tmp_scan = QWidget()
            tmp_scan.setFixedWidth(160)
            tmp_horizontalLayout = QHBoxLayout(tmp_scan)

            tmp_scan_label = QPushButton()
            tmp_scan_label.setText(str(scan_id))
            tmp_scan_label.setStyleSheet(tmp_scan_label_str)
            tmp_scan_label.setFixedWidth(90)
            tmp_scan_label.setObjectName("left26")
            tmp_scan_label.clicked.connect(lambda: self.load_special_spectrum(self.sender().text()))
            # tmp_scan_label.setCursor(Qt.PointingHandCursor)
            tmp_scan_btn = QPushButton("-")
            tmp_scan_btn.clicked.connect(lambda: self.sub_scan(scan_id))
            tmp_scan_btn.setFixedWidth(36)
            tmp_scan_btn.setStyleSheet(scan_btn_str)
            tmp_horizontalLayout.addWidget(tmp_scan_label)
            tmp_horizontalLayout.addWidget(tmp_scan_btn)

            self.scan_context_verticalLayout.addWidget(tmp_scan)
            self.scan_widget[scan_id] = tmp_scan
            self.add_scan_label.setText("")
            self.spectrumIDList.append(scan_id)

    def sub_scan(self, scan_id):
        for i in range(len(self.spectrumIDList)):
            if self.spectrumIDList[i] == scan_id:
                self.scan_widget[scan_id].deleteLater()
                self.spectrumIDList.pop(i)
                self.scan_plot[scan_id][0].set_visible(False)
                self.scan_plot[scan_id][1][0].set_visible(False)
                self.scan_plot[scan_id][2].set_visible(False)
                self._fig.canvas.draw()
                break

    def sub_scan_origin_fig(self, wid):
        if len(self.spectrumIDList) == 1:
            QMessageBox.information(self, "Message", "Cannot delete the spectrum being analysed")
        for i in range(0, self.right_tic_verticalLayout.count()):
            # self.scan_com_button[1003].layout().itemAt(1).widget()
            if self.right_tic_verticalLayout.itemAt(i).widget().layout().itemAt(2).widget() == wid:
                scan_id = int(self.right_tic_verticalLayout.itemAt(i).widget().layout().itemAt(0).widget().text())
                if scan_id == self.spectrumID:
                    QMessageBox.information(self, "Message", "Cannot delete the spectrum being analysed")
                else:
                    for i in range(len(self.spectrumIDList)):
                        if self.spectrumIDList[i] == scan_id:
                            self.scan_com_button[scan_id].deleteLater()
                            self.spectrumIDList.pop(i)
                            break
                break

    def change_comp(self):
        if self.figFlag < 2:
            QMessageBox.information(self, "Message", "Please loading spectra data first")
        elif self.figFlag == 2:
            QMessageBox.information(self, "Message", "Please analysing spectra data first")
        else:
            if len(self.chk_list) == 0:
                select_id, better_score = get_first_max_num(self.candi_score, self.all_key_with_order)
                for i in range(0, len(self.candi_score)):
                    if i in select_id:
                        self.chk_list.append(True)
                    else:
                        self.chk_list.append(False)
            dlgTableSize = QmyDialogSize(comps=self.all_right_struct, chk_list=self.chk_list,
                                         candi_score=self.candi_score, key_with_order=self.all_key_with_order)
            ret = dlgTableSize.exec()  # 模态方式运行对话框
            if (ret == QDialog.Accepted):
                self.chk_list = dlgTableSize.getCheckList()

            new_key_with_order = []
            tmp_acend_key = sorted(self.all_key_with_order)
            for i in range(len(self.chk_list)):
                if self.chk_list[i]:
                    new_key_with_order.append(tmp_acend_key[i])
            self.key_with_order = new_key_with_order
            self._draw_composition()

    def ppm_text_changed(self):
        self.right_anylyse.setStyleSheet(qstr)

    def apply_ppm(self):
        self.figFlag = 3

        self.ppm = int(self.edit_ppm.text())
        self.load_origin_peaks()
        self.dataDlgProcess = QAnalyseBar()
        self.dataDlgProcess.show()

        # save_file(spectrum.peaks("centroided"), 'data/' + str(self.spectrumID) + ".mgf")
        self.dataThread = DataWorker(peaks=self.peaks, exp_isp=self.exp_isp, max_int=self.maxIntensity, total_int=self.total_int,
                                     the_spectra=self.the_spectra, dict_list=self.dict_list,
                                     the_HP=self.the_HP, ppm=self.ppm, bound_th=self.bound_th,
                                     bound_intensity=self.bound_intensity,
                                     chb_dA=self.chb_dA.isChecked(),
                                     chb_aM=self.chb_aM.isChecked(),
                                     chb_aG=self.chb_aG.isChecked(),
                                     min_dp=int(self.dp_min.text()),
                                     max_dp=int(self.dp_max.text())
                                     )
        self.dataThread.sinID.connect(self.updateDataProcessBar)
        self.dataThread.sinDataInfo.connect(self.infoParseProcess)
        self.dataThread.finished.connect(self._analyse_Composition)
        self.dataThread.start()

    '''以下是一些事件'''

    def pick_event(self, event):  # 这里是tic图的响应
        series = event.artist  # 产生事件的对象

        if isinstance(series, mpl.lines.Line2D) and self.figFlag == 1:  # 折线序列
            x = event.mouseevent.xdata  # 标量数据点
            y = event.mouseevent.ydata  # 标量数据点
            index = event.ind[0]  # 索引号,是array([int32])类型,可能有多个对象被pick，只取第1个
            # startIndex, endIndex = max(0, index - 10), min(len(self.xmlInfo[0]), index + 11)
            startIndex, endIndex = max(0, index - 1), min(len(self.xmlInfo[0]), index + 2)
            maxIndex, maxIntensity = index, self.xmlInfo[1][index]
            for i in range(startIndex, endIndex):
                if self.xmlInfo[1][i] > maxIntensity and self.xmlInfo[1][i] < self.xmlInfo[1][index] * 1.2:
                    maxIndex, maxIntensity = i, self.xmlInfo[1][i]
            index = maxIndex
            info = "scan=%d, time=%.4f, total intensity=%.4f " % (index + 1, x, y)
            if (index + 1) not in self.spectrumIDList:
                self.add_scan(index + 1)

    def openTICByMzML(self):
        mzmlFileName, fileType = QFileDialog.getOpenFileName(self, "Open file", "", "*.mzML;;*.mzXML;;All Files(*)")
        if mzmlFileName != '':
            self.mzmlFileName = mzmlFileName
            self.inited_tic = False
            copy = [id for id in self.spectrumIDList]
            for i in range(0, len(copy)):
                self.sub_scan(copy[i])
            self.mxmlParseProcess()

    def openTICByRawFile(self):
        rawFileName, fileType = QFileDialog.getOpenFileName(self, "Open file", "", "*.raw;;*.RAW;;All Files(*)")

        if rawFileName != '':
            self.rawFileName = rawFileName
            self.curPath = os.path.abspath('.').replace("\\", "/") + '/mzML/'
            self.mzmlFileName = 'mzML/' + rawFileName.strip(".raw").split('/')[-1] + ".mzML"
            self.inited_tic = False
            copy = [id for id in self.spectrumIDList]
            for i in range(0, len(copy)):
                self.sub_scan(copy[i])
            self.getConvertProcess()

    def openTICByRawDir(self):
        selectDir = QFileDialog.getExistingDirectory(self, "select the raw directory", "", QFileDialog.ShowDirsOnly)

        if selectDir != '':
            self.rawFileName = selectDir
            self.curPath = os.path.abspath('.').replace("\\", "/") + '/mzML/'
            self.mzmlFileName = 'mzML/' + selectDir.split('/')[-1] + ".mzML"
            self.getConvertProcess()

    def showTIC(self):
        if self.figFlag == 0:
            QMessageBox.information(self, "Message", " Please loading spectra raw data first")
        else:
            self._drawTIC()

    def downloadTabel(self):
        if self.figFlag < 3:
            QMessageBox.information(self, "Message", "Please loading spectra data first")
        else:
            selectedDir, filtUsed = QFileDialog.getSaveFileName(self, "Download component", 'result/annotation.xlsx',
                                                                "*.xlsx;;All Files(*)")
            if selectedDir != '':
                save_com = []
                for x in self.key_with_order:
                    save_com.append(self.label_info[1][x])
                save_com = [str(x) for x in save_com]
                tmp_df = self.df
                tmp_df['Components'] = tmp_df['Components'].astype('string')
                save_df = self.df[tmp_df.Components.isin(save_com)]
                writer = pd.ExcelWriter(selectedDir)
                save_df.to_excel(writer, sheet_name='annotation', index=None)
                self.struct_df.to_excel(writer, sheet_name='components', index=None)
                writer.save()


    def setOpacity(self):
        self.showTICAction.setEnabled(self.opacity[0])
        self.changeAction.setEnabled(self.opacity[1])
        self.tableAction.setEnabled(self.opacity[2])
        self.downloadAction.setEnabled(self.opacity[3])

    def aboutUs(self):
        if platform.system() != "Windows":
            QMessageBox.about(self, "About hepParser",
                              "     Version 1.0.0(Beta)      \n      Copyright © ICT       \n"
                              "Institute of Computing Technology, Chinese Academy of Sciences")
        else:
            QMessageBox.about(self, "About hepParser",
                              "     Version 1.0.0(Beta)      \n     Copyright © ICT       \n"
                              "Institute of Computing Technology, Chinese Academy of Sciences")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.No | QMessageBox.Yes
                                     , QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # 画三维图
    def draw_one_mass(self, dict_list, mass, scanstride=1, digital=1):
        draw_data = []
        mass = np.round(mass, digital)
        for i in range(len(dict_list)):
            if i % scanstride != 0:
                continue
            if mass in dict_list[i].keys():
                one_val = dict_list[i][mass]
            else:
                one_val = 0
            draw_data.append(one_val)
        return draw_data

    def data_filter(self, data_file, mass_range, scan_range, mass_list=None):
        ret_data = [[], [], []]  # x,y,z
        if mass_list is None:
            f = open(data_file, 'rb')
            rawdata = pk.load(f)
            for i, mass in enumerate(rawdata[0]):
                if mass < mass_range[0] or mass > mass_range[1]:
                    continue
                ret_data[0].append(mass)
                ret_data[2].append(rawdata[2][i][scan_range[0]:scan_range[1]])

            ret_data[1] = rawdata[1][scan_range[0]:scan_range[1]]
            tic = rawdata[3][scan_range[0]:scan_range[1]]

        else:
            last_index = None
            for mass in mass_list:
                if mass < mass_range[0] or mass > mass_range[1]:
                    continue
                index = int(mass / SAVEMASSSTRIDE)
                if index != last_index:
                    f = open(data_file + str(index) + '.pk', 'rb')
                    rawalldata = pk.load(f)
                last_index = index
                ret_data[0].append(mass)
                z_data = self.draw_one_mass(rawalldata, mass)[scan_range[0]:scan_range[1]]
                ret_data[2].append(z_data)

            ret_data[1] = list(range(scan_range[0], scan_range[1]))

        ret_data.append(tic)
        return ret_data

    def draw_3d_plot(self, data_file, mass_range, scan_range, mass_list=None):
        # 准备数据，[0]:mass, [1]:range(1400), [2]:intensity
        alldata = self.data_filter(data_file, mass_range, scan_range, mass_list)
        # self._fig = plt.figure(figsize=(12, 8))
        ax = plt.gca(projection='3d')
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
        ax.disable_mouse_rotation()

        cursor = EventFactory(ax, alldata, mass_range, scan_range)
        plt.connect('motion_notify_event', cursor.mouse_move)
        plt.connect('button_press_event', cursor.mouse_press)
        plt.connect('button_release_event', cursor.mouse_release)
        plt.connect('scroll_event', cursor.scroll)

        self._fig.canvas.draw_idle()
        # plt.show()
        # return fig

    # 右击函数的处理
    def createContextMenu(self):
        '''''
        创建右键菜单
        '''
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QMenu(self)
        self.actionA = self.contextMenu.addAction(u'Action A')
        self.actionB = self.contextMenu.addAction(u'Action B')
        self.actionC = self.contextMenu.addAction(u'Action C')
        # 将动作与处理函数相关联
        # 这里为了简单，将所有action与同一个处理函数相关联，
        # 当然也可以将他们分别与不同函数关联，实现不同的功能
        self.actionA.triggered.connect(self.actionHandler)
        self.actionB.triggered.connect(self.actionHandler)
        self.actionC.triggered.connect(self.actionHandler)

    def showContextMenu(self, pos):
        '''''
        右键点击时调用的函数
        '''
        # 菜单显示前，将它移动到鼠标点击的位置
        print("right pick", self.pos)
        self.contextMenu.move(self.pos() + pos)
        self.contextMenu.show()

    def actionHandler(self):
        '''''
        菜单中的具体action调用的函数
        '''
        print('action handler')


if __name__ == "__main__":
    # 每个PyQt5应用都必须创建一个应用对象。sys.argv是一组命令行参数的列表
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("icon/loading.png"))
    splash.showMessage("", Qt.AlignHCenter | Qt.AlignBottom, Qt.black)
    splash.show()  # 显示启动界面
    qApp.processEvents()

    win = MainWindow()
    win.show()
    splash.finish(win)
    app.exit(app.exec_())
    dataClosed()
