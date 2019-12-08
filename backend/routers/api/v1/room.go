package v1

import (
	"github.com/codingchan/ysj_5/backend/service/room_service"
	"net/http"

	"github.com/gin-gonic/gin"

	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/app"
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/codingchan/ysj_5/backend/pkg/setting"
	"github.com/codingchan/ysj_5/backend/pkg/util"
)

// @Summary 获取聊天室
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms [get]
func GetRooms(c *gin.Context) {
	maps := make(map[string]interface{})
	data := make(map[string]interface{})

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
// @Produce  json
// @Param room_type query int false "RoomType"
// @Param people_limit query int false "PeopleLimit"
// @Param room_count query int false "RoomCount"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms [post]
func AddRoom(c *gin.Context) {
	var req app.RoomAddReq
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
// @Produce  json
// @Param id query string true "RoomId"
// @Param room_name query string true "RoomName"
// @Param room_desc query string false "RoomDesc"
// @Param room_type query int false "RoomType"
// @Param people_limit query int false "PeopleLimit"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms [put]
func EditRoom(c *gin.Context) {
}

// @Summary 删除聊天室
// @Produce  json
// @Param id query string true "RoomId"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms [delete]
func DeleteRoom(c *gin.Context) {
}
