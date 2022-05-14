use example;
-- Create admins table 
CREATE TABLE `admins` (
  `ID` int NOT NULL,
  `NAME` varchar(50) NOT NULL,
  `PHONE` varchar(10) NOT NULL,
  `PWD` varchar(100) NOT NULL
);

--
-- Dumping data for table `admins` --Default User Id is : 1234567890 --Default password is admin (BCrypt Hashed and stored!)
--

INSERT INTO `admins` (`ID`, `NAME`, `PHONE`, `PWD`) VALUES
(1, 'ADMINISTRATOR', '1234567890', '$2a$12$D9Edm0zbqczu/ax8FQ6bI.65Hu9R.bjyM0QorhPNKxVTqqAG9.9fa');

-- --------------------------------------------------------

--
-- Table structure for table `developers`
--

CREATE TABLE `developers` (
  `NAME` varchar(50) NOT NULL,
  `EMAIL` varchar(100) NOT NULL,
  `PHONE` varchar(10) NOT NULL,
  `CITY` varchar(30) NOT NULL,
  `AGE` int NOT NULL
);

-- --------------------------------------------------------

--
-- Table structure for table `verified_devs`
--

CREATE TABLE `verified_devs` (
  `NAME` varchar(100) NOT NULL,
  `EMAIL` varchar(50) NOT NULL,
  `PHONE` varchar(10) NOT NULL,
  `CITY` varchar(50) NOT NULL,
  `AGE` int NOT NULL,
  `PWD` varchar(15) NOT NULL
);

-- Setting admins table unique and primary keys

ALTER TABLE `admins`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `PHONE` (`PHONE`);

--
-- Indexes for table `developers`
--
ALTER TABLE `developers`
  ADD UNIQUE KEY `PHONE` (`PHONE`),
  ADD UNIQUE KEY `EMAIL` (`EMAIL`);

COMMIT;
