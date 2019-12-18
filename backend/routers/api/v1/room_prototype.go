package v1

import (
	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/app"
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/codingchan/ysj_5/backend/pkg/setting"
	"github.com/codingchan/ysj_5/backend/pkg/util"
	"github.com/codingchan/ysj_5/backend/service/room_prototype_service"
	"github.com/gin-gonic/gin"
	"github.com/unknwon/com"
	"net/http"
)

// @Summary 获取聊天室原型列表
// @Tags Room Prototype
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/room_prototypes [GET]
func GetRoomPrototypes(c *gin.Context) {
	maps := make(map[string]interface{})
	data := make(map[string]interface{})

	code := e.SUCCESS

	data["lists"] = models.GetRoomPrototypes(util.GetPage(c), setting.PageSize, maps)
	data["total"] = models.GetRoomPrototypeTotal(maps)

	c.JSON(http.StatusOK, gin.H{
		"code" : code,
		"msg" : e.GetMsg(code),
		"data" : data,
	})
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
	var req app.RoomPrototypeAddReq
	if err := c.BindJSON(&req); err != nil {
		code := e.INVALID_PARAMS
		c.JSON(http.StatusOK, gin.H{
			"code" : code,
			"msg" : e.GetMsg(code),
			"data" : req,
		})
		return
	}

	prototype := room_prototype_service.RoomPrototype{
		PrototypeName: req.PrototypeName,
		PeopleLimit: req.PeopleLimit,
		Friendship: req.Friendship,
	}
	if err := prototype.Add(); err != nil {
		code := e.ERROR
		c.JSON(http.StatusOK, gin.H{
			"code" : code,
			"msg" : e.GetMsg(code),
			"data" : req,
		})
		return
	}

	code := e.SUCCESS
	c.JSON(http.StatusOK, gin.H{
		"code" : code,
		"msg" : e.GetMsg(code),
		"data" : req,
	})
}

// @Summary 删除聊天室原型
// @Tags Room Prototype
// @Produce  json
// @Param id query int true "Room Prototype Id"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/room_prototypes/{id} [DELETE]
func DeleteRoomPrototype(c *gin.Context) {
	id := com.StrTo(c.Param("id")).MustInt()
	prototype := room_prototype_service.RoomPrototype{ID: id}
	if err := prototype.Delete(); err != nil {
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