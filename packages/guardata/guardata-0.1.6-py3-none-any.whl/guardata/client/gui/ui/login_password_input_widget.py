# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/login_password_input_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginPasswordInputWidget(object):
    def setupUi(self, LoginPasswordInputWidget):
        LoginPasswordInputWidget.setObjectName("LoginPasswordInputWidget")
        LoginPasswordInputWidget.resize(350, 176)
        LoginPasswordInputWidget.setStyleSheet("#label_instructions {\n"
"    color: #333333;\n"
"}\n"
"\n"
"#button_login, #button_back {\n"
"    text-transform: uppercase;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(LoginPasswordInputWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 10)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_instructions = QtWidgets.QLabel(LoginPasswordInputWidget)
        self.label_instructions.setText("")
        self.label_instructions.setWordWrap(True)
        self.label_instructions.setObjectName("label_instructions")
        self.verticalLayout.addWidget(self.label_instructions)
        self.line_edit_password = QtWidgets.QLineEdit(LoginPasswordInputWidget)
        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_password.setObjectName("line_edit_password")
        self.verticalLayout.addWidget(self.line_edit_password)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_back = QtWidgets.QPushButton(LoginPasswordInputWidget)
        self.button_back.setObjectName("button_back")
        self.horizontalLayout.addWidget(self.button_back)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.button_login = QtWidgets.QPushButton(LoginPasswordInputWidget)
        self.button_login.setObjectName("button_login")
        self.horizontalLayout.addWidget(self.button_login)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)

        self.retranslateUi(LoginPasswordInputWidget)
        QtCore.QMetaObject.connectSlotsByName(LoginPasswordInputWidget)

    def retranslateUi(self, LoginPasswordInputWidget):
        _translate = QtCore.QCoreApplication.translate
        LoginPasswordInputWidget.setWindowTitle(_translate("LoginPasswordInputWidget", "Form"))
        self.button_back.setText(_translate("LoginPasswordInputWidget", "ACTION_BACK"))
        self.button_login.setText(_translate("LoginPasswordInputWidget", "ACTION_LOG_IN"))
