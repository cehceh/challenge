# challenge
Making Events App.
 
Building two app. in this project because it is so small,
Files are arranged as follow :

1- accounts app. for handeling the authintication of users.

2- events app. for handeling the entire process of create and edit events for every users and make join to an event or withdraw. 

3- we replaced views.py file in events app by a folder called views to facilitate arranging project files as follow. 
  a- home.py    b- events.py    c- participants.py    d- deleted_events.py    e- auto_join.py
 
4- templates are arranged as (main templates folder under the main project) as follow.
  a- account folder  b- home folder  c- base.html  d- dashboard.html  e- frontpage.html

5- all templates for events app in this path events/templates/events/

6- all tables in this app. are collected in tables folder with tables.py under events app.

7- templates for tables are collected in this path events/templates/events/tables/
   
8- we use postgresql databse as it appears in settings.py file

9- this project built on linux platform so if you try to use requirements.txt on another plateform like windows 
   you must redownload and resetup some liberaries like "psycopg2" on your target plateform
 
10- you will find a "run" file it enables you to run django project easy it consists of:(interminal type : source run)
   a- make activate the environment  b- restart the postgresql service
   c- make collectstatic             e- makemigrations and migrate the databse 

