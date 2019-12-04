module gitee.com/codingchan/ysj_5/backend

go 1.13

require (
	github.com/EDDYCJY/go-gin-example v0.0.0-20191007083155-a98c25f2172a
	github.com/alecthomas/template v0.0.0-20190718012654-fb15b899a751
	github.com/astaxie/beego v1.12.0
	github.com/dgrijalva/jwt-go v3.2.0+incompatible
	github.com/fatih/color v1.7.0 // indirect
	github.com/gin-gonic/gin v1.5.0
	github.com/go-ini/ini v1.51.0
	github.com/go-playground/universal-translator v0.17.0 // indirect
	github.com/go-siris/siris v7.4.0+incompatible // indirect
	github.com/jinzhu/gorm v1.9.11
	github.com/json-iterator/go v1.1.8 // indirect
	github.com/konsorten/go-windows-terminal-sequences v1.0.2 // indirect
	github.com/labstack/echo v3.3.10+incompatible // indirect
	github.com/labstack/gommon v0.3.0 // indirect
	github.com/leodido/go-urn v1.2.0 // indirect
	github.com/mattn/go-colorable v0.1.4 // indirect
	github.com/mattn/go-isatty v0.0.10 // indirect
	github.com/oxequa/interact v0.0.0-20171114182912-f8fb5795b5d7 // indirect
	github.com/oxequa/realize v2.0.2+incompatible // indirect
	github.com/satori/go.uuid v1.2.0 // indirect
	github.com/sirupsen/logrus v1.4.2 // indirect
	github.com/swaggo/gin-swagger v1.2.0
	github.com/swaggo/swag v1.5.1
	github.com/unknwon/com v1.0.1
	github.com/valyala/fasttemplate v1.1.0 // indirect
	golang.org/x/crypto v0.0.0-20191202143827-86a70503ff7e // indirect
	golang.org/x/net v0.0.0-20191204025024-5ee1b9f4859a // indirect
	golang.org/x/sys v0.0.0-20191204072324-ce4227a45e2e // indirect
	google.golang.org/appengine v1.6.5 // indirect
	gopkg.in/go-playground/validator.v9 v9.30.2 // indirect
	gopkg.in/ini.v1 v1.51.0 // indirect
	gopkg.in/urfave/cli.v2 v2.0.0-20190806201727-b62605953717 // indirect
	gopkg.in/yaml.v2 v2.2.7 // indirect
)

replace (
	gitee.com/codingchan/ysj_5/backend/conf => ./conf
	gitee.com/codingchan/ysj_5/backend/docs => ./docs
	gitee.com/codingchan/ysj_5/backend/middleware => ./middleware
	gitee.com/codingchan/ysj_5/backend/middleware/jwt => ./middleware/jwt
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
