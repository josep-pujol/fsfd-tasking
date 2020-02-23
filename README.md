# Task List

![Python](https://img.shields.io/static/v1?label=python&message=3.7.6&color=blue)
![Django](https://img.shields.io/static/v1?label=django&message=2.2.10&color=092E20)
[![Build Status](https://travis-ci.org/josep-pujol/fsfd-tasking.svg?branch=master)](https://travis-ci.org/josep-pujol/fsfd-tasking)
[![codecov](https://codecov.io/gh/josep-pujol/fsfd-tasking/branch/master/graph/badge.svg)](https://codecov.io/gh/josep-pujol/fsfd-tasking)

This repository contains a solution code for the milestone project of the *Full Stack Frameworks with Django* module at Code Institute. This is the last step to obtain the Diploma.

Consists on a "Tasks List" or "To-Do" application in which users can organize their tasks or to-dos. Users not only can create and update tasks but as well search, filter or sort tasks.

Most of the functionality is available for free, however users can get additional features by subscribing.
Subscribed users can create a To-Do list with a list of users of his/her choice, and collaborate online from their PC or mobile phone.

A demo of the app can be viewed [HERE](https://fsfd-tasking.herokuapp.com/)




## UX

### Free User
The app consists of three main sections: 

- Non registered users: Landing page and Sign-in Sign-up functionality

    ![Main page or Tasks page](https://github.com/josep-pujol/learning_dcd-task-list/blob/master/wireframes/tasks_mockup.png)

- Tasks: 
    - Section to manage different Task Lists or To-Do lists
    - The available Task Lists are:
        - "Personal Tasks": Tasks aimed only at the owner of the account - all features avilable 
        - "Assigned Tasks": Tasks assigned to the user from other registered users of Tasking - restricted features
        - "Completed Tasks": all the tasks completed by the user - restricted features

    ![Add Task](https://github.com/josep-pujol/learning_dcd-task-list/blob/master/wireframes/add_task_mockup.png)

- User: section for the owner of the account in which he can update profile or logout

    ![Completed Tasks](https://github.com/josep-pujol/learning_dcd-task-list/blob/master/wireframes/completed_tasks_mockup.png)


Additionally, modals and popup windows are used to perform actions like Edit the Status of a Task, Update any of the fields of a Task etc.

These actions can be activated by clicking on the menu-dots item on the right-hand side of each Task - if user has right permissions.




## Features

### Existing Features

- Main Page
    - Navigation links
    - Display tasks that are not completed
    - Pagination, including dropdown menu to select number of items per page
    - Search and Sorting functionality for all fields in the Table
    - Fixed floating button with tooltip, to add tasks
    - Menu-dots per Task which opens a window to:
        - Edit the Status of a Task
        - Edit any of the fields of a Task
        - Add or Remove the "Issues" sign

- Completed Tasks Page
    - Navigation links
    - Display tasks that are not completed
    - Pagination, including dropdown menu to select number of rows per page
    - Search and Sorting functionality for all fields in the Table
    
- Add and Edit Task Pages
    - Navigation links
    - Button to Cancel and go back to the Main Page
    - Button to Add and Store the Task
    - Insert the "Task Name" field; with validation
    - Select a "Task Category" from the dropdown menu or leave default option
    - Select a "Task Status" from the dropdown menu or leave default option
    - Add a text description
    - Select the "Due Date" of the Task from a Calendar popup window; with validation
    - Select the "Task Importance" from the dropdown menu or leave default option 



### Features Left to Implement
In the future, it could be nice to implement additional options to duplicate or delete a task.
As well, email notifications for:
 - A user has been added to a Team
 - A task has been assigned to a User
 - Optional alerts when the due date of a task is close



## Technologies Used

### The main technologies used are:
- [GitPod](https://gitpod.io/)
    - Online IDE used to develop this project
- [Python](https://www.python.org/)
    - Base language used for the application
- [Django](https://https://docs.djangoproject.com/en/2.2/)
    - Web application framework for **Python**
- **HTML**, **CSS** and **Javascript**
    - Base languages used to create the site frontend
- [Materialize](https://materializecss.com)
    - Used **Materialize 1.0.0** for a responsive layout and styling
- [DataTables](https://datatables.net)
    - Plugin for **jQuery** that adds interactive features to data stored in **HTML** tables
- [JQuery](https://jquery.com)
    - **JQuery** as a dependency for **DataTables**
- [Github](https://github.com)
    - Used as repository of the project 
- [ElephantSQL](https://www.elephantsql.com/)
    - PostgreSQL as a service used during development
- [Heroku](https://heroku.com)
    - To deploy the project
- [Heroku Postgres](https://elements.heroku.com/addons/heroku-postgresql)
    - Relational Database based on PostgreSQL as main point of information storage
- [Travis](https://travis-ci.org/)
    - Continuous integration and testing
- [Codecov](https://codecov.io/)
    - Coverage reports
- [SendGrid](https://sendgrid.com/)
    - SendGrid API is used to email users that request a password reset
- [Stripe](https://stripe.com/docs/api)
    - Stripe API to process payments in users subscritions 

## Testing
- Python Unit tests with over 90% coverage, including:
    - Page rendering
    - CRUD operations
   
- All code used on this site has been manually tested to ensure everything is working as expected. Some tests include:
    - Site responsiveness from small mobile up to 17" desktop screens
    - Content is displayed correctly for screens of small mobiles to 17" desktop screens
    - Functionality:
        - Loading all pages
        - Links and buttons are working
        - Popup windows and its contents are opening correctly
        - Popup windows are performing the intended actions
        - DataTables functionality like Search, Sort, Pagination and Table wrapping is working correctly
    - Data entry and editing
        - Added several tasks using major browsers
        - Added tasks with empty fields for validation
        - Added tasks with empty fields to test default values
- Site viewed and tested in the following browsers:
  - Google Chrome
  - Microsoft Edge
  - Mozilla Firefox




## Deployment
 
### Getting the code up and running
0. The following instructions are meant for a Linux System running Python3
1. First it is recommended to create a virtual environment
2. Create your own repository
3. Download or clone this repository by running the ```git clone <project's Github URL>``` command
4. Install Python packages from ```requirements.txt``` file - from Terminal type ```pip install -r requirements.txt```
5. Add the following environmental variables in your environment:
    - ```DATABASE_URL```: conection string to your Database. https://www.elephantsql.com/ was used in this project
    - ```IP```: set to ```0.0.0.0```
    - ```PORT```: set to ```8080```
    - ```SECRET_KEY```: Django secret key. You can generate one in this site https://djecrety.ir/
    - ```SENDGRID_API_KEY```: create a SendGrid account to get a key
    - ```STRIPE_PUBLIC_KEY```: create a Stripe account to get a key
    - ```STRIPE_SECRET_KEY```: create a Stripe account to get a key
6. To have the Database ready to run the app do the following in your Terminal (see below*):
    - Make migrations typing ```python3 manage.py makemigrations```
    - Migrate typing ```python3 manage.py migrate```
7. Run Unit tests to ensure everything is working properly, type ```python3 manage.py test``` in your Terminal 

### Deploy in Heroku
0. If previous steps ran successfully, do the following to deploy the app in Heroku 
1. Frist you need to create an account in Heroku
2. Create an Heroku app
3. In the "Resources" section Add the Heroku Postgres add-on
4. In the "Settings" section make sure you have the same environmental variables previously discussed
5. In the "Deploy" section: 
    - Select "GitHub" as a source in the "Deployment method" subsection 
    - Click the "Deploy Branch" button in the "Manual Deploy" subsection
6. Open the given Heroku url to test that the application is up and running
7. If issues, please have a look at the deployment logs in Heroku


*Notice that migrations automatically create options for the Dropdown menus
    - ```task_category``` with a single field name ```category```. 
        - Add any category names you like plus the default value ```Undefined```
    - ```task_importance``` with two fields named ```importance``` and ```order```. 
        - Add any levels of task importance you like with their associated order 
        - Make sure you add the default value ```Low``` with order ```1```, which will be the lowest level of importance
    - ```task_status``` with two fields named ```status``` and ```order```. 
        - Add any status you like plus their associated order
        - Make sure you add the default values ```Not started``` with order ```0```, and ```Completed``` which show have the highest order




## Credits
Inspired by the [Materialize](https://materializecss.com) admin dashboards built by [Pixinvent.com](https://pixinvent.com/materialize-material-design-admin-template/html/ltr/vertical-modern-menu-template/)

Many thanks to my mentor [Sindhu Kolli](https://github.com/itssindhu13) for her great advise and suggestions.