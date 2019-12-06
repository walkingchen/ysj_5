package room_service

import (
	"gitee.com/codingchan/ysj_5/backend/models"
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
		roomService.Add()
	}
	return nil
}

func (a *Room) Add() (bool, error) {
	return models.AddRoom(a.RoomName, a.RoomDesc, a.RoomType, a.PeopleLimit)
}
