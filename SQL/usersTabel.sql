DROP TABLE IF EXISTS userstable;
CREATE TABLE userstable (
	ID int NOT NULL AUTO_INCREMENT,
	userName varchar(50) NOT NULL,
	CONSTRAINT usersTable_pk PRIMARY KEY (ID)
);
