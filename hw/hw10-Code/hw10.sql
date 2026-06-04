.read hw10_data.sql

-- The size of each dog
CREATE TABLE size_of_dogs AS
  SELECT name, size
  FROM dogs, sizes
  WHERE height > min
  AND height <= max;


-- All dogs with parents ordered by decreasing height of their parent
CREATE TABLE by_parent_height AS
  SELECT child AS name
  FROM parents, dogs
  WHERE parent = name
  ORDER BY height DESC;


-- Sentences about siblings that are the same size
CREATE TABLE sentences AS
  SELECT "The two siblings, " || d1.name || " plus " ||
    d2.name ||" have the same size: " || s1.size
  FROM dogs AS d1, dogs AS d2, parents AS p1, parents AS p2,
  size_of_dogs AS s1, size_of_dogs AS s2
  WHERE d1.name = p1.child AND d2.name = p2.child
  AND d1.name = s1.name AND d2.name = s2.name
  AND p1.parent = p2.parent AND s1.size = s2.size
  AND d1.name < d2.name;


-- The almighty midterm score of the SICP'25 students
CREATE TABLE midterm_almighty AS
  SELECT MAX(p1_wwpd) + MAX(p2_env) + MAX(p3_lists) + MAX(p4_functions) + 
    MAX(p5_abstraction) + MAX(p6_tests) + MAX(p7_generators) + MAX(p8_bonus)
  FROM midterm;


-- The total score distribution of SICP'25 midterm exam
CREATE TABLE midterm_distribution AS
  SELECT FLOOR(total / 10) * 10, COUNT(*)
  FROM midterm
  GROUP BY FLOOR(total / 10) * 10
  ORDER BY FLOOR(total / 10) * 10 DESC;
