package v1

import (
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/codingchan/ysj_5/backend/service/user_service"
	"github.com/gin-gonic/gin"
	"github.com/unknwon/com"
	"net/http"
)

// @Summary 获取指定user
// @Tags User
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/users/{id} [GET]
func GetUser(c *gin.Context) {
	code := e.SUCCESS
	id := com.StrTo(c.Param("id")).MustInt()
	userService := user_service.User{ID:id}
	user, err := userService.Get()
	if err != nil {
		code := e.ERROR
		c.JSON(http.StatusOK, gin.H{
			"code" : code,
			"msg" : e.GetMsg(code),
		})
	}

	c.JSON(http.StatusOK, gin.H{
		"code" : code,
		"msg" : e.GetMsg(code),
		"data" : user,
	})
}

// @Summary 获取user列表
// @Tags User
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/users [GET]
func GetUsers() {

}

// @Summary 新增user
// see auth register api

// @Summary 修改user
// @Tags User
// @Produce  json
// @Param username query int true "Username"
// @Param nickname query int true "Nickname"
// @Param password query int true "password"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/users/{id} [PUT]
func EditUser() {

}

// @Summary 删除user
// @Tags User
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/users/{id} [DELETE]
func DeleteUser(c *gin.Context) {
	id := com.StrTo(c.Param("id")).MustInt()
	userService := user_service.User{ID:id}
	if err := userService.Delete(); err != nil {
		code := e.ERROR
		c.JSON(http.StatusOK, gin.H{
			"code" : code,
			"msg" : e.GetMsg(code),
		})
		return
	}

	code := e.SUCCESS
	c.JSON(http.StatusOK, gin.H{
		"code" : code,
		"msg" : e.GetMsg(code),
	})
}