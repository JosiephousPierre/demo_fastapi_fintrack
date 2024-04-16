-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 07, 2024 at 03:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uic_clinic`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `nurseID` int(11) NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`nurseID`, `username`, `password`, `email`) VALUES
(1, 'admin1', 'admin1', 'admin1@uic.edu.ph'),
(2, 'admin2', 'admin2', 'admin2@uic.edu.ph'),
(3, 'admin3', 'admin3', 'admin3@uic.edu.ph'),
(4, 'admin4', 'admin4', 'admin4@uic.edu.ph'),
(5, 'admin5', 'admin5', 'admin5@uic.edu.ph');

-- --------------------------------------------------------

--
-- Table structure for table `consult`
--

CREATE TABLE `consult` (
  `Consultation_Id` int(11) NOT NULL,
  `student_Id` int(11) NOT NULL,
  `nurseID` int(11) NOT NULL,
  `illness` varchar(200) NOT NULL,
  `medicine` varchar(200) NOT NULL,
  `date` date NOT NULL,
  `time_In` varchar(200) NOT NULL,
  `check_out` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `consult`
--

INSERT INTO `consult` (`Consultation_Id`, `student_Id`, `nurseID`, `illness`, `medicine`, `date`, `time_In`, `check_out`) VALUES
(1, 2, 2, 'Headache', '', '0000-00-00', '1:00PM', '2:30PM'),
(2, 3, 1, 'Cold', '', '0000-00-00', '3:00PM', '4:00PM'),
(3, 4, 4, 'Fever', '', '0000-00-00', '10:20AM', '12:30NN'),
(4, 5, 1, 'Diarrhea', '', '0000-00-00', '11:20AM', '1:30PM'),
(5, 6, 5, 'Stomachache', '', '0000-00-00', '10:20AM', '12:30NN');

-- --------------------------------------------------------

--
-- Table structure for table `consulted_illness`
--

CREATE TABLE `consulted_illness` (
  `consIllness_Id` int(11) NOT NULL,
  `illness_Id` int(11) NOT NULL,
  `Consultation_Id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `consulted_illness`
--

INSERT INTO `consulted_illness` (`consIllness_Id`, `illness_Id`, `Consultation_Id`) VALUES
(1, 4, 1),
(2, 6, 2),
(3, 1, 3),
(4, 3, 4),
(5, 5, 5);

-- --------------------------------------------------------

--
-- Table structure for table `consulted_med`
--

CREATE TABLE `consulted_med` (
  `prescription_Id` int(11) NOT NULL,
  `Consultation_Id` int(11) NOT NULL,
  `medicine_ID` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `consulted_med`
--

INSERT INTO `consulted_med` (`prescription_Id`, `Consultation_Id`, `medicine_ID`, `quantity`) VALUES
(1, 2, 3, 4),
(2, 3, 1, 6),
(3, 1, 2, 4),
(4, 4, 3, 4),
(5, 5, 5, 6);

-- --------------------------------------------------------

--
-- Table structure for table `manage`
--

CREATE TABLE `manage` (
  `student_Id` int(11) NOT NULL,
  `nurseID` int(11) NOT NULL,
  `student_Lname` varchar(200) NOT NULL,
  `student_Fname` varchar(200) NOT NULL,
  `course` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manage`
--

INSERT INTO `manage` (`student_Id`, `nurseID`, `student_Lname`, `student_Fname`, `course`) VALUES
(2, 2, 'Batoy', 'Reuben Rex', 'BSIT'),
(3, 1, 'Lapating', 'Laurence', 'BSIT'),
(4, 4, 'Labor', 'Zachary', 'BSIT'),
(5, 1, 'Bayson', 'Lemuel', 'BSIT'),
(6, 5, 'Ibuyan', 'Adi', 'BSIT');

-- --------------------------------------------------------

--
-- Table structure for table `manage_illness`
--

CREATE TABLE `manage_illness` (
  `illness_Id` int(11) NOT NULL,
  `nurseID` int(11) NOT NULL,
  `illness` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manage_illness`
--

INSERT INTO `manage_illness` (`illness_Id`, `nurseID`, `illness`) VALUES
(1, 1, 'Fever'),
(2, 1, 'Cough'),
(3, 4, 'diarrhea'),
(4, 3, 'Headache'),
(5, 2, 'Stomachache'),
(6, 1, 'Cold');

-- --------------------------------------------------------

--
-- Table structure for table `manage_med`
--

CREATE TABLE `manage_med` (
  `medicine_ID` int(11) NOT NULL,
  `nurseID` int(11) NOT NULL,
  `brandName` varchar(200) NOT NULL,
  `drugName` varchar(200) NOT NULL,
  `expiration` date NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `manage_med`
--

INSERT INTO `manage_med` (`medicine_ID`, `nurseID`, `brandName`, `drugName`, `expiration`, `quantity`) VALUES
(1, 2, 'Biogesic', 'Paracetamol', '0000-00-00', 10),
(2, 4, 'Advil', 'Ibuprofen', '0000-00-00', 10),
(3, 2, 'Benadryl', 'Diphenhydramine', '0000-00-00', 10),
(5, 1, 'Bioflu', 'Phenylephrine HCl', '0000-00-00', 10),
(6, 5, 'Kremil-S', 'Aluminum hydroxide', '0000-00-00', 10);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`nurseID`);

--
-- Indexes for table `consult`
--
ALTER TABLE `consult`
  ADD PRIMARY KEY (`Consultation_Id`),
  ADD KEY `nurseID` (`nurseID`),
  ADD KEY `student_Id` (`student_Id`);

--
-- Indexes for table `consulted_illness`
--
ALTER TABLE `consulted_illness`
  ADD PRIMARY KEY (`consIllness_Id`),
  ADD KEY `Consultation_Id` (`Consultation_Id`),
  ADD KEY `illness_Id` (`illness_Id`);

--
-- Indexes for table `consulted_med`
--
ALTER TABLE `consulted_med`
  ADD PRIMARY KEY (`prescription_Id`),
  ADD KEY `Consultation_Id` (`Consultation_Id`),
  ADD KEY `medicine_ID` (`medicine_ID`);

--
-- Indexes for table `manage`
--
ALTER TABLE `manage`
  ADD PRIMARY KEY (`student_Id`),
  ADD KEY `nurseID` (`nurseID`);

--
-- Indexes for table `manage_illness`
--
ALTER TABLE `manage_illness`
  ADD PRIMARY KEY (`illness_Id`),
  ADD KEY `nurseID` (`nurseID`);

--
-- Indexes for table `manage_med`
--
ALTER TABLE `manage_med`
  ADD PRIMARY KEY (`medicine_ID`),
  ADD KEY `nurseID` (`nurseID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `nurseID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `consult`
--
ALTER TABLE `consult`
  MODIFY `Consultation_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `consulted_illness`
--
ALTER TABLE `consulted_illness`
  MODIFY `consIllness_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `consulted_med`
--
ALTER TABLE `consulted_med`
  MODIFY `prescription_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `manage`
--
ALTER TABLE `manage`
  MODIFY `student_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `manage_illness`
--
ALTER TABLE `manage_illness`
  MODIFY `illness_Id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `manage_med`
--
ALTER TABLE `manage_med`
  MODIFY `medicine_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `consult`
--
ALTER TABLE `consult`
  ADD CONSTRAINT `consult_ibfk_1` FOREIGN KEY (`nurseID`) REFERENCES `admin` (`nurseID`),
  ADD CONSTRAINT `consult_ibfk_3` FOREIGN KEY (`student_Id`) REFERENCES `manage` (`student_Id`);

--
-- Constraints for table `consulted_illness`
--
ALTER TABLE `consulted_illness`
  ADD CONSTRAINT `consulted_illness_ibfk_1` FOREIGN KEY (`Consultation_Id`) REFERENCES `consult` (`Consultation_Id`),
  ADD CONSTRAINT `consulted_illness_ibfk_2` FOREIGN KEY (`illness_Id`) REFERENCES `manage_illness` (`illness_Id`);

--
-- Constraints for table `consulted_med`
--
ALTER TABLE `consulted_med`
  ADD CONSTRAINT `consulted_med_ibfk_1` FOREIGN KEY (`Consultation_Id`) REFERENCES `consult` (`Consultation_Id`),
  ADD CONSTRAINT `consulted_med_ibfk_2` FOREIGN KEY (`medicine_ID`) REFERENCES `manage_med` (`medicine_ID`);

--
-- Constraints for table `manage`
--
ALTER TABLE `manage`
  ADD CONSTRAINT `manage_ibfk_1` FOREIGN KEY (`nurseID`) REFERENCES `admin` (`nurseID`);

--
-- Constraints for table `manage_illness`
--
ALTER TABLE `manage_illness`
  ADD CONSTRAINT `manage_illness_ibfk_1` FOREIGN KEY (`nurseID`) REFERENCES `admin` (`nurseID`);

--
-- Constraints for table `manage_med`
--
ALTER TABLE `manage_med`
  ADD CONSTRAINT `manage_med_ibfk_1` FOREIGN KEY (`nurseID`) REFERENCES `admin` (`nurseID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
