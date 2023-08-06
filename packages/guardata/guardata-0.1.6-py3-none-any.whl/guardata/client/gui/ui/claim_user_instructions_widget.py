# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/claim_user_instructions_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClaimUserInstructionsWidget(object):
    def setupUi(self, ClaimUserInstructionsWidget):
        ClaimUserInstructionsWidget.setObjectName("ClaimUserInstructionsWidget")
        ClaimUserInstructionsWidget.resize(400, 64)
        self.verticalLayout = QtWidgets.QVBoxLayout(ClaimUserInstructionsWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(ClaimUserInstructionsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setLineWidth(0)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_start = QtWidgets.QPushButton(ClaimUserInstructionsWidget)
        self.button_start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_start.setObjectName("button_start")
        self.horizontalLayout.addWidget(self.button_start)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ClaimUserInstructionsWidget)
        QtCore.QMetaObject.connectSlotsByName(ClaimUserInstructionsWidget)

    def retranslateUi(self, ClaimUserInstructionsWidget):
        _translate = QtCore.QCoreApplication.translate
        ClaimUserInstructionsWidget.setWindowTitle(_translate("ClaimUserInstructionsWidget", "Form"))
        self.label.setText(_translate("ClaimUserInstructionsWidget", "TEXT_CLAIM_USER_INSTRUCTIONS"))
        self.button_start.setText(_translate("ClaimUserInstructionsWidget", "ACTION_START"))
