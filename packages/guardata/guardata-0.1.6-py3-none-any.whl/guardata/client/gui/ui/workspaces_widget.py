# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guardata/client/gui/forms/workspaces_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WorkspacesWidget(object):
    def setupUi(self, WorkspacesWidget):
        WorkspacesWidget.setObjectName("WorkspacesWidget")
        WorkspacesWidget.resize(625, 428)
        WorkspacesWidget.setStyleSheet("#button_goto_file, #button_add_workspace {\n"
"    background-color: none;\n"
"    border: none;\n"
"    color: #2185d0;\n"
"}\n"
"\n"
"#button_goto_file:hover, #button_add_workspace:hover {\n"
"    color: #0070DD;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(WorkspacesWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(24)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_edit_search = QtWidgets.QLineEdit(WorkspacesWidget)
        self.line_edit_search.setMinimumSize(QtCore.QSize(0, 32))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.line_edit_search.setFont(font)
        self.line_edit_search.setObjectName("line_edit_search")
        self.horizontalLayout.addWidget(self.line_edit_search)
        self.button_add_workspace = Button(WorkspacesWidget)
        self.button_add_workspace.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/add_to_queue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_workspace.setIcon(icon)
        self.button_add_workspace.setIconSize(QtCore.QSize(24, 24))
        self.button_add_workspace.setFlat(True)
        self.button_add_workspace.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_add_workspace.setObjectName("button_add_workspace")
        self.horizontalLayout.addWidget(self.button_add_workspace)
        self.button_goto_file = Button(WorkspacesWidget)
        self.button_goto_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/images/material/subdirectory_arrow_right.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_goto_file.setIcon(icon1)
        self.button_goto_file.setIconSize(QtCore.QSize(24, 24))
        self.button_goto_file.setFlat(True)
        self.button_goto_file.setProperty("color", QtGui.QColor(0, 146, 255))
        self.button_goto_file.setObjectName("button_goto_file")
        self.horizontalLayout.addWidget(self.button_goto_file)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spinner = SpinnerWidget(WorkspacesWidget)
        self.spinner.setMinimumSize(QtCore.QSize(120, 120))
        self.spinner.setMaximumSize(QtCore.QSize(120, 120))
        self.spinner.setObjectName("spinner")
        self.horizontalLayout_2.addWidget(self.spinner)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.scrollArea = QtWidgets.QScrollArea(WorkspacesWidget)
        self.scrollArea.setStyleSheet("")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 625, 150))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout_content = QtWidgets.QVBoxLayout()
        self.layout_content.setContentsMargins(0, 0, 4, 0)
        self.layout_content.setSpacing(20)
        self.layout_content.setObjectName("layout_content")
        self.verticalLayout_2.addLayout(self.layout_content)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(WorkspacesWidget)
        QtCore.QMetaObject.connectSlotsByName(WorkspacesWidget)

    def retranslateUi(self, WorkspacesWidget):
        _translate = QtCore.QCoreApplication.translate
        WorkspacesWidget.setWindowTitle(_translate("WorkspacesWidget", "Form"))
        self.line_edit_search.setPlaceholderText(_translate("WorkspacesWidget", "TEXT_WORKSPACE_FILTER_WORKSPACES_PLACEHOLDER"))
        self.button_add_workspace.setText(_translate("WorkspacesWidget", "ACTION_WORKSPACE_ADD_WORKSPACE"))
        self.button_goto_file.setText(_translate("WorkspacesWidget", "ACTION_WORKSPACE_GOTO_FILE_LINK"))
from guardata.client.gui.custom_widgets import Button, SpinnerWidget
from guardata.client.gui import resources_rc
