package scheduler

import (
	"backend_go/db_utils"
	"fmt"
	"strconv"
)

// Scheduler is a single instance, which cannot be created twice.
// In the lifespan of the program, there will be only one scheduler.
type UpdateOperation struct {
	Types  []string
	RoomID int
	Values []string
}

type Scheduler struct {
	RoomCount   int
	ServingSize int
	WaitingSize int
	UpdateChan  chan UpdateOperation
}

type ScheduleBody struct {
	Room_id       int
	Name          string
	IdCard        string
	CheckinDate   string
	Cost          float32
	ExpectTempera string
	Speed         string
	Tempera       float32
	Power         string
	Timer         string
	Min           string
	HaveCheckedin string
	ShowDetail    string
}

var RoomList []*ScheduleBody
var Sche *Scheduler

func (s *Scheduler) Start() {
	go func() {
		for op := range s.UpdateChan { // Here we use a for loop to receive the update operations from the channel.
			operateTask(op)
		}
	}()
}

func operateTask(op UpdateOperation) {
	for idx, field := range op.Types {
		switch field {
		case "Name":
			RoomList[op.RoomID].Name = op.Values[idx]
		case "IdCard":
			RoomList[op.RoomID].IdCard = op.Values[idx]
		case "CheckinDate":
			RoomList[op.RoomID].CheckinDate = op.Values[idx]
		case "Cost":
			cost, _ := strconv.ParseFloat(op.Values[idx], 32)
			RoomList[op.RoomID].Cost = float32(cost)
		case "ExpectTempera":
			RoomList[op.RoomID].ExpectTempera = op.Values[idx]
		case "Speed":
			RoomList[op.RoomID].Speed = op.Values[idx]
		case "Tempera":
			tempera, _ := strconv.ParseFloat(op.Values[idx], 32)
			RoomList[op.RoomID].Tempera = float32(tempera)
		case "Power":
			RoomList[op.RoomID].Power = op.Values[idx]
		case "Timer":
			RoomList[op.RoomID].Timer = op.Values[idx]
		case "Min":
			RoomList[op.RoomID].Min = op.Values[idx]
		case "HaveCheckedin":
			RoomList[op.RoomID].HaveCheckedin = op.Values[idx]
		case "ShowDetail":
			RoomList[op.RoomID].ShowDetail = op.Values[idx]
		default:
			fmt.Println("Invalid field name")
		}
	}
}

func CreateScheduler(roomCount, servingSize, waitingSize int) *Scheduler {
	if servingSize+waitingSize > roomCount {
		return nil
	}
	RoomList = make([]*ScheduleBody, roomCount)
	for i := 0; i < roomCount; i++ {
		floor := i/10 + 1
		roomNumber := i%10 + 1
		room_id := floor*100 + roomNumber
		RoomList[i] = &ScheduleBody{
			Room_id:       room_id,
			Name:          "",
			IdCard:        "",
			CheckinDate:   "",
			Cost:          0,
			ExpectTempera: "20",
			Speed:         "medium",
			Tempera:       30,
			Power:         "False",
			Timer:         "False",
			Min:           "False",
			HaveCheckedin: "False",
			ShowDetail:    "False",
		}

		db_utils.CreateScheduleRecord(int32(room_id), "", "", "", 0, "20", "medium", 30, "False", "False", "False", "False", "False")
	}
	return &Scheduler{
		RoomCount:   roomCount,
		ServingSize: servingSize,
		WaitingSize: waitingSize,
		UpdateChan:  make(chan UpdateOperation, 20), // 20 is the buffer size of the channel
	}
}

func InitSche(RoomTotal, ServingSize, WaitingSize int) {
	Sche = CreateScheduler(RoomTotal, ServingSize, WaitingSize)
	go Sche.Start()
} // offer an entrance for scheduler, and scheduler will work as a global variable, and run in a goroutine.
