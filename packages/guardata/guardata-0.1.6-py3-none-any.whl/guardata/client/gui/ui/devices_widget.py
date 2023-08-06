# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/devices_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DevicesWidget(object):
    def setupUi(self, DevicesWidget):
        DevicesWidget.setObjectName("DevicesWidget")
        DevicesWidget.resize(750, 800)
        DevicesWidget.setStyleSheet("#button_add_device {\n"
"    background-color: none;\n"
"    border: none;\n"
"    color: #2185d0;\n"
"}\n"
"\n"
"#button_add_device:hover {\n"
"    color: #0070DD;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(DevicesWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_search = QtWidgets.QLineEdit(DevicesWidget)
        self.line_edit_search.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_search.setFont(font)
        self.line_edit_search.setObjectName("line_edit_search")
        self.horizontalLayout.addWidget(self.line_edit_search)
        self.button_add_device = Button(DevicesWidget)
        self.button_add_device.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/add_to_queue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_device.setIcon(icon)
        self.button_add_device.setIconSize(QtCore.QSize(24, 24))
        self.button_add_device.setFlat(True)
        self.button_add_device.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_add_device.setObjectName("button_add_device")
        self.horizontalLayout.addWidget(self.button_add_device)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(DevicesWidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 740, 750))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.layout_content = QtWidgets.QVBoxLayout()
        self.layout_content.setObjectName("layout_content")
        self.verticalLayout_3.addLayout(self.layout_content)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spinner = SpinnerWidget(self.scrollAreaWidgetContents)
        self.spinner.setObjectName("spinner")
        self.horizontalLayout_2.addWidget(self.spinner)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_previous_page = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.button_previous_page.setStyleSheet("")
        self.button_previous_page.setObjectName("button_previous_page")
        self.horizontalLayout_3.addWidget(self.button_previous_page)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.button_next_page = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.button_next_page.setObjectName("button_next_page")
        self.horizontalLayout_3.addWidget(self.button_next_page)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 558, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)

        self.retranslateUi(DevicesWidget)
        QtCore.QMetaObject.connectSlotsByName(DevicesWidget)

    def retranslateUi(self, DevicesWidget):
        _translate = QtCore.QCoreApplication.translate
        DevicesWidget.setWindowTitle(_translate("DevicesWidget", "Form"))
        self.line_edit_search.setPlaceholderText(_translate("DevicesWidget", "TEXT_DEVICE_FILTER_PLACEHOLDER"))
        self.button_add_device.setToolTip(_translate("DevicesWidget", "TEXT_DEVICE_ADD_NEW_TOOLTIP"))
        self.button_add_device.setText(_translate("DevicesWidget", "ACTION_DEVICE_ADD_NEW"))
        self.button_previous_page.setText(_translate("DevicesWidget", "ACTION_LIST_PREVIOUS_PAGE"))
        self.button_next_page.setText(_translate("DevicesWidget", "ACTION_LIST_NEXT_PAGE"))
from guardata.client.gui.custom_widgets import Button, SpinnerWidget
from guardata.client.gui import resources_rc
