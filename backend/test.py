schedule1=[1,2,3]
schedule2 = [4,5,6,7,8]
schedule3 = [7,8,9]
schedule4 = schedule3+schedule2+schedule1
schedule5 = list(set(schedule2) - set(schedule3))
print(schedule4)
print(schedule5)
room_serial_dict = {
    "Room101": "Serial001",
    "Room102": "Serial002",
    "Room103": "Serial003",
    # 添加更多的房间和序列号
}
k="Room104"
v="Serial004"
room_serial_dict[k] = v
print(room_serial_dict)
date_str = ('2023-12-06 12:22:38 ',)
formatted_date = date_str[0].strip()
print(formatted_date)
