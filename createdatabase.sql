CREATE DATABASE DistributedSystems;

CREATE TABLE `Account`(
	`ID` INT(10) NOT NULL AUTO_INCREMENT,
	`Username` TEXT NOT NULL,
	`Password` TEXT NOT NULL,
	PRIMARY KEY(`ID`)
);

CREATE TABLE `Artist`(
    `ID` INT(10) NOT NULL AUTO_INCREMENT,
    `Name` TEXT NOT NULL,
    PRIMARY KEY(`ID`)
);

CREATE TABLE `Album`(
    `ID` INT(10) NOT NULL AUTO_INCREMENT,
    `Artist_ID` INT(10) NOT NULL,
    `Name` TEXT NOT NULL,
    `Year` TEXT NOT NULL,
    `Genre` TEXT NOT NULL,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (`Artist_ID`) REFERENCES ARTIST(`ID`)
);

CREATE TABLE `Song`(
    `ID` INT(10) NOT NULL AUTO_INCREMENT,
    `Name` TEXT NOT NULL,
    `Album_ID` INT(10) NOT NULL,
    `File` TEXT NOT NULL,
    PRIMARY KEY(`ID`),
    FOREIGN KEY (`Album_ID`) REFERENCES ALBUM(`ID`)
);

INSERT INTO `album` (`ID`, `Artist_ID`, `Name`, `Year`, `Genre`) VALUES
(1, 2, 'Whenever You Need Somebody', '1987', 'Pop'),
(2, 5, 'Mylo Xyloto', '2011', 'Pop'),
(3, 5, 'Viva La Vida', '2008', 'Alternative'),
(4, 6, 'Meteora', '2003', 'Rap'),
(5, 6, 'Minutes to Midnight', '2008', 'Rock'),
(6, 7, 'A Night At The Opera', '1975', 'Rock'),
(7, 3, '1989', '2014', 'Pop');

INSERT INTO `artist` (`ID`, `Name`) VALUES
(2, 'Rick Astley'),
(3, 'Taylor Swift'),
(5, 'Coldplay'),
(6, 'Linkin Park'),
(7, 'Queen');

INSERT INTO `song` (`ID`, `Name`, `Album_ID`, `File`) VALUES
(1, 'Never Gonna Give You Up', 1, 'Rick_Astley-Never_Gonna_Give_You_Up'),
(2, 'Paradise', 2, 'Coldplay-Paradise'),
(3, 'Viva La Vida', 3, 'Codplay-Viva_La_Vida'),
(4, 'Faint', 4, 'Linkin_Park-Faint'),
(5, 'Leave Out All The Rest', 5, 'Linkin_Park-Leave_Out_All_The_Rest'),
(6, 'Numb', 4, 'Linkin_Park-Numb'),
(7, 'Bohemian Rhapsody', 6, 'Queen-Bohemian_Rhapsody'),
(8, 'Bad Blood', 7, 'Taylor_Swift-Bad_Blood');