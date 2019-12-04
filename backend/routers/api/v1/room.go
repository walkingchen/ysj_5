package v1

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"gitee.com/codingchan/ysj_5/backend/models"
	"gitee.com/codingchan/ysj_5/backend/pkg/e"
	"gitee.com/codingchan/ysj_5/backend/pkg/setting"
	"gitee.com/codingchan/ysj_5/backend/pkg/util"
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
// @Param room_name query string true "RoomName"
// @Param room_desc query string false "RoomDesc"
// @Param room_type query int false "RoomType"
// @Param people_limit query int false "PeopleLimit"
// @Param created_at query string false "CreatedAt"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/rooms [post]
func AddRoom(c *gin.Context) {
}

//修改聊天室
func EditRoom(c *gin.Context) {
}

//删除聊天室
func DeleteRoom(c *gin.Context) {
}
