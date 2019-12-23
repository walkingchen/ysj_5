package room_member_service

type RoomMember struct {
	UserId int
	SeatNo int
	RoomId int
}

func GetRoomMembers(roomId int) ([]RoomMember, error) {

}
