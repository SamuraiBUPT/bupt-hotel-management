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
