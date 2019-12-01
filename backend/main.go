package main

import (
	"fmt"
	"net/http"

	"gitee.com/codingchan/ysj_5/backend/pkg/setting"
	"gitee.com/codingchan/ysj_5/backend/routers"
)

func main() {
	router := routers.InitRouter()

	s := &http.Server{
		Addr:           fmt.Sprintf(":%d", setting.HTTPPort),
		Handler:        router,
		ReadTimeout:    setting.ReadTimeout,
		WriteTimeout:   setting.WriteTimeout,
		MaxHeaderBytes: 1 << 20,
	}

	s.ListenAndServe()
}