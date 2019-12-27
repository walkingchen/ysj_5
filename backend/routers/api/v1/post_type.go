package v1

import (
	"github.com/codingchan/ysj_5/backend/models"
	"github.com/codingchan/ysj_5/backend/pkg/app"
	"github.com/codingchan/ysj_5/backend/pkg/e"
	"github.com/codingchan/ysj_5/backend/pkg/setting"
	"github.com/codingchan/ysj_5/backend/pkg/util"
	"github.com/codingchan/ysj_5/backend/service/post_service"
	"github.com/gin-gonic/gin"
	"github.com/unknwon/com"
	"net/http"
)

// @Summary 获取 PostType 列表
// @Tags Post Type
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/post_types [GET]
func GetPostTypes(c *gin.Context) {
	appG := app.Gin{C: c}

	maps := make(map[string]interface{})
	data := make(map[string]interface{})

	data["lists"] = models.GetPostTypes(util.GetPage(c), setting.PageSize, maps)
	data["total"] = models.GetPostTypeTotal(maps)

	appG.Response(http.StatusOK, e.SUCCESS, data)
}

// @Summary 新增 PostType
// @Tags Post Type
// @Produce  json
// @Param type_name query string true "Type Name"
// @Param type_structure query string true "Type Structure"
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/post_types [POST]
func AddPostType(c *gin.Context) {
	appG := app.Gin{C: c}

	var req app.PostTypeReq
	if err := c.BindJSON(&req); err != nil {
		appG.Response(http.StatusBadRequest, e.INVALID_PARAMS, nil)
		return
	}

	postTypeService := post_service.PostType{
		TypeName:      req.TypeName,
		TypeStructure: req.TypeStructure,
	}
	if err := postTypeService.Add(); err != nil {
		appG.Response(http.StatusInternalServerError, e.ERROR, nil)
		return
	}

	appG.Response(http.StatusOK, e.SUCCESS, req)
}

// @Summary 删除 PostType
// @Tags Post Type
// @Produce  json
// @Success 200 {string} string "{"code":200,"data":{},"msg":"ok"}"
// @Router /api/v1/post_types/{id} [DELETE]
func DeletePostType(c *gin.Context) {
	appG := app.Gin{C: c}

	id := com.StrTo(c.Param("id")).MustInt()
	postTypeService := post_service.PostType{ID: id}
	if err := postTypeService.Delete(); err != nil {
		appG.Response(http.StatusInternalServerError, e.ERROR, nil)
		return
	}

	appG.Response(http.StatusOK, e.SUCCESS, nil)
}