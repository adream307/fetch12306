# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ui.login import dlgLogin

if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    ui_login=dlgLogin()
    ui_login.show();
    sys.exit(app.exec_())
