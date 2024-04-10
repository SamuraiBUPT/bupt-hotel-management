package scheduler

import (
	"fmt"
	"strconv"
	"sync"
	"time"
)

// Scheduler is a single instance, which cannot be created twice.
// In the lifespan of the program, there will be only one scheduler.
type SchedulerTask struct {
	Types  []string
	RoomID int
	Values []string
}

type Scheduler struct {
	RoomCount   int
	ServingSize int
	TaskChan    chan *SchedulerTask
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

// The design of this package is: scheduler can be created through `InitSche()` function,
// and the global variable `Sche` will be instantiated in this package.
// And after instantiate the `Sche`, it will start a goroutine to run the scheduler, and the scheduler
// will receive the update operation from the channel `Sche.UpdateChan`, and update the corresponding
// field of the `ScheduleBody` struct.
var Sche *Scheduler // public, global variable

// the essential data structure of the scheduler, private
var scheMutex sync.Mutex
var sche_room_list []*ScheduleBody

// ===================== structure method field =====================
func (s *Scheduler) Start() {
	go func() {
		for op := range s.TaskChan {
			executeTask(op)
		}
	}()

	go func() {
		ticker := time.NewTicker(time.Second)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				s.step()
			}
		}
	}()
}

func (s *Scheduler) step() {
	fmt.Println("schedule")
	scheMutex.Lock()
	defer scheMutex.Unlock()
}

func (s *Scheduler) Stop() {
	close(s.TaskChan)
}

// ===================== helper function field =====================
func executeTask(op *SchedulerTask) {
	scheMutex.Lock()
	defer scheMutex.Unlock()

	for idx, field := range op.Types {
		decoded_idx := op.RoomID%100 + op.RoomID/100 - 1 // decode: convert the room ID to the index of the sche_room_list
		if decoded_idx < 0 || decoded_idx >= len(sche_room_list) {
			fmt.Println("Invalid room ID")
			return
		}

		switch field {
		case "Name":
			sche_room_list[decoded_idx].Name = op.Values[idx]
		case "IdCard":
			sche_room_list[decoded_idx].IdCard = op.Values[idx]
		case "CheckinDate":
			sche_room_list[decoded_idx].CheckinDate = op.Values[idx]
		case "Cost":
			cost, _ := strconv.ParseFloat(op.Values[idx], 32)
			sche_room_list[decoded_idx].Cost = float32(cost)
		case "ExpectTempera":
			sche_room_list[decoded_idx].ExpectTempera = op.Values[idx]
		case "Speed":
			sche_room_list[decoded_idx].Speed = op.Values[idx]
		case "Tempera":
			tempera, _ := strconv.ParseFloat(op.Values[idx], 32)
			sche_room_list[decoded_idx].Tempera = float32(tempera)
		case "Power":
			sche_room_list[decoded_idx].Power = op.Values[idx]
		case "Timer":
			sche_room_list[decoded_idx].Timer = op.Values[idx]
		case "Min":
			sche_room_list[decoded_idx].Min = op.Values[idx]
		case "HaveCheckedin":
			sche_room_list[decoded_idx].HaveCheckedin = op.Values[idx]
		case "ShowDetail":
			sche_room_list[decoded_idx].ShowDetail = op.Values[idx]
		default:
			fmt.Println("Invalid field name")
		}
	}
}

func CreateScheduler(roomCount, servingSize, waitingSize int) *Scheduler {
	if servingSize+waitingSize > roomCount {
		return nil
	}
	sche_room_list = make([]*ScheduleBody, roomCount)
	for i := 0; i < roomCount; i++ {
		floor := i/10 + 1
		roomNumber := i%10 + 1
		room_id := floor*100 + roomNumber
		sche_room_list[i] = &ScheduleBody{
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

	}
	return &Scheduler{
		RoomCount:   roomCount,
		ServingSize: servingSize,
		TaskChan:    make(chan *SchedulerTask, servingSize*10), // 20 is the buffer size of the channel
	}
}

func InitSche(RoomTotal, ServingSize, WaitingSize int) {
	Sche = CreateScheduler(RoomTotal, ServingSize, WaitingSize)
	go Sche.Start()
} // offer an entrance for scheduler, and scheduler will work as a global variable, and run in a goroutine.
