package api

import (
	"github.com/codingchan/ysj_5/backend/pkg/app"
	"github.com/codingchan/ysj_5/backend/service/user_service"
	"net/http"

	"github.com/astaxie/beego/validation"
	"github.com/gin-gonic/gin"

	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/codingchan/ysj_5/backend/pkg/logging"
	"github.com/codingchan/ysj_5/backend/pkg/util"
)

type auth struct {
	Username string `valid:"Required; MaxSize(50)"`
	Password string `valid:"Required; MaxSize(50)"`
}

type register struct {
	Username string `valid:"Required; MaxSize(50)"`
	Nickname string `valid:"Required; MaxSize(50)"`
	Password string `valid:"Required; MaxSize(50)"`
}

// @Summary 登录
// @Tags User
// @Produce  json
// @Param username query string true "Username"
// @Param password query string true "Password"
// @Success 200 {string} string "{"code":2000,"data":{},"msg":"ok"}"
// @Router /auth [POST]
func GetAuth(c *gin.Context) {
	username := c.Query("username")
	password := c.Query("password")

	valid := validation.Validation{}
	a := auth{Username: username, Password: password}
	ok, _ := valid.Valid(&a)

	data := make(map[string]interface{})
	code := e.INVALID_PARAMS
	if ok {
		isExist := models.CheckAuth(username, util.GenMD5(password))
		if isExist {
			token, err := util.GenerateToken(username, password)
			if err != nil {
				code = e.ERROR_AUTH_TOKEN
			} else {
				data["token"] = token
				code = e.SUCCESS
			}
		} else {
			code = e.ERROR_AUTH
		}
	} else {
		for _, err := range valid.Errors {
			logging.Info(err.Key, err.Message)
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"code" : code,
		"msg" : e.GetMsg(code),
		"data" : data,
	})
}

// @Summary 注册
// @Tags User
// @Produce  json
// @Param username query string true "Username"
// @Param nickname query string true "Nickname"
// @Param password query string true "Password"
// @Success 200 {string} string "{"code":2000,"data":{},"msg":"ok"}"
// @Router /register [POST]
func Register(c *gin.Context) {
	var req app.RegisterReq
	if err := c.BindJSON(&req); err != nil {
		code := e.INVALID_PARAMS
		c.JSON(http.StatusOK, gin.H{
			"code" : code,
			"msg" : e.GetMsg(code),
			"data" : req,
		})
		return
	}
	valid := validation.Validation{}
	r := register{
		Username: req.Username,
		Nickname: req.Nickname,
		Password: req.Password,
	}
	ok, _ := valid.Valid(&r)

	data := make(map[string]interface{})
	code := e.INVALID_PARAMS
	if ok {
		isExist := models.CheckRegistered(req.Username)
		if isExist {
			code = e.ERROR
		} else {
			userService := user_service.User{
				Username: r.Username,
				Nickname: r.Nickname,
				Password: r.Password,
			}
			if err := userService.Add(); err != nil {
				code = e.ERROR
			} else {
				code = e.SUCCESS
			}
		}
	} else {
		for _, err := range valid.Errors {
			logging.Info(err.Key, err.Message)
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"code" : code,
		"msg" : e.GetMsg(code),
		"data" : data,
	})
}
