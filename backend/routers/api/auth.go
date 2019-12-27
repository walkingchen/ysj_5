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
	appG := app.Gin{C: c}
	username := c.Query("username")
	password := c.Query("password")

	valid := validation.Validation{}
	a := auth{Username: username, Password: password}
	ok, _ := valid.Valid(&a)

	data := make(map[string]interface{})
	if ok {
		isExist := models.CheckAuth(username, util.GenMD5(password))
		if isExist {
			token, err := util.GenerateToken(username, password)
			if err != nil {
				appG.Response(http.StatusInternalServerError, e.ERROR_AUTH_TOKEN, err)
			} else {
				data["token"] = token
				appG.Response(http.StatusOK, e.SUCCESS, data)
			}
		} else {
			appG.Response(http.StatusInternalServerError, e.ERROR_AUTH, nil)
		}
	} else {
		for _, err := range valid.Errors {
			logging.Info(err.Key, err.Message)
		}
	}

	appG.Response(http.StatusOK, e.SUCCESS, data)
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
	appG := app.Gin{C: c}

	var req app.RegisterReq
	if err := c.BindJSON(&req); err != nil {
		appG.Response(http.StatusInternalServerError, e.INVALID_PARAMS, err)
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
	if ok {
		isExist := models.CheckRegistered(req.Username)
		if isExist {
			appG.Response(http.StatusInternalServerError, e.ERROR, nil)
		} else {
			userService := user_service.User{
				Username: r.Username,
				Nickname: r.Nickname,
				Password: r.Password,
			}
			if err := userService.Add(); err != nil {
				appG.Response(http.StatusInternalServerError, e.ERROR, err)
			} else {
				appG.Response(http.StatusOK, e.SUCCESS, nil)
			}
		}
	} else {
		for _, err := range valid.Errors {
			logging.Info(err.Key, err.Message)
		}
	}

	appG.Response(http.StatusOK, e.SUCCESS, data)
}
