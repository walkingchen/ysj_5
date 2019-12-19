package models

type PostType struct {
	Model

	TypeName string `json:"type_name"`
	TypeStructure string `json:"type_structure"`
}

type PostTypeList struct {
	PostType []PostType `json:"post_type"`
}

func GetPostTypes(pageNum int, pageSize int, maps interface {}) (PostType []PostType) {
	db.Where(maps).Offset(pageNum).Limit(pageSize).Find(&PostType)

	return
}

func GetPostTypeTotal(maps interface {}) (count int){
	db.Model(&PostType{}).Where(maps).Count(&count)

	return
}

func AddPostType(typeName string, typeStructure string) error {
	postType := PostType{
		TypeName:      typeName,
		TypeStructure: typeStructure,
	}

	if err := db.Create(&postType).Error; err != nil {
		return err
	}

	return nil
}

func EditPostType(id int, data interface{}) error {
	if err := db.Model(&PostType{}).Where("id = ?", id).Update(data).Error; err != nil {
		return err
	}

	return nil
}

func DeletePostType(id int) error {
	if err := db.Where("id = ?", id).Delete(PostType{}).Error; err != nil {
		return err
	}

	return nil
}