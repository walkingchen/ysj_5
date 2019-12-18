package models

type RoomPrototype struct {
	Model

	PrototypeName string `json:prototype_name`
	Friendship string `json:"friendship"`
	PeopleLimit int `json:"people_limit"`
}

func GetRoomPrototypes(pageNum int, pageSize int, maps interface {}) (roomPrototypes []RoomPrototype) {
	db.Where(maps).Offset(pageNum).Limit(pageSize).Find(&roomPrototypes)

	return
}

func GetRoomPrototypeTotal(maps interface {}) (count int){
	db.Model(&RoomPrototype{}).Where(maps).Count(&count)

	return
}

func ExistRoomPrototypeByName(name string) bool {
	var roomPrototype RoomPrototype
	db.Select("id").Where("prototype_name = ?", name).First(&roomPrototype)
	if roomPrototype.ID > 0 {
		return true
	}

	return false
}

func GetRoomPrototypeById(id int) (prototype RoomPrototype) {
	db.Where("id = ?", id).First(&prototype)

	return
}

func AddRoomPrototype(name string, peopleLimit int, friendship string) error {
	prototype := RoomPrototype {
		PrototypeName: name,
		PeopleLimit: peopleLimit,
		Friendship: friendship,
	}
	if err := db.Create(&prototype).Error; err != nil {
		return err
	}

	return nil
}

func EditRoomPrototype(id int, data interface{}) error {
	if err := db.Model(&RoomPrototype{}).Where("id = ?", id).Updates(data).Error; err != nil {
		return err
	}

	return nil
}

func DeleteRoomPrototype(id int) error {
	if err := db.Where("id = ?", id).Delete(RoomPrototype{}).Error; err != nil {
		return err
	}

	return nil
}
