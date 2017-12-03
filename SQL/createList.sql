DELIMITER //
DROP PROCEDURE IF EXISTS createAList //

CREATE PROCEDURE createAList (IN userNameIn varchar(50), IN listNameIn varchar(50))
BEGIN
INSERT INTO liststable(userName, listName) VALUES (userNameIn, listNameIn);
END//
DELIMITER ;
