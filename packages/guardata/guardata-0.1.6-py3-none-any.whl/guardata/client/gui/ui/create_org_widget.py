# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/create_org_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateOrgWidget(object):
    def setupUi(self, CreateOrgWidget):
        CreateOrgWidget.setObjectName("CreateOrgWidget")
        CreateOrgWidget.resize(558, 395)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateOrgWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(CreateOrgWidget)
        self.label.setMinimumSize(QtCore.QSize(188, 121))
        self.label.setMaximumSize(QtCore.QSize(188, 121))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logos/images/logos/guardata.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.widget = QtWidgets.QWidget(CreateOrgWidget)
        self.widget.setMinimumSize(QtCore.QSize(350, 200))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(20, 40, 20, 40)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("main_layout")
        self.verticalLayout_3.addLayout(self.main_layout)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_previous = QtWidgets.QPushButton(CreateOrgWidget)
        self.button_previous.setFlat(True)
        self.button_previous.setObjectName("button_previous")
        self.horizontalLayout_2.addWidget(self.button_previous)
        self.button_validate = QtWidgets.QPushButton(CreateOrgWidget)
        self.button_validate.setFlat(True)
        self.button_validate.setObjectName("button_validate")
        self.horizontalLayout_2.addWidget(self.button_validate)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(CreateOrgWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateOrgWidget)

    def retranslateUi(self, CreateOrgWidget):
        _translate = QtCore.QCoreApplication.translate
        CreateOrgWidget.setWindowTitle(_translate("CreateOrgWidget", "Form"))
        self.button_previous.setText(_translate("CreateOrgWidget", "ACTION_PREVIOUS"))
        self.button_validate.setText(_translate("CreateOrgWidget", "ACTION_NEXT"))
from guardata.client.gui import resources_rc
