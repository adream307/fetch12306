# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from ui.mainwindow import MainWindow

if __name__=="__main__":
    import sys
    app=QtGui.QApplication(sys.argv)
    a=MainWindow(sys.argv);
    a.show()
    sys.exit(app.exec_())
