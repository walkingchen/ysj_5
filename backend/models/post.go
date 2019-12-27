package models

type Post struct {
	Model

	PostTitle string `json:"post_title"`
	PostContent string `json:"post_content"`
}

type PostList struct {
	Post []Post `json:"post"`
}