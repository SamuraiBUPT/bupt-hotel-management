# bupt hotel management system
A hotel management system, Software Engineering, for bupt 2023 autumn course design.

# Project structure & planning
+ backend: Python flask, for faster developing.
+ frontend: Simple HTML, css, Javascript. `bootstrap` will be used for boosting the page structing.

Notice that we will build a front-backend split system, communicating with standard API.

# Quick start
## Front End

```bash
cd frontend
# install required packages
npm install

# run app
num run dev
```

## Back End
First you need to open your MySQL service.

Then you need to create a database (schema) called `backend`.

```sql
CREATE DATABASE 'backend';
USE 'backend';
```

You can start your service now:

```bash
cd backend
python3 server.py
```

Just use `pip install` to install any python package, which is required by the application.

# Stack
+ Vue3 (axios, element-plus)
+ Flask
+ pymysql


