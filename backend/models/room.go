package models

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

func AddRoom(roomName string, roomDesc string, roomType int, peopleLimit int) bool{
	db.Create(&Room {
		RoomName: roomName,
		RoomDesc: roomDesc,
		RoomType: roomType,
		PeopleLimit: peopleLimit,
	})

	return true
}