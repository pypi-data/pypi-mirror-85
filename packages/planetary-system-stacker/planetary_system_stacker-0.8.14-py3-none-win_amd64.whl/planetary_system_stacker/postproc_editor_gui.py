# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'postproc_editor_gui.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_postproc_editor(object):
    def setupUi(self, postproc_editor):
        postproc_editor.setObjectName("postproc_editor")
        postproc_editor.resize(865, 682)
        postproc_editor.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        postproc_editor.setFrameShape(QtWidgets.QFrame.Panel)
        postproc_editor.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridLayout = QtWidgets.QGridLayout(postproc_editor)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 1, 1, 1)
        self.SharpeningLayerWidget_1 = QtWidgets.QLabel(postproc_editor)
        self.SharpeningLayerWidget_1.setText("")
        self.SharpeningLayerWidget_1.setObjectName("SharpeningLayerWidget_1")
        self.gridLayout.addWidget(self.SharpeningLayerWidget_1, 1, 1, 1, 1)
        self.SharpeningLayerWidget_2 = QtWidgets.QLabel(postproc_editor)
        self.SharpeningLayerWidget_2.setText("")
        self.SharpeningLayerWidget_2.setObjectName("SharpeningLayerWidget_2")
        self.gridLayout.addWidget(self.SharpeningLayerWidget_2, 2, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_message = QtWidgets.QLabel(postproc_editor)
        self.label_message.setText("")
        self.label_message.setObjectName("label_message")
        self.horizontalLayout.addWidget(self.label_message)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonBox = QtWidgets.QDialogButtonBox(postproc_editor)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 7, 0, 1, 2)
        self.pushButton_add_layer = QtWidgets.QPushButton(postproc_editor)
        self.pushButton_add_layer.setObjectName("pushButton_add_layer")
        self.gridLayout.addWidget(self.pushButton_add_layer, 0, 1, 1, 1)
        self.VersionManagerWidget = QtWidgets.QLabel(postproc_editor)
        self.VersionManagerWidget.setText("")
        self.VersionManagerWidget.setObjectName("VersionManagerWidget")
        self.gridLayout.addWidget(self.VersionManagerWidget, 6, 1, 1, 1)
        self.SharpeningLayerWidget_3 = QtWidgets.QLabel(postproc_editor)
        self.SharpeningLayerWidget_3.setText("")
        self.SharpeningLayerWidget_3.setObjectName("SharpeningLayerWidget_3")
        self.gridLayout.addWidget(self.SharpeningLayerWidget_3, 3, 1, 1, 1)
        self.SharpeningLayerWidget_4 = QtWidgets.QLabel(postproc_editor)
        self.SharpeningLayerWidget_4.setText("")
        self.SharpeningLayerWidget_4.setObjectName("SharpeningLayerWidget_4")
        self.gridLayout.addWidget(self.SharpeningLayerWidget_4, 4, 1, 1, 1)
        self.FrameViewer = QtWidgets.QLabel(postproc_editor)
        self.FrameViewer.setText("")
        self.FrameViewer.setAlignment(QtCore.Qt.AlignCenter)
        self.FrameViewer.setObjectName("FrameViewer")
        self.gridLayout.addWidget(self.FrameViewer, 0, 0, 7, 1)
        self.gridLayout.setColumnStretch(0, 1)

        self.retranslateUi(postproc_editor)
        QtCore.QMetaObject.connectSlotsByName(postproc_editor)

    def retranslateUi(self, postproc_editor):
        _translate = QtCore.QCoreApplication.translate
        postproc_editor.setWindowTitle(_translate("postproc_editor", "Frame"))
        self.buttonBox.setToolTip(_translate("postproc_editor", "Press \"OK\" to save the selected version and exit, or \"Cancel\" to discard changes"))
        self.pushButton_add_layer.setToolTip(_translate("postproc_editor", "Add a sharpening layer (up to four)"))
        self.pushButton_add_layer.setText(_translate("postproc_editor", "Add correction layer"))


