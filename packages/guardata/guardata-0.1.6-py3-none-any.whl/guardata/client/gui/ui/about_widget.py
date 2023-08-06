# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/about_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutWidget(object):
    def setupUi(self, AboutWidget):
        AboutWidget.setObjectName("AboutWidget")
        AboutWidget.resize(532, 271)
        self.verticalLayout = QtWidgets.QVBoxLayout(AboutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(AboutWidget)
        self.label.setMinimumSize(QtCore.QSize(348, 60))
        self.label.setMaximumSize(QtCore.QSize(348, 60))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logos/images/logos/guardata_vert.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_version = QtWidgets.QLabel(AboutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_version.setFont(font)
        self.label_version.setText("")
        self.label_version.setAlignment(QtCore.Qt.AlignCenter)
        self.label_version.setObjectName("label_version")
        self.verticalLayout.addWidget(self.label_version)
        self.label_2 = QtWidgets.QLabel(AboutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(AboutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)

        self.retranslateUi(AboutWidget)
        QtCore.QMetaObject.connectSlotsByName(AboutWidget)

    def retranslateUi(self, AboutWidget):
        _translate = QtCore.QCoreApplication.translate
        AboutWidget.setWindowTitle(_translate("AboutWidget", "Form"))
        self.label_2.setText(_translate("AboutWidget", "TEXT_GUARDATA_DEVELOPMENT_INFO"))
        self.label_3.setText(_translate("AboutWidget", "TEXT_ATTRIBUTE_LIC"))
from guardata.client.gui import resources_rc
