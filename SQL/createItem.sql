DELIMITER //
DROP PROCEDURE IF EXISTS createAItem //

CREATE PROCEDURE createAItem(IN L_IDIn int, IN NameIn varchar(50))
BEGIN
INSERT INTO itemstable(L_ID, Name) VALUES
   (L_IDIn, NameIn);
END//
DELIMITER ;
