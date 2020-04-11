-- MariaDB dump 10.17  Distrib 10.4.10-MariaDB, for osx10.15 (x86_64)
--
-- Host: localhost    Database: ysj_5
-- ------------------------------------------------------
-- Server version	10.4.10-MariaDB

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
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
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
  `message` varchar(2048) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_notice`
--

LOCK TABLES `tb_notice` WRITE;
/*!40000 ALTER TABLE `tb_notice` DISABLE KEYS */;
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
  `post_content` text DEFAULT NULL,
  `keywords` varchar(256) DEFAULT NULL,
  `post_type` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `room_id` int(11) DEFAULT NULL,
  `timeline_type` int(11) DEFAULT NULL COMMENT '0: public\n1: private\n2: both',
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post`
--

LOCK TABLES `tb_post` WRITE;
/*!40000 ALTER TABLE `tb_post` DISABLE KEYS */;
INSERT INTO `tb_post` VALUES (1,'测试标题','测试内容',NULL,1,1,NULL,1,'2020-03-29 14:03:00','2020-04-03 03:09:30'),(2,'test1','cccccc',NULL,0,2,28,1,'2020-04-02 22:58:06','2020-04-03 03:09:30'),(3,'test2','cccccc',NULL,0,3,28,1,'2020-04-02 22:58:06','2020-04-03 03:09:30'),(4,'test3','cccccc',NULL,0,4,28,1,'2020-04-02 22:58:06','2020-04-03 03:09:30');
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
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_comment`
--

LOCK TABLES `tb_post_comment` WRITE;
/*!40000 ALTER TABLE `tb_post_comment` DISABLE KEYS */;
INSERT INTO `tb_post_comment` VALUES (1,2,17,'测试评论','2020-03-30 16:59:33','2020-04-02 15:07:17'),(2,3,18,'测试评论2','2020-03-30 16:59:00','2020-04-02 15:07:17');
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
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_factcheck`
--

LOCK TABLES `tb_post_factcheck` WRITE;
/*!40000 ALTER TABLE `tb_post_factcheck` DISABLE KEYS */;
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
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_like`
--

LOCK TABLES `tb_post_like` WRITE;
/*!40000 ALTER TABLE `tb_post_like` DISABLE KEYS */;
INSERT INTO `tb_post_like` VALUES (1,2,18,1,'2020-03-30 09:00:28','2020-04-03 03:18:34');
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
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
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
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_room`
--

LOCK TABLES `tb_room` WRITE;
/*!40000 ALTER TABLE `tb_room` DISABLE KEYS */;
INSERT INTO `tb_room` VALUES (28,'tUxrFAHu','tUxrFAHu',NULL,12,10,'2020-04-03 02:29:47','2020-04-03 02:30:03'),(30,'JDcirOtR','JDcirOtR',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(31,'M46HQWno','M46HQWno',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(32,'3IJWM2fk','3IJWM2fk',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(33,'9J0Xvsr1','9J0Xvsr1',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(34,'W3GBO6qg','W3GBO6qg',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(35,'hXP8fq04','hXP8fq04',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(36,'twbZcfXq','twbZcfXq',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(37,'AfkJV16u','AfkJV16u',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48'),(38,'OVmnWlXp','OVmnWlXp',NULL,12,10,'2020-04-03 02:29:48','2020-04-03 02:29:48');
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
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
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
  `friendship` mediumtext DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_room_prototype`
--

LOCK TABLES `tb_room_prototype` WRITE;
/*!40000 ALTER TABLE `tb_room_prototype` DISABLE KEYS */;
INSERT INTO `tb_room_prototype` VALUES (9,9,'prototype_demo',4,'{\"1\":[\"2\",\"3\",\"4\"],\"2\":[\"1\"],\"3\":[\"1\",\"2\"],\"4\":[\"1\",\"2\",\"3\"]}','2019-12-21 23:11:18','2020-03-27 06:49:55'),(10,12,'test',10,'{\"6\": [2, 3, 4]}','2020-04-02 14:19:58','2020-04-02 06:24:06');
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
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
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
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COMMENT='用户';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user`
--

LOCK TABLES `tb_user` WRITE;
/*!40000 ALTER TABLE `tb_user` DISABLE KEYS */;
INSERT INTO `tb_user` VALUES (2,NULL,'test123','86fcb4c0551ea48ede7df5ed9626eee7',NULL,'nickname',NULL,NULL,'2019-12-17 16:50:14','2020-04-02 05:23:45'),(3,NULL,'user1','a722c63db8ec8625af6cf71cb8c2d939',NULL,'nick1',NULL,NULL,'2020-01-29 13:25:47','2020-04-02 08:30:03'),(4,NULL,'user2','c1572d05424d0ecb2a65ec6a82aeacbf',NULL,'nick2',NULL,NULL,'2020-01-29 13:26:03','2020-04-02 08:30:03'),(7,NULL,'user3','3afc79b597f88a72528e864cf81856d2',NULL,'nick3',NULL,NULL,'2020-01-29 13:26:08','2020-04-02 05:23:45'),(8,NULL,'user4','fc2921d9057ac44e549efaf0048b2512',NULL,'nick4',NULL,NULL,'2020-01-29 13:26:14','2020-04-02 05:23:45'),(9,NULL,'user5','d35f6fa9a79434bcd17f8049714ebfcb',NULL,'nick5',NULL,NULL,'2020-01-29 13:26:20','2020-04-02 05:23:45'),(10,NULL,'user6','e9568c9ea43ab05188410a7cf85f9f5e',NULL,'nick6',NULL,NULL,'2020-01-29 13:26:25','2020-04-02 05:23:45'),(11,NULL,'user7','8c96c3884a827355aed2c0f744594a52',NULL,'nick7',NULL,NULL,'2020-01-29 13:26:31','2020-04-02 05:23:45'),(12,NULL,'user8','ccd3cd18225730c5edfc69f964b9d7b3',NULL,'nick8',NULL,NULL,'2020-01-29 13:26:40','2020-04-02 05:23:45'),(13,NULL,'user9','c28cce9cbd2daf76f10eb54478bb0454',NULL,'nick9',NULL,NULL,'2020-01-29 13:26:47','2020-04-02 05:23:45'),(14,NULL,'user10','a3224611fd03510682690769d0195d66',NULL,'nick10',NULL,NULL,'2020-01-29 13:26:54','2020-04-02 05:23:45'),(15,NULL,'user11','0102812fbd5f73aa18aa0bae2cd8f79f',NULL,'nick11',NULL,NULL,'2020-01-29 13:26:59','2020-04-02 05:23:45'),(16,NULL,'user12','0bd0fe6372c64e09c4ae81e056a9dbda',NULL,'nick12',NULL,NULL,'2020-01-29 13:27:26','2020-04-02 05:23:45'),(17,NULL,'user13','c868bff94e54b8eddbdbce22159c0299',NULL,'nick13',NULL,NULL,'2020-01-29 13:27:31','2020-04-02 05:23:45'),(18,NULL,'user14','123456',NULL,'nick14',NULL,NULL,'2020-01-29 13:27:36','2020-04-02 05:23:45'),(19,NULL,'hello','world','hello@world.com',NULL,NULL,NULL,'2020-03-30 14:43:43','2020-04-02 05:23:45'),(20,NULL,'helloz','world','helloz@world.com',NULL,NULL,NULL,'2020-03-30 14:45:11','2020-04-02 05:23:45');
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
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
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

-- Dump completed on 2020-04-11  9:16:31
