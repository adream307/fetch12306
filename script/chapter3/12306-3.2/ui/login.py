# -*- coding: utf-8 -*-

"""
Module implementing dlgLogin.
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature

from Ui_login import Ui_dlgLogin

class dlgLogin(QDialog, Ui_dlgLogin):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.lblCaptcha.mouseReleaseEvent=self.on_lblCaptcha_released
        self.click_pos=[]
        self.click_icon=[]
        self.pos_zero=QtCore.QPoint(0, 30)
    
    @pyqtSignature("")
    def on_btnLogin_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    @pyqtSignature("")
    def on_btnRefresh_released(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        raise NotImplementedError
    
    def on_lblCaptcha_released(self, event):
        click_icon = QtGui.QLabel(self)
        click_icon.setGeometry(QtCore.QRect(self.lblCaptcha.x()+event.x()-10,self.lblCaptcha.y()-10+event.y(),  20, 20))
        click_icon.setStyleSheet("QLabel { background-color : red; }")
        click_icon.show()
        self.click_icon.append(click_icon)
        self.click_pos.append(event.pos()-self.pos_zero)
        print event.pos()-self.pos_zero
