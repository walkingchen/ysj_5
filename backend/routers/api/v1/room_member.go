package v1

import (
	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/app"
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/gin-gonic/gin"
	"net/http"
)

// @Summary 获取room member list
// @Tags Room Member
// @Produce json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/room_members [GET]
func GetRoomMembers(c *gin.Context) {
	appG := app.Gin{C: c}

	maps := make(map[string]interface{})
	data := make(map[string]interface{})

	params := c.Request.URL.Query()
	for k, v := range params {
		maps[k] = v[0]
	}

	data["lists"] = models.GetMembers(maps)
	data["total"] = models.GetMemberTotal(maps)

	appG.Response(http.StatusOK, e.SUCCESS, data)
}