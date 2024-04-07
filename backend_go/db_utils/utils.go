package db_utils

import (
	"database/sql"
	"fmt"
	"os"
	"time"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

const DB_FILE_NAME string = "hotel.db"

var DB *gorm.DB
var SQLDB *sql.DB

func Init_DB() {
	var init bool = false

	if _, err := os.Stat(DB_FILE_NAME); os.IsNotExist(err) {
		// 文件不存在，进行数据库初始化
		init = true
	} else {
		// 文件存在，进行检查操作
		fmt.Println("`hotel.db` exists, performing check operation")
		// 添加检查操作的代码
	}

	db, err := gorm.Open(sqlite.Open(DB_FILE_NAME), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}
	sqlDB, err := db.DB()
	if err != nil {
		panic("failed to get database connection")
	}
	sqlDB.SetMaxOpenConns(10)
	sqlDB.SetMaxIdleConns(10)
	sqlDB.SetConnMaxLifetime(time.Hour)

	DB = db
	SQLDB = sqlDB // allocate once, the gorm will manage the connection pool for you, even if you use many goroutines

	if init {
		initLocalSqliteDB()
	}
}

func initLocalSqliteDB() {
	fmt.Println("Initializing local SQLite DB")

	// Migrate the schema
	DB.AutoMigrate(&Room{}, &Bill{}, &Checkboard{}, &Detail{}, &User{}, &OpRecord{}, &ScheduleBoard{})

	// // 注意：实际上Room表我们是用不到的，在这里仅仅是为了验证CRUD功能是否能正常运作。剩下的表才是我们真正要用的。
	// // 插入内容
	// DB.Create(&Room{Room_id: 101, Bill: 250.0, Status: "available"})
	// DB.Create(&Room{Room_id: 102, Bill: 365.78, Status: "busy"})

	// // 读取内容
	// var product Room
	// DB.First(&product, 1)                   // find product with integer primary key
	// DB.First(&product, "Bill = ?", "250.0") // find product with Bill equal to 250.0

	// // 更新操作：更新单个字段
	// DB.Model(&product).Update("Bill", 2000.5)

	// // 更新操作：更新多个字段
	// DB.Model(&product).Updates(Room{Bill: 2001.5, Status: "exit"}) // non-zero fields
	// // db.Model(&product).Updates(map[string]interface{}{"Price": 2000, "Code": "F42"})

	// // 删除操作：
	// DB.Delete(&product, 1)

	// DB.Create(&User{Account: "manager", Password: "password", Identity: "0"})
	// DB.Create(&User{Account: "reception", Password: "password", Identity: "1"})

	fmt.Println("Done initializing local SQLite DB!")
}

func CreateScheduleRecord(
	room_id int32,
	Name string,
	IdCard string,
	CheckinDate string,
	Cost float32,
	ExpectTempera string,
	Speed string,
	Tempera float32,
	Power string,
	Timer string,
	Min string,
	HaveCheckedin string,
	ShowDetail string,
) bool {
	schedule_record := ScheduleBoard{
		ID:            room_id,
		Name:          Name,
		IDCard:        IdCard,
		CheckinDate:   CheckinDate,
		Cost:          Cost,
		ExpectTempera: ExpectTempera,
		Speed:         Speed,
		Tempera:       Tempera,
		Power:         Power,
		Timer:         Timer,
		Min:           Min,
		HaveCheckedin: HaveCheckedin,
		ShowDetail:    ShowDetail,
	}
	if err := DB.Create(&schedule_record).Error; err != nil {
		return false
	}
	return true
}

func UpdateScheduleRecord(
	name string,
	idCard string,
	checkinDate string,
	timer string,
	haveCheckIn string,
	showDetail string,
	room_id int,
) {
	DB.Model(&ScheduleBoard{}).Where("id = ?", int32(room_id)).Updates(map[string]interface{}{
		"Name":          name,
		"IDCard":        idCard,
		"CheckinDate":   checkinDate,
		"Timer":         timer,
		"HaveCheckedin": haveCheckIn,
		"ShowDetail":    showDetail,
	})
}

func QueryUser(account, password string) (bool, string) {
	var user User
	if err := DB.Where("account = ?", account).First(&user).Error; err != nil {
		return false, "Invalid account"
	}
	if user.Password != password {
		return false, "Invalid password"
	}
	return true, string(user.Identity)
}
