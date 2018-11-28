

insert into tl_institution_levels(id,code, name, description) VALUES
(1,'kinder_garden','Kinder Garden (KG)','Kinder Garden [LKG / UKG]'),
(2,'lower_primary','Lower Primary (LP)','Lower Primary [1st to 4th]'),
(3,'primary','Primary','Primary [5th to 7th]'),
(4,'secondary','Secondary (UP)','Upper Primary [8th to 10th]'),
(5,'senior_secondary','Senior Secondary','Senior Secondary [11th & 12th]'),
(6,'under_gratuate','Under Graduate (UG)','Under Graduate'),
(7,'post_graduate','Post Graduate (PG)','Post Graduate'),
(8,'research','Research Studies','Research Studies');







INSERT INTO en_classes (class_name, batch_nick_name, academic_starting_year, academic_ending_year, batch_name, organization_id, organization_level_id, timing_id)
    VALUES
      ('12-A','Computer Science','2018-11-11','2019-11-11','2018-19',1,5,1),
      ('12-B','Bio Maths - 1','2018-11-11','2019-11-11','2018-19',1,5,1),
      ('12-C','Bio Maths - 2','2018-11-11','2019-11-11','2018-19',1,5,1),
      ('12-D','Commerce','2018-11-11','2019-11-11','2018-19',1,5,1),
      ('11-A','Computer Science','2018-11-11','2019-11-11','2018-19',1,5,1),
      ('11-B','Bio Maths - 1','2018-11-11','2019-11-11','2018-19',1,5,1),
      ('11-D','Commerce','2018-11-11','2019-11-11','2018-19',1,5,1);
