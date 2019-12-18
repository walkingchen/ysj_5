package routers

import (
	"github.com/gin-gonic/gin"
	"github.com/swaggo/gin-swagger"
	"github.com/swaggo/gin-swagger/swaggerFiles"

	_ "github.com/codingchan/ysj_5/backend/docs"
	"github.com/codingchan/ysj_5/backend/pkg/setting"
	"github.com/codingchan/ysj_5/backend/routers/api"
	"github.com/codingchan/ysj_5/backend/routers/api/v1"
)

func InitRouter() *gin.Engine {
	r := gin.New()

	r.Use(gin.Logger())

	r.Use(gin.Recovery())

	gin.SetMode(setting.RunMode)

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	r.POST("/auth", api.GetAuth)
	r.POST("/register", api.Register)

	apiv1 := r.Group("/api/v1")
	// apiv1.Use(jwt.JWT())
	{
		apiv1.GET("/rooms", v1.GetRooms)
		apiv1.POST("/rooms", v1.AddRoom)
		apiv1.PUT("/rooms/:id", v1.EditRoom)
		apiv1.DELETE("/rooms/:id", v1.DeleteRoom)

		apiv1.GET("/room_prototypes", v1.GetRoomPrototypes)
		apiv1.POST("/room_prototypes", v1.AddRoomPrototype)
		// apiv1.PUT("/room_prototypes/:id", v1.EditRoomPrototype)
		apiv1.DELETE("/room_prototypes/:id", v1.DeleteRoomPrototype)
	}

	return r
}
