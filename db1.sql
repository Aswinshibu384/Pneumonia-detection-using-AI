-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: pneumonia_db
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `appointment_date` datetime DEFAULT NULL,
  `status` enum('pending','completed','cancelled') DEFAULT 'pending',
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (2,'aswin111','mbbs','07593095434',14,'$2b$12$j7JKiE5Tiaaj4VvTMW7Ne.OQ5no4yGFBqB.q79vzx7y.AIy5Du8cK'),(3,'aswin01234','mbbs','07593095434',15,'$2b$12$WuHP8AqSGWEbN91voH.6L.6ZfZ16HPRmA2JdpZXf2loFdCsmScCQK'),(5,'qwef','mbbs','07593095434',17,'$2b$12$bpJJ1Exx/ktc0VRXbZAfx.5Wfv7cF2x8uap3v7H8OgjPBNfb5I46K'),(6,'arjun','md','07593095434',18,'arjun');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `contact` varchar(20) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `patients_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'nave',32,'Male','naveen',19),(3,'patient1',12,'Male','123456789',48),(4,'shibuannan',50,'Male','7865483747',49);
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pneumonia_results`
--

DROP TABLE IF EXISTS `pneumonia_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pneumonia_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `image_path` varchar(255) DEFAULT NULL,
  `result` enum('normal','pneumonia') DEFAULT NULL,
  `scanned_by` int DEFAULT NULL,
  `diagnosis_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `scanned_by` (`scanned_by`),
  CONSTRAINT `pneumonia_results_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  CONSTRAINT `pneumonia_results_ibfk_2` FOREIGN KEY (`scanned_by`) REFERENCES `doctors` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pneumonia_results`
--

LOCK TABLES `pneumonia_results` WRITE;
/*!40000 ALTER TABLE `pneumonia_results` DISABLE KEYS */;
/*!40000 ALTER TABLE `pneumonia_results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prescriptions`
--

DROP TABLE IF EXISTS `prescriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prescriptions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `medicine` text,
  `notes` text,
  `prescribed_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `prescriptions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`id`) ON DELETE CASCADE,
  CONSTRAINT `prescriptions_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prescriptions`
--

LOCK TABLES `prescriptions` WRITE;
/*!40000 ALTER TABLE `prescriptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `prescriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','doctor','patient') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'testuser','pbkdf2:sha256:1000000$1b7qS8pbSSnXIHME$3066b77c3d8e774ebaec78ef7e476eb9433856eb23c60b619860f3b41e6590e7','doctor'),(2,'admin','pbkdf2:sha256:1000000$HgvjGrGyFLlxXYUt$af719a8433553a6f3e853f196558d036c5dad40a87fa2aa5cc1c9a3816b4ecda','admin'),(3,'naveen','$2b$12$9y13KTWGKn36/5U7cFPmquOJUrr3Dv2wZZZamQbpjed7XPzr3jR3S','admin'),(4,'aswin','$2b$12$d/KKmzZnv8m3A7NjA.w8qOQOB/vWN2Kgqjnm6yytv7iiVd/lJ0qL2','doctor'),(5,'qwerty','1234','doctor'),(6,'qwerty1','1234','doctor'),(7,'aswin1','12345','doctor'),(8,'a1','123asd','doctor'),(9,'a2','1234','doctor'),(10,'qwe','1234','doctor'),(12,'aswin123','$2b$12$hqXrKcH8PmQ6UFyZAhP2y.HC2KAS3gAwDq8onMKfF/tWDUpIq773.','doctor'),(14,'aswin1234','$2b$12$j7JKiE5Tiaaj4VvTMW7Ne.OQ5no4yGFBqB.q79vzx7y.AIy5Du8cK','doctor'),(15,'aswin01234','$2b$12$WuHP8AqSGWEbN91voH.6L.6ZfZ16HPRmA2JdpZXf2loFdCsmScCQK','doctor'),(16,'aswin001234','$2b$12$SCWnYpD3TvrWjL7z0rxTfOM6y3WRlAMmx/dNa0SizzhYtXu0RcnIO','doctor'),(17,'qwef','$2b$12$bpJJ1Exx/ktc0VRXbZAfx.5Wfv7cF2x8uap3v7H8OgjPBNfb5I46K','doctor'),(18,'arjun','$2b$12$wQvjp3NmosB1RDHvv/aQbuRDeD73lP3MY7t35dnvk2levHTQxDyca','doctor'),(19,'nav','$2b$12$nfm.330guvm37ytmSB1FdeW39dnwa92RwNHm4YfZN8Zp1S5JSukf6','admin'),(21,'nav1','$2b$12$4KioVqvSisYLCJxgEZleHeS64ElJPIBVFxyLvZlCNTi2KwaWU92Ui','admin'),(39,'nav111','$2b$12$wclbnsswkdhZ.Z4Fy/Slr.fMG4/jNGI1cWk11YDGVy6rkNAdBpSgO','patient'),(45,'nav1222','1234','patient'),(48,'patient1','$2b$12$iOAKYdhvBX7/yojwIzewYu5H7NkhU4qsXZenp269RaWHXrSyChxWy','patient'),(49,'shibuannan','$2b$12$PA6PDv89CqsGxTEnz.dpmu7Ybg5PNZ35iuK.g/nt3Eh3pHt3qirRC','patient');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-11 23:42:06
