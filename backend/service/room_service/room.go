package room_service

import (
	"github.com/codingchan/ysj_5/backend/models"
	"strconv"
	"time"
)

type Rooms struct {
	rooms []Room
}

type Room struct {
	ID int
	RoomName string
	RoomDesc string
	RoomType int
	PeopleLimit int
	CreatedAt time.Time
	UpdatedAt time.Time
}

func (r *Room) Get() (*models.Room, error) {
	room, err := models.GetRoom(r.ID)
	if err != nil {
		return nil, err
	}

	return room, nil
}

func AddAll(roomType int, peopleLimit int, roomCount int) error {
	for i := 0; i < roomCount; i++ {
		roomService := Room{
			RoomName:    strconv.Itoa(i),
			RoomDesc:    "",
			RoomType:    roomType,
			PeopleLimit: peopleLimit,
			CreatedAt:   time.Time{},
			UpdatedAt:   time.Time{},
		}
		if err := roomService.Add(); err != nil {
			return err
		}

	}

	return nil
}

func (r *Room) Add() error {
	return models.AddRoom(r.RoomName, r.RoomDesc, r.RoomType, r.PeopleLimit)
}

func (r *Room) Edit() error {
	return models.EditRoom(r.ID, map[string]interface{}{
		"room_name":    r.RoomName,
		"room_desc":    r.RoomDesc,
		"room_type":    r.RoomType,
		"people_limit": r.PeopleLimit,
	})
}


func (r *Room) Delete() error {
	return models.DeleteRoom(r.ID)
}