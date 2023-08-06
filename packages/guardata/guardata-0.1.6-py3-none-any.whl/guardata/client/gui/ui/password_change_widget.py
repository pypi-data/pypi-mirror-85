# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/password_change_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PasswordChangeWidget(object):
    def setupUi(self, PasswordChangeWidget):
        PasswordChangeWidget.setObjectName("PasswordChangeWidget")
        PasswordChangeWidget.resize(400, 240)
        self.verticalLayout = QtWidgets.QVBoxLayout(PasswordChangeWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(PasswordChangeWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(PasswordChangeWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(PasswordChangeWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.line_edit_old_password = QtWidgets.QLineEdit(PasswordChangeWidget)
        self.line_edit_old_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_old_password.setObjectName("line_edit_old_password")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line_edit_old_password)
        self.line_edit_password = QtWidgets.QLineEdit(PasswordChangeWidget)
        self.line_edit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_password.setObjectName("line_edit_password")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.line_edit_password)
        self.line_edit_password_check = QtWidgets.QLineEdit(PasswordChangeWidget)
        self.line_edit_password_check.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_password_check.setObjectName("line_edit_password_check")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.line_edit_password_check)
        self.verticalLayout.addLayout(self.formLayout)
        self.layout_password_strength = QtWidgets.QHBoxLayout()
        self.layout_password_strength.setContentsMargins(0, -1, 0, -1)
        self.layout_password_strength.setObjectName("layout_password_strength")
        self.verticalLayout.addLayout(self.layout_password_strength)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_change = QtWidgets.QPushButton(PasswordChangeWidget)
        self.button_change.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_change.setObjectName("button_change")
        self.horizontalLayout_2.addWidget(self.button_change)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(PasswordChangeWidget)
        QtCore.QMetaObject.connectSlotsByName(PasswordChangeWidget)

    def retranslateUi(self, PasswordChangeWidget):
        _translate = QtCore.QCoreApplication.translate
        PasswordChangeWidget.setWindowTitle(_translate("PasswordChangeWidget", "Form"))
        self.label_2.setText(_translate("PasswordChangeWidget", "TEXT_LABEL_PASSWORD_OLD"))
        self.label_3.setText(_translate("PasswordChangeWidget", "TEXT_LABEL_PASSWORD"))
        self.label_4.setText(_translate("PasswordChangeWidget", "TEXT_LABEL_PASSWORD_CONFIRMATION"))
        self.button_change.setText(_translate("PasswordChangeWidget", "ACTION_CHANGE_PASSWORD"))
