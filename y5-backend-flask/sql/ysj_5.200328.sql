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
  `room_id` int(11) DEFAULT NULL,
  `from` int(11) DEFAULT NULL,
  `to` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp(),
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
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp(),
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
  `timeline_id` int(11) DEFAULT NULL,
  `post_title` varchar(256) DEFAULT NULL,
  `post_content` text DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post`
--

LOCK TABLES `tb_post` WRITE;
/*!40000 ALTER TABLE `tb_post` DISABLE KEYS */;
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
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_comment`
--

LOCK TABLES `tb_post_comment` WRITE;
/*!40000 ALTER TABLE `tb_post_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `tb_post_comment` ENABLE KEYS */;
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
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_like`
--

LOCK TABLES `tb_post_like` WRITE;
/*!40000 ALTER TABLE `tb_post_like` DISABLE KEYS */;
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
  `updated_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_post_type`
--

LOCK TABLES `tb_post_type` WRITE;
/*!40000 ALTER TABLE `tb_post_type` DISABLE KEYS */;
INSERT INTO `tb_post_type` VALUES (2,'name2','\"structure\"','2019-12-19 18:16:37','2019-12-19 18:16:37');
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
  `room_name` varchar(255) DEFAULT NULL,
  `room_desc` varchar(255) DEFAULT NULL,
  `room_type` int(255) DEFAULT NULL,
  `people_limit` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_room`
--

LOCK TABLES `tb_room` WRITE;
/*!40000 ALTER TABLE `tb_room` DISABLE KEYS */;
INSERT INTO `tb_room` VALUES (6,'test','',1,100,'2019-12-06 16:46:04','2019-12-19 10:33:30'),(7,'1','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(8,'2','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(9,'3','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(10,'4','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(11,'5','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(12,'6','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(13,'7','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(14,'8','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(15,'9','',1,100,'2019-12-06 16:46:04','2019-12-06 16:46:04'),(16,'0','',2,10,'2019-12-08 13:01:05','2019-12-08 13:01:05'),(17,'1','',2,10,'2019-12-08 13:01:05','2019-12-08 13:01:05'),(18,'2','',2,10,'2019-12-08 13:01:05','2019-12-08 13:01:05'),(19,'7wWRY2b8',NULL,1,10,'2020-03-27 01:46:23',NULL),(20,'bB7wYDWf',NULL,1,10,'2020-03-27 01:46:23',NULL),(21,'vjG4UuxK',NULL,1,10,'2020-03-27 01:46:23',NULL),(22,'BUhtPKFw',NULL,1,10,'2020-03-27 01:46:23',NULL),(23,'qtZwlO1a',NULL,1,10,'2020-03-27 01:46:23',NULL),(24,'oTrEFUv3',NULL,9,10,'2020-03-27 06:50:00',NULL),(25,'uvJjpnAo',NULL,9,10,'2020-03-27 06:50:00',NULL),(26,'Yvxer48R',NULL,9,10,'2020-03-27 06:50:00',NULL),(27,'PmHngiEh',NULL,9,3,'2020-03-27 07:32:22',NULL),(28,'aJu38fz9',NULL,9,3,'2020-03-27 07:33:23',NULL);
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
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_room_member`
--

LOCK TABLES `tb_room_member` WRITE;
/*!40000 ALTER TABLE `tb_room_member` DISABLE KEYS */;
INSERT INTO `tb_room_member` VALUES (2,15,1,21,'2020-03-27 15:21:28',NULL),(3,15,1,28,'2020-03-27 15:47:42',NULL);
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
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_room_prototype`
--

LOCK TABLES `tb_room_prototype` WRITE;
/*!40000 ALTER TABLE `tb_room_prototype` DISABLE KEYS */;
INSERT INTO `tb_room_prototype` VALUES (9,9,'prototype_demo',4,'{\"1\":[\"2\",\"3\",\"4\"],\"2\":[\"1\"],\"3\":[\"1\",\"2\"],\"4\":[\"1\",\"2\",\"3\"]}','2019-12-21 23:11:18','2020-03-27 14:49:55');
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
  `updated_at` datetime DEFAULT NULL ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_timeline`
--

LOCK TABLES `tb_timeline` WRITE;
/*!40000 ALTER TABLE `tb_timeline` DISABLE KEYS */;
INSERT INTO `tb_timeline` VALUES (5,NULL,28,0,'2020-03-27 15:33:25',NULL),(6,15,28,1,'2020-03-27 15:47:43',NULL);
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
  `user_id` int(11) DEFAULT NULL,
  `username` varchar(32) DEFAULT NULL,
  `password` varchar(128) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `nickname` varchar(32) DEFAULT NULL,
  `realname` varchar(32) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COMMENT='用户';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_user`
--

LOCK TABLES `tb_user` WRITE;
/*!40000 ALTER TABLE `tb_user` DISABLE KEYS */;
INSERT INTO `tb_user` VALUES (2,NULL,'test123','86fcb4c0551ea48ede7df5ed9626eee7',NULL,'nickname',NULL,'2019-12-17 16:50:14',NULL),(5,NULL,'user1','a722c63db8ec8625af6cf71cb8c2d939',NULL,'nick1',NULL,'2020-01-29 13:25:47',NULL),(6,NULL,'user2','c1572d05424d0ecb2a65ec6a82aeacbf',NULL,'nick2',NULL,'2020-01-29 13:26:03',NULL),(7,NULL,'user3','3afc79b597f88a72528e864cf81856d2',NULL,'nick3',NULL,'2020-01-29 13:26:08',NULL),(8,NULL,'user4','fc2921d9057ac44e549efaf0048b2512',NULL,'nick4',NULL,'2020-01-29 13:26:14',NULL),(9,NULL,'user5','d35f6fa9a79434bcd17f8049714ebfcb',NULL,'nick5',NULL,'2020-01-29 13:26:20',NULL),(10,NULL,'user6','e9568c9ea43ab05188410a7cf85f9f5e',NULL,'nick6',NULL,'2020-01-29 13:26:25',NULL),(11,NULL,'user7','8c96c3884a827355aed2c0f744594a52',NULL,'nick7',NULL,'2020-01-29 13:26:31',NULL),(12,NULL,'user8','ccd3cd18225730c5edfc69f964b9d7b3',NULL,'nick8',NULL,'2020-01-29 13:26:40',NULL),(13,NULL,'user9','c28cce9cbd2daf76f10eb54478bb0454',NULL,'nick9',NULL,'2020-01-29 13:26:47',NULL),(14,NULL,'user10','a3224611fd03510682690769d0195d66',NULL,'nick10',NULL,'2020-01-29 13:26:54',NULL),(15,NULL,'user11','0102812fbd5f73aa18aa0bae2cd8f79f',NULL,'nick11',NULL,'2020-01-29 13:26:59',NULL),(16,NULL,'user12','0bd0fe6372c64e09c4ae81e056a9dbda',NULL,'nick12',NULL,'2020-01-29 13:27:26',NULL),(17,NULL,'user13','c868bff94e54b8eddbdbce22159c0299',NULL,'nick13',NULL,'2020-01-29 13:27:31',NULL),(18,NULL,'user14','d1f38b569c772ebb8fa464e1a90c5a00',NULL,'nick14',NULL,'2020-01-29 13:27:36',NULL);
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
  `updated_at` datetime DEFAULT NULL,
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

-- Dump completed on 2020-03-28 21:00:18
