package util

import (
	"github.com/codingchan/ysj_5/backend/pkg/setting"
	"github.com/gin-gonic/gin"
	"github.com/unknwon/com"
)

func GetPage(c *gin.Context) int {
	result := 0
	page, _ := com.StrTo(c.Query("page")).Int()
	size, _ := com.StrTo(c.Query("size")).Int()
	if page > 0 {
		if size != 0 {
			result = (page - 1) * size
		} else {
			result = (page - 1) * setting.PageSize
		}
	}

	return result
}
