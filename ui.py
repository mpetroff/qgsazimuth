# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Wed Nov 18 14:28:29 2009
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ui(object):
    def setupUi(self, ui):
        ui.setObjectName("ui")
        ui.resize(537, 576)
        self.verticalLayout_10 = QtGui.QVBoxLayout(ui)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label = QtGui.QLabel(ui)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout_13.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(56, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem)
        self.comboBox = QtGui.QComboBox(ui)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_13.addWidget(self.comboBox)
        self.verticalLayout_10.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_3 = QtGui.QGroupBox(ui)
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_8 = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_8.setEnabled(True)
        self.radioButton_8.setChecked(True)
        self.radioButton_8.setObjectName("radioButton_8")
        self.verticalLayout.addWidget(self.radioButton_8)
        self.radioButton_7 = QtGui.QRadioButton(self.groupBox_3)
        self.radioButton_7.setEnabled(True)
        self.radioButton_7.setCheckable(True)
        self.radioButton_7.setChecked(False)
        self.radioButton_7.setObjectName("radioButton_7")
        self.verticalLayout.addWidget(self.radioButton_7)
        self.horizontalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(ui)
        self.groupBox_4.setEnabled(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButton_11 = QtGui.QRadioButton(self.groupBox_4)
        self.radioButton_11.setEnabled(True)
        self.radioButton_11.setCheckable(True)
        self.radioButton_11.setChecked(True)
        self.radioButton_11.setObjectName("radioButton_11")
        self.verticalLayout_3.addWidget(self.radioButton_11)
        self.radioButton_12 = QtGui.QRadioButton(self.groupBox_4)
        self.radioButton_12.setEnabled(True)
        self.radioButton_12.setChecked(False)
        self.radioButton_12.setObjectName("radioButton_12")
        self.verticalLayout_3.addWidget(self.radioButton_12)
        self.horizontalLayout_3.addWidget(self.groupBox_4)
        self.verticalLayout_9.addLayout(self.horizontalLayout_3)
        self.groupBox = QtGui.QGroupBox(ui)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_6.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_6.addWidget(self.lineEdit)
        self.pushButton_8 = QtGui.QPushButton(self.groupBox)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_6.addWidget(self.pushButton_8)
        spacerItem2 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        spacerItem3 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.lineEdit_2 = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_7.addWidget(self.lineEdit_2)
        spacerItem4 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem4)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_8.addWidget(self.label_4)
        spacerItem5 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.lineEdit_3 = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_3.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_8.addWidget(self.lineEdit_3)
        spacerItem6 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.verticalLayout_9.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(ui)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        spacerItem7 = QtGui.QSpacerItem(2, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem7)
        self.lineEdit_7 = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_7.sizePolicy().hasHeightForWidth())
        self.lineEdit_7.setSizePolicy(sizePolicy)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_9.addWidget(self.lineEdit_7)
        self.pushButton_10 = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_10.setEnabled(False)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_9.addWidget(self.pushButton_10)
        spacerItem8 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem8)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_10.addWidget(self.label_9)
        self.lineEdit_8 = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_8.sizePolicy().hasHeightForWidth())
        self.lineEdit_8.setSizePolicy(sizePolicy)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.horizontalLayout_10.addWidget(self.lineEdit_8)
        spacerItem9 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem9)
        self.verticalLayout_8.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_11.addWidget(self.label_10)
        spacerItem10 = QtGui.QSpacerItem(6, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem10)
        self.lineEdit_9 = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_9.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_9.sizePolicy().hasHeightForWidth())
        self.lineEdit_9.setSizePolicy(sizePolicy)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.horizontalLayout_11.addWidget(self.lineEdit_9)
        spacerItem11 = QtGui.QSpacerItem(15, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem11)
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_11.addWidget(self.pushButton)
        spacerItem12 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem12)
        self.verticalLayout_8.addLayout(self.horizontalLayout_11)
        self.verticalLayout_9.addWidget(self.groupBox_2)
        self.horizontalLayout_12.addLayout(self.verticalLayout_9)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBox_5 = QtGui.QGroupBox(ui)
        self.groupBox_5.setEnabled(True)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.radioButton_14 = QtGui.QRadioButton(self.groupBox_5)
        self.radioButton_14.setEnabled(True)
        self.radioButton_14.setCheckable(True)
        self.radioButton_14.setChecked(True)
        self.radioButton_14.setObjectName("radioButton_14")
        self.verticalLayout_4.addWidget(self.radioButton_14)
        self.radioButton_13 = QtGui.QRadioButton(self.groupBox_5)
        self.radioButton_13.setEnabled(False)
        self.radioButton_13.setChecked(False)
        self.radioButton_13.setObjectName("radioButton_13")
        self.verticalLayout_4.addWidget(self.radioButton_13)
        self.radioButton_15 = QtGui.QRadioButton(self.groupBox_5)
        self.radioButton_15.setEnabled(False)
        self.radioButton_15.setChecked(False)
        self.radioButton_15.setObjectName("radioButton_15")
        self.verticalLayout_4.addWidget(self.radioButton_15)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem13 = QtGui.QSpacerItem(17, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem13)
        self.checkBox = QtGui.QCheckBox(self.groupBox_5)
        self.checkBox.setEnabled(False)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_5.addWidget(self.checkBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem14 = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem14)
        self.label_6 = QtGui.QLabel(self.groupBox_5)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.spinBox = QtGui.QSpinBox(self.groupBox_5)
        self.spinBox.setEnabled(False)
        self.spinBox.setMaximum(9999)
        self.spinBox.setProperty("value", QtCore.QVariant(2010))
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_4.addWidget(self.spinBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.verticalLayout_6.addWidget(self.groupBox_5)
        self.groupBox_6 = QtGui.QGroupBox(ui)
        self.groupBox_6.setEnabled(True)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.radioButton_17 = QtGui.QRadioButton(self.groupBox_6)
        self.radioButton_17.setEnabled(True)
        self.radioButton_17.setCheckable(True)
        self.radioButton_17.setChecked(True)
        self.radioButton_17.setObjectName("radioButton_17")
        self.verticalLayout_5.addWidget(self.radioButton_17)
        self.radioButton_16 = QtGui.QRadioButton(self.groupBox_6)
        self.radioButton_16.setEnabled(False)
        self.radioButton_16.setChecked(False)
        self.radioButton_16.setObjectName("radioButton_16")
        self.verticalLayout_5.addWidget(self.radioButton_16)
        self.radioButton_18 = QtGui.QRadioButton(self.groupBox_6)
        self.radioButton_18.setEnabled(False)
        self.radioButton_18.setChecked(False)
        self.radioButton_18.setObjectName("radioButton_18")
        self.verticalLayout_5.addWidget(self.radioButton_18)
        self.verticalLayout_6.addWidget(self.groupBox_6)
        self.horizontalLayout_12.addLayout(self.verticalLayout_6)
        self.verticalLayout_10.addLayout(self.horizontalLayout_12)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidget = QtGui.QTableWidget(ui)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_2 = QtGui.QPushButton(ui)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        spacerItem15 = QtGui.QSpacerItem(20, 28, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem15)
        self.pushButton_4 = QtGui.QPushButton(ui)
        self.pushButton_4.setEnabled(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_5 = QtGui.QPushButton(ui)
        self.pushButton_5.setEnabled(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_2.addWidget(self.pushButton_5)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_5 = QtGui.QLabel(ui)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_14.addWidget(self.label_5)
        self.lineEdit_4 = QtGui.QLineEdit(ui)
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_14.addWidget(self.lineEdit_4)
        self.pushButton_11 = QtGui.QPushButton(ui)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())
        self.pushButton_11.setSizePolicy(sizePolicy)
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_14.addWidget(self.pushButton_11)
        self.verticalLayout_10.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_7 = QtGui.QPushButton(ui)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_2.addWidget(self.pushButton_7)
        self.pushButton_6 = QtGui.QPushButton(ui)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.pushButton_3 = QtGui.QPushButton(ui)
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_9 = QtGui.QPushButton(ui)
        self.pushButton_9.setEnabled(False)
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_2.addWidget(self.pushButton_9)
        self.verticalLayout_10.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ui)
        QtCore.QMetaObject.connectSlotsByName(ui)
        ui.setTabOrder(self.comboBox, self.lineEdit)
        ui.setTabOrder(self.lineEdit, self.lineEdit_2)
        ui.setTabOrder(self.lineEdit_2, self.lineEdit_3)
        ui.setTabOrder(self.lineEdit_3, self.radioButton_8)
        ui.setTabOrder(self.radioButton_8, self.radioButton_7)
        ui.setTabOrder(self.radioButton_7, self.radioButton_12)
        ui.setTabOrder(self.radioButton_12, self.lineEdit_7)
        ui.setTabOrder(self.lineEdit_7, self.lineEdit_8)
        ui.setTabOrder(self.lineEdit_8, self.lineEdit_9)

    def retranslateUi(self, ui):
        ui.setWindowTitle(QtGui.QApplication.translate("ui", "Geometry from Azimuth and Distance", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("ui", "Layer:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("ui", "Survey type", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_8.setText(QtGui.QApplication.translate("ui", "Polygonal", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_7.setText(QtGui.QApplication.translate("ui", "Irradiate", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("ui", "Input type", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_11.setText(QtGui.QApplication.translate("ui", "Decimal Degrees", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_12.setText(QtGui.QApplication.translate("ui", "Degrees, Minutes, Seconds", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("ui", "Starting vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("ui", "X0:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("ui", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_8.setText(QtGui.QApplication.translate("ui", "Capture from Map", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("ui", "Y0:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_2.setText(QtGui.QApplication.translate("ui", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("ui", "Z0:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_3.setText(QtGui.QApplication.translate("ui", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("ui", "Next vertex", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("ui", "Azimuth:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_7.setText(QtGui.QApplication.translate("ui", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_10.setText(QtGui.QApplication.translate("ui", "Capture from Map", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("ui", "Distance:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_8.setText(QtGui.QApplication.translate("ui", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("ui", "Vertical:", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_9.setText(QtGui.QApplication.translate("ui", "90", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("ui", "Insert", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_5.setTitle(QtGui.QApplication.translate("ui", "North type", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_14.setText(QtGui.QApplication.translate("ui", "Coordinate System", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_13.setText(QtGui.QApplication.translate("ui", "True", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_15.setText(QtGui.QApplication.translate("ui", "Magnetic", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("ui", "Get from NIMA", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("ui", "Year:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_6.setTitle(QtGui.QApplication.translate("ui", "Angle type", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_17.setText(QtGui.QApplication.translate("ui", "Azimuth", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_16.setText(QtGui.QApplication.translate("ui", "Polar coordinates", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_18.setText(QtGui.QApplication.translate("ui", "Bearing", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("ui", "Azimuth", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("ui", "Distance", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("ui", "Vertical Angle", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("ui", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("ui", "Up", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_5.setText(QtGui.QApplication.translate("ui", "Down", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("ui", "Coordinate System:", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_11.setText(QtGui.QApplication.translate("ui", "Change", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_7.setText(QtGui.QApplication.translate("ui", "Draw", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_6.setText(QtGui.QApplication.translate("ui", "Clear List", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(QtGui.QApplication.translate("ui", "Import List", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_9.setText(QtGui.QApplication.translate("ui", "Export List", None, QtGui.QApplication.UnicodeUTF8))
