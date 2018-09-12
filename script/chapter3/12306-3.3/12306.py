# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ui.login import dlgLogin
import requests

if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    conn=requests.Session()
    ui_login=dlgLogin(conn)
    ui_login.show();
    sys.exit(app.exec_())
