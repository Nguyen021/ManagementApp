-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: quanlyhocsinh
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `class_size` int NOT NULL,
  `grade_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `name_2` (`name`),
  KEY `grade_id` (`grade_id`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'10a1',8,1),(2,'10a2',9,1),(8,'11a1',0,2),(9,'12a1',0,3);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grade`
--

DROP TABLE IF EXISTS `grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grade` (
  `id` int NOT NULL AUTO_INCREMENT,
  `number` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
INSERT INTO `grade` VALUES (1,10),(2,11),(3,12);
/*!40000 ALTER TABLE `grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mark`
--

DROP TABLE IF EXISTS `mark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mark` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mark15_1` float DEFAULT NULL,
  `mark15_2` float DEFAULT NULL,
  `mark15_3` float DEFAULT NULL,
  `mark15_4` float DEFAULT NULL,
  `mark15_5` float DEFAULT NULL,
  `mark45_1` float DEFAULT NULL,
  `mark45_2` float DEFAULT NULL,
  `mark45_3` float DEFAULT NULL,
  `final` float DEFAULT NULL,
  `avg` float DEFAULT NULL,
  `subject_id` int NOT NULL,
  `student_id` int NOT NULL,
  `semester_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `subject_id` (`subject_id`),
  KEY `student_id` (`student_id`),
  KEY `semester_id` (`semester_id`),
  CONSTRAINT `mark_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`subject_id`),
  CONSTRAINT `mark_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `mark_ibfk_3` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mark`
--

LOCK TABLES `mark` WRITE;
/*!40000 ALTER TABLE `mark` DISABLE KEYS */;
INSERT INTO `mark` VALUES (1,8,8,8,-1,-1,8,8,-1,9,8.3,1,1,1),(2,8,9,5,3,-1,1,4,7,6,5.15385,1,2,1),(3,8,9,6,-1,-1,1,6,5,8,5.91667,1,3,1),(4,8,5,6,3,-1,7,2,6,7,5.61538,1,7,1),(5,5,6,9,7,10,6,3,3,9,6.28571,1,8,1),(6,9,6,5,3,1,7,9,5,6,6,1,10,1),(7,2,3,6,1,2,7,3,10,4,4.71429,1,11,1),(8,5,6,9,-1,-1,1,5,-1,9,5.9,6,2,1),(9,9,8,5,-1,-1,7,6,-1,9,7.5,1,1,2),(10,6,9,8,-1,-1,7,6,-1,8,7.3,2,1,1),(11,6,9,8,-1,-1,5,6,9,-1,5,2,2,1),(12,9,6,8,-1,-1,7,8,9,4,6.91667,1,14,1),(13,9.255,10,6.5,7.25,6.75,9.75,5.5,8.7,9.55,8.3075,1,4,1),(14,9,8,6,7,8,9,5,9,7,7.5,2,4,1),(15,8,9,7,5,9,6,4,7,9,7.07143,3,4,1),(16,8,9,7,4,6,9,5,4,7,6.5,4,4,1),(17,5,9,8,6,7,8,9,4,7,7,5,4,1),(18,8,9,6,7,8,9,7,9,5,7.35714,6,4,1),(19,8,9,6,7,9,8,7,5,9,7.57143,7,4,1),(20,8,9,7,4,8,9,5,7,9,7.5,8,4,1),(21,5,6,2,1,6,6,1,5,2,3.57143,2,5,1),(22,10,10,10,10,10,10,10,10,10,10,1,9,1),(23,8,5,9,6,7,7,9,5,7,7,1,12,1),(24,10,10,10,10,10,9.2,9.5,10,9,9.6,1,15,1),(25,8,9,7,6,-1,4,9,-1,9.25,7.61364,1,5,1),(26,5,9,8,-1,-1,4,5,-1,7,6.1,1,42,2);
/*!40000 ALTER TABLE `mark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `requirement`
--

DROP TABLE IF EXISTS `requirement`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `requirement` (
  `id` int NOT NULL AUTO_INCREMENT,
  `min_age_student` int DEFAULT NULL,
  `max_age_student` int DEFAULT NULL,
  `max_class_size` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `requirement`
--

LOCK TABLES `requirement` WRITE;
/*!40000 ALTER TABLE `requirement` DISABLE KEYS */;
INSERT INTO `requirement` VALUES (1,15,17,30),(3,15,20,40);
/*!40000 ALTER TABLE `requirement` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester` (
  `id` int NOT NULL AUTO_INCREMENT,
  `semester_name` varchar(15) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `school_year_name` varchar(15) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,'1','2019-2020'),(2,'2','2019-2020'),(3,'1','2020-2021'),(4,'2','2020-2021');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `fullname` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `address` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `dob` date DEFAULT NULL,
  `gender` tinyint(1) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `class_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `email_2` (`email`),
  UNIQUE KEY `phone_2` (`phone`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('Huỳnh Nguyễn','huynhnguyen@gmail.com','0125698546','Ea Bung','2005-10-13',0,1,1),('Nguyễn Thiện Khải','thienkhai@gmail.com','0159846935','Ea Súp','2004-10-13',0,2,1),('Nguyễn Văn Thắng','vanthang@gmail.com','0269854693','Ea Súp','2005-10-14',0,3,1),('Phạm Anh Dũng','anhdung@gmail.com','0125478936','Ea Súp','2006-06-19',0,4,1),('Trần Đại Quý','daiquy@gmail.com','0125985469','Ea Bung','2005-07-11',0,5,1),('Nguyễn Thị Thu Uyên','thuuyen@gmail.com','0127478936','Cư Mlan','2005-05-11',1,7,2),('Lê Thị Thu Thương','thuthuong@gmail.com','0125697453','Ea Súp','2005-10-18',1,8,1),('Lê Thị Thanh Thuỳ','qminnn@gmail.com','0125987463','Bắc Kạn','2006-05-11',1,9,2),('Huỳnh Đức Tòng','ductong@gmail.com','0597164398','Cư Mlan','2004-10-12',0,10,2),('Lương Hoàng Nam','lhoangnam@gmail.com','0365478216','HCM','2005-08-17',0,11,1),('Hoàng Quốc Việt','quocviet@gmail.com','0125697463','HCM','2005-10-07',0,12,2),('Nguyễn Hoàng Yến','hoangyen@gmail.com','0256369847','HCM','2005-07-15',1,14,2),('Nguyễn Hoàng Nam','nguyenhoangn023@gmail.com','0532145967','Ea Súp','2005-09-19',0,15,1),('test-tiep-nhan','test-tiep-nhan','645645365','test-tiep-nhan','2005-09-25',0,39,2),('Nguyễn Thành Nam','thanhnam@gmail.com','0236547956','HCM','2004-05-21',0,40,2),('Trần Văn Khương','khuongtran@gmail.com','0236589478','Hà Nội','2006-05-24',0,41,2),('Nguyen Van A','email@gmail.com','026565434635','HCM','2005-03-15',0,42,2);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  PRIMARY KEY (`subject_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (1,'Toán'),(2,'Vật Lí'),(3,'Hoá Học'),(4,'Sinh Học'),(5,'Ngữ Văn'),(6,'Lịch Sử'),(7,'Địa Lí'),(8,'Công Nghệ');
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `fullname` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `address` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `dob` date DEFAULT NULL,
  `gender` tinyint(1) NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_vietnamese_ci NOT NULL,
  `avatar` varchar(150) COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  `joined_date` datetime DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `user_role` enum('NONE','ADMIN','STAFF','TEACHER') COLLATE utf8mb4_vietnamese_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email_2` (`email`),
  UNIQUE KEY `phone_2` (`phone`),
  UNIQUE KEY `username_2` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vietnamese_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin','admin@gmail.com','0123456789','Ea Súp','2001-09-19',0,1,'admin','21232f297a57a5a743894a0e4a801fc3','/static/assets/img/avatar1.jpg','2022-01-09 20:24:17',1,'ADMIN'),('Lê Thị Thanh Thuỳ','thanhthuy1105@gmail.com','023685471','Bắc Kạn','1999-05-11',1,2,'gv','7dc2e5a1851b162c949b9a7bd58ea968','https://res.cloudinary.com/dxorabap0/image/upload/v1642220028/ww4k2grhbjokqqiz8foi.png','2022-01-09 20:24:17',1,'TEACHER'),('Quann Minh','qmin@gmail.com','0567897899','HCM','2000-12-10',0,3,'nv','f9eab7a52fbda6f4788f438ba1a8da94','https://res.cloudinary.com/dxorabap0/image/upload/v1642074403/xyfcmarcia1knohjbo3m.png','2022-01-09 20:24:17',1,'STAFF');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-12 21:18:46
