insert into tl_account_status (id, code, name, description) VALUES
(1,'inactive','Inactive','Account is Inactive'),
(2,'active','Active','Account is Active'),
(3,'retired','Retired','Account is Retired'),
(4,'blocked','Blocked','Account is Blocked');

INSERT INTO en_country (id,name,mobile_code,css_code) VALUES
(1,'India','+91','in'),
(2,'Pakisthan','+92','pk');

insert into tl_gender (id,code, name, description) VALUES
(1,'male','Male','Male'),
(2,'female','Female','Female'),
(3,'other','Other','Other');

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


insert into tl_institution_type(id,code, name, description) VALUES
(1,'school','School','School Education'),
(2,'engineering','Engineering','All Engineering Studies'),
(3,'medicine','Medical Science','All Medical Subjects'),
(4,'law','Law','Law College'),
(5,'arts','Arts','Arts College'),
(6,'business','Business','Business Studies');

INSERT INTO en_activity_pattern (id, pattern_name, subject, description, priority, escalation_days) VALUES
(1,'first_user_login','Welcome To Myshishya','Welcome To Myshishya',1,0),
(2,'received_role_request','Role Request','Received new role request',1,3),
(3,'role_request_rejected','Role Request Rejected','Role request Rejected',1,0),
(4,'role_request_approved','Role Request Approved','Role request Approved',1,0),
(5,'assigned_new_role','New Role Assigned','New Role Assigned',1,0);

