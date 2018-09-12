# -*- coding: utf-8 -*-

"""
Module implementing dlgBooking.
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSignature
import random

from Ui_booking import Ui_dlgBooking

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class dlgBooking(QDialog, Ui_dlgBooking):
    """
    Class documentation goes here.
    """
    def __init__(self,conn,parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.conn=conn
        self.rand_pic_url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp&'
        self.rand_check_url="https://kyfw.12306.cn/otn/passcodeNew/checkRandCodeAnsyn"
        self.check_order_url="https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo"
        self.count_url="https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
        self.confirm_url="https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue"
        self.headers={
                      "Host":"kyfw.12306.cn",
                      "User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0",
                      "Connection":"keep-alive"}
        self.isDoen=False
        self.lblCaptcha.mouseReleaseEvent=self.on_lblCaptcha_released
        self.click_pos=[]
        self.click_icon=[]
        self.pos_zero=QtCore.QPoint(0, 30)
        self.seat_type_dir={
                _fromUtf8(u"二等座"):u"O", 
                _fromUtf8(u"一等座"):u"M",
                _fromUtf8(u"商务座"):u"9", 
                _fromUtf8(u"特等座"):u"P", 
                _fromUtf8(u"高级软卧"):u"6", 
                _fromUtf8(u"软卧"):u"4", 
                _fromUtf8(u"硬卧"):u"3", 
                _fromUtf8(u"软座"):u"2", 
                _fromUtf8(u"硬座"):u"1", 
                _fromUtf8(u"无座"):u"O", 
                }
        self.weekdays={1:"Mon",2:"Tue",3:"Wed",4:"Thu",5:"Fri",6:"Sat",7:"Sun"}
        self.months={1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun", 
                     7:"Jul",8:"Aug",9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
        
    def get_seat_type(self, seat_type):
        if seat_type==_fromUtf8(u"无座"):
            if self.train_info["ze_num"] !=u"--":
                return u"O"
            else:
                return u"1"
        else:
            return self.seat_type_dir[seat_type]
    
    @pyqtSignature("")
    def on_btnBooking_released(self):
        """
        booking tickets
        """
        #check passengers
        index=0
        checked_passengers=[]
        while index < self.listPassengers.count():
            if self.listPassengers.item(index).checkState()==QtCore.Qt.Checked:
                checked_passengers.append(index)
            index=index+1
        if len(checked_passengers)==0:
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8("请选择乘客"))
            msg.exec_()
            return
        #check the rand code
        payload={"rand" : "randp", 
                 "randCode" : "", 
                 "_json_att":"", 
                 "REPEAT_SUBMIT_TOKEN":self.repeatToken}
        randCode=""
        for pos in self.click_pos:
            if randCode=="":
                randCode ="%s,%s" %(pos.x(), pos.y())
            else:
                randCode += ",%s,%s" %(pos.x(), pos.y())
        payload["randCode"]=randCode
        r=self.conn.post(self.rand_check_url, data=payload, headers=self.headers, verify=False)
        if r.json()["data"]["msg"]!="TRUE":
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8("验证码错误"))
            msg.exec_()
            self.on_bntFresh_released()
            return
        print "rand code verify success"
        #check order
        del payload["rand"]
        payload["cancel_flag"]="2"
        payload["bed_level_order_num"]="000000000000000000000000000000"
        payload["tour_flag"]="dc"
        passengerTicketStr=u""
        oldPassengerStr=u""
        for index in checked_passengers:
            if passengerTicketStr!=u"":
                passengerTicketStr=passengerTicketStr+u"_"
            passengerTicketStr=passengerTicketStr+self.get_seat_type(self.seat_type)+u","
            passengerTicketStr=passengerTicketStr+u"0,"
            passengerTicketStr=passengerTicketStr+self.passengers_info[index]["passenger_type"]+u","
            passengerTicketStr=passengerTicketStr+self.passengers_info[index]["passenger_name"]+u","
            passengerTicketStr=passengerTicketStr+self.passengers_info[index]["passenger_id_type_code"]+u","
            passengerTicketStr=passengerTicketStr+self.passengers_info[index]["passenger_id_no"]+u","
            passengerTicketStr=passengerTicketStr+self.passengers_info[index]["mobile_no"]+u",N"
            
            oldPassengerStr=oldPassengerStr+self.passengers_info[index]["passenger_name"]+u","
            oldPassengerStr=oldPassengerStr+self.passengers_info[index]["passenger_type"]+u","
            oldPassengerStr=oldPassengerStr+self.passengers_info[index]["passenger_id_no"]+u","
            oldPassengerStr=oldPassengerStr+self.passengers_info[index]["passenger_id_type_code"]+u"_"
            
        payload["passengerTicketStr"]=passengerTicketStr.encode("utf-8")
        payload["oldPassengerStr"]=oldPassengerStr.encode("utf-8")
        checkorder_page=self.conn.post(self.check_order_url, data=payload, headers=self.headers, verify=False)
        checkorder_page_json=checkorder_page.json()
        if checkorder_page_json["status"]==False or checkorder_page_json["data"]["submitStatus"]==False:
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8(checkorder_page_json["messages"][0]))
            msg.exec_()
            return
        print "check order success"
        # get count
        start_index=self.confirm_page_text.find("ypInfoDetail\':\'")+len("ypInfoDetail\':\'");
        end_index=self.confirm_page_text.find("\'", start_index);
        self.ypInfoDetail=self.confirm_page_text[start_index:end_index]
#        payload={"train_date":self.weekdays[self.train_date.dayOfWeek()]+"+"+self.months[self.train_date.month()]+"+"+
#                              "{0:02}+{1:04}+00:00:00+GMT+0800+(CST)".format(self.train_date.day(), self.train_date.year()), 
#                 "train_no":self.train_info["train_no"].encode("utf-8"), 
#                 "stationTrainCode":self.train_info["station_train_code"].encode("utf-8"), 
#                 "seatType":self.get_seat_type(self.seat_type).encode("utf-8"), 
#                 "fromStationTelecode":self.train_info["from_station_telecode"].encode("utf-8"), 
#                 "toStationTelecode":self.train_info["to_station_telecode"].encode("utf-8"), 
#                 "leftTicket":self.ypInfoDetail.encode("utf-8"), 
#                 "purpose_codes":"00", 
#                 "_json_att":"", 
#                 "REPEAT_SUBMIT_TOKEN":self.repeatToken.encode("utf-8")
#                 }
#        print payload
#        count_page=self.conn.post(self.count_url, data=payload, headers=self.headers, verify=False)
#        count_page_json=count_page.json()
#        if count_page_json["status"]==False or len(count_page_json["messages"])!=0:
#            msg=QtGui.QMessageBox()
#            msg.setText(_fromUtf8(count_page_json["messages"][0]))
#            msg.exec_()
#            return
#        print "get cout success"
        #confirm
        start_index=self.confirm_page_text.find("key_check_isChange\':\'")+len("key_check_isChange\':\'");
        end_index=self.confirm_page_text.find("\'", start_index);
        self.key_check_isChange=self.confirm_page_text[start_index:end_index]
        payload={"passengerTicketStr":passengerTicketStr.encode("utf-8"), 
                 "oldPassengerStr":oldPassengerStr.encode("utf-8"), 
                 "randCode":randCode, 
                 "purpose_codes":"00", 
                 "key_check_isChange":self.key_check_isChange, 
                 "leftTicketStr":self.ypInfoDetail, 
                 "train_location":self.train_info["location_code"], 
                 "roomType":"00", 
                 "dwAll":"N", 
                 "_json_att":"", 
                 "REPEAT_SUBMIT_TOKEN":self.repeatToken}
        print payload
        confirm_page=self.conn.post(self.confirm_url, data=payload, headers=self.headers, verify=False)
        confirm_page_json=confirm_page.json()
        if confirm_page_json["status"]==False or confirm_page_json["data"]["submitStatus"]==False:
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8(confirm_page_json["messages"][0]))
            msg.exec_()
            return
        self.isDoen=True
        self.done(QDialog.Accepted)
        msg=QtGui.QMessageBox()
        msg.setText(_fromUtf8(u"订票成功，请登录12306完成支付"))
        msg.exec_()
    
    @pyqtSignature("")
    def on_bntFresh_released(self):
        """
        reload the rand picture
        """
        for icon in self.click_icon:
            icon.hide()
        self.click_icon=[]
        self.click_pos=[]
        url="%s%0.17f"%(self.rand_pic_url, random.random())
        r = self.conn.get(url+"%0.17f",headers=self.headers,verify=False)
        if len(r.content)==0:
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8("下载验证吗失败,请刷新或重新登录"))
            msg.exec_()
            self.fresh_status=False
            return
        rand_pic= QtGui.QPixmap()
        rand_pic.loadFromData(r.content)
        self.lblCaptcha.setPixmap(rand_pic)
        self.fresh_status=True
        
    def set_passenger_list(self, passengers):
        self.passengers_info=passengers
        self.listPassengers.clear()
        for p in passengers:
            #print p['passenger_name']
            item=QtGui.QListWidgetItem(_fromUtf8(p['passenger_name']))
            item.setCheckState(QtCore.Qt.Unchecked)
            if p['total_times']=='98':
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable)
            self.listPassengers.addItem(item)
            
    def set_passenger_check_status(self, index, status):
        item=self.listPassengers.item(index)
        if status==True:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)
    
    def set_train_info(self, train, date, seat_type, tickets):
        self.train_info=train
        self.train_date=date
        str=QtCore.QString(_fromUtf8("%1-%2-%3,%4次,%5(%6)--%7(%8)\n")).arg( 
                                            QtCore.QString.number(date.year()), 
                                            QtCore.QString.number(date.month()), 
                                            QtCore.QString.number(date.day()),
                                           _fromUtf8(train["station_train_code"]), 
                                           _fromUtf8(train["from_station_name"]),
                                           _fromUtf8(train["start_time"]),
                                           _fromUtf8(train["to_station_name"]),
                                           _fromUtf8(train["arrive_time"]))
        str=str+QtCore.QString(_fromUtf8("%1,剩余票数：%2")).arg(seat_type, tickets)
        self.seat_type=seat_type
        self.lblTrainInfo.setText(str)
    
    def exec_(self):
        self.on_bntFresh_released()
        if self.fresh_status:
            super(dlgBooking, self).exec_()
            
    def on_lblCaptcha_released(self, event):
        click_icon = QtGui.QLabel(self)
        click_icon.setGeometry(QtCore.QRect(self.lblCaptcha.x()+event.x()-10,self.lblCaptcha.y()-10+event.y(),  20, 20))
        click_icon.setStyleSheet("QLabel { background-color : red; }")
        click_icon.show()
        self.click_icon.append(click_icon)
        self.click_pos.append(event.pos()-self.pos_zero)
        print event.pos()-self.pos_zero
        
