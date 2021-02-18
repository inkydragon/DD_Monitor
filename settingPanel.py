# -*- coding: utf-8 -*-
"""选项菜单
"""
from PyQt5.QtWidgets import (QWidget)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class SettingDialog(QDialog):
    """弹出式选项菜单

    布局参考 https://github.com/visualfc/liteide/blob/master/liteidex/src/liteapp/optionswidget.ui
    TODO: 切换到 QML
    """

    def __init__(self):
        super(SettingDialog, self).__init__()
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setWindowTitle('偏好设置')
        self.leftList = QListWidget()
        self.rightStack = QStackedWidget()
        self.initUI()

    def initUI(self):
        # 采用左右双栏布局
        #   分类列表    |   设置区域
        mainLayout = QHBoxLayout()
        vLayout = QVBoxLayout()
        mainLayout.addWidget(self.leftList)
        mainLayout.addLayout(vLayout)
        self.setLayout(mainLayout)

        # ---- 左侧设置分类列表
        self.leftList.addItem('UI 设置')
        # TODO: 合并更多设置
        self.leftList.setMaximumWidth(150)

        # ---- 详细设置区域
        # 竖向布局
        #   + 主设置面板
        #   + 提示与按钮
        tipAndIcon = QHBoxLayout()
        vLayout.addWidget(self.rightStack)
        vLayout.addLayout(tipAndIcon)

        # 提示栏 和 按钮
        tips = QLabel('[*] 需要重启程序')
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        buttonBox.accepted.connect(self.accept)
        tipAndIcon.addWidget(tips)
        tipAndIcon.addSpacing(2)
        tipAndIcon.addWidget(buttonBox)

        # 详细设置页
        w = QWidget()
        wLay = QVBoxLayout()

        # 高 DPI
        # advanced
        g1 = QGroupBox('High DPI [*]')
        label_g1 = QLabel('开启高 DPI 适配')
        self.checkbox_enable_high_dpi = QCheckBox()
        lay_g1 = QFormLayout()
        lay_g1.addRow(self.checkbox_enable_high_dpi, label_g1)
        g1.setLayout(lay_g1)
        wLay.addWidget(g1)

        w.setLayout(wLay)
        self.rightStack.addWidget(w)


# 组件单独测试
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = SettingDialog()
    dialog.show()
    sys.exit(app.exec())
