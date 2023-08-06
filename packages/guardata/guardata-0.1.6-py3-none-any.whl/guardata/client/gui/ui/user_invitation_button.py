# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/user_invitation_button.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UserInvitationButton(object):
    def setupUi(self, UserInvitationButton):
        UserInvitationButton.setObjectName("UserInvitationButton")
        UserInvitationButton.resize(200, 185)
        UserInvitationButton.setMinimumSize(QtCore.QSize(200, 185))
        UserInvitationButton.setMaximumSize(QtCore.QSize(200, 185))
        UserInvitationButton.setStyleSheet("#label_addr, label_email {\n"
"    color: #999999;\n"
"}\n"
"\n"
"#UserInvitationButton, #widget {\n"
"    background-color: #FFFFFF;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"#button_cancel {\n"
"    border: none;\n"
"    background: none;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(UserInvitationButton)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(UserInvitationButton)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(10, 5, 10, 5)
        self.verticalLayout_2.setSpacing(8)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.button_cancel = Button(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_cancel.sizePolicy().hasHeightForWidth())
        self.button_cancel.setSizePolicy(sizePolicy)
        self.button_cancel.setMinimumSize(QtCore.QSize(32, 32))
        self.button_cancel.setMaximumSize(QtCore.QSize(32, 32))
        self.button_cancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_cancel.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/block.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_cancel.setIcon(icon)
        self.button_cancel.setIconSize(QtCore.QSize(32, 32))
        self.button_cancel.setFlat(True)
        self.button_cancel.setProperty("color", QtGui.QColor(244, 67, 54))
        self.button_cancel.setProperty("hover_color", QtGui.QColor(249, 33, 36))
        self.button_cancel.setObjectName("button_cancel")
        self.horizontalLayout_3.addWidget(self.button_cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(35, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label_icon = IconLabel(self.widget)
        self.label_icon.setMinimumSize(QtCore.QSize(48, 48))
        self.label_icon.setMaximumSize(QtCore.QSize(48, 48))
        self.label_icon.setText("")
        self.label_icon.setPixmap(QtGui.QPixmap(":/icons/images/material/help.svg"))
        self.label_icon.setScaledContents(True)
        self.label_icon.setProperty("color", QtGui.QColor(140, 140, 150))
        self.label_icon.setObjectName("label_icon")
        self.horizontalLayout.addWidget(self.label_icon)
        spacerItem3 = QtWidgets.QSpacerItem(35, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.label_email = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_email.setFont(font)
        self.label_email.setText("")
        self.label_email.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_email.setFont(font)
        self.label_email.setObjectName("label_email")
        self.verticalLayout_2.addWidget(self.label_email)
        spacerItem4 = QtWidgets.QSpacerItem(18, 16, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem5 = QtWidgets.QSpacerItem(35, 18, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.button_greet = QtWidgets.QPushButton(self.widget)
        self.button_greet.setObjectName("button_greet")
        self.horizontalLayout_2.addWidget(self.button_greet)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(UserInvitationButton)
        QtCore.QMetaObject.connectSlotsByName(UserInvitationButton)

    def retranslateUi(self, UserInvitationButton):
        _translate = QtCore.QCoreApplication.translate
        UserInvitationButton.setWindowTitle(_translate("UserInvitationButton", "Form"))
        self.button_cancel.setToolTip(_translate("UserInvitationButton", "ACTION_CANCEL_USER_INVITATION_TOOLTIP"))
        self.button_greet.setText(_translate("UserInvitationButton", "ACTION_GREET_USER"))
from guardata.client.gui.custom_widgets import Button, IconLabel
from guardata.client.gui import resources_rc
