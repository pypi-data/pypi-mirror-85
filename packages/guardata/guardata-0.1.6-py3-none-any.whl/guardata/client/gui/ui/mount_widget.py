# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/mount_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MountWidget(object):
    def setupUi(self, MountWidget):
        MountWidget.setObjectName("MountWidget")
        MountWidget.resize(533, 407)
        self.verticalLayout = QtWidgets.QVBoxLayout(MountWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_content = QtWidgets.QVBoxLayout()
        self.layout_content.setContentsMargins(0, 0, 0, 0)
        self.layout_content.setSpacing(0)
        self.layout_content.setObjectName("layout_content")
        self.verticalLayout.addLayout(self.layout_content)

        self.retranslateUi(MountWidget)
        QtCore.QMetaObject.connectSlotsByName(MountWidget)

    def retranslateUi(self, MountWidget):
        _translate = QtCore.QCoreApplication.translate
        MountWidget.setWindowTitle(_translate("MountWidget", "Form"))
