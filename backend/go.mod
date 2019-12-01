module gitee.com/codingchan/ysj_5/backend

go 1.13

require (
	github.com/astaxie/beego v1.12.0
	github.com/gin-gonic/gin v1.5.0
	github.com/go-ini/ini v1.51.0
	github.com/go-playground/universal-translator v0.17.0 // indirect
	github.com/jinzhu/gorm v1.9.11
	github.com/json-iterator/go v1.1.8 // indirect
	github.com/leodido/go-urn v1.2.0 // indirect
	github.com/mattn/go-isatty v0.0.10 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.1 // indirect
	github.com/unknwon/com v1.0.1
	golang.org/x/sys v0.0.0-20191128015809-6d18c012aee9 // indirect
	google.golang.org/appengine v1.6.5 // indirect
	gopkg.in/go-playground/validator.v9 v9.30.2 // indirect
	gopkg.in/yaml.v2 v2.2.7 // indirect
)

replace (
	gitee.com/codingchan/ysj_5/backend/conf => ./conf
	gitee.com/codingchan/ysj_5/backend/middleware => ./middleware
	gitee.com/codingchan/ysj_5/backend/models => ./models
	gitee.com/codingchan/ysj_5/backend/pkg => ./pkg
	gitee.com/codingchan/ysj_5/backend/pkg/e => ./pkg/e
	gitee.com/codingchan/ysj_5/backend/pkg/util => ./pkg/util
	gitee.com/codingchan/ysj_5/backend/routers => ./routers
	gitee.com/codingchan/ysj_5/backend/routers/api => ./routers/api
	gitee.com/codingchan/ysj_5/backend/runtime => ./runtime
)
