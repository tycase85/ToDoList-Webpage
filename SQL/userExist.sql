DELIMITER //
DROP PROCEDURE IF EXISTS userExist //

CREATE PROCEDURE userExist (IN userNameIn varchar(50))
BEGIN
	SELECT userNameIn
	FROM userstable
	WHERE userNameIn = userName;
END//
DELIMITER ;
