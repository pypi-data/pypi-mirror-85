# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/greet_device_instructions_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GreetDeviceInstructionsWidget(object):
    def setupUi(self, GreetDeviceInstructionsWidget):
        GreetDeviceInstructionsWidget.setObjectName("GreetDeviceInstructionsWidget")
        GreetDeviceInstructionsWidget.resize(400, 259)
        self.verticalLayout = QtWidgets.QVBoxLayout(GreetDeviceInstructionsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_instructions = QtWidgets.QLabel(GreetDeviceInstructionsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_instructions.sizePolicy().hasHeightForWidth())
        self.label_instructions.setSizePolicy(sizePolicy)
        self.label_instructions.setTextFormat(QtCore.Qt.RichText)
        self.label_instructions.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label_instructions.setWordWrap(True)
        self.label_instructions.setObjectName("label_instructions")
        self.verticalLayout.addWidget(self.label_instructions)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_send_email = QtWidgets.QPushButton(GreetDeviceInstructionsWidget)
        self.button_send_email.setObjectName("button_send_email")
        self.horizontalLayout_2.addWidget(self.button_send_email)
        self.button_copy_addr = QtWidgets.QPushButton(GreetDeviceInstructionsWidget)
        self.button_copy_addr.setObjectName("button_copy_addr")
        self.horizontalLayout_2.addWidget(self.button_copy_addr)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label = QtWidgets.QLabel(GreetDeviceInstructionsWidget)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_start = QtWidgets.QPushButton(GreetDeviceInstructionsWidget)
        self.button_start.setMaximumWidth(120)
        self.button_start.setObjectName("button_start")
        self.horizontalLayout.addWidget(self.button_start)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(GreetDeviceInstructionsWidget)
        QtCore.QMetaObject.connectSlotsByName(GreetDeviceInstructionsWidget)

    def retranslateUi(self, GreetDeviceInstructionsWidget):
        _translate = QtCore.QCoreApplication.translate
        GreetDeviceInstructionsWidget.setWindowTitle(_translate("GreetDeviceInstructionsWidget", "Form"))
        self.label_instructions.setText(_translate("GreetDeviceInstructionsWidget", "TEXT_GREET_DEVICE_INSTRUCTIONS_email"))
        self.button_send_email.setText(_translate("GreetDeviceInstructionsWidget", "ACTION_SEND_EMAIL"))
        self.button_copy_addr.setText(_translate("GreetDeviceInstructionsWidget", "ACTION_COPY_ADDR"))
        self.label.setText(_translate("GreetDeviceInstructionsWidget", "TEXT_GREET_DEVICE_INSTRUCTIONS_START"))
        self.button_start.setText(_translate("GreetDeviceInstructionsWidget", "ACTION_START"))
