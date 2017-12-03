DELIMITER //
DROP PROCEDURE IF EXISTS createAUser //

CREATE PROCEDURE createAUser(IN userNameIn varchar(50))
BEGIN
INSERT INTO userstable(userName) VALUES
   (userNameIn);
END//
DELIMITER ;
