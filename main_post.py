# -*- coding: utf-8 -*-
from typing import Dict, Any
import requests
import sqlite3
import json
from bs4 import UnicodeDammit

##################################################
##################################################
# create a new database
class planDB():
    def __init__(self):
        self.con = sqlite3.connect('plan.db') # connect to database
        self.cursor = self.con.cursor()

    def openDB(self):
        sql_table = '''create table plan_table (planId int (8),stageId int (8), createdTs int (16),praiseCount int (4),commentCount int (4),html varchar (8000),img varchar (8000),constraint pk_plan primary key (planId,stageId))'''
        try:
            self.cursor.execute(sql_table)
            print("create table successfully")
        except Exception as err:
            self.cursor.execute("delete from plan_table")
            print("create table failed")
            print(err)

    def closeDB(self):
        self.con.commit()
        self.con.close()

    def insert(self, plan, stage, createdtime, prasisecount, commentcount, htmlcontent, img_urls): # insert data into this database
        sql_insert = "insert into plan_table (planId,stageId,createdTs,praiseCount,commentCount,html,img)values (?,?,?,?,?,?,?)"
        sql_insertpara = (plan, stage, createdtime, prasisecount, commentcount, htmlcontent, img_urls)
        try:
            self.cursor.execute(sql_insert,sql_insertpara)
            print("insert successfully")
        except Exception as err:
            print("insert failed")
            print(err)

    ###############################################
    # this function is unfished

    def show(self):
        self.cursor.execute("pragma table_info(plan_table)")
        print(self.cursor.fetchall())


###############################################
###############################################
# noinspection PyTypeChecker
class qingxiangplan():
    def __init__(self):
        self.db = planDB()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh,en-US;q=0.7,en;q=0.3",
            "Connection": "keep-alive",
            "Cookie": "rememberme=; "
                      "PLAY_SESSION= "
        } # specialise the headers
        self.planCode = {"plan_name_1": "plan_id_1", "plan_name_2": "plan_id_2"}

    def plan_id(self, plan, pagenumber):
        if plan not in self.planCode.keys():
            print(plan + "planId cannot be found")
            return
        curplanname = plan
        pgnb = str(pagenumber)
        print("curplanname=",curplanname) # check curplanname
        print(pgnb)
        unread = "http://www.lianzai.me/api/v2/stage/stages?planUid=******&loginUid=******0&planId="
        urlbase = "&isOrderByCreatedTsDesc=true&curPage="
        url = unread + self.planCode[plan] + urlbase + pgnb + "&pageSize=15" # specialise the get url
        try:
            req = requests.get(url, headers=self.headers)
            print(req.json())
            soup = req.json() # translate json
            curpage = soup.get('curPage')
            pagecount = soup.get('pageCount')
            data_result = soup.get('results')
            planstage = data_result.get('planStages')
            curplanid = planstage[0].get('planId')
            print("curpage=",curpage)
            print("pagecount=",pagecount)
            print("curplanid=",curplanid)
            for i in range(len(planstage)):
                try:
                    stageid = planstage[i].get('stageId')
                    createdtime = planstage[i].get('createdTs')
                    praisecount = planstage[i].get('praiseCount')
                    commentcount = planstage[i].get('commentCount')
                    htmltext = planstage[i].get('html')
                    imglink = planstage[i].get('img')
                    self.db.insert(curplanid,stageid,createdtime,praisecount,commentcount,htmltext,imglink)
                except Exception as err:
                    print("fail to insert loop",err)
            if pagecount >= curpage + 1:
                nextpage = str(curpage+1)
                print("nextpage=",nextpage)
                curplanid = str(curplanid)
                self.plan_id(curplanname,nextpage)

        except Exception as err:
            print(err)

    def process(self, plans,pagenumber):
        """

        :type plans: object
        """
        self.db.openDB()
        for plan in plans:
            self.plan_id(plan,pagenumber) # run self.plan_id for all plans

        self.db.show()
        self.db.closeDB()


mian_process = qingxiangplan()
mian_process.process(["plan_name_1","plan_name_2","..."],1)
print("completed")
    
