package app

import (
	"github.com/astaxie/beego/validation"

	"github.com/codingchan/ysj_5/backend/pkg/logging"
)

// MarkErrors logs error logs
func MarkErrors(errors []*validation.Error) {
	for _, err := range errors {
		logging.Info(err.Key, err.Message)
	}

	return
}

type RegisterReq struct {
	ID int `json:"id"`
	Username string `json:"username" valid:"Required; MaxSize(50)"`
	Nickname string `json:"nickname" valid:"Required; MaxSize(50)"`
	Password string `json:"password" valid:"Required; MaxSize(20)"`
}

type RoomReq struct {
	ID int `json:"id"`
	RoomName string `json:"room_name"`
	RoomDesc string `json:"room_desc"`
	RoomType int `json:"room_type"`
	PeopleLimit int `json:"people_limit"`
	RoomCount int `json:"room_count"`
}

type RoomPrototypeReq struct {
	ID int `json:"id"`
	PrototypeName string `json:"prototype_name"`
	PeopleLimit int `json:"people_limit"`
	Friendship string `json:"friendship"`
}

type PostTypeReq struct {
	ID            int    `json:"id"`
	TypeName      string `json:"type_name"`
	TypeStructure string `json:"type_structure"`
}
