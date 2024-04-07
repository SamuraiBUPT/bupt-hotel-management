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
		// fmt.Println("Field:", field, "Value:", op.Values[idx])
		decoded_idx := op.RoomID%100 + op.RoomID/100 - 1
		// fmt.Println("Decoded index:", decoded_idx)
		switch field {
		case "Name":
			RoomList[decoded_idx].Name = op.Values[idx]
		case "IdCard":
			RoomList[decoded_idx].IdCard = op.Values[idx]
		case "CheckinDate":
			RoomList[decoded_idx].CheckinDate = op.Values[idx]
		case "Cost":
			cost, _ := strconv.ParseFloat(op.Values[idx], 32)
			RoomList[decoded_idx].Cost = float32(cost)
		case "ExpectTempera":
			RoomList[decoded_idx].ExpectTempera = op.Values[idx]
		case "Speed":
			RoomList[decoded_idx].Speed = op.Values[idx]
		case "Tempera":
			tempera, _ := strconv.ParseFloat(op.Values[idx], 32)
			RoomList[decoded_idx].Tempera = float32(tempera)
		case "Power":
			RoomList[decoded_idx].Power = op.Values[idx]
		case "Timer":
			RoomList[decoded_idx].Timer = op.Values[idx]
		case "Min":
			RoomList[decoded_idx].Min = op.Values[idx]
		case "HaveCheckedin":
			RoomList[decoded_idx].HaveCheckedin = op.Values[idx]
		case "ShowDetail":
			RoomList[decoded_idx].ShowDetail = op.Values[idx]
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

		if db_utils.Init {
			db_utils.CreateScheduleRecord(int32(room_id), "", "", "", 0, "20", "medium", 30, "False", "False", "False", "False", "False")
		}
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
