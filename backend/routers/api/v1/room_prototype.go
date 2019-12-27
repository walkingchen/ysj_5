package v1

import (
	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/app"
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/codingchan/ysj_5/backend/pkg/setting"
	"github.com/codingchan/ysj_5/backend/pkg/util"
	"github.com/codingchan/ysj_5/backend/service/room_service"
	"github.com/gin-gonic/gin"
	"github.com/unknwon/com"
	"net/http"
)

// @Summary 根据ID获取聊天室原型
// @Tags Room Prototype
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/room_prototypes/{id} [GET]
func GetRoomPrototype(c *gin.Context) {
	appG := app.Gin{C: c}

	id := com.StrTo(c.Param("id")).MustInt()
	prototypeService := room_service.RoomPrototype{ID: id}
	prototype, err := prototypeService.Get()
	if err != nil {
		appG.Response(http.StatusInternalServerError, e.ERROR, err)
	}

	appG.Response(http.StatusOK, e.SUCCESS, prototype)
}

// @Summary 获取聊天室原型列表
// @Tags Room Prototype
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/room_prototypes [GET]
func GetRoomPrototypes(c *gin.Context) {
	appG := app.Gin{C: c}

	maps := make(map[string]interface{})
	data := make(map[string]interface{})

	data["lists"] = models.GetRoomPrototypes(util.GetPage(c), setting.PageSize, maps)
	data["total"] = models.GetRoomPrototypeTotal(maps)

	appG.Response(http.StatusOK, e.SUCCESS, data)
}

// @Summary 新增聊天室原型
// @Tags Room Prototype
// @Produce  json
// @Param prototype_name query string true "PrototypeName"
// @Param people_limit query int true "PeopleLimit"
// @Param friendship query string true "Friendship"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/room_prototypes [POST]
func AddRoomPrototype(c *gin.Context) {
	appG := app.Gin{C: c}

	var req app.RoomPrototypeReq
	if err := c.BindJSON(&req); err != nil {
		appG.Response(http.StatusOK, e.INVALID_PARAMS, req)
		return
	}

	prototypeService := room_service.RoomPrototype{
		PrototypeName: req.PrototypeName,
		PeopleLimit: req.PeopleLimit,
		Friendship: req.Friendship,
	}
	if err := prototypeService.Add(); err != nil {
		appG.Response(http.StatusInternalServerError, e.ERROR, err)
		return
	}

	appG.Response(http.StatusOK, e.SUCCESS, req)
}

// @Summary 删除聊天室原型
// @Tags Room Prototype
// @Produce  json
// @Param id query int true "Room Prototype Id"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/room_prototypes/{id} [DELETE]
func DeleteRoomPrototype(c *gin.Context) {
	appG := app.Gin{C: c}

	id := com.StrTo(c.Param("id")).MustInt()
	prototypeService := room_service.RoomPrototype{ID: id}
	if err := prototypeService.Delete(); err != nil {
		appG.Response(http.StatusInternalServerError, e.ERROR, err)
		return
	}

	appG.Response(http.StatusOK, e.SUCCESS, nil)
}