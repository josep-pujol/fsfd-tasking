![Tasking mockups](readme_files/multidevice_mockups.png?raw=true "Tasking mockups")

# Tasking

![Python](https://img.shields.io/static/v1?label=python&message=3.7.6&color=blue)
![Django](https://img.shields.io/static/v1?label=django&message=2.2.10&color=092E20)
[![Build Status](https://travis-ci.org/josep-pujol/fsfd-tasking.svg?branch=master)](https://travis-ci.org/josep-pujol/fsfd-tasking)
[![codecov](https://codecov.io/gh/josep-pujol/fsfd-tasking/branch/master/graph/badge.svg)](https://codecov.io/gh/josep-pujol/fsfd-tasking)

This repository contains a solution code for the milestone project of the *Full Stack Frameworks with Django* module at [Code Institute](https://codeinstitute.net/). This is the last step to obtain the Diploma.

Consists on a "Tasks List" or "To-Do" application in which users can organize their tasks or to-dos. Users not only can create and update tasks but as well search, filter or sort tasks.

Most of the functionality is available for free, however users can get additional features by subscribing.
Subscribed users can create a To-Do list with a list of users of his/her choice, and collaborate online from their PC or mobile phone.

A demo of the app can be viewed [HERE](https://fsfd-tasking.herokuapp.com/)

<br>
<br>

## Table of Contents
1. [**UX**](#ux)
    - [**User Stories**](#user-stories)
    - [**Free User**](#free-user)
    - [**Premium User**](#premium-user)

2. [**Features**](#features)
    - [**Existing Features**](#existing-features)
    - [**Features Left to Implement**](#features-left-to-implement)

3. [**Technologies Used**](#technologies-used)

4. [**Testing**](#testing)

5. [**Deployment**](#deployment)
    - [**Getting the code up and running**](#getting-the-code-up-and-running)
    - [**Deploy in Heroku**](#deploy-in-heroku)
    - [**Database initial values**](#database-initial-values)
    - [**Database Schema**](#database-schema)

6. [**Credits**](#credits)


##### back to [top](#tasking)

<br>
<br>

## UX

### Free User
The app consists of three main sections: 

- Non registered users: Landing page with Sign-in and Sign-up functionality

    ![Main page or Tasks page](https://github.com/josep-pujol/learning_dcd-task-list/blob/master/wireframes/tasks_mockup.png)

- Tasks: 
    - Section to manage different Task Lists or To-Do lists
    - The available Task Lists are:
        - "Personal Tasks": Tasks aimed only at the owner of the account - all features avilable 
        - "Assigned Tasks": Tasks assigned to the user from other registered users of Tasking - restricted features
        - "Completed Tasks": all the tasks completed by the user

    ![Add Task](https://github.com/josep-pujol/learning_dcd-task-list/blob/master/wireframes/add_task_mockup.png)

- User: section for the owner of the account in which the user profile can be updated and from where you can logout

    ![Completed Tasks](https://github.com/josep-pujol/learning_dcd-task-list/blob/master/wireframes/completed_tasks_mockup.png)


Additionally, modals and popup windows are used to perform actions like Edit the Status of a Task, Update any of the fields of a Task etc.

These actions can be activated by clicking on the menu-dots item on the right-hand side of each Task - if user has right permissions.

### Premium User

A Premium user has all the sections and features of a Free User plus the following:
- Tasks: 
    - "Team Tasks": Tasks that the Team Lead or Team Owner assign to other users - all features avilable 
- User:
    - "Team": where a Team owner manage the users in the Team

##### back to [top](#tasking)

<br>
<br>

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
In the future, it could be nice to implement additional options to duplicate or delete tasks, and to allow a Team owner to remove a user from his/her Team.
manage categories so users can add or remove the default ones. 
As well, the posibility to manage categories or to get alerts and notifications could be a nice features to implement.

##### back to [top](#tasking)

<br>
<br>

## Technologies Used

The main technologies used are:
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

##### back to [top](#tasking)

<br>
<br>

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

### Chrome DevTools Audit
- Files with the tests ran in Chrome DevTools Audit can be found in this repository folder [test_files](readme_files/test_files "Chrome DevTools Audit"). The tests were done on the [landing](https://fsfd-tasking.herokuapp.com/) and the [Tasks](https://fsfd-tasking.herokuapp.com/) pages
- As a summary:
    - Landing Page: results about 90 for Performance, Accessibility, Best Practices and SEO
    - Tasks Page: results around 70 for Performance and Best Practices, and about 90 for Accessibility and SEO
    - Runtime settings: 
        - Emulated Nexus 5X device
        - User Agent (network) Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36


##### back to [top](#tasking)

<br>
<br>

## Deployment
 
### Getting the code up and running
0. The following instructions are meant for a Linux System running Python3
1. First it is recommended to create a virtual environment
2. Create your own repository
3. Download or clone this repository by running the ```git clone <project's Github URL>``` command
4. Install Python packages from ```requirements.txt``` file - from Terminal type ```pip install -r requirements.txt```
5. Add the following environmental variables in your environment:
    - ```DATABASE_URL```: conection string to your Database. [elephantsql](https://www.elephantsql.com/) was used in this project
    - ```IP```: set to ```0.0.0.0```
    - ```PORT```: set to ```8080```
    - ```SECRET_KEY```: Django secret key. You can generate one on the site [djecrety](https://djecrety.ir/)
    - ```SENDGRID_API_KEY```: create a SendGrid account to get a key
    - ```STRIPE_PUBLIC_KEY```: create a Stripe account to get a key
    - ```STRIPE_SECRET_KEY```: create a Stripe account to get a key
6. To have the Database ready to run the app do the following in your Terminal (see below*):
    - Make migrations typing ```python3 manage.py makemigrations```
    - Migrate typing ```python3 manage.py migrate```
    - Notice a default superuser is created with username and password ```admin```
7. Run Unit tests to ensure everything is working properly, type ```python3 manage.py test``` in your Terminal
8. Go to Django Admin and change the default Superuser password


### Deploy in Heroku
0. If previous steps ran successfully, do the following to deploy the app in Heroku 
1. Frist you need to create an account in Heroku
2. Create an Heroku app
3. In the "Resources" section Add the "Heroku Postgres" add-on
4. In the "Settings" section make sure you have the same environmental variables previously discussed
5. In the "Deploy" section: 
    - Select "GitHub" as a source in the "Deployment method" subsection 
    - Click the "Deploy Branch" button in the "Manual Deploy" subsection
6. Open the given Heroku url to test that the application is up and running
7. Go to Django Admin and change the default Superuser password
8. If issues, please have a look at the deployment logs in Heroku


### Database initial values
The Database migrations automatically create a superuser and the following tables with default values:
- ```superuser``` : the administrator user to access Django Admin, with credentials username  ```admin``` and password  ```admin``` 
- ```team_team``` (table): table that stores information related to Teams
    - A default Team called ````tasking``` is set for all users
- ```team_userteam``` (table): table to store the relationship of a User with a Team. In other words, which Users belong to each Teams
    - A relationship between the default Team ```tasking``` and all users is created by default
    - The superuser ```àdmin``` is the Team Owner of ```tasking``` Team
- ```task_category``` (table): used in dropdown menus to classify the tasks in different category groups 
    - The category groups are:  ```undefined```,  ```admin```, ```meetings```, ```other```, ```planning```, ```projects```, ```training``` and ```travel```   
- ```task_importance``` (table): with values to define the importance or urgency of a Task to be completed
    - A Task can be labelled with Importance values: ```low```, ```medium``` and ```high```
- ```task_status``` (table): provide information to the user about the degree of completion of a Task, and sets the start and completed date of a Task
    - The status available are: ```not started```, ```started```, ```25%```, ```50%```, ```75%``` and ```completed```
    - Notice that some status modify the start or completed date of a Task:
        - For example, when the status ```started``` is selected, the Task start date is set to current date
        - When the status ```completed``` is selected, the Task completed date is set to current date

### Database Schema
![Database schema](readme_files/database_schema.png?raw=true "Database Schema")


##### back to [top](#tasking)

<br>
<br>

## Credits
Inspired by the [Materialize](https://materializecss.com) admin dashboards built by [Pixinvent.com](https://pixinvent.com/materialize-material-design-admin-template/html/ltr/vertical-modern-menu-template/).
Wallpaper images taken from [pixabay.com](https://pixabay.com/), and multidevice mockups, on this README file, were generated on [techsini.com](http://techsini.com/multi-mockup/).

Many thanks to my mentor [Sindhu Kolli](https://github.com/itssindhu13) for her great advise and suggestions.

##### back to [top](#tasking)
