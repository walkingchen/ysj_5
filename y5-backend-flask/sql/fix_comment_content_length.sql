-- 修复 tb_post_comment 表的 comment_content 字段长度限制
-- 将 varchar(140) 改为 TEXT 类型以支持更长的评论内容

USE ysj_5;

-- 修改字段类型
ALTER TABLE `tb_post_comment` 
MODIFY COLUMN `comment_content` TEXT DEFAULT NULL;

-- 验证修改
DESCRIBE `tb_post_comment`;



