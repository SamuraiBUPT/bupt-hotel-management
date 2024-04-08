# 设计方案

业务层面的东西，任何一个请求到来了，应该先在业务方面做修改，业务稳定了，再向数据库发送持久化请求。



从请求侧来区分：

首先是可能造成层删改的请求：

+ /api/rooms/checkIn  可能有新记录建立
+ /api/rooms/checkOut  有新记录建立、有修改
+ /api/turn_on   有建立、修改
+ /api/turn_off  有建立、修改
+ /api/setTemperature
+ /api/setTemperature_init
+ /api/setSpeed
+ /api/query_room_info/
+ /api/rooms/updateRooms



只有查的请求：

+ /api/login
+ /api/query_room_bill
+ /api/query_schedule
+ /api/detail_bill
+ /api/form/roomList



不想进行数据库的设计工作，也就是不想设计接口，在我们这里全部使用嵌入式SQL语句。

# TODO
把Python的后端全部重构，摒弃所有架构，从头开始实现一个server，而不是照搬py的框架。