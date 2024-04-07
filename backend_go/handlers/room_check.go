package handlers

import (
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

	room_number, _ := strconv.Atoi(form.RoomNumber) // update local data: for scheduler
	op := scheduler.UpdateOperation{
		Types:  []string{"Name", "CheckinDate", "ShowDetail", "IdCard", "HaveCheckedin"},
		RoomID: room_number,
		Values: []string{form.Name, formated_time, form.ShowDetails, form.IdCard, strconv.FormatBool(have_check_in)},
	}
	scheduler.Sche.UpdateChan <- op // here we send the data through the channel to the scheduler
	c.JSON(200, gin.H{
		"message": "Check in successfully",
	})

}

func CheckOut(c *gin.Context) {

}
