package room_service

import "github.com/codingchan/ysj_5/backend/models"

type RoomMember struct {
	UserId int
	SeatNo int
	RoomId int
}

func (m *RoomMember) Get() (*models.RoomMember, error) {
	member, err := models.GetMember(m.UserId)
	if err != nil {
		return nil, err
	}

	return member, nil
}
