USE schoolms;


/**************************************************************************************************/
CREATE TABLE auth_group
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name varchar(80) NOT NULL
);
CREATE UNIQUE INDEX sqlite_autoindex_auth_group_1 ON auth_group (name);

/**************************************************************************************************/
CREATE TABLE django_content_type
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    app_label varchar(100) NOT NULL,
    model varchar(100) NOT NULL
);
CREATE UNIQUE INDEX django_content_type_app_label_model_76bd3d3b_uniq ON django_content_type (app_label, model);

/**************************************************************************************************/
CREATE TABLE auth_permission
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    content_type_id integer NOT NULL,
    codename varchar(100) NOT NULL,
    name varchar(255) NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
);
CREATE UNIQUE INDEX auth_permission_content_type_id_codename_01ab375a_uniq ON auth_permission (content_type_id, codename);
CREATE INDEX auth_permission_content_type_id_2f476e4b ON auth_permission (content_type_id);

/**************************************************************************************************/
CREATE TABLE auth_group_permissions
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL,
    FOREIGN KEY (group_id) REFERENCES auth_group (id),
    FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
);
CREATE UNIQUE INDEX auth_group_permissions_group_id_permission_id_0cd325b0_uniq ON auth_group_permissions (group_id, permission_id);
CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON auth_group_permissions (group_id);
CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON auth_group_permissions (permission_id);

/**************************************************************************************************/
CREATE TABLE auth_user
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    password varchar(128) NOT NULL,
    last_login datetime,
    is_superuser bool NOT NULL,
    username varchar(150) NOT NULL,
    first_name varchar(30) NOT NULL,
    email varchar(254) NOT NULL,
    is_staff bool NOT NULL,
    is_active bool NOT NULL,
    date_joined datetime NOT NULL,
    last_name varchar(150) NOT NULL
);
CREATE UNIQUE INDEX sqlite_autoindex_auth_user_1 ON auth_user (username);

/**************************************************************************************************/
CREATE TABLE auth_user_groups
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user (id),
    FOREIGN KEY (group_id) REFERENCES auth_group (id)
);
CREATE UNIQUE INDEX auth_user_groups_user_id_group_id_94350c0c_uniq ON auth_user_groups (user_id, group_id);
CREATE INDEX auth_user_groups_user_id_6a12ed8b ON auth_user_groups (user_id);
CREATE INDEX auth_user_groups_group_id_97559544 ON auth_user_groups (group_id);


/**************************************************************************************************/
CREATE TABLE auth_user_user_permissions
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user (id),
    FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
);
CREATE UNIQUE INDEX auth_user_user_permissions_user_id_permission_id_14a6b632_uniq ON auth_user_user_permissions (user_id, permission_id);
CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON auth_user_user_permissions (user_id);
CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON auth_user_user_permissions (permission_id);


/**************************************************************************************************/
CREATE TABLE django_admin_log
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    action_time datetime NOT NULL,
    object_id text,
    object_repr varchar(200) NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    action_flag smallint unsigned NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
    FOREIGN KEY (user_id) REFERENCES auth_user (id)
);
CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON django_admin_log (content_type_id);
CREATE INDEX django_admin_log_user_id_c564eba6 ON django_admin_log (user_id);


/**************************************************************************************************/
CREATE TABLE django_migrations
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    app varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    applied datetime NOT NULL
);


/**************************************************************************************************/
CREATE TABLE django_session
(
    session_key varchar(40) PRIMARY KEY NOT NULL,
    session_data text NOT NULL,
    expire_date datetime NOT NULL
);
CREATE INDEX django_session_expire_date_a5c62663 ON django_session (expire_date);



-- =======================================




INSERT INTO django_content_type (app_label, model) VALUES 
('admin', 'logentry'),
('auth', 'permission'),
('auth', 'group'),
('auth', 'user'),
('contenttypes', 'contenttype'),
('sessions', 'session'),
('utilities', 'en_country'),
('utilities', 'en_sequenceutil'),
('utilities', 'en_zipcode'),
('utilities', 'tl_accountstatus'),
('sign_up', 'en_userregistration'),
('users', 'en_addressbook'),
('users', 'en_contacts'),
('users', 'en_users'),
('users', 'tl_gender'),
('login', 'en_logincredentials'),
('organization', 'en_organization'),
('organization', 'en_organizationgroup'),
('organization', 'tl_affiliation'),
('organization', 'tl_institutiontype'),
('roles', 'en_userroles'),
('roles', 'tl_roles'),
('activity', 'en_activitypattern'),
('activity', 'en_activity'),
('tasks', 'en_tasks'),
('messaging', 'en_message'),
('books', 'en_books'),
('books', 'tl_bookscategory'),
('books', 'tl_bookssubcategory'),
('roles', 'en_retireduserroles'),
('documents', 'en_documents'),
('school_timings', 'en_schooltimings'),
('organization', 'tl_institutionlevels'),
('classes', 'en_classes'),
('subjects', 'en_classsubjects'),
('school_timings', 'en_schooltimingbreakup');


INSERT INTO auth_permission (content_type_id, codename, name) VALUES (1, 'add_logentry', 'Can add log entry');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (1, 'change_logentry', 'Can change log entry');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (1, 'delete_logentry', 'Can delete log entry');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (1, 'view_logentry', 'Can view log entry');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (2, 'add_permission', 'Can add permission');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (2, 'change_permission', 'Can change permission');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (2, 'delete_permission', 'Can delete permission');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (2, 'view_permission', 'Can view permission');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (3, 'add_group', 'Can add group');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (3, 'change_group', 'Can change group');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (3, 'delete_group', 'Can delete group');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (3, 'view_group', 'Can view group');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (4, 'add_user', 'Can add user');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (4, 'change_user', 'Can change user');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (4, 'delete_user', 'Can delete user');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (4, 'view_user', 'Can view user');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (5, 'add_contenttype', 'Can add content type');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (5, 'change_contenttype', 'Can change content type');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (5, 'delete_contenttype', 'Can delete content type');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (5, 'view_contenttype', 'Can view content type');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (6, 'add_session', 'Can add session');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (6, 'change_session', 'Can change session');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (6, 'delete_session', 'Can delete session');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (6, 'view_session', 'Can view session');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (7, 'add_en_country', 'Can add e n_ country');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (7, 'change_en_country', 'Can change e n_ country');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (7, 'delete_en_country', 'Can delete e n_ country');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (7, 'view_en_country', 'Can view e n_ country');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (8, 'add_en_sequenceutil', 'Can add e n_ sequence util');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (8, 'change_en_sequenceutil', 'Can change e n_ sequence util');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (8, 'delete_en_sequenceutil', 'Can delete e n_ sequence util');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (8, 'view_en_sequenceutil', 'Can view e n_ sequence util');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (9, 'add_en_zipcode', 'Can add e n_ zipcode');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (9, 'change_en_zipcode', 'Can change e n_ zipcode');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (9, 'delete_en_zipcode', 'Can delete e n_ zipcode');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (9, 'view_en_zipcode', 'Can view e n_ zipcode');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (10, 'add_tl_accountstatus', 'Can add t l_ account status');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (10, 'change_tl_accountstatus', 'Can change t l_ account status');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (10, 'delete_tl_accountstatus', 'Can delete t l_ account status');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (10, 'view_tl_accountstatus', 'Can view t l_ account status');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (11, 'add_en_userregistration', 'Can add e n_ user registration');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (11, 'change_en_userregistration', 'Can change e n_ user registration');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (11, 'delete_en_userregistration', 'Can delete e n_ user registration');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (11, 'view_en_userregistration', 'Can view e n_ user registration');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (12, 'add_en_addressbook', 'Can add e n_ address book');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (12, 'change_en_addressbook', 'Can change e n_ address book');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (12, 'delete_en_addressbook', 'Can delete e n_ address book');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (12, 'view_en_addressbook', 'Can view e n_ address book');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (13, 'add_en_contacts', 'Can add e n_ contacts');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (13, 'change_en_contacts', 'Can change e n_ contacts');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (13, 'delete_en_contacts', 'Can delete e n_ contacts');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (13, 'view_en_contacts', 'Can view e n_ contacts');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (14, 'add_en_users', 'Can add e n_ users');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (14, 'change_en_users', 'Can change e n_ users');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (14, 'delete_en_users', 'Can delete e n_ users');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (14, 'view_en_users', 'Can view e n_ users');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (15, 'add_tl_gender', 'Can add t l_ gender');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (15, 'change_tl_gender', 'Can change t l_ gender');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (15, 'delete_tl_gender', 'Can delete t l_ gender');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (15, 'view_tl_gender', 'Can view t l_ gender');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (16, 'add_en_logincredentials', 'Can add e n_ login credentials');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (16, 'change_en_logincredentials', 'Can change e n_ login credentials');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (16, 'delete_en_logincredentials', 'Can delete e n_ login credentials');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (16, 'view_en_logincredentials', 'Can view e n_ login credentials');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (17, 'add_en_organization', 'Can add e n_ organization');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (17, 'change_en_organization', 'Can change e n_ organization');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (17, 'delete_en_organization', 'Can delete e n_ organization');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (17, 'view_en_organization', 'Can view e n_ organization');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (18, 'add_en_organizationgroup', 'Can add e n_ organization group');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (18, 'change_en_organizationgroup', 'Can change e n_ organization group');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (18, 'delete_en_organizationgroup', 'Can delete e n_ organization group');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (18, 'view_en_organizationgroup', 'Can view e n_ organization group');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (19, 'add_tl_affiliation', 'Can add t l_ affiliation');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (19, 'change_tl_affiliation', 'Can change t l_ affiliation');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (19, 'delete_tl_affiliation', 'Can delete t l_ affiliation');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (19, 'view_tl_affiliation', 'Can view t l_ affiliation');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (20, 'add_tl_institutiontype', 'Can add t l_ institution type');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (20, 'change_tl_institutiontype', 'Can change t l_ institution type');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (20, 'delete_tl_institutiontype', 'Can delete t l_ institution type');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (20, 'view_tl_institutiontype', 'Can view t l_ institution type');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (21, 'add_en_userroles', 'Can add e n_ user roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (21, 'change_en_userroles', 'Can change e n_ user roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (21, 'delete_en_userroles', 'Can delete e n_ user roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (21, 'view_en_userroles', 'Can view e n_ user roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (22, 'add_tl_roles', 'Can add t l_ roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (22, 'change_tl_roles', 'Can change t l_ roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (22, 'delete_tl_roles', 'Can delete t l_ roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (22, 'view_tl_roles', 'Can view t l_ roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (23, 'add_en_activitypattern', 'Can add e n_ activity pattern');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (23, 'change_en_activitypattern', 'Can change e n_ activity pattern');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (23, 'delete_en_activitypattern', 'Can delete e n_ activity pattern');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (23, 'view_en_activitypattern', 'Can view e n_ activity pattern');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (24, 'add_en_activity', 'Can add e n_ activity');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (24, 'change_en_activity', 'Can change e n_ activity');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (24, 'delete_en_activity', 'Can delete e n_ activity');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (24, 'view_en_activity', 'Can view e n_ activity');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (25, 'add_en_tasks', 'Can add e n_ tasks');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (25, 'change_en_tasks', 'Can change e n_ tasks');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (25, 'delete_en_tasks', 'Can delete e n_ tasks');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (25, 'view_en_tasks', 'Can view e n_ tasks');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (26, 'add_en_message', 'Can add e n_ message');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (26, 'change_en_message', 'Can change e n_ message');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (26, 'delete_en_message', 'Can delete e n_ message');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (26, 'view_en_message', 'Can view e n_ message');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (27, 'add_en_books', 'Can add e n_ books');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (27, 'change_en_books', 'Can change e n_ books');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (27, 'delete_en_books', 'Can delete e n_ books');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (27, 'view_en_books', 'Can view e n_ books');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (28, 'add_tl_bookscategory', 'Can add t l_ books category');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (28, 'change_tl_bookscategory', 'Can change t l_ books category');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (28, 'delete_tl_bookscategory', 'Can delete t l_ books category');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (28, 'view_tl_bookscategory', 'Can view t l_ books category');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (29, 'add_tl_bookssubcategory', 'Can add t l_ books sub category');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (29, 'change_tl_bookssubcategory', 'Can change t l_ books sub category');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (29, 'delete_tl_bookssubcategory', 'Can delete t l_ books sub category');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (29, 'view_tl_bookssubcategory', 'Can view t l_ books sub category');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (30, 'add_en_retireduserroles', 'Can add e n_ retired user roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (30, 'change_en_retireduserroles', 'Can change e n_ retired user roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (30, 'delete_en_retireduserroles', 'Can delete e n_ retired user roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (30, 'view_en_retireduserroles', 'Can view e n_ retired user roles');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (31, 'add_en_documents', 'Can add e n_ documents');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (31, 'change_en_documents', 'Can change e n_ documents');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (31, 'delete_en_documents', 'Can delete e n_ documents');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (31, 'view_en_documents', 'Can view e n_ documents');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (32, 'add_en_schooltimings', 'Can add e n_ school timings');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (32, 'change_en_schooltimings', 'Can change e n_ school timings');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (32, 'delete_en_schooltimings', 'Can delete e n_ school timings');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (32, 'view_en_schooltimings', 'Can view e n_ school timings');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (33, 'add_tl_institutionlevels', 'Can add t l_ institution levels');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (33, 'change_tl_institutionlevels', 'Can change t l_ institution levels');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (33, 'delete_tl_institutionlevels', 'Can delete t l_ institution levels');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (33, 'view_tl_institutionlevels', 'Can view t l_ institution levels');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (34, 'add_en_classes', 'Can add e n_ classes');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (34, 'change_en_classes', 'Can change e n_ classes');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (34, 'delete_en_classes', 'Can delete e n_ classes');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (34, 'view_en_classes', 'Can view e n_ classes');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (35, 'add_en_classsubjects', 'Can add e n_ class subjects');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (35, 'change_en_classsubjects', 'Can change e n_ class subjects');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (35, 'delete_en_classsubjects', 'Can delete e n_ class subjects');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (35, 'view_en_classsubjects', 'Can view e n_ class subjects');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (36, 'add_en_schooltimingbreakup', 'Can add e n_ school timing breakup');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (36, 'change_en_schooltimingbreakup', 'Can change e n_ school timing breakup');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (36, 'delete_en_schooltimingbreakup', 'Can delete e n_ school timing breakup');
INSERT INTO auth_permission (content_type_id, codename, name) VALUES (36, 'view_en_schooltimingbreakup', 'Can view e n_ school timing breakup');



INSERT INTO django_migrations (app, name, applied) VALUES ('contenttypes', '0001_initial', '2018-11-08 17:37:39.306364');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0001_initial', '2018-11-08 17:37:39.509402');
INSERT INTO django_migrations (app, name, applied) VALUES ('admin', '0001_initial', '2018-11-08 17:37:39.681238');
INSERT INTO django_migrations (app, name, applied) VALUES ('admin', '0002_logentry_remove_auto_add', '2018-11-08 17:37:39.853076');
INSERT INTO django_migrations (app, name, applied) VALUES ('admin', '0003_logentry_add_action_flag_choices', '2018-11-08 17:37:40.009286');
INSERT INTO django_migrations (app, name, applied) VALUES ('contenttypes', '0002_remove_content_type_name', '2018-11-08 17:37:40.149878');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0002_alter_permission_name_max_length', '2018-11-08 17:37:40.321770');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0003_alter_user_email_max_length', '2018-11-08 17:37:40.493547');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0004_alter_user_username_opts', '2018-11-08 17:37:40.712248');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0005_alter_user_last_login_null', '2018-11-08 17:37:40.884083');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0006_require_contenttypes_0002', '2018-11-08 17:37:40.962191');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0007_alter_validators_add_error_messages', '2018-11-08 17:37:41.102781');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0008_alter_user_username_max_length', '2018-11-08 17:37:41.227753');
INSERT INTO django_migrations (app, name, applied) VALUES ('auth', '0009_alter_user_last_name_max_length', '2018-11-08 17:37:41.352750');
INSERT INTO django_migrations (app, name, applied) VALUES ('sessions', '0001_initial', '2018-11-08 17:37:41.946334');
INSERT INTO django_migrations (app, name, applied) VALUES ('utilities', '0001_initial', '2018-11-08 17:37:42.071387');
INSERT INTO django_migrations (app, name, applied) VALUES ('users', '0001_initial', '2018-11-08 17:45:48.676559');
INSERT INTO django_migrations (app, name, applied) VALUES ('sign_up', '0001_initial', '2018-11-08 17:45:48.817099');
INSERT INTO django_migrations (app, name, applied) VALUES ('sign_up', '0002_auto_20181108_2315', '2018-11-08 17:45:49.020185');
INSERT INTO django_migrations (app, name, applied) VALUES ('login', '0001_initial', '2018-11-08 18:17:48.151391');
INSERT INTO django_migrations (app, name, applied) VALUES ('sign_up', '0003_auto_20181109_1826', '2018-11-09 12:56:15.736593');
INSERT INTO django_migrations (app, name, applied) VALUES ('sign_up', '0004_auto_20181110_0834', '2018-11-10 03:04:43.234159');
INSERT INTO django_migrations (app, name, applied) VALUES ('login', '0002_auto_20181112_1517', '2018-11-12 09:47:53.338014');
INSERT INTO django_migrations (app, name, applied) VALUES ('organization', '0001_initial', '2018-11-13 02:07:01.737139');
INSERT INTO django_migrations (app, name, applied) VALUES ('roles', '0001_initial', '2018-11-13 05:07:12.928008');
INSERT INTO django_migrations (app, name, applied) VALUES ('activity', '0001_initial', '2018-11-13 05:10:08.422790');
INSERT INTO django_migrations (app, name, applied) VALUES ('tasks', '0001_initial', '2018-11-14 08:24:07.470813');
INSERT INTO django_migrations (app, name, applied) VALUES ('messaging', '0001_initial', '2018-11-14 08:32:04.304556');
INSERT INTO django_migrations (app, name, applied) VALUES ('books', '0001_initial', '2018-11-14 08:44:00.368886');
INSERT INTO django_migrations (app, name, applied) VALUES ('roles', '0002_en_retireduserroles', '2018-11-28 02:26:09.740133');
INSERT INTO django_migrations (app, name, applied) VALUES ('documents', '0001_initial', '2018-11-29 17:19:05.977523');
INSERT INTO django_migrations (app, name, applied) VALUES ('sign_up', '0005_auto_20181129_2359', '2018-11-30 02:13:05.709035');
INSERT INTO django_migrations (app, name, applied) VALUES ('users', '0002_auto_20181130_0010', '2018-11-30 02:13:05.910959');
INSERT INTO django_migrations (app, name, applied) VALUES ('school_timings', '0001_initial', '2018-12-01 06:38:16.474046');
INSERT INTO django_migrations (app, name, applied) VALUES ('organization', '0002_tl_institutionlevels', '2018-12-01 06:57:15.334846');
INSERT INTO django_migrations (app, name, applied) VALUES ('classes', '0001_initial', '2018-12-01 07:44:01.340154');
INSERT INTO django_migrations (app, name, applied) VALUES ('documents', '0002_auto_20181201_2357', '2018-12-01 18:28:57.232655');
INSERT INTO django_migrations (app, name, applied) VALUES ('documents', '0003_auto_20181202_0004', '2018-12-01 18:34:47.207637');
INSERT INTO django_migrations (app, name, applied) VALUES ('documents', '0004_auto_20181202_0017', '2018-12-01 18:47:11.632947');
INSERT INTO django_migrations (app, name, applied) VALUES ('documents', '0005_auto_20181202_0029', '2018-12-01 18:59:52.284064');
INSERT INTO django_migrations (app, name, applied) VALUES ('subjects', '0001_initial', '2018-12-02 07:42:37.941340');
INSERT INTO django_migrations (app, name, applied) VALUES ('users', '0003_en_users_activation_token', '2018-12-02 09:08:09.725918');
INSERT INTO django_migrations (app, name, applied) VALUES ('school_timings', '0002_auto_20181204_1131', '2018-12-04 06:01:46.848095');
INSERT INTO django_migrations (app, name, applied) VALUES ('school_timings', '0003_auto_20181204_1218', '2018-12-04 06:48:38.855654');
INSERT INTO django_migrations (app, name, applied) VALUES ('school_timings', '0004_auto_20181204_1401', '2018-12-04 08:31:21.552177');
INSERT INTO django_migrations (app, name, applied) VALUES ('school_timings', '0005_remove_en_schooltimings_off_days', '2018-12-04 08:32:52.394568');
INSERT INTO django_migrations (app, name, applied) VALUES ('school_timings', '0006_remove_en_schooltimings_no_of_periods', '2018-12-05 01:50:57.214898');
INSERT INTO django_migrations (app, name, applied) VALUES ('school_timings', '0007_auto_20181205_0736', '2018-12-05 02:06:27.518555');


