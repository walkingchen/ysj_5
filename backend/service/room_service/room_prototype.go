package room_service

import (
	"github.com/codingchan/ysj_5/backend/models"
	"time"
)

type RoomPrototype struct {
	ID int
	PrototypeName string
	Friendship string
	PeopleLimit int
	CreatedAt time.Time
	UpdatedAt time.Time
}

func (p *RoomPrototype) Get() (*models.RoomPrototype, error) {
	prototype, err := models.GetRoomPrototype(p.ID)
	if err != nil {
		return nil, err
	}

	return prototype, nil
}

func (p *RoomPrototype) Add() error {
	return models.AddRoomPrototype(p.PrototypeName, p.PeopleLimit, p.Friendship)
}

func (p *RoomPrototype) Edit() error {
	return models.EditRoomPrototype(p.ID, map[string]interface{}{
		"prototype_name": p.PrototypeName,
		"people_limit": p.PeopleLimit,
		"friendship": p.Friendship,
	})
}

func (p *RoomPrototype) Delete() error {
	return models.DeleteRoomPrototype(p.ID)
}