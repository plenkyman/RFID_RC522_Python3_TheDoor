-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: RfidDoor
-- ------------------------------------------------------
-- Server version	5.5.44-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `AccLog`
--

DROP TABLE IF EXISTS `AccLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AccLog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `card` tinytext NOT NULL,
  `acc` datetime DEFAULT NULL,
  `nam` varchar(45) DEFAULT NULL,
  `err` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AccLog`
--

LOCK TABLES `AccLog` WRITE;
/*!40000 ALTER TABLE `AccLog` DISABLE KEYS */;
/*!40000 ALTER TABLE `AccLog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RfidCards`
--

DROP TABLE IF EXISTS `RfidCards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RfidCards` (
  `ID` text NOT NULL COMMENT 'serial id from rfid card, in square brackets',
  `name` text COMMENT 'name of cardholder',
  `counter` int(10) DEFAULT '1' COMMENT 'total count of access',
  `acc_group` varchar(20) DEFAULT NULL COMMENT 'whatever you want, used for logs only',
  `access` int(1) NOT NULL COMMENT '0 access revoked\n1 access granted 24/7\n2 accces granted by schedule\n3 OverRide (opens door permanently until swiped again)\n4 make house cards\n5 make guest cards',
  `weekdays` varchar(45) DEFAULT '"''0'',''1'',''2'',''3'',''4'',''5'',''6''"' COMMENT 'scheduled access for work (access=2) at these days only:\n\n0 = Monday\n1= Tuesday\n2 = Wednesday\n3 = Thursday\n4 = Friday\n5 = Saturday\n6 = Sunday',
  `hours_wk_end` int(2) DEFAULT '21' COMMENT 'end hour of scheduled access for work (access=2) during weekend',
  `hours_wk_st` int(2) DEFAULT '9' COMMENT 'start hour of scheduled access for work (access=2) during weekend',
  `hours_wkend_st` int(2) DEFAULT '10' COMMENT 'start hour of scheduled access for work (access=2) during week',
  `hours_wkend_end` int(2) DEFAULT '17' COMMENT 'end hour of scheduled access for work (access=2) during week',
  `OrderID` int(11) NOT NULL AUTO_INCREMENT COMMENT 'running id for cards',
  PRIMARY KEY (`ID`(10)),
  UNIQUE KEY `RfidCardscol_UNIQUE` (`OrderID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RfidCards`
--

LOCK TABLES `RfidCards` WRITE;
/*!40000 ALTER TABLE `RfidCards` DISABLE KEYS */;
/*!40000 ALTER TABLE `RfidCards` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-04 17:48:54
