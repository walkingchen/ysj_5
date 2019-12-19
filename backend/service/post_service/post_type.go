package post_service

import (
	"github.com/codingchan/ysj_5/backend/models"
	"time"
)

type PostType struct {
	ID int
	TypeName string
	TypeStructure string
	CreatedAt time.Time
	UpdatedAt time.Time
}

func (p *PostType) Add() error {
	return models.AddPostType(p.TypeName, p.TypeStructure)
}

func (p *PostType) Edit() error {
	return models.EditPostType(p.ID, map[string]interface{}{
		"type_name": p.TypeName,
		"type_structure": p.TypeStructure,
	})
}

func (p *PostType) Delete() error {
	return models.DeletePostType(p.ID)
}