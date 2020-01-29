package models

type User struct {
	ID       int    `gorm:"primary_key" json:"id"`
	Username string `json:"username"`
	Nickname string `json:"nickname"`
	Password string `json:"password"`
}

func CheckAuth(username, password string) bool {
	var user User
	db.Select("id").Where(User{Username: username, Password: password}).First(&user)
	if user.ID > 0 {
		return true
	}

	return false
}

func CheckRegistered(username string) bool {
	var user User
	db.Select("id").Where(User{Username: username}).First(&user)
	if user.ID > 0 {
		return true
	}

	return false
}

func GetUser(id int) (*User, error) {
	var user User
	err := db.Where("id = ?", id).First(&user).Error
	if err != nil {
		return nil, err
	}

	return &user, nil
}

func GetUsers(pageNum int, pageSize int, maps interface {}) (users []User) {
	db.Where(maps).Offset(pageNum).Limit(pageSize).Find(&users)

	return
}

func GetUserTotal(maps interface {}) (count int){
	db.Model(&User{}).Where(maps).Count(&count)

	return
}

func AddUser(username string, nickname string, password string) error {
	user := User{
		Username: username,
		Nickname: nickname,
		Password: password,
	}

	if err := db.Create(&user).Error; err != nil {
		return err
	}

	return nil
}

func DeleteUser(id int) error {
	if err := db.Where("id = ?", id).Delete(User{}).Error; err != nil {
		return err
	}

	return nil
}