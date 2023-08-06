# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/create_org_first_page_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateOrgFirstPageWidget(object):
    def setupUi(self, CreateOrgFirstPageWidget):
        CreateOrgFirstPageWidget.setObjectName("CreateOrgFirstPageWidget")
        CreateOrgFirstPageWidget.resize(399, 207)
        self.verticalLayout = QtWidgets.QVBoxLayout(CreateOrgFirstPageWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(CreateOrgFirstPageWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.radio_create_org = QtWidgets.QRadioButton(CreateOrgFirstPageWidget)
        self.radio_create_org.setObjectName("radio_create_org")
        self.verticalLayout.addWidget(self.radio_create_org)
        self.radio_bootstrap_org = QtWidgets.QRadioButton(CreateOrgFirstPageWidget)
        self.radio_bootstrap_org.setObjectName("radio_bootstrap_org")
        self.verticalLayout.addWidget(self.radio_bootstrap_org)

        self.retranslateUi(CreateOrgFirstPageWidget)
        QtCore.QMetaObject.connectSlotsByName(CreateOrgFirstPageWidget)

    def retranslateUi(self, CreateOrgFirstPageWidget):
        _translate = QtCore.QCoreApplication.translate
        CreateOrgFirstPageWidget.setWindowTitle(_translate("CreateOrgFirstPageWidget", "Form"))
        self.label.setText(_translate("CreateOrgFirstPageWidget", "TEXT_ORG_WIZARD_CHOICE_INSTRUCTIONS"))
        self.radio_create_org.setText(_translate("CreateOrgFirstPageWidget", "TEXT_ORG_WIZARD_CREATE_FROM_SCRATCH"))
        self.radio_bootstrap_org.setText(_translate("CreateOrgFirstPageWidget", "TEXT_ORG_WIZARD_ALREADY_HAS_URL"))
