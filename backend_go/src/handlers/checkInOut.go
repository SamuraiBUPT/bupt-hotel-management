package handlers

import (
	"backend_go/db_utils"

	"github.com/gin-gonic/gin"
)

type CheckInRequest struct {
	RoomNumber int    `json:"room_number"`
	ClientName string `json:"clientName"`
	ClientID   string `json:"clientID"`
}

type CheckOutRequest struct {
	RoomNumber int `json:"room_number"`
}

// 整体思路：优先进行数据库IO，然后将信息传递给scheduler
func CheckIn(c *gin.Context) {
	formatted_time := GetCurrentTime()

	var form CheckInRequest
	if err := c.BindJSON(&form); err != nil {
		c.JSON(400, gin.H{
			"error": err.Error(),
		})
		return
	}

	// db IO first
	sql := "INSERT INTO room_infos (room_id, client_id, client_name, checkin_time, state, current_speed, current_tempera) values (?,?,?,?,?, ?, ?)"
	if err := db_utils.DB.Exec(sql, form.RoomNumber, form.ClientID, form.ClientName, formatted_time, 1, "medium", 24.0).Error; err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	// send message to scheduler to update local data for schedule
	// op := scheduler.SchedulerTask{
	// 	Types:  []string{"Name", "CheckinDate", "ShowDetail", "IdCard", "HaveCheckedin"},
	// 	RoomID: room_number,
	// 	Values: []string{form.Name, formated_time, form.ShowDetails, form.IdCard, strconv.FormatBool(have_check_in)},
	// }
	// scheduler.Sche.TaskChan <- &op // here we send the operation message ptr through the channel to the scheduler

	c.JSON(200, gin.H{
		"message": "Check in successfully",
	})
}

func CheckOut(c *gin.Context) {
	var form CheckOutRequest
	if err := c.BindJSON(&form); err != nil {
		c.JSON(400, gin.H{
			"error": err.Error(),
		})
		return
	}
	formatted_time := GetCurrentTime()

	sql := "UPDATE room_infos SET checkout_time =?, state = 0 WHERE room_id =?"
	if err := db_utils.DB.Exec(sql, formatted_time, form.RoomNumber).Error; err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	// TODO: 通知结算系统进行结算

	c.JSON(200, gin.H{
		"message": "Check in successfully",
	})
}
