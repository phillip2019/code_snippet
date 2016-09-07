create table treeNodes
   (
    id int primary key,
    nodename varchar(20),
    pid int
   );

   insert into treeNodes(id, nodename, pid)  
   values(1, 'A', 0),
   (2, 'B', 1),
   (3, 'C', 1),
   (4, 'D', 2),
   (5, 'E', 2),
   (6, 'F', 3),
   (7, 'G', 6),
   (8, 'H', 0),
   (9, 'I', 8),
   (10, 'J', 8),
   (11, 'K', 8),
   (12, 'L', 9),
   (13, 'M', 9),
   (14, 'N', 12),
   (15, 'O', 12),
   (16, 'P', 15),
   (17, 'Q', 15);


delimiter //
# 入口过程
 CREATE PROCEDURE showChildLst (IN rootId INT)
 BEGIN
  CREATE TEMPORARY TABLE IF NOT EXISTS tmpLst 
   (sno int primary key auto_increment,id int,depth int);
  DELETE FROM tmpLst;

  CALL createChildLst(rootId,0);

  select tmpLst.*,treeNodes.* from tmpLst,treeNodes where tmpLst.id=treeNodes.id order by tmpLst.sno;
 END;
 //

 # 递归过程
CREATE PROCEDURE createChildLst (IN rootId INT,IN nDepth INT)
  BEGIN
   DECLARE done INT DEFAULT 0;
   DECLARE b INT;
   DECLARE cur1 CURSOR FOR SELECT id FROM treeNodes where pid=rootId;
   DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
 
   insert into tmpLst values (null,rootId,nDepth);

 
   OPEN cur1;
 
   FETCH cur1 INTO b;
   WHILE done=0 DO
           CALL createChildLst(b,nDepth+1);
           FETCH cur1 INTO b;
   END WHILE;
 
   CLOSE cur1;
  END;
  //
delimiter ;