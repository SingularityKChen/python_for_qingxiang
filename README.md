# python_for_qingxiang

This is a project to gain information from qingxiang.com in python.

## INDEX

+ [main_post.py](https://github.com/SingularityKChen/python_for_qingxiang/blob/master/README.md#main_postpy)

	- [Classes and functions](https://github.com/SingularityKChen/python_for_qingxiang/blob/master/README.md#classes_and_functions)

		* [class planDB](https://github.com/SingularityKChen/python_for_qingxiang/blob/master/README.md#class_plandb)

		* [class qingxiangplan](https://github.com/SingularityKChen/python_for_qingxiang/blob/master/README.md#class_qingxiangplan)

	- [Problems and Solutions](https://github.com/SingularityKChen/python_for_qingxiang/blob/master/README.md#problems_and_solutions)

+ img_download.py

+ comment.py

## main_post.py

### Classes and functions

#### class planDB

This class is used to create a database named planDB which will store the main information of all stages in each plan.

* openDB

	Create table and initialize it.

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

	- self.headers: initialize the headers of json

	- self.planCode: stores both the name and order of the plan.

* plan_id

	Input plan id and current page munber, and then get the information we need, following the insert.

	Firstly we are supposed to decide whether the plan name processing is in the plan list(that's self.planCode) and then we keep current page number and current plan name. After that, we can gain our goal information via url connected by unread, urlbase and plan id. The plan id can be found by self.planCode[plan name].

	**Part Of the Parameters**

	- curplanname: the name of current plan.

	- pgnb: the current page.

	- url: the correct url of json.

	- req: the response of the require for information.

	- soup: the json part.

	- pagecount: the total number of page.

* process

	The whole process from create the database to gain information via qingxiang.com then show the database finally close it.


### Problems and Solutions
