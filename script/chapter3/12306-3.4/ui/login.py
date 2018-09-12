# -*- coding: utf-8 -*-

"""
Module implementing dlgLogin.
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
import random

from Ui_login import Ui_dlgLogin

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class dlgLogin(QDialog, Ui_dlgLogin):
    """
    Class documentation goes here.
    """
    def __init__(self,conn,  parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        winflag=self.windowFlags()
        winflag |= QtCore.Qt.CustomizeWindowHint
        winflag &= ~QtCore.Qt.WindowMaximizeButtonHint
        self.setWindowFlags(winflag)
        self.conn=conn
        self.rand_pic_url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand&'
        self.rand_check_url='https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn'
        self.login_url='https://kyfw.12306.cn/otn/login/loginAysnSuggest'
        self.headers={
                      "Host":"kyfw.12306.cn",
                      "User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0",
                      "Connection":"keep-alive"}
        self.conn.get('https://kyfw.12306.cn/otn/login/init#', headers=self.headers, verify=False);
        self.conn.get("https://kyfw.12306.cn/otn/resources/merged/login_js.js",
                      headers=self.headers, verify=False)
        r = self.conn.get(self.rand_pic_url+"%0.17f" % random.random(),headers=self.headers,verify=False)
        rand_pic= QtGui.QPixmap()
        rand_pic.loadFromData(r.content)
        self.resize(rand_pic.width()+(387-293), rand_pic.height()+(312-190))
        self.lblCaptcha.setPixmap(rand_pic)
        self.lblCaptcha.mouseReleaseEvent=self.on_lblCaptcha_released
        self.click_pos=[]
        self.click_icon=[]
        self.pos_zero=QtCore.QPoint(0, 30)
        self.islogin=False
    
    @pyqtSignature("")
    def on_btnLogin_released(self):
        """
        user login
        """
        #verify the rand code
        payload={"rand" : "sjrand", "randCode" : ""}
        for pos in self.click_pos:
            if payload["randCode"]=="":
                payload["randCode"] ="%s,%s" %(pos.x(), pos.y())
            else:
                payload["randCode"] += ",%s,%s" %(pos.x(), pos.y())
        r=self.conn.post(self.rand_check_url, data=payload, headers=self.headers, verify=False)
        if r.json()["data"]["msg"]!="TRUE":
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8("验证码错误"))
            msg.exec_()
            self.on_btnRefresh_released()
            return
        print "rand code verify success"
        #check the uer name and password
        del payload["rand"]
        payload["loginUserDTO.user_name"]=str(self.txtUsername.text())
        payload["userDTO.password"]=str(self.txtPasswd.text())
        r=self.conn.post(self.login_url, data=payload, headers=self.headers, verify=False)
        if r.json()["data"]=={}:
            print "username or password error"
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8("用户名或密码错误"))
            msg.exec_()
            self.on_btnRefresh_released()
            return
        elif r.json()["data"]["loginCheck"]!="Y":
            print "username or password error"
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8("用户名或密码错误"))
            msg.exec_()
            self.on_btnRefresh_released()
            return
        print "login success."
        self.islogin=True
        self.done(QDialog.Accepted)
    
    @pyqtSignature("")
    def on_btnRefresh_released(self):
        """
        reflash the rand picture
        """
        for icon in self.click_icon:
            icon.hide()
        self.click_icon=[]
        self.click_pos=[]
        r = self.conn.get(self.rand_pic_url+"%0.17f" % random.random(),headers=self.headers,verify=False)
        rand_pic= QtGui.QPixmap()
        rand_pic.loadFromData(r.content)
        self.lblCaptcha.setPixmap(rand_pic)
    
    def on_lblCaptcha_released(self, event):
        click_icon = QtGui.QLabel(self)
        click_icon.setGeometry(QtCore.QRect(self.lblCaptcha.x()+event.x()-10,self.lblCaptcha.y()-10+event.y(),  20, 20))
        click_icon.setStyleSheet("QLabel { background-color : red; }")
        click_icon.show()
        self.click_icon.append(click_icon)
        self.click_pos.append(event.pos()-self.pos_zero)
        print event.pos()-self.pos_zero
