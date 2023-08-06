# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/login_no_devices_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginNoDevicesWidget(object):
    def setupUi(self, LoginNoDevicesWidget):
        LoginNoDevicesWidget.setObjectName("LoginNoDevicesWidget")
        LoginNoDevicesWidget.resize(400, 138)
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginNoDevicesWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_no_device = QtWidgets.QLabel(LoginNoDevicesWidget)
        self.label_no_device.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_no_device.setWordWrap(True)
        self.label_no_device.setObjectName("label_no_device")
        self.verticalLayout.addWidget(self.label_no_device)
        self.button_create_org = QtWidgets.QPushButton(LoginNoDevicesWidget)
        self.button_create_org.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.button_create_org.setObjectName("button_create_org")
        self.verticalLayout.addWidget(self.button_create_org)
        self.button_join_org = QtWidgets.QPushButton(LoginNoDevicesWidget)
        self.button_join_org.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.button_join_org.setObjectName("button_join_org")
        self.verticalLayout.addWidget(self.button_join_org)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(LoginNoDevicesWidget)
        QtCore.QMetaObject.connectSlotsByName(LoginNoDevicesWidget)

    def retranslateUi(self, LoginNoDevicesWidget):
        _translate = QtCore.QCoreApplication.translate
        LoginNoDevicesWidget.setWindowTitle(_translate("LoginNoDevicesWidget", "Form"))
        self.label_no_device.setText(_translate("LoginNoDevicesWidget", "TEXT_LOGIN_NO_AVAILABLE_DEVICE"))
        self.button_create_org.setText(_translate("LoginNoDevicesWidget", "ACTION_MAIN_MENU_CREATE_ORGANIZATION"))
        self.button_join_org.setText(_translate("LoginNoDevicesWidget", "ACTION_MAIN_MENU_JOIN_ORGANIZATION"))
