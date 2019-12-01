module gitee.com/codingchan/ysj_5/backend

go 1.13

require (
	github.com/alecthomas/template v0.0.0-20160405071501-a0175ee3bccc
	github.com/denisenkom/go-mssqldb v0.0.0-20190920000552-128d9f4ae1cd // indirect
	github.com/dgrijalva/jwt-go v3.2.0+incompatible
	github.com/gin-gonic/gin v1.5.0
	github.com/go-ini/ini v1.51.0
	github.com/go-playground/universal-translator v0.17.0 // indirect
	github.com/jinzhu/gorm v1.9.11
	github.com/json-iterator/go v1.1.8 // indirect
	github.com/leodido/go-urn v1.2.0 // indirect
	github.com/lib/pq v1.2.0 // indirect
	github.com/mattn/go-isatty v0.0.10 // indirect
	github.com/smartystreets/goconvey v0.0.0-20190731233626-505e41936337 // indirect
	github.com/swaggo/gin-swagger v1.2.0
	github.com/swaggo/swag v1.5.1
	github.com/unknwon/com v1.0.1
	golang.org/x/crypto v0.0.0-20190605123033-f99c8df09eb5 // indirect
	golang.org/x/sys v0.0.0-20191128015809-6d18c012aee9 // indirect
	google.golang.org/appengine v1.6.5 // indirect
	gopkg.in/go-playground/validator.v9 v9.30.2 // indirect
	gopkg.in/ini.v1 v1.51.0 // indirect
	gopkg.in/yaml.v2 v2.2.7 // indirect
)

replace (
	gitee.com/codingchan/ysj_5/backend/conf => ./conf
	gitee.com/codingchan/ysj_5/backend/docs => ./docs
	gitee.com/codingchan/ysj_5/backend/middleware => ./middleware
	gitee.com/codingchan/ysj_5/backend/models => ./models
	gitee.com/codingchan/ysj_5/backend/pkg => ./pkg
	gitee.com/codingchan/ysj_5/backend/pkg/e => ./pkg/e
	gitee.com/codingchan/ysj_5/backend/pkg/logging => ./pkg/logging
	gitee.com/codingchan/ysj_5/backend/pkg/setting => ./pkg/setting
	gitee.com/codingchan/ysj_5/backend/pkg/util => ./pkg/util
	gitee.com/codingchan/ysj_5/backend/routers => ./routers
	gitee.com/codingchan/ysj_5/backend/routers/api => ./routers/api
	gitee.com/codingchan/ysj_5/backend/runtime => ./runtime
)
