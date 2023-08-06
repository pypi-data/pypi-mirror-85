# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/license_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LicenseWidget(object):
    def setupUi(self, LicenseWidget):
        LicenseWidget.setObjectName("LicenseWidget")
        LicenseWidget.resize(500, 400)
        LicenseWidget.setMinimumSize(QtCore.QSize(500, 400))
        self.verticalLayout = QtWidgets.QVBoxLayout(LicenseWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_license = QtWidgets.QTextEdit(LicenseWidget)
        self.text_license.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_license.setReadOnly(True)
        self.text_license.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.text_license.setObjectName("text_license")
        self.verticalLayout.addWidget(self.text_license)

        self.retranslateUi(LicenseWidget)
        QtCore.QMetaObject.connectSlotsByName(LicenseWidget)

    def retranslateUi(self, LicenseWidget):
        _translate = QtCore.QCoreApplication.translate
        LicenseWidget.setWindowTitle(_translate("LicenseWidget", "Form"))
