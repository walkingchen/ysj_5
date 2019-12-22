package v1

import (
	"github.com/codingchan/ysj_5/backend/service/room_service"
	"github.com/gin-gonic/gin"
	"github.com/unknwon/com"
	"net/http"

	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/app"
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/codingchan/ysj_5/backend/pkg/setting"
	"github.com/codingchan/ysj_5/backend/pkg/util"
)

// @Summary 获取指定聊天室
// @Tags Room
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms/{id} [GET]
func GetRoom(c *gin.Context) {
	code := e.SUCCESS
	id := com.StrTo(c.Param("id")).MustInt()
	roomService := room_service.Room{ID:id}
	room, err := roomService.Get()
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
		"data" : room,
	})
}

// @Summary 获取聊天室列表
// @Tags Room
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms [GET]
func GetRooms(c *gin.Context) {
	maps := make(map[string]interface{})
	data := make(map[string]interface{})

	params := c.Request.URL.Query()
	for k, v := range params {
		maps[k] = v[0]
	}

	code := e.SUCCESS

	data["lists"] = models.GetRooms(util.GetPage(c), setting.PageSize, maps)
	data["total"] = models.GetRoomTotal(maps)

	c.JSON(http.StatusOK, gin.H{
		"code" : code,
		"msg" : e.GetMsg(code),
		"data" : data,
	})
}

// @Summary 新增聊天室
// @Tags Room
// @Produce  json
// @Param room_type query int true "RoomType"
// @Param people_limit query int true "PeopleLimit"
// @Param room_count query int true "RoomCount"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms [POST]
func AddRoom(c *gin.Context) {
	var req app.RoomReq
	if err := c.BindJSON(&req); err != nil {
		code := e.INVALID_PARAMS
		c.JSON(http.StatusOK, gin.H{
			"code" : code,
			"msg" : e.GetMsg(code),
			"data" : req,
		})
		return
	}

	if err := room_service.AddAll(req.RoomType, req.PeopleLimit, req.RoomCount); err != nil {
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

// @Summary 修改聊天室
// @Tags Room
// @Produce  json
// @Param room_name query string false "RoomName"
// @Param room_desc query string false "RoomDesc"
// @Param room_type query int false "RoomType"
// @Param people_limit query int false "PeopleLimit"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms/{id} [PUT]
func EditRoom(c *gin.Context) {
	var req app.RoomReq
	if err := c.BindJSON(&req); err != nil {
		code := e.INVALID_PARAMS
		c.JSON(http.StatusOK, gin.H{
			"code" : code,
			"msg" : e.GetMsg(code),
			"data" : req,
		})
		return
	}

	id := com.StrTo(c.Param("id")).MustInt()
	roomService := room_service.Room{
		ID: id,
		RoomName:    req.RoomName,
		RoomDesc:    req.RoomDesc,
		RoomType:    req.RoomType,
		PeopleLimit: req.PeopleLimit,
	}
	if err := roomService.Edit(); err != nil {
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

// @Summary 删除聊天室
// @Tags Room
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms/{id} [DELETE]
func DeleteRoom(c *gin.Context) {
	id := com.StrTo(c.Param("id")).MustInt()
	roomService := room_service.Room{ID: id}
	if err := roomService.Delete(); err != nil {
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
