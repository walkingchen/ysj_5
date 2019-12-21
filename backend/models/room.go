package models

import "github.com/jinzhu/gorm"

type Room struct {
	Model

	RoomName string `json:"room_name"`
	RoomDesc string `json:"room_desc"`
	RoomType int `json:"room_type"`
	PeopleLimit int `json:"people_limit"`
}

type RoomList struct {
	Room []Room `json:"room"`
}

func GetRoom(id int) (Room, error) {
	var room Room
	err := db.Where("id = ?", id).First(&room).Error
	if err != nil && err != gorm.ErrRecordNotFound {
		return room, err
	}

	return room, nil
}

func GetRooms(pageNum int, pageSize int, maps interface {}) (rooms []Room) {
	db.Where(maps).Offset(pageNum).Limit(pageSize).Find(&rooms)

	return
}

func GetRoomTotal(maps interface {}) (count int){
	db.Model(&Room{}).Where(maps).Count(&count)

	return
}

func ExistRoomByName(name string) bool {
	var room Room
	db.Select("id").Where("room_name = ?", name).First(&room)
	if room.ID > 0 {
		return true
	}

	return false
}

func AddRoom(roomName string, roomDesc string, roomType int, peopleLimit int) error {
	room := Room {
		RoomName: roomName,
		RoomDesc: roomDesc,
		RoomType: roomType,
		PeopleLimit: peopleLimit,
	}
	if err := db.Create(&room).Error; err != nil {
		return err
	}

	return nil
}

func EditRoom(id int, data interface{}) error {
	if err := db.Model(&Room{}).Where("id = ?", id).Updates(data).Error; err != nil {
		return err
	}

	return nil
}

func DeleteRoom(id int) error {
	if err := db.Where("id = ?", id).Delete(Room{}).Error; err != nil {
		return err
	}

	return nil
}
