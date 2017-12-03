DELIMITER //
DROP PROCEDURE IF EXISTS getAllLists //

CREATE PROCEDURE getAllLists(IN userNameIn varchar(50))
BEGIN
   SELECT *
      FROM liststable
      WHERE userName = userNameIn;
END//
DELIMITER
