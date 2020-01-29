package v1

import (
	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/app"
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/codingchan/ysj_5/backend/pkg/setting"
	"github.com/codingchan/ysj_5/backend/pkg/util"
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
	appG := app.Gin{C: c}

	id := com.StrTo(c.Param("id")).MustInt()
	userService := user_service.User{ID:id}
	user, err := userService.Get()
	if err != nil {
		appG.Response(http.StatusInternalServerError, e.ERROR, err)
		return
	}

	appG.Response(http.StatusOK, e.SUCCESS, user)
}

// @Summary 获取user列表
// @Tags User
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/users [GET]
func GetUsers(c *gin.Context) {
	appG := app.Gin{C: c}

	maps := make(map[string]interface{})
	data := make(map[string]interface{})

	//params := c.Request.URL.Query()
	//for k, v := range params {
	//	maps[k] = v[0]
	//}


	data["lists"] = models.GetUsers(util.GetPage(c), setting.PageSize, maps)
	data["total"] = models.GetUserTotal(maps)

	appG.Response(http.StatusOK, e.SUCCESS, data)
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
	appG := app.Gin{C: c}

	id := com.StrTo(c.Param("id")).MustInt()
	userService := user_service.User{ID:id}
	if err := userService.Delete(); err != nil {
		appG.Response(http.StatusInternalServerError, e.ERROR, err)
		return
	}

	appG.Response(http.StatusOK, e.SUCCESS, nil)
}