  # -*- coding: utf-8 -*-
from typing import Dict, Any
from bs4 import UnicodeDammit
import sqlite3
import urllib.request
import os
import sys
import socket
import requests
import json

##################################################
##################################################
# create database of comment
class commentDB():
    def __init__(self):
        self.con = sqlite3.connect('comment.db')
        self.cursor = self.con.cursor()


    def openDB(self):
        sql_table = '''create table comment_table (planId int (8),stageId int (8),commentText varchar (8000),commentParentUid int (6),commentParentId int (6),commentAuthorUid int (6),commentAuthorNick varchar (5000),commentparentNick varchar (5000),createdTs int (16),createdTsStr varchar (20),commentId int (6),constraint pk_createdTs primary key (commentId))'''
        try:
            self.cursor.execute(sql_table)
            print("create table successfully")
        except Exception as err:
            self.cursor.execute("delete from comment_table")
            print("create table failed")
            print(err)

    def closeDB(self):
        self.con.commit()
        self.con.close()

    def insert(self, plan, stage, commenttext, compauid, compaid, comauid, comaunick, companick, createdtime, createdtimestr, commentid):
        sql_insert = "insert into comment_table (planId, stageId, commentText, commentParentUid, commentParentId, commentAuthorUid, commentAuthorNick, commentparentNick, createdTs, createdTsStr,commentId)values (?,?,?,?,?,?,?,?,?,?,?)"
        sql_insertpara = (plan, stage, commenttext, compauid, compaid, comauid, comaunick, companick, createdtime, createdtimestr, commentid)
        try:
            self.cursor.execute(sql_insert,sql_insertpara)
            print("insert successfully")
        except Exception as err:
            print("insert failed")
            print(err)

    ###############################################
    # this function is unfinished

    def show(self):
        #self.cursor.execute("select * from plan_table")
        #rows = self.cursor.fetchall()
        self.cursor.execute("pragma table_info(comment_table)")
        print(self.cursor.fetchall())

class avatarDB(): # create avatarDB to store users' icons
    def __init__(self):
        self.con = sqlite3.connect('avatar.db')
        self.cursor = self.con.cursor()

    def openDB(self):
        sql_table = '''create table avatar_table (uid int (8),nickName varchar (200),avatarurl varchar (1000),constraint pk_plan primary key (uid))'''
        try:
            self.cursor.execute(sql_table)
            print("create table avatar_table successfully")
        except Exception as err:
            self.cursor.execute("delete from avatar_table")
            print("create table avatar_table failed")
            print(err)

    def readDB(self):
        self.cursor.execute("pragma table_info(Faces)")

    def closeDB(self): # close the database after we add all the information
        self.con.commit()
        self.con.close()

    def close_readDB(self): # close the database after we read the information we need
        self.mydb.commit()
        self.mydb.close()

    def insert(self, uid, nickName, avatarurl):
        sql_insert = "insert into avatar_table (uid, nickName, avatarurl)values (?,?,?)"
        sql_insertpara = (uid, nickName, avatarurl)
        try:
            self.cursor.execute(sql_insert,sql_insertpara)
            print("avatar insert successfully")
        except Exception as err:
            print("avatar insert failed")
            print(err)

    def avatar_find(self):
        avatardetail = self.cursor.execute("SELECT uid,avatarurl from avatar_table")
        avatardload = avatarprocess()
        for row in avatardetail:
            uid = row[0]
            avatarurl = row[1]
            path_start = '**'
            cur_path = str(path_start) + 'uimg'
            file_name = cur_path + '\\' + str(uid) + '.jpg'
            try:
                avatardload.uimg_download(avatarurl,file_name)
                print('the icon of user', uid, "is finished")
            except socket.timeout:
                count: int = 1
                while count <=5:
                    try:
                        avatardload.download.uimg_download(url,file_name)
                    except socket.timeout:
                        err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
                        print(err_info)
                        count += 1
                if count > 5:
                    print("downloading picture fialed!")
            continue
    ###############################################
    # this function is unfinished

    def show(self):
        #self.cursor.execute("select * from plan_table")
        #rows = self.cursor.fetchall()
        self.cursor.execute("pragma table_info(comment_table)")
        print(self.cursor.fetchall())
###############################################
###############################################
# noinspection PyTypeChecker


#sys.setrecursionlimit(100000)
socket.setdefaulttimeout(30)

class planDB(): # we need to read some information from planDB to know whether this stage was commented
    def __init__(self):
        self.mydb = sqlite3.connect("plan.db")
        self.cursor = self.mydb.cursor()
        self.comment = commentDOWNLOAD()

    def openDB(self):
        self.cursor.execute("pragma table_info(Faces)")
        # print(self.cursor.fetchall())

    def closeDB(self):
        self.mydb.commit()
        self.mydb.close()

    def commentnum(self):
        commentdetail = self.cursor.execute("SELECT planId,stageId,commentCount from plan_table")
        comment_process = commentDOWNLOAD()
        comment_process.db.openDB()
        avatar_process = avatarprocess()
        avatar_process.db.openDB()
        for row in commentdetail:
            planid = row[0]
            stageid = row[1]
            if row[2] != 0:
                comment_process.commentget(planid,stageid)
                avatar_process.uiming_url_save(planid,stageid)
                print("completed")
            else:
                print('plan', planid, "stage", stageid, "has no comment")

        comment_process.db.show()
        comment_process.db.closeDB()
        avatar_process.db.show()
        avatar_process.db.closeDB()

class avatarprocess(): # to download the users' icons
    def __init__(self):
        self.db = avatarDB()

    def uiming_url_save(self, plan, stage):
        curplanname = plan
        curstage = stage
        print("curplanname=",curplanname)
        print("curstage=", curstage)
        url = "http://www.lianzai.me/lianzai/CommentCtrl/showPlanComment"
        params = {
            "planId" : plan,
            "stageId" : stage,
            "curPage" : "1",
            "pageSize" : "15"
        }
        headers = {
            "Host": "www.lianzai.me",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://www.lianzai.me/planDetail/******/" + str(plan) + ".html",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Content-Length": "51",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": "PLAY_SESSION=********************;"
                      "rememberme=************"
        }
        try:
            print("try get comment json")
            req = requests.post(url,headers=headers, data=params )
            print(req.json())
            soup = req.json()
            data_result = soup.get('results')
            for i in range(len(data_result)):
                try:
                    print(i)
                    comauid = data_result[i].get('commentAuthorUid')
                    comaunick = data_result[i].get('commentAuthorNick')
                    avatarurl = data_result[i].get('avatar')
                    print('try to insert information into avatardb')
                    self.db.insert(comauid, comaunick, avatarurl)
                except Exception as err:
                    print("fail to insert loop of avatar",err)


        except Exception as err:
            print("error")
            print(err)

    def uimg_download(self,url,filename):
        try:
            urllib.request.urlretrieve(url, filename)
        except OSError:
            pass


class commentDOWNLOAD(): # to store the comment and some additional information
    def __init__(self):
        self.db = commentDB()


    def commentget(self, plan, stage):
        curplanname = plan
        curstage = stage
        print("curplanname=",curplanname)
        print("curstage=", curstage)
        url = "http://www.lianzai.me/lianzai/CommentCtrl/showPlanComment"
        params = {
            "planId" : plan,
            "stageId" : stage,
            "curPage" : "1",
            "pageSize" : "15"
        }
        headers = {
            "Host": "www.lianzai.me",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh,en-US;q=0.7,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://www.lianzai.me/planDetail/******/" + str(plan) + ".html",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Content-Length": "51",
            "X-Requested-With": "XMLHttpRequest",
            "DNT": "1",
            "Connection": "keep-alive",
            "Cookie": "PLAY_SESSION=*************;"
                      "rememberme=***************"
        }
        try:
            print("try get comment json")
            req = requests.post(url,headers=headers, data=params )
            print(req.json())
            soup = req.json()
            data_result = soup.get('results')
            for i in range(len(data_result)):
                try:
                    print(i)
                    plan = data_result[i].get('planId')
                    stage = data_result[i].get('stageId')
                    commenttext = data_result[i].get('comment')
                    compaid = data_result[i].get('commentParentId')
                    compauid = data_result[i].get('commentParentUid')
                    comauid = data_result[i].get('commentAuthorUid')
                    comaunick = data_result[i].get('commentAuthorNick')
                    companick = data_result[i].get('commentParentNick')
                    createdtime = data_result[i].get('createdTs')
                    createdtimestr = data_result[i].get('createdTsStr')
                    commentid = data_result[i].get('commentId')
                    print('try to insert information into commentdb')
                    self.db.insert(plan, stage, commenttext, compauid, compaid, comauid, comaunick, companick, createdtime, createdtimestr ,commentid)
                except Exception as err:
                    print("fail to insert loop of comment database bacause",err)


        except Exception as err:
            print("error")
            print(err)


class start_process_save():
    def __init__(self):
        self.db = planDB()

    def process(self):
        self.db.commentnum()

class start_process_download():
    def __init__(self):
        self.db = avatarDB()

    def process(self):
        self.db.readDB()
        self.db.avatar_find()

m_process = start_process_save()
m_process.process()
a_process = start_process_download()
a_process.process()
