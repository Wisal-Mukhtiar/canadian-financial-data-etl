DROP DATABASE IF EXISTS ETLProject;

CREATE DATABASE ETLProject;

USE ETLProject;

CREATE TABLE Expenses
(
	date datetime,
	USD int,
	rate DECIMAL(6,5),
	CAD int
)