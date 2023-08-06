# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/create_org_second_page_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateOrgSecondPageWidget(object):
    def setupUi(self, CreateOrgSecondPageWidget):
        CreateOrgSecondPageWidget.setObjectName("CreateOrgSecondPageWidget")
        CreateOrgSecondPageWidget.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateOrgSecondPageWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(CreateOrgSecondPageWidget)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(CreateOrgSecondPageWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setWordWrap(True)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(CreateOrgSecondPageWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateOrgSecondPageWidget)

    def retranslateUi(self, CreateOrgSecondPageWidget):
        _translate = QtCore.QCoreApplication.translate
        CreateOrgSecondPageWidget.setWindowTitle(_translate("CreateOrgSecondPageWidget", "Form"))
        self.label.setText(_translate("CreateOrgSecondPageWidget", "TEXT_ORG_WIZARD_CREATE_ORG_INSTRUCTIONS"))
        self.label_2.setText(_translate("CreateOrgSecondPageWidget", "ACTION_ACCEPT_CONTRACT"))
