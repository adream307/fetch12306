# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cyf/work/fetch_12306/script/chapter3/12306.git/ui/booking.ui'
#
# Created: Fri Oct 30 21:00:16 2015
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgBooking(object):
    def setupUi(self, dlgBooking):
        dlgBooking.setObjectName(_fromUtf8("dlgBooking"))
        dlgBooking.resize(419, 274)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgBooking.sizePolicy().hasHeightForWidth())
        dlgBooking.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(dlgBooking)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lblTrainInfo = QtGui.QLabel(dlgBooking)
        self.lblTrainInfo.setObjectName(_fromUtf8("lblTrainInfo"))
        self.verticalLayout.addWidget(self.lblTrainInfo)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.listPassengers = QtGui.QListWidget(dlgBooking)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listPassengers.sizePolicy().hasHeightForWidth())
        self.listPassengers.setSizePolicy(sizePolicy)
        self.listPassengers.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.listPassengers.setObjectName(_fromUtf8("listPassengers"))
        item = QtGui.QListWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listPassengers.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listPassengers.addItem(item)
        self.horizontalLayout_2.addWidget(self.listPassengers)
        self.lblCaptcha = QtGui.QLabel(dlgBooking)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblCaptcha.sizePolicy().hasHeightForWidth())
        self.lblCaptcha.setSizePolicy(sizePolicy)
        self.lblCaptcha.setText(_fromUtf8(""))
        self.lblCaptcha.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../pic/chapter3/12306-login-check.jpeg")))
        self.lblCaptcha.setObjectName(_fromUtf8("lblCaptcha"))
        self.horizontalLayout_2.addWidget(self.lblCaptcha)
        self.horizontalLayout_2.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnBooking = QtGui.QPushButton(dlgBooking)
        self.btnBooking.setObjectName(_fromUtf8("btnBooking"))
        self.horizontalLayout.addWidget(self.btnBooking)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.bntFresh = QtGui.QPushButton(dlgBooking)
        self.bntFresh.setObjectName(_fromUtf8("bntFresh"))
        self.horizontalLayout.addWidget(self.bntFresh)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(dlgBooking)
        QtCore.QMetaObject.connectSlotsByName(dlgBooking)

    def retranslateUi(self, dlgBooking):
        dlgBooking.setWindowTitle(QtGui.QApplication.translate("dlgBooking", "订票确认", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTrainInfo.setText(QtGui.QApplication.translate("dlgBooking", "2015-10-31,G117次,北京南(9:43)--上海虹桥(15:41)", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.listPassengers.isSortingEnabled()
        self.listPassengers.setSortingEnabled(False)
        item = self.listPassengers.item(0)
        item.setText(QtGui.QApplication.translate("dlgBooking", "甲某某", None, QtGui.QApplication.UnicodeUTF8))
        item = self.listPassengers.item(1)
        item.setText(QtGui.QApplication.translate("dlgBooking", "乙某某", None, QtGui.QApplication.UnicodeUTF8))
        self.listPassengers.setSortingEnabled(__sortingEnabled)
        self.btnBooking.setText(QtGui.QApplication.translate("dlgBooking", "订票", None, QtGui.QApplication.UnicodeUTF8))
        self.bntFresh.setText(QtGui.QApplication.translate("dlgBooking", "刷新", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlgBooking = QtGui.QDialog()
    ui = Ui_dlgBooking()
    ui.setupUi(dlgBooking)
    dlgBooking.show()
    sys.exit(app.exec_())

