-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 01, 2016 at 08:08 PM
-- Server version: 10.0.26-MariaDB
-- PHP Version: 5.6.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kernelscope`
--
CREATE DATABASE IF NOT EXISTS `kernelscope` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `kernelscope`;

-- --------------------------------------------------------

--
-- Table structure for table `offcputime`
--

CREATE TABLE `offcputime` (
  `id` int(11) NOT NULL,
  `hostname` varchar(256) NOT NULL,
  `time` datetime NOT NULL,
  `process` varchar(256) NOT NULL,
  `pid` int(11) NOT NULL,
  `stack` text NOT NULL,
  `elapsed` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `offcputime`
--
ALTER TABLE `offcputime`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `offcputime`
--
ALTER TABLE `offcputime`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
