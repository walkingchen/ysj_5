-- MariaDB dump 10.18  Distrib 10.5.8-MariaDB, for osx10.16 (x86_64)
--
-- Host: ysj_5.soulfar.com    Database: ysj_5
-- ------------------------------------------------------
-- Server version	10.0.38-MariaDB-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_message`
--

DROP TABLE IF EXISTS `tb_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(255) DEFAULT NULL,
  `message_type` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `user_id_from` int(11) DEFAULT NULL,
  `user_id_to` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_message`
--

LOCK TABLES `tb_message` WRITE;
/*!40000 ALTER TABLE `tb_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_notice`
--

DROP TABLE IF EXISTS `tb_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_notice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notice_type` tinyint(4) DEFAULT NULL COMMENT '公告类型：0全局，1room',
  `message` text,
  `images` text,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_notice`
--

LOCK TABLES `tb_notice` WRITE;
/*!40000 ALTER TABLE `tb_notice` DISABLE KEYS */;
INSERT INTO `tb_notice` VALUES (7,1,'','[\'p2593584943.jpg\', \'v2-cd6d71e4481f5ffe432c6b1255ae601b_hd.jpg\']','2021-03-28 02:16:55','2021-03-28 10:16:55');
/*!40000 ALTER TABLE `tb_notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_post`
--

DROP TABLE IF EXISTS `tb_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_title` varchar(256) DEFAULT NULL,
  `post_content` text,
  `keywords` varchar(256) DEFAULT NULL,
  `post_type` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `timeline_type` int(11) DEFAULT NULL COMMENT '0: public\n1: private\n2: both',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post`
--

LOCK TABLES `tb_post` WRITE;
/*!40000 ALTER TABLE `tb_post` DISABLE KEYS */;
INSERT INTO `tb_post` VALUES (1,'测试标题','测试内容',NULL,1,1,NULL,1,'2020-03-29 14:03:00','2020-04-03 03:09:30'),(2,'test1','cccccc',NULL,0,2,28,2,'2020-04-02 22:58:06','2020-04-16 07:01:45'),(3,'test2','cccccc',NULL,0,3,28,2,'2020-04-02 22:58:06','2020-05-24 14:47:44'),(4,'test3','cccccc',NULL,0,4,28,2,'2020-04-02 22:58:06','2020-04-16 09:09:23'),(5,'aaaaa','sdfsdf','#oihj',1,18,28,0,'2020-04-16 15:20:38','2020-04-16 07:20:38'),(6,'testtttt','cmomlsdjfk','',1,18,28,0,'2020-04-16 17:01:17','2020-04-16 09:01:17'),(7,'test socket post pull','Can i succeed?','',1,4,28,0,'2020-04-22 15:19:04','2020-04-22 07:19:04'),(8,'test socket post pull agin','Can i succeed this time?','',1,4,28,0,'2020-04-22 16:57:22','2020-04-22 08:57:22'),(9,'test socket post pull again','View Results','',1,18,28,0,'2020-04-23 15:38:40','2020-04-23 07:38:40'),(10,'123','123','123',1,4,28,0,'2020-04-23 21:41:49','2020-04-23 13:41:49'),(11,'123','123','123',1,4,28,0,'2020-04-23 21:46:05','2020-04-23 13:46:05'),(12,'12','123','12',1,4,28,0,'2020-04-23 21:57:17','2020-04-23 13:57:17'),(13,'test test test','456677878','',1,18,28,0,'2020-04-24 14:19:23','2020-04-24 06:19:23'),(14,'adfsfsdf','dddddddddddddddd','',1,18,28,0,'2020-04-24 14:25:29','2020-04-24 06:25:29'),(15,'更多就看见','微推图','',1,4,28,0,'2020-04-24 14:27:18','2020-04-24 06:27:18'),(16,'kfkfkssssodfpj','345637657567','',1,18,28,0,'2020-04-24 14:27:42','2020-04-24 06:27:42'),(17,'hi','hello','world',1,18,28,0,'2020-07-16 10:39:51','2020-07-16 02:39:51');
/*!40000 ALTER TABLE `tb_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_post_comment`
--

DROP TABLE IF EXISTS `tb_post_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_post_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `comment_content` varchar(140) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_comment`
--

LOCK TABLES `tb_post_comment` WRITE;
/*!40000 ALTER TABLE `tb_post_comment` DISABLE KEYS */;
INSERT INTO `tb_post_comment` VALUES (1,2,17,'测试评论','2020-03-30 16:59:33','2020-04-02 15:07:17'),(2,3,18,'测试评论2','2020-03-30 16:59:00','2020-04-02 15:07:17'),(3,17,18,'comment','2020-07-16 10:39:58','2020-07-16 02:39:58');
/*!40000 ALTER TABLE `tb_post_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_post_factcheck`
--

DROP TABLE IF EXISTS `tb_post_factcheck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_post_factcheck` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) DEFAULT NULL,
  `post_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_factcheck`
--

LOCK TABLES `tb_post_factcheck` WRITE;
/*!40000 ALTER TABLE `tb_post_factcheck` DISABLE KEYS */;
INSERT INTO `tb_post_factcheck` VALUES (4,NULL,3,18,'2020-04-16 10:23:02');
/*!40000 ALTER TABLE `tb_post_factcheck` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_post_like`
--

DROP TABLE IF EXISTS `tb_post_like`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_post_like` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `post_like` int(11) DEFAULT NULL COMMENT '0: none; 1: like; 2: dislike; 3: ...',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_like`
--

LOCK TABLES `tb_post_like` WRITE;
/*!40000 ALTER TABLE `tb_post_like` DISABLE KEYS */;
INSERT INTO `tb_post_like` VALUES (1,2,18,1,'2020-03-30 09:00:28','2020-04-03 03:18:34'),(2,3,18,1,'2020-04-15 07:55:35','2020-04-15 07:55:35'),(5,4,18,1,'2020-04-16 02:23:46','2020-04-16 02:26:10'),(6,6,18,1,'2020-04-16 14:30:45','2020-04-16 14:30:45'),(7,17,18,1,'2020-07-16 02:40:21','2020-07-16 02:40:21'),(8,17,18,1,'2020-07-16 02:40:22','2020-07-16 02:40:22'),(9,17,18,1,'2020-07-16 02:40:29','2020-07-16 02:40:29');
/*!40000 ALTER TABLE `tb_post_like` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_post_type`
--

DROP TABLE IF EXISTS `tb_post_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_post_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(64) NOT NULL,
  `type_structure` varchar(2048) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_type`
--

LOCK TABLES `tb_post_type` WRITE;
/*!40000 ALTER TABLE `tb_post_type` DISABLE KEYS */;
INSERT INTO `tb_post_type` VALUES (2,'name2','\"structure\"','2019-12-19 18:16:37','2019-12-19 10:16:37');
/*!40000 ALTER TABLE `tb_post_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_question`
--

DROP TABLE IF EXISTS `tb_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_question`
--

LOCK TABLES `tb_question` WRITE;
/*!40000 ALTER TABLE `tb_question` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_room`
--

DROP TABLE IF EXISTS `tb_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_room` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` varchar(255) DEFAULT NULL,
  `room_name` varchar(255) DEFAULT NULL,
  `room_desc` varchar(255) DEFAULT NULL,
  `room_type` int(255) DEFAULT NULL,
  `people_limit` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_room`
--

LOCK TABLES `tb_room` WRITE;
/*!40000 ALTER TABLE `tb_room` DISABLE KEYS */;
INSERT INTO `tb_room` VALUES (28,'tUxrFAHu','tUxrFAHu',NULL,9,10,'2020-04-03 02:29:47','2020-04-22 03:45:18'),(30,'JDcirOtR','JDcirOtR',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(31,'M46HQWno','M46HQWno',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(32,'3IJWM2fk','3IJWM2fk',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(33,'9J0Xvsr1','9J0Xvsr1',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(34,'W3GBO6qg','W3GBO6q','test edit',10,9,'2020-04-03 02:29:48','2020-05-26 02:54:47'),(39,'mGy4I5iC','mGy4I5iC','',9,12,'2020-05-26 06:35:17','2020-05-26 06:35:17'),(41,'Um3iqQdo','Um3iqQdo','',9,12,'2020-05-26 06:35:17','2020-05-26 06:35:17'),(42,'hsytjGFv','hsytjGFv','sss',13,5,'2020-05-26 06:36:10','2020-05-26 06:36:10'),(43,'5goN9zK6','5goN9zK6','sss',13,5,'2020-05-26 06:36:10','2020-05-26 06:36:10'),(44,'Be5tZiS6','Be5tZiS6','sss',13,5,'2020-05-26 06:36:10','2020-05-26 06:36:10'),(45,'9JXl47ag','9JXl47ag','sss',13,5,'2020-05-26 06:36:10','2020-05-26 06:36:10'),(46,'Fps1CGaH','Fps1CGaH','sss',13,5,'2020-05-26 06:36:10','2020-05-26 06:36:10');
/*!40000 ALTER TABLE `tb_room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_room_member`
--

DROP TABLE IF EXISTS `tb_room_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_room_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `seat_no` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_room_member`
--

LOCK TABLES `tb_room_member` WRITE;
/*!40000 ALTER TABLE `tb_room_member` DISABLE KEYS */;
INSERT INTO `tb_room_member` VALUES (3,14,1,28,'2020-03-27 15:47:42','2020-04-06 15:11:41'),(4,2,2,28,'2020-04-02 14:18:39','2020-04-02 06:18:39'),(5,3,3,28,'2020-04-02 14:18:52','2020-04-02 06:18:52'),(6,4,4,28,'2020-04-02 14:19:00','2020-04-02 06:19:00'),(7,5,5,28,'2020-04-02 14:19:08','2020-04-02 06:19:08'),(8,18,6,28,'2020-03-27 15:47:42','2020-04-02 08:25:57');
/*!40000 ALTER TABLE `tb_room_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_room_prototype`
--

DROP TABLE IF EXISTS `tb_room_prototype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_room_prototype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prototype_id` int(11) DEFAULT NULL,
  `prototype_name` varchar(128) DEFAULT NULL,
  `people_limit` int(11) DEFAULT NULL,
  `friendship` mediumtext,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_room_prototype`
--

LOCK TABLES `tb_room_prototype` WRITE;
/*!40000 ALTER TABLE `tb_room_prototype` DISABLE KEYS */;
INSERT INTO `tb_room_prototype` VALUES (9,9,'prototype_demo',10,'{\"1\":[\"2\",\"3\",\"4\"],\"2\":[\"1\",\"3\",\"4\",\"6\"],\"3\":[\"1\",\"2\",\"6\"],\"4\":[\"1\",\"2\",\"6\"],\"6\":[\"2\",\"3\",\"4\"]}','2019-12-21 23:11:18','2020-04-22 07:07:28'),(10,12,'test',10,'{\"6\": [2, 3, 4]}','2020-04-02 14:19:58','2020-04-02 06:24:06'),(13,NULL,'test',4,'{\"1\":[\"2\",\"3\",\"4\"],\"2\":[\"1\"],\"3\":[\"1\",\"2\"],\"4\":[\"1\",\"2\",\"3\"]}','2020-04-30 14:17:54','2020-04-30 06:17:54');
/*!40000 ALTER TABLE `tb_room_prototype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_timeline`
--

DROP TABLE IF EXISTS `tb_timeline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_timeline` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `timeline_type` int(11) DEFAULT NULL COMMENT '公共0/私人1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_timeline`
--

LOCK TABLES `tb_timeline` WRITE;
/*!40000 ALTER TABLE `tb_timeline` DISABLE KEYS */;
INSERT INTO `tb_timeline` VALUES (5,NULL,28,0,'2020-03-27 15:33:25','2020-04-02 05:23:45'),(6,15,28,1,'2020-03-27 15:47:43','2020-04-02 05:23:45');
/*!40000 ALTER TABLE `tb_timeline` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user`
--

DROP TABLE IF EXISTS `tb_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(255) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `nickname` varchar(32) DEFAULT NULL,
  `realname` varchar(32) DEFAULT NULL,
  `avatar` varchar(2048) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COMMENT='用户';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user`
--

LOCK TABLES `tb_user` WRITE;
/*!40000 ALTER TABLE `tb_user` DISABLE KEYS */;
INSERT INTO `tb_user` VALUES (2,NULL,'test123','86fcb4c0551ea48ede7df5ed9626eee7',NULL,'nickname',NULL,NULL,'2019-12-17 16:50:14','2020-04-02 05:23:45'),(3,NULL,'user1','a722c63db8ec8625af6cf71cb8c2d939',NULL,'nick1',NULL,NULL,'2020-01-29 13:25:47','2020-04-02 08:30:03'),(4,NULL,'user2','123456',NULL,'nick2',NULL,NULL,'2020-01-29 13:26:03','2020-04-21 06:51:39'),(5,NULL,'user3','3afc79b597f88a72528e864cf81856d2',NULL,'nick3',NULL,NULL,'2020-01-29 13:26:08','2020-04-22 06:54:57'),(8,NULL,'user4','fc2921d9057ac44e549efaf0048b2512',NULL,'nick4',NULL,NULL,'2020-01-29 13:26:14','2020-04-02 05:23:45'),(9,NULL,'user5','d35f6fa9a79434bcd17f8049714ebfcb',NULL,'nick5',NULL,NULL,'2020-01-29 13:26:20','2020-04-02 05:23:45'),(10,NULL,'user6','e9568c9ea43ab05188410a7cf85f9f5e',NULL,'nick6',NULL,NULL,'2020-01-29 13:26:25','2020-04-02 05:23:45'),(11,NULL,'user7','8c96c3884a827355aed2c0f744594a52',NULL,'nick7',NULL,NULL,'2020-01-29 13:26:31','2020-04-02 05:23:45'),(12,NULL,'user8','ccd3cd18225730c5edfc69f964b9d7b3',NULL,'nick8',NULL,NULL,'2020-01-29 13:26:40','2020-04-02 05:23:45'),(13,NULL,'user9','c28cce9cbd2daf76f10eb54478bb0454',NULL,'nick9',NULL,NULL,'2020-01-29 13:26:47','2020-04-02 05:23:45'),(14,NULL,'user10','a3224611fd03510682690769d0195d66',NULL,'nick10',NULL,NULL,'2020-01-29 13:26:54','2020-04-02 05:23:45'),(15,NULL,'user11','0102812fbd5f73aa18aa0bae2cd8f79f',NULL,'nick11',NULL,NULL,'2020-01-29 13:26:59','2020-04-02 05:23:45'),(16,NULL,'user12','0bd0fe6372c64e09c4ae81e056a9dbda',NULL,'nick12',NULL,NULL,'2020-01-29 13:27:26','2020-04-02 05:23:45'),(17,NULL,'user13','c868bff94e54b8eddbdbce22159c0299',NULL,'nick13',NULL,NULL,'2020-01-29 13:27:31','2020-04-02 05:23:45'),(18,NULL,'user14','123456',NULL,'nick14',NULL,NULL,'2020-01-29 13:27:36','2020-04-02 05:23:45'),(19,NULL,'hello','world','hello@world.com',NULL,NULL,NULL,'2020-03-30 14:43:43','2020-04-02 05:23:45'),(20,NULL,'helloz','world','helloz@world.com',NULL,NULL,NULL,'2020-03-30 14:45:11','2020-04-02 05:23:45'),(21,NULL,'tian@test.com','123456','tian@test.com','tiant',NULL,'data:image/jpg;base64,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','2020-04-13 16:10:50','2020-04-13 08:10:50');
/*!40000 ALTER TABLE `tb_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_user_profile`
--

DROP TABLE IF EXISTS `tb_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_user_profile` (
  `user_id` int(11) NOT NULL,
  `user_status` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user_profile`
--

LOCK TABLES `tb_user_profile` WRITE;
/*!40000 ALTER TABLE `tb_user_profile` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_user_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-28 10:23:25
