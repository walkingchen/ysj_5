package models

import "github.com/jinzhu/gorm"

type RoomMember struct {
	Model

	UserId int `json:"user_id"`
	SeatNo int `json:"seat_no"`
	RoomId int `json:"room_id"`
}

func GetMember(id int) (*RoomMember, error) {
	var member RoomMember
	err := db.Where("id = ?", id).First(&member).Error
	if err != nil && err != gorm.ErrRecordNotFound {
		return nil, err
	}

	return &member, nil
}

func GetMembers(maps interface {}) (roomMember []RoomMember) {
	db.Where(maps).Find(&roomMember)

	return
}

func GetMemberTotal(maps interface {}) (count int){
	db.Model(&RoomMember{}).Where(maps).Count(&count)

	return
}

func AddMember(id int, seat int, room int) error {
	member := RoomMember{
		UserId:id,
		SeatNo:seat,
		RoomId:room,
	}
	if err := db.Create(member).Error; err != nil {
		return err
	}

	return nil
}

func DeleteMember(id int) error {
	if err := db.Where("id = ?", id).Delete(User{}).Error; err != nil {
		return err
	}

	return nil
}