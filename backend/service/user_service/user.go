package user_service

import (
	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/util"
)

type User struct {
	ID       int
	Username string
	Nickname string
	Password string
}

func (u *User) Add() error {
	password := util.GenMD5(u.Password)
	return models.AddUser(u.Username, u.Nickname, password)
}