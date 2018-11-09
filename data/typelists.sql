insert into tl_roles (id,code, name, description) VALUES
(1,'site_admin','Site Admin','Site Admin'),
(2,'institution_super_user','Super User','Institution Super User'),
(3,'director','Director','Director'),
(4,'board_member','Board Member','Board Member'),
(5,'school_admin','School Admin','School Admin'),
(6,'principal','Principal','Principal'),
(7,'teacher','Teacher','Teacher'),
(8,'student','Student','Student'),
(9,'parent','Parent','Parent'),
(10,'librarian','Librarian','Librarian'),
(11,'accountant','Accountant','Accountant'),
(12,'lab_assistant','Lab Assistant','Lab Assistant'),
(13,'enquiry_assistant','Enquiry Assistant','Enquiry Assistant'),
(14,'security','Securty','School Security');

insert into tl_affiliation(id,code, name, description) VALUES
(1,'cbse_syllabus','CBSE','Central Board Of Secondary Education'),
(2,'icse_syllabus','ICSE','ICSE'),
(3,'state_syllabus','State Syllabus','State Syllabus'),
(4,'kerala_university','Kerala / Abdul Kalam University','Kerala / Abdul Kalam University'),
(5,'cusat','Cochin University','Cochin Uiversity'),
(6,'mahatma_gandhi','MG University','MG Uiversity');

insert into tl_institution_levels(id,code, name, description) VALUES
(1,'kinder_garden','Kinder Garden (KG)','Kinder Garden [LKG / UKG]'),
(2,'lower_primary','Lower Primary (LP)','Lower Primary [1st to 4th]'),
(3,'primary','Primary','Primary [5th to 7th]'),
(4,'secondary','Secondary (UP)','Upper Primary [8th to 10th]'),
(5,'senior_secondary','Senior Secondary','Senior Secondary [11th & 12th]'),
(6,'under_gratuate','Under Graduate (UG)','Under Graduate'),
(7,'post_graduate','Post Graduate (PG)','Post Graduate'),
(8,'research','Research Studies','Research Studies');

insert into tl_institution_type(id,code, name, description) VALUES
(1,'school','School','School Education'),
(2,'engineering','Engineering','All Engineering Studies'),
(3,'medicine','Medical Science','All Medical Subjects'),
(4,'law','Law','Law College'),
(5,'arts','Arts','Arts College'),
(6,'business','Business','Business Studies');

INSERT INTO tl_books_category(id,code, name, description) VALUES
(1,'science','Science','Science'),
(2,'mathematics','Mathematics','Mathematics'),
(3,'fiction','Fiction','Fiction'),
(4,'literature','Literature','Literature');

INSERT INTO tl_books_sub_category(id,code, name, category_id, description) VALUES
(1,'physics','Physics',1,'Physics'),
(2,'chemistry','Chemistry',1,'Chemistry'),
(3,'biology','Biology',1,'Biology');


