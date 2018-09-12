# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cyf/work/fetch_12306/script/chapter3/12306/ui/login.ui'
#
# Created: Sun Sep  6 20:45:55 2015
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgLogin(object):
    def setupUi(self, dlgLogin):
        dlgLogin.setObjectName(_fromUtf8("dlgLogin"))
        dlgLogin.resize(378, 314)
        self.gridLayout_2 = QtGui.QGridLayout(dlgLogin)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(dlgLogin)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtUsername = QtGui.QLineEdit(dlgLogin)
        self.txtUsername.setObjectName(_fromUtf8("txtUsername"))
        self.gridLayout.addWidget(self.txtUsername, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(dlgLogin)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.txtPasswd = QtGui.QLineEdit(dlgLogin)
        self.txtPasswd.setObjectName(_fromUtf8("txtPasswd"))
        self.gridLayout.addWidget(self.txtPasswd, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(dlgLogin)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lblCaptcha = QtGui.QLabel(dlgLogin)
        self.lblCaptcha.setText(_fromUtf8(""))
        self.lblCaptcha.setPixmap(QtGui.QPixmap(_fromUtf8("/home/cyf/work/fetch_12306/pic/chapter3/12306-login-check.jpeg")))
        self.lblCaptcha.setObjectName(_fromUtf8("lblCaptcha"))
        self.gridLayout.addWidget(self.lblCaptcha, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnLogin = QtGui.QPushButton(dlgLogin)
        self.btnLogin.setObjectName(_fromUtf8("btnLogin"))
        self.horizontalLayout.addWidget(self.btnLogin)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnRefresh = QtGui.QPushButton(dlgLogin)
        self.btnRefresh.setObjectName(_fromUtf8("btnRefresh"))
        self.horizontalLayout.addWidget(self.btnRefresh)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(dlgLogin)
        QtCore.QMetaObject.connectSlotsByName(dlgLogin)

    def retranslateUi(self, dlgLogin):
        dlgLogin.setWindowTitle(QtGui.QApplication.translate("dlgLogin", "12306 Login", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("dlgLogin", "用户名：", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("dlgLogin", "密码:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("dlgLogin", "验证码：", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLogin.setText(QtGui.QApplication.translate("dlgLogin", "登录", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRefresh.setText(QtGui.QApplication.translate("dlgLogin", "刷新", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dlgLogin = QtGui.QDialog()
    ui = Ui_dlgLogin()
    ui.setupUi(dlgLogin)
    dlgLogin.show()
    sys.exit(app.exec_())

