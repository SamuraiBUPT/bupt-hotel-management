package db_utils

import (
	"gorm.io/gorm"
)

type Room struct {
	Room_id int32
	Bill    float32
	Status  string
	gorm.Model
}

type Bill struct {
	RoomID       int32 `gorm:"primary_key"`
	Record       int32
	CheckinDate  string  `gorm:"type:varchar(255)"`
	CheckoutDate string  `gorm:"type:varchar(255)"`
	Cost         float32 `gorm:"type:float(7,2)"`
}

type Checkboard struct {
	Record       int32  `gorm:"primary_key"`
	Idcard       string `gorm:"type:varchar(255)"`
	RoomID       int32
	CheckinDate  string `gorm:"type:varchar(255)"`
	CheckoutDate string `gorm:"type:varchar(255)"`
	State        int16
}

type Detail struct {
	Record    int32
	RoomID    int32
	QueryTime string  `gorm:"type:varchar(255)"`
	StartTime string  `gorm:"type:varchar(255)"`
	EndTime   string  `gorm:"type:varchar(255)"`
	ServeTime string  `gorm:"type:varchar(255)"`
	Speed     string  `gorm:"type:varchar(255)"`
	Cost      float32 `gorm:"type:float(7,2)"`
	Rate      int16
	HaveDone  int16
}

type User struct {
	Account  string `gorm:"primary_key"`
	Password string `gorm:"type:varchar(255)"`
	Identity string `gorm:"type:varchar(255)"`
}

type OpRecord struct {
	Record int32
	RoomID int32
	OpTime string  `gorm:"type:varchar(255)"`
	OpType string  `gorm:"type:varchar(255)"`
	Old    string  `gorm:"type:varchar(255)"`
	New    string  `gorm:"type:varchar(255)"`
	Wind   float32 `gorm:"type:float(7,2)"`
	Cost   float32 `gorm:"type:float(7,2)"`
}

type ScheduleBoard struct {
	ID            int32   `gorm:"primary_key"`
	Name          string  `gorm:"type:varchar(255)"`
	IDCard        string  `gorm:"type:varchar(255)"`
	CheckinDate   string  `gorm:"type:varchar(255)"`
	Cost          float32 `gorm:"type:float(7,2)"`
	ExpectTempera string  `gorm:"type:varchar(255)"`
	Speed         string  `gorm:"type:varchar(255)"`
	Tempera       float32 `gorm:"type:float(7,2)"`
	Power         string  `gorm:"type:varchar(255)"`
	Timer         string  `gorm:"type:varchar(255)"`
	Min           string  `gorm:"type:varchar(255)"`
	HaveCheckedin string  `gorm:"type:varchar(255)"`
	ShowDetail    string  `gorm:"type:varchar(255)"`
}
