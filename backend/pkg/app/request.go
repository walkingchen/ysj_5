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

type RoomAddReq struct {
	RoomType int `json:"room_type"`
	PeopleLimit int `json:"people_limit"`
	RoomCount int `json:"room_count"`
}
