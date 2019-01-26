# python_for_qingxiang

This is a project to gain information from qingxiang.com in python.

---
---

## INDEX

+ [main_post.py](#main_postpy)
    - [Classes and functions](#classes-and-functions)
        * [class planDB](#class-plandb)
        * [class qingxiangplan](#class-qingxiangplan)
    - [Problems and Solutions](#problems-and-solutions)
+ [img_download.py](img_downloadpy)
+ [comment.py](#commentpy)

---
---

## main_post.py

This file is used to gain some information from qingxiang.com and then stores it in a local database named planDB.db.

---

### Classes and functions

In this section, I will introduce the detail function of each class.

#### class planDB

This class is used to create a database named planDB which will store the main information of all stages in each plan.

* openDB

    Create a table and initialize it.

    **Parameters:**

    + planId: plan id.
    + stageId: stage id.
    + createdTs: the time stage was writed.
    + prasiseCount: the number of prasise in this stage.
    + commentCount: the number of comment in this stage.
    + html: the messages of this stage.
    + img: the urls of additional images in this stage.

* closeDB

    Close table after we insert all the information.

* insert

    Add the proper information into the database.

    **Parameters:**

    + plan: plan id.
    + stage: stage id.
    + createdtime: the time stage was writed.
    + prasisecount: the number of prasise in this stage.
    + commentcount: the number of comment in this stage.
    + htmlcontent: the messages of this stage.
    + img_urls: the urls of additional images in this stage. 

* show

    Show the table.

#### class qingxiangplan

* init

    Some base parameters.

    **Parameters:**

    - self.db: declare database name
    - self.headers: initialize the headers of JSON
    - self.planCode: stores both the name and order of the plan.

* plan_id

    Input plan id and current page number, and then get the information we need, following the insert.

    Firstly we are supposed to decide whether the plan name processing is in the plan list(that's self.planCode) and then we keep current page number and current plan name. After that, we can gain our goal information via URL connected by unread, urlbase and plan id. The plan id can be found by self.planCode[plan name].

    **Part Of the Parameters**

    - curplanname: the name of the current plan.
    - pgnb: the current page.
    - url: the correct URL of JSON.
    - req: the response of the required for information.
    - soup: the JSON part.
    - pagecount: the total number of the page.

* process

    The whole process from creating the database to gain information via qingxiang.com then show the database finally close it.

---

### Problems and Optimizations

#### Problems

It cost me a great time on gaining the har files and found the inner connections of the parameters.

I need to keep a watchful eyes on the source panel and open each response to see if this response was produced by my action.

#### Optimizations

I used cookies to sign in, and input plan name and plan code were used to get the true links. Finally, I input a list of plan names to start the python file.

It would be better to input user name and user password to sign in, then gain the list of plans, including plan names and plan orders, to gain the true links and then start the programme.

---
---

## img_download.py

This file is used to download all the images posted by the user in all the plans.

## comment.py

This file is used to store all the comment below every stage of the user.	
