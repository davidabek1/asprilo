%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Grid Size X:                      15
% Grid Size Y:                      16
% Number of Nodes:                  240
% Number of Highway Nodes:          0
% Number of Robots:                 5
% Number of Shelves:                5
% Number of Picking Stations:       0
% Number of Products:               0
% Number of Product Units in Total: 0
% Number of Orders:                 0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#program base.

% init
init(object(node,1),value(at,(6,5))).
init(object(node,2),value(at,(7,5))).
init(object(node,3),value(at,(8,5))).
init(object(node,4),value(at,(9,5))).
init(object(node,5),value(at,(10,5))).
init(object(node,6),value(at,(11,5))).
init(object(node,7),value(at,(12,5))).
init(object(node,8),value(at,(13,5))).
init(object(node,9),value(at,(14,5))).
init(object(node,10),value(at,(4,6))).
init(object(node,11),value(at,(5,6))).
init(object(node,12),value(at,(6,6))).
init(object(node,13),value(at,(7,6))).
init(object(node,14),value(at,(8,6))).
init(object(node,15),value(at,(9,6))).
init(object(node,16),value(at,(10,6))).
init(object(node,17),value(at,(11,6))).
init(object(node,18),value(at,(12,6))).
init(object(node,19),value(at,(13,6))).
init(object(node,20),value(at,(14,6))).
init(object(node,21),value(at,(4,7))).
init(object(node,22),value(at,(5,7))).
init(object(node,23),value(at,(6,7))).
init(object(node,24),value(at,(7,7))).
init(object(node,25),value(at,(8,7))).
init(object(node,26),value(at,(9,7))).
init(object(node,27),value(at,(10,7))).
init(object(node,28),value(at,(11,7))).
init(object(node,29),value(at,(12,7))).
init(object(node,30),value(at,(13,7))).
init(object(node,31),value(at,(14,7))).
init(object(node,32),value(at,(4,8))).
init(object(node,33),value(at,(5,8))).
init(object(node,34),value(at,(6,8))).
init(object(node,35),value(at,(7,8))).
init(object(node,36),value(at,(8,8))).
init(object(node,37),value(at,(9,8))).
init(object(node,38),value(at,(10,8))).
init(object(node,39),value(at,(11,8))).
init(object(node,40),value(at,(12,8))).
init(object(node,41),value(at,(13,8))).
init(object(node,42),value(at,(14,8))).
init(object(node,43),value(at,(4,9))).
init(object(node,44),value(at,(5,9))).
init(object(node,45),value(at,(6,9))).
init(object(node,46),value(at,(7,9))).
init(object(node,47),value(at,(8,9))).
init(object(node,48),value(at,(9,9))).
init(object(node,49),value(at,(10,9))).
init(object(node,50),value(at,(11,9))).
init(object(node,51),value(at,(12,9))).
init(object(node,52),value(at,(4,10))).
init(object(node,53),value(at,(5,10))).
init(object(node,54),value(at,(6,10))).
init(object(node,55),value(at,(10,10))).
init(object(node,56),value(at,(11,10))).
init(object(node,57),value(at,(12,10))).
init(object(node,58),value(at,(4,11))).
init(object(node,59),value(at,(10,11))).
init(object(node,60),value(at,(11,11))).
init(object(node,61),value(at,(12,11))).
init(object(node,62),value(at,(13,11))).
init(object(node,63),value(at,(4,12))).
init(object(node,64),value(at,(5,12))).
init(object(node,65),value(at,(6,12))).
init(object(node,66),value(at,(7,12))).
init(object(node,67),value(at,(10,12))).
init(object(node,68),value(at,(11,12))).
init(object(node,69),value(at,(12,12))).
init(object(node,70),value(at,(13,12))).
init(object(node,71),value(at,(4,13))).
init(object(node,72),value(at,(5,13))).
init(object(node,73),value(at,(6,13))).
init(object(node,74),value(at,(7,13))).
init(object(node,75),value(at,(10,13))).
init(object(node,76),value(at,(11,13))).
init(object(node,77),value(at,(12,13))).
init(object(node,78),value(at,(13,13))).
init(object(node,79),value(at,(4,14))).
init(object(node,80),value(at,(5,14))).
init(object(node,81),value(at,(6,14))).
init(object(node,82),value(at,(7,14))).
init(object(node,83),value(at,(4,15))).
init(object(node,84),value(at,(5,15))).
init(object(node,85),value(at,(6,15))).
init(object(node,86),value(at,(7,15))).
init(object(robot,1),value(at,(5,8))).
init(object(robot,2),value(at,(12,13))).
init(object(robot,3),value(at,(5,6))).
init(object(robot,4),value(at,(11,6))).
init(object(robot,5),value(at,(5,12))).
init(object(shelf,1),value(at,(8,5))).
init(object(product,1),value(on,(1,1))).
init(object(order,1),value(pickingStation,1)).
init(object(order,1),value(line,(1,1))).
init(object(shelf,2),value(at,(7,14))).
init(object(product,2),value(on,(2,1))).
init(object(order,2),value(pickingStation,1)).
init(object(order,2),value(line,(2,1))).
init(object(shelf,3),value(at,(4,9))).
init(object(product,3),value(on,(3,1))).
init(object(order,3),value(pickingStation,1)).
init(object(order,3),value(line,(3,1))).
init(object(shelf,4),value(at,(7,9))).
init(object(product,4),value(on,(4,1))).
init(object(order,4),value(pickingStation,1)).
init(object(order,4),value(line,(4,1))).
init(object(shelf,5),value(at,(11,10))).
init(object(product,5),value(on,(5,1))).
init(object(order,5),value(pickingStation,1)).
init(object(order,5),value(line,(5,1))).
init(object(pickingStation,1),value(at,(4,8))).
assign(robot(1),shelf(4),station(1)).
assign(robot(2),shelf(1),station(1)).
assign(robot(3),shelf(2),station(1)).
assign(robot(4),shelf(3),station(1)).
assign(robot(5),shelf(5),station(1)).



