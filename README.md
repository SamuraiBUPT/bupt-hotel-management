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

---

# 2023-12.07 update
上面的都是在画饼放屁，这里才是真话。

前端写得一坨屎，我自己主导负责的，主打一个能跑就行，部分工程架构**或许**有参考价值。

后端才是我们项目的重点，考虑空调管理系统的需求背景，我们实现了调度算法，包括：

+ 时间片调度
+ 风速优先级

这两个调度算法的implement就是后端的**价值所在**。

__已知存在的问题__

后端与数据库的交互部分时不时会崩掉，原因未知，但是大多数时候是能跑的。（不清楚到底是他妈网络的问题还是电脑与MySQL Connection的问题还是他妈的代码的问题，不过从报错信息上来看似乎是使用连接的方式有问题，后人可以完善一下连接池的处理）



[![LICENSE](https://img.shields.io/badge/license-傻逼软件工程-blue.svg?style=flat-square)](https://zh.wikipedia.org/wiki/%E8%BD%AF%E4%BB%B6%E5%B7%A5%E7%A8%8B)
