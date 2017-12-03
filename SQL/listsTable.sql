DROP TABLE IF EXISTS liststable;
CREATE TABLE liststable (
	ID int NOT NULL AUTO_INCREMENT,
	userName varchar(50) NOT NULL,
	listName varchar(50) NOT NULL,
	CONSTRAINT liststable_pk PRIMARY KEY (ID)
);
