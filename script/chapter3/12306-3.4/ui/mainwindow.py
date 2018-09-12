# -*- coding: utf-8 -*-

from ui.login import dlgLogin
from ui.booking import dlgBooking
import requests
import random
import json
import datetime
import time
import urllib

"""
Module implementing MainWindow.
"""
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QMainWindow, QSortFilterProxyModel, QCompleter
from PyQt4.QtCore import pyqtSignature

from Ui_mainwindow import Ui_MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class StationNameFilterProxy(QSortFilterProxyModel):
    """
    user defined QSortFilterProxyModel
    get the station name by pinying
    """
    def __init__(self,name_dict,  parent=None):
        super(StationNameFilterProxy, self).__init__(parent)
        self.name_dict=name_dict
        self.text=None
    
    @pyqtSignature("QString")
    def setFilterFixedString(self, text):
        self.text=text
        return super(StationNameFilterProxy, self).setFilterFixedString(text)
        
    def filterAcceptsRow (self, source_row, source_parent ):
        if not self.text:return True
        if self.text=="":return True
        if self.name_dict[source_row][0].startswith(self.text):return True
        if self.name_dict[source_row][1].startswith(self.text):return True
        if self.name_dict[source_row][2].startswith(self.text):return True
        return False
        

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self,argv=[], parent = None):
        """
        Constructor
        """
        self.conn=requests.Session()
        self.login_form=dlgLogin(self.conn)
        if len(argv)==3:
            self.login_form.txtUsername.setText(argv[1])
            self.login_form.txtPasswd.setText(argv[2])
        self.login_form.first_time_called=True;
        self.booking_form=dlgBooking(self.conn)
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        #set the table column width
        self.tableTickets.resizeColumnsToContents()
        header=self.tableTickets.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.Stretch)
        #set the date to current date
        self.dateStart.setDateTime(QtCore.QDateTime.currentDateTime())
        #set the request headers
        self.headers={
                      "Host":"kyfw.12306.cn",
                      "User-Agent":"Mozilla/5.0 (X11; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0",
                      "Connection":"keep-alive"}
        #initial the combobox
        self.station_url="https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"
        self.log_url="https://kyfw.12306.cn/otn/leftTicket/log"
        self.confirm_url="https://kyfw.12306.cn/otn/confirmPassenger/initDc"
        self.queryT_url="https://kyfw.12306.cn/otn/leftTicket/query"
        self.check_user_url="https://kyfw.12306.cn/otn/login/checkUser"
        self.submit_order_url="https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest"
        self.repeat_init_url="https://kyfw.12306.cn/otn/leftTicket/init?random="
        self.passengers_info_url="https://kyfw.12306.cn/otn/passengers/init"
        self.init_station_name()
        self.cmbFrom.setStyleSheet("combobox-popup: 0;"); #make  maxVisibleItems property available in GTK+
        self.cmbTo.setStyleSheet("combobox-popup: 0;");
        self.cmbFrom.setFocusPolicy(Qt.StrongFocus)
        self.cmbTo.setFocusPolicy(Qt.StrongFocus)
        self.cmbFrom.setCurrentIndex(-1)
        self.cmbTo.setCurrentIndex(-1)
        self.filtermodFrom=StationNameFilterProxy(self.station_name_dict, self.cmbFrom)
        self.filtermodFrom.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtermodFrom.setSourceModel(self.cmbFrom.model())
        self.completerFrom=QCompleter(self.filtermodFrom, self.cmbFrom)
        self.completerFrom.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.cmbFrom.setCompleter(self.completerFrom)
        self.cmbFrom.lineEdit().textEdited[unicode].connect(self.filtermodFrom.setFilterFixedString)
        self.completerFrom.activated.connect(self.on_completerFrom_activated)
        #-------------
        self.filtermodTo=StationNameFilterProxy(self.station_name_dict, self.cmbTo)
        self.filtermodTo.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filtermodTo.setSourceModel(self.cmbTo.model())
        self.completerTo=QCompleter(self.filtermodTo, self.cmbTo)
        self.completerTo.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.cmbTo.setCompleter(self.completerTo)
        self.cmbTo.lineEdit().textEdited[unicode].connect(self.filtermodTo.setFilterFixedString)
        self.completerTo.activated.connect(self.on_completerTo_activated)
        #initial tableview's context menu and mainwindow's menu
        self.menuBar().setNativeMenuBar(False)
        self.tableTickets.addAction(self.action_login)#用户登录
        self.menuBar().addAction(self.action_login)
        self.tableTickets.addAction(self.action_tickets)#定时抢票
        self.menuBar().addAction(self.action_tickets)
        self.tableTickets.addAction(self.action_fresh_tickets)#自动刷票
        self.menuBar().addAction(self.action_fresh_tickets)
        if self.login_form.islogin : 
            self.action_login.setEnabled (False)
            self.get_passengers()
            self.booking_form.set_passenger_list(self.passengers_info)
        #initial tableview's column name
        self.dict_table_column={
            0:("station_train_code",_fromUtf8(u"车次")), 
            1:("from_station_name",_fromUtf8(u"出发站")), 
            2:("to_station_name",_fromUtf8(u"到达站")), 
            3:("start_time",_fromUtf8(u"出发时间")), 
            4:("arrive_time",_fromUtf8(u"达到时间")), 
            5:("lishi",_fromUtf8(u"历时")), 
            6:("swz_num",_fromUtf8(u"商务座")), 
            7:("tz_num",_fromUtf8(u"特等座")), 
            8:("zy_num",_fromUtf8(u"一等座")), 
            9:("ze_num",_fromUtf8(u"二等座")), 
            10:("gr_num",_fromUtf8(u"高级软卧")), 
            11:("rw_num",_fromUtf8(u"软卧")), 
            12:("yw_num",_fromUtf8(u"硬卧")), 
            13:("rz_num",_fromUtf8(u"软座")), 
            14:("yz_num",_fromUtf8(u"硬座")), 
            15:("wz_num",_fromUtf8(u"无座"))}
        self.monitor_list={}
        self.query_date=""
        self.from_station=""
        self.to_station=""
        self.conn.get("https://kyfw.12306.cn/otn/resources/js/query/qss.js", 
                      headers=self.headers,verify=False)
        
            
    def showEvent(self, event):
        super(MainWindow, self).showEvent(event)
        if self.login_form.first_time_called==False:return
        self.login_form.first_time_called=False
        self.login_form.exec_()
        if self.login_form.islogin : 
            self.action_login.setEnabled (False)
            self.get_passengers()
            self.booking_form.set_passenger_list(self.passengers_info)
    def closeEvent(self, event):
        if self.login_form.islogin==True:
            self.conn.get("https://kyfw.12306.cn/otn/login/loginOut", headers=self.headers, verify=False)
            print "Exit"
        
    def on_completerTo_activated(self, text):
        if text:
            index = self.cmbTo.findText(text)
            self.cmbTo.setCurrentIndex(index)
        
    def on_completerFrom_activated(self, text):
        if text:
            index = self.cmbFrom.findText(text)
            self.cmbFrom.setCurrentIndex(index)
        
    def init_station_name(self):
        self.print_log(u"获取站点信息")
        init_page_url="https://kyfw.12306.cn/otn/lcxxcx/init"
        init_page=requests.get(init_page_url, headers=self.headers,verify=False)
        init_str=init_page.text
        start=init_str.find("?station_version=")
        end=init_str.find("\"", start)
        station_version=init_str[start:end]
        station_page=requests.get(self.station_url+station_version, headers=self.headers, verify=False)
        station_str=station_page.text
        start=station_str.find("@", 0)+1
        end=station_str.find("@", start)
        self.station_name_dict={}
        self.station_name_index=0
        while end>0:
            str_tmp=station_str[start:end]
            token_tmp=str_tmp.split('|')
            self.cmbFrom.addItem(token_tmp[1])
            self.cmbTo.addItem(token_tmp[1])
            self.station_name_dict[self.station_name_index]=(token_tmp[0], token_tmp[3], token_tmp[4], token_tmp[2], token_tmp[1])
            self.station_name_index=self.station_name_index+1
            start=end+1
            end=station_str.find("@", start)
        end=station_str.find("\'", start)
        str_tmp=station_str[start:end]
        token_tmp=str_tmp.split('|')
        self.cmbFrom.addItem(token_tmp[1])
        self.cmbTo.addItem(token_tmp[1])
        self.station_name_dict[self.station_name_index]= (token_tmp[0], token_tmp[3], token_tmp[4], token_tmp[2], token_tmp[1])
        self.station_name_index=self.station_name_index+1
        
    def get_passengers(self):
        self.print_log(u"获取乘客信息")
        header=self.headers
        header["Referer"]="https://kyfw.12306.cn/otn/index/initMy12306"
        payload={"_json_att":""}
        passenger_page=self.conn.post(self.passengers_info_url, data=payload, headers=header, verify=False)
        passenger_text=passenger_page.text
        start_str="var passengers="
        start_index=passenger_text.find(start_str)
        start_index=start_index+len(start_str)
        end_index=passenger_text.find(";", start_index)
        passengers_info=passenger_text[start_index:end_index].replace("\'", "\"")
        self.passengers_info=json.loads(passengers_info)
        self.tableTickets.passengers_menu=QtGui.QMenu(_fromUtf8("乘客选择"), self.tableTickets)
        self.passengers_menu_actions=[]
        for p in self.passengers_info:
            self.passengers_menu_actions.append(QtGui.QAction(_fromUtf8(p['passenger_name']), self.tableTickets))
            actions_len=len(self.passengers_menu_actions)
            self.passengers_menu_actions[actions_len-1].setCheckable(True)
            if p['total_times']=='98':
                self.passengers_menu_actions[actions_len-1].setEnabled(False)
            self.tableTickets.passengers_menu.addAction(self.passengers_menu_actions[actions_len-1])
        self.tableTickets.addAction(self.tableTickets.passengers_menu.menuAction())
        self.menuBar().addAction(self.tableTickets.passengers_menu.menuAction())
        
    def query_tickets(self):
        query_date="{0:04}-{1:02}-{2:02}".format(self.dateStart.date().year(), self.dateStart.date().month(), self.dateStart.date().day())
        from_station=self.station_name_dict[self.cmbFrom.currentIndex()][3]
        to_station=self.station_name_dict[self.cmbTo.currentIndex()][3]
        if query_date!=self.query_date or from_station!=self.from_station or to_station!=self.to_station:
            self.monitor_list.clear()
            self.query_date=query_date
            self.from_station=from_station
            self.to_station=to_station
        query_params="?leftTicketDTO.train_date="+query_date
        query_params=query_params+"&leftTicketDTO.from_station="+from_station
        query_params=query_params+"&leftTicketDTO.to_station="+to_station
        query_params=query_params+"&purpose_codes=ADULT"
        log_page=self.conn.get(self.log_url+query_params+"A=T", headers=self.headers,verify=False)
        log_page_json=log_page.json()
        if log_page_json["status"] != True:
            return None
        query_page=self.conn.get(self.queryT_url+query_params, headers=self.headers,verify=False)
        query_page_json=query_page.json()
        if query_page_json["status"] == True and query_page_json.has_key('data'):
            return query_page_json['data']
        else:
            return None
    
    def fetch_tickes(self, station_from, station_to, query_date):
        tickets_url="https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate="+query_date
        tickets_url=tickets_url+"&from_station="+station_from
        tickets_url=tickets_url+"&to_station="+station_to
        tickets_page=requests.get(tickets_url, headers=self.headers,verify=False)
        tickets_dict=tickets_page.json()
        if tickets_dict["data"]["flag"]:
            return tickets_dict["data"]["datas"]
        else:return None
        
    def show_tickets(self, tickets):
        if not tickets:
            self.print_log(u"没有符合条件的数据")
            self.clear_table_content()
            return False
        col=0
        index=self.tableTickets.rowCount()
        if index!=len(tickets):
            self.tableTickets.setRowCount(len(tickets))
            index=0
            while index<len(tickets):
                col=0
                while col<len(self.dict_table_column):
                    item=QtGui.QTableWidgetItem(QtCore.QString(u""))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableTickets.setItem(index, col,item)
                    col=col+1
                index=index+1
        index=0
        for t in tickets:
            col=0
            if self.monitor_list.has_key(t['queryLeftNewDTO']['station_train_code']):
                red_col=self.monitor_list[t['queryLeftNewDTO']['station_train_code']]
            else:
                red_col=None
            while col<len(self.dict_table_column):
                item=self.tableTickets.item(index, col)
                item.setText(QtCore.QString(t['queryLeftNewDTO'][self.dict_table_column[col][0]]))
                if red_col and col in red_col:
                    item.setBackground(Qt.red)
                else:
                    item.setBackground(Qt.transparent)
                col=col+1
            index=index+1
        return True
            
    def print_log(self, text):
        str=QtCore.QString(datetime.datetime.now().strftime('%H:%M:%S')) + QtCore.QString(" - ") + QtCore.QString(_fromUtf8(text))
        self.plainTextEdit.appendPlainText(str)
    
    def print_session_info(self, conn):
        print"Headers:"
        for (k, v) in conn.headers.iteritems():
            print "\t%s:%s" %(k, v)
        print"Cookies:"
        for (k, v) in conn.cookies.iteritems():
            print "\t%s:%s" %(k, v)
    
    #action slots
    @pyqtSignature("")
    def on_action_login_triggered(self):
        print "on login triggered"
        self.login_form.on_btnRefresh_released()
        self.login_form.exec_()
        if self.login_form.islogin : 
            self.action_login.setEnabled (False)
            self.get_passengers()
            self.booking_form.set_passenger_list(self.passengers_info)
        
    @pyqtSignature("")
    def on_action_tickets_triggered(self):
        print "on tickets triggered"
        
    @pyqtSignature("")
    def on_action_fresh_tickets_triggered(self):
        print "on fresh triggered"
        
    @pyqtSignature("")
    def on_btnQuery_clicked(self):
        self.print_log(u"查询车次信息。。。")
        if self.cmbFrom.currentIndex()<0:
            self.print_log(u"请选择始发站点")
            self.clear_table_content()
            return
        if self.cmbTo.currentIndex()<0:
            self.print_log(u"请选择终点站")
            self.clear_table_content()
            return
        if self.dateStart.date() < QtCore.QDateTime.currentDateTime().date():
            self.print_log(u"请选择正确的乘车日期")
            self.clear_table_content()
            return
        if self.login_form.islogin==False:
            self.print_log("请先登录")
            self.clear_table_content()
            return
        self.print_log(u"正在获取车票信息。。。")
        self.current_tickets=self.query_tickets()
        #self.current_tickets=self.fetch_tickes(station_from, station_to, query_date)
        if self.show_tickets(self.current_tickets):
            self.print_log(u"获取车票信息完成")
            self.print_log(u"双击剩余票数，即可订票")
        #del self.monitor_list[:]
        
    def check_the_user(self):
        payload={"_json_att":""}
        self.print_log(u"执行用户认证。。。")
        check_page=self.conn.post(self.check_user_url,data=payload,headers=self.headers, verify=False)
        check_page_json = check_page.json()
        if check_page_json["data"]["flag"]==False:
            self.login_form.islogin=False
        if self.login_form.islogin==False:
            self.action_login.setEnabled (True)
            #self.clear_table_content()
            return False
        return True
        
    def submit_ticket(self, ticket_info):
        payload={
                 "secretStr":urllib.unquote(ticket_info["secretStr"]), 
                 "train_date":'{0:04}-{1:02}-{2:02}'.format(self.dateStart.date().year(), self.dateStart.date().month(), self.dateStart.date().day()),  
                 "back_train_date":'{0:04}-{1:02}-{2:02}'.format(self.dateStart.date().year(), self.dateStart.date().month(), self.dateStart.date().day()), 
                 "tour_flag":"dc", 
                 "purpose_codes":"ADULT", 
                 "query_from_station_name":self.station_name_dict[self.cmbFrom.currentIndex()][4].encode("utf-8"), 
                 "query_to_station_name":self.station_name_dict[self.cmbTo.currentIndex()][4].encode("utf-8"), 
                 "undefined":""
                 }
        self.print_log(u"提交订票信息。。。")
        submit_page=self.conn.post(self.submit_order_url, data=payload,headers=self.headers, verify=False)
        submit_page_json=submit_page.json()
        if submit_page_json["status"]==False:
            return False
        return True
        
    def load_confirm_page(self):
        payload={"_json_att":""}
        confirm_page=self.conn.post(self.confirm_url, data=payload,headers=self.headers, verify=False)
        confirm_page_text=confirm_page.text
        start_index=confirm_page_text.find("var globalRepeatSubmitToken = \'")+len("var globalRepeatSubmitToken = \'");
        end_index=confirm_page_text.find("\'", start_index);
        self.repeatToken=confirm_page_text[start_index:end_index]
        return confirm_page_text

    def clear_table_content(self):
        row=0
        col=0
        rowCount=self.tableTickets.rowCount()
        columnCount=self.tableTickets.columnCount()
        while row<rowCount:
            col=0
            while col<columnCount:
                item=self.tableTickets.item(row, col)
                item.setText(QtCore.QString(u""))
                item.setBackground(Qt.transparent)
                col=col+1
            row=row+1
        
    @pyqtSignature("int,int")
    def on_tableTickets_cellDoubleClicked(self, row, column):
        if column<5:return
        item=self.tableTickets.item(row, column)
        if item.text()==_fromUtf8(u"--"):
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8(u"当前车次不发售")+self.dict_table_column[column][1])
            msg.exec_()
            return
        if item.text()==_fromUtf8(u"无"):
            train_code=self.current_tickets[row]["queryLeftNewDTO"]["station_train_code"]
            if self.monitor_list.has_key(train_code):
                if column in self.monitor_list[train_code]:
                    self.monitor_list[train_code].remove(column)
                    if len(self.monitor_list[train_code])==0:
                        del self.monitor_list[train_code]
                    item.setBackground(Qt.transparent)
                else:
                    self.monitor_list[train_code].add(column)
                    item.setBackground(Qt.red)
            else:
                self.monitor_list[train_code]=set([column])
                item.setBackground(Qt.red)
            return
        self.print_log(u"开始订票")
        #check the user
        if self.check_the_user()==False:
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8(u"用户认证失败，请登录"))
            msg.exec_()
            return
        #submit tickets
        if self.submit_ticket(self.current_tickets[row])==False:
            msg=QtGui.QMessageBox()
            msg.setText(_fromUtf8(submit_page_json["messages"][0]))
            msg.exec_()
            return
        #load confirm page
        self.booking_form.confirm_page_text=self.load_confirm_page()
        self.booking_form.isDone=False
        self.booking_form.repeatToken=self.repeatToken
        index=0
        #set passengers checked in the booking form
        while index<len(self.passengers_menu_actions):
            if self.passengers_menu_actions[index].isChecked():
                self.booking_form.set_passenger_check_status(index, True)
            else:
                self.booking_form.set_passenger_check_status(index, False)
            index=index+1
        self.booking_form.ticket_infos=self.current_tickets[row]
        self.booking_form.set_train_info(self.current_tickets[row]["queryLeftNewDTO"], self.dateStart.date(), 
                                         self.dict_table_column[column][1], item.text())
        #start booking form
        self.booking_form.exec_()
        if self.booking_form.fresh_status==False:
            self.login_form.islogin=False
            self.action_login.setEnabled(True)
        #if booking failed, reload tickets infos
        if self.booking_form.isDone==False:
            t=datetime.datetime.now()
            posix_ms=int(time.mktime(t.timetuple()))*1000+(t.microsecond/1000)
            payload={"REPEAT_SUBMIT_TOKEN":self.repeatToken, 
                     "_json_att":"", 
                     "pre_step_flag":"preStep"}
            init_page=self.conn.post(self.repeat_init_url+str(posix_ms), data=payload, 
                                   headers=self.headers, verify=False)
            self.on_btnQuery_clicked()
        else:
            self.print_log(u"订票成功，请登录12306完成支付")
            
        

