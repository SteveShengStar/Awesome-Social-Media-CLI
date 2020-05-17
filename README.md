## ECE356 Project

### Created by:  
(Name, student number, user id)
- Qiyuan Bao, 20621162, q5bao
- Steven Siyu Xiong, 20661836, ssxiong

ER Diagram:
https://app.creately.com/diagram/Id97ysOhrTj/view and ER diagrams.zip


### Overview
- 
- ```scripts``` folder consist of SQL code to to create the tables, primary keys, foreign keys, and any additional indexes. Load the data from data folder.
- ```data``` folder consist of csv raw social media data
- ```commandLine.py``` is the prototype command line client consist of frontend and backend code.

### Setup
- Create database ```create database projecttest;```
- Use database ```use projecttest;```
- Under ```cd scripts``` directory ```use projecttest;``` then ```source CreateTables.sql;```
- Under ```cd data``` directory ```use projecttest;``` then ```source ../scripts/LoadData.sql```
- ```pip install click```
- ```pip install click_repl```
- ```pip install mysql-connector```
- In ```commandLine.py```, under ```startDb()``` function, change the ```host```, ```user```, and ```password``` parameters.

### Run
- Note you have to run all the commands inside the interactive shell
- Run the interactive shell with ```python3 commandLine.py repl```
- To check available commands run ```--help``` in the interactive shell

### Commands
#### Run these commands after you have enter the interactive shell with ```python3 commandLine.py repl```
  - For help, run ```--help``` and see the available commands.
  - Helpful tip, you can use ```tab``` to auto complete partially typed commands, arrow up and down to select as well.

#### Exit
- ```exit```

#### Account 
- ```signin```
- ```signingroup``` to login as group admin
- ```register```

#### Post
- ```myposts``` show posts made by the logged in user
- ```newpost```
- ```reactpost```
- ```readpost```
- ```deletepost```
- ```comment```
- ```showallpostsbyuser```

#### Unread Posts
- ```showunreadpostsbygroup```
- ```showunreadpostsbytopic```
- ```showunreadpostsbyuser```

#### Follow
- ```followgroup```
- ```followperson```
- ```followtopic```
- ```unfollowgroup```
- ```unfollowperson```
- ```unfollowtopic```

#### Friend
- ```acceptfriendrequests```
- ```addfriend```
- ```seefriends```
- ```friendrequestscreatedbyme```
- ```deletefriend```

#### Group
- ```creategroup```
- ```showallpostsbygroup```
- ```showmyfollowedgroups```
- ```grantgroupmembership```
- ```requestgroupmembership```
- ```showallgroupscmd``` Show a list of groups and their Group IDs
- ```showgroupswhereiamadmin```
- ```showgroupswhereiammember```

#### Topic
- ```showtopics```
- ```showmyfollowedtopics```
- ```showallpostsbytopic```





