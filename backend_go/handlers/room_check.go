package handlers

import (
	"backend_go/db_utils"
	"backend_go/scheduler"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
)

type CheckInRequest struct {
	RoomNumber  string `json:"room_number"`
	CheckinDate string `json:"checkInDate"`
	HaveCheckin string `json:"haveCheckIn"`
	Name        string `json:"name"`
	IdCard      string `json:"idCard"`
	ShowDetails string `json:"showDetails"`
}

type CheckOutRequest struct {
	RoomNumber string `json:"room_number"`
}

func CheckIn(c *gin.Context) {
	check_in_time := time.Now()
	formated_time := check_in_time.Format("2006-01-02 15:04:05")
	have_check_in := true

	var form CheckInRequest
	if err := c.BindJSON(&form); err != nil {
		c.JSON(400, gin.H{
			"error": err.Error(),
		})
		return
	}

	// send message to scheduler to update local data for schedule
	room_number, _ := strconv.Atoi(form.RoomNumber) // update local data: for scheduler
	op := scheduler.UpdateOperation{
		Types:  []string{"Name", "CheckinDate", "ShowDetail", "IdCard", "HaveCheckedin"},
		RoomID: room_number,
		Values: []string{form.Name, formated_time, form.ShowDetails, form.IdCard, strconv.FormatBool(have_check_in)},
	}
	scheduler.Sche.UpdateChan <- op // here we send the operation message through the channel to the scheduler

	// db IO
	// update schedule_boards table
	sql_1 := "UPDATE schedule_boards SET name = ?, checkin_date = ?, show_detail = ?, id_card = ?, have_checkedin = ? where id = ?"
	if err := db_utils.DB.Exec(sql_1, form.Name, formated_time, form.ShowDetails, form.IdCard, have_check_in, room_number).Error; err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	record_num := NextRecord()
	sql_2 := "INSERT INTO checkboards (record, idcard, room_id, checkin_date, checkout_date, state) VALUES (?, ?, ?, ?, ?, ?)"
	if err := db_utils.DB.Exec(sql_2, record_num, form.IdCard, room_number, formated_time, "", '1').Error; err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	sql_3 := "INSERT INTO bills (room_id, record, checkin_date, checkout_date, cost) VALUES (?, ?, ?, ?, ?)"
	if err := db_utils.DB.Exec(sql_3, record_num, room_number, formated_time, "", 0).Error; err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	sql_4 := "INSERT INTO users (account, password, identity) VALUES (?, ?, ?)"
	if err := db_utils.DB.Exec(sql_4, form.RoomNumber, form.IdCard, "2").Error; err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	c.JSON(200, gin.H{
		"message": "Check in successfully",
	})
}

func CheckOut(c *gin.Context) {
	// check_in_time := time.Now()
	// formated_time := check_in_time.Format("2006-01-02 15:04:05")

	// var form CheckInRequest
	// if err := c.BindJSON(&form); err != nil {
	// 	c.JSON(400, gin.H{
	// 		"error": err.Error(),
	// 	})
	// 	return
	// }
	// room_number, _ := strconv.Atoi(form.RoomNumber)

	// // 查看空调状态：是否为关机，不是关机就计算费用。
	// sql := "SELECT power from schedule_boards where id = ?"
	// var power string
	// if err := db_utils.DB.Raw(sql, room_number).Scan(&power).Error; err != nil {
	// 	c.JSON(500, gin.H{
	// 		"error": err.Error(),
	// 	})
	// 	return
	// }
	// if power != "0" {

	// }
}
