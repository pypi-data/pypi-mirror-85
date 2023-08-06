# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/users_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UsersWidget(object):
    def setupUi(self, UsersWidget):
        UsersWidget.setObjectName("UsersWidget")
        UsersWidget.resize(760, 719)
        UsersWidget.setStyleSheet("#button_add_user {\n"
"    background-color: none;\n"
"    border: none;\n"
"    color: #2185d0;\n"
"}\n"
"\n"
"#button_add_user:hover {\n"
"    color: #0070DD;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(UsersWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_search = QtWidgets.QLineEdit(UsersWidget)
        self.line_edit_search.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_search.setFont(font)
        self.line_edit_search.setText("")
        self.line_edit_search.setObjectName("line_edit_search")
        self.horizontalLayout.addWidget(self.line_edit_search)
        self.button_add_user = Button(UsersWidget)
        self.button_add_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/person_add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_user.setIcon(icon)
        self.button_add_user.setIconSize(QtCore.QSize(24, 24))
        self.button_add_user.setFlat(True)
        self.button_add_user.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_add_user.setObjectName("button_add_user")
        self.horizontalLayout.addWidget(self.button_add_user)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.scrollArea = QtWidgets.QScrollArea(UsersWidget)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 760, 615))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout_content = QtWidgets.QVBoxLayout()
        self.layout_content.setContentsMargins(0, 0, 4, -1)
        self.layout_content.setSpacing(20)
        self.layout_content.setObjectName("layout_content")
        self.verticalLayout_2.addLayout(self.layout_content)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spinner = SpinnerWidget(self.scrollAreaWidgetContents)
        self.spinner.setObjectName("spinner")
        self.horizontalLayout_2.addWidget(self.spinner)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.button_previous_page = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.button_previous_page.setObjectName("button_previous_page")
        self.horizontalLayout_3.addWidget(self.button_previous_page)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.button_next_page = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.button_next_page.setObjectName("button_next_page")
        self.horizontalLayout_3.addWidget(self.button_next_page)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 440, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem5)

        self.retranslateUi(UsersWidget)
        QtCore.QMetaObject.connectSlotsByName(UsersWidget)

    def retranslateUi(self, UsersWidget):
        _translate = QtCore.QCoreApplication.translate
        UsersWidget.setWindowTitle(_translate("UsersWidget", "Form"))
        self.line_edit_search.setPlaceholderText(_translate("UsersWidget", "TEXT_USERS_FILTER_USERS_PLACEHOLDER"))
        self.button_add_user.setText(_translate("UsersWidget", "ACTION_USER_INVITE_USER"))
        self.button_previous_page.setText(_translate("UsersWidget", "ACTION_LIST_PREVIOUS_PAGE"))
        self.button_next_page.setText(_translate("UsersWidget", "ACTION_LIST_NEXT_PAGE"))
from guardata.client.gui.custom_widgets import Button, SpinnerWidget
from guardata.client.gui import resources_rc
