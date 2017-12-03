DELIMITER //
DROP PROCEDURE IF EXISTS getListID  //
CREATE PROCEDURE getListID(IN listNameIn varchar(50))
BEGIN
   SELECT ID
      FROM liststable
      WHERE listName = listNameIn;
END//
DELIMITER ;
