package routers

import (
	"github.com/gin-gonic/gin"
	"github.com/swaggo/gin-swagger"
	"github.com/swaggo/gin-swagger/swaggerFiles"

	_ "gitee.com/codingchan/ysj_5/backend/docs"
	"gitee.com/codingchan/ysj_5/backend/middleware/jwt"
	"gitee.com/codingchan/ysj_5/backend/pkg/setting"
	"gitee.com/codingchan/ysj_5/backend/routers/api"
	"gitee.com/codingchan/ysj_5/backend/routers/api/v1"
)

func InitRouter() *gin.Engine {
	r := gin.New()

	r.Use(gin.Logger())

	r.Use(gin.Recovery())

	gin.SetMode(setting.RunMode)

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	r.GET("/auth", api.GetAuth)

	apiv1 := r.Group("/api/v1")
	apiv1.Use(jwt.JWT())
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