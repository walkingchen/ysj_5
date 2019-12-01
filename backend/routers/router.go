package routers

import (
	"github.com/gin-gonic/gin"

	"gitee.com/codingchan/ysj_5/backend/pkg/setting"
	"gitee.com/codingchan/ysj_5/backend/routers/api/v1"
)

func InitRouter() *gin.Engine {
	r := gin.New()

	r.Use(gin.Logger())

	r.Use(gin.Recovery())

	gin.SetMode(setting.RunMode)

	apiv1 := r.Group("/api/v1")
	{
		//获取标签列表
		apiv1.GET("/rooms", v1.GetRooms)
		//新建标签
		apiv1.POST("/rooms", v1.AddRoom)
		//更新指定标签
		apiv1.PUT("/rooms/:id", v1.EditRoom)
		//删除指定标签
		apiv1.DELETE("/rooms/:id", v1.DeleteRoom)
	}

	return r
}