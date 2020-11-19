Diarycards.com: my cs50x final project

Diarycards.com is a web application made with python, javaScript, SQL, HTML and CSS to solve a specific problem I and many of my
colleagues face in real life.

I am a participant in a Dialectical Behavioural Therapy (DBT) program, which runs for 9 months and involves recording on a daily basis
a wide variety of statistics relating to my emotional and physical wellbeing and actions throughout each day into a DBT Diary Card. To date, all
participants are provided with a double-sided sheet of paper with a 23x7 table on each side, which is filled in by pen or pencil and
handed to their individual therapist each week. The limitations of this paper-based system are large: data cannot be visualised at any speed, averages cannot be
calculated without time and human effort, each table only holds the past 7 days' worth of data and is discrete from all other tables,
and the environmental impact of printing all of these DBT Diary Cards has the potential to be greatly reduced, for example.

I decided to design and implement a web application that allows users to record their DBT Diary Card data on a central database
where we can employ all the power of a computer to interpret and visualise the user's input data in functional ways.

This python application references the SQL database named diarycards.db. There are four tables in this database,
namely 'users', 'diarycards', 'skills' and 'tips'. Users can sign up and log in to their account via the /signup and /login page respectfully. Users' data is saved in the 'users' table
of diarycards.db.

Once users have signed up and logged in, users can track and update their progress in their DBT diary cards and DBT skills.At
/updatecard, users can update their diary card, and the user's input data is stored in the 'diarycards' table. Users can then view
their past week's worth of diary card entries at /diarycard, and users can view their entire diary card input history at
/diarycardhistory.

At /updateskills, users can check which skills they have used each day and submit those skills to the 'skills' table. The user's skills
used in the past week are then displayed on /skills, and the user can view the entire history of their used skills at /skillshistory.
/skillshistory also displays to the user (via a db.execute() function call in application.py) their strongest and weakest skills
(measured by the frequency the user has used the skill, according to data input by the user to the 'skills' table). Users are able to
specify which module of DBT they are currently studying, which will result in the site displaying tips specific to the user from the
'tips' table in the SQL database.

The dashboard provides a summary of the user's average inputs over the past week for some key data points, and an embedded Twitter
feed from Dr Marsha Linehan, the founder of DBT.

Dynamic tips are displayed to the user depending on what statistics their diary card data averages to. Users are also able to add
their own custom tips at /tips, which will then be recorded in the 'tips' table along with their relevant module. These custom tips
will then be displayed to the user at relevant areas.
