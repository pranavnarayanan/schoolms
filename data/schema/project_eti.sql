USE schoolms;


CREATE TABLE en_sequence_util
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(25) NOT NULL,
    value integer NOT NULL
);
CREATE UNIQUE INDEX autoindex_en_sequence_util_1 ON en_sequence_util (code);



CREATE TABLE en_country
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name varchar(100) NOT NULL,
    mobile_code varchar(5) NOT NULL,
    css_code varchar(15) NOT NULL
);
CREATE UNIQUE INDEX en_country_4c3132bf_uniq ON en_country (name, mobile_code, css_code);
CREATE UNIQUE INDEX autoindex_en_country_1 ON en_country (name);


CREATE TABLE en_zipcode
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    pincode varchar(8) NOT NULL,
    city varchar(20) NOT NULL,
    district varchar(20) NOT NULL,
    state varchar(20) NOT NULL,
    country_id integer NOT NULL,
    FOREIGN KEY (country_id) REFERENCES en_country (id)
);
CREATE INDEX en_zipcode_07a7e18e ON en_zipcode (country_id);


CREATE TABLE en_user_registration
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    session_token varchar(100) NOT NULL,
    mobile_number varchar(10),
    secondary_number varchar(15),
    is_landline_number bool NOT NULL,
    email_id varchar(254),
    website varchar(100),
    publish_your_site bool NOT NULL,
    date_of_birth date,
    display_picture varchar(100),
    permanent_house_name varchar(100),
    permanent_street varchar(100),
    permanent_landmark varchar(100),
    is_current_address bool NOT NULL,
    current_house_name varchar(100),
    current_street varchar(100),
    current_landmark varchar(100),
    username varchar(25),
    password varchar(25),
    subscribe_for_news_letter bool NOT NULL,
    current_zipcode varchar(7),
    gender_id integer,
    mobile_country_code_id integer,
    permanent_zipcode varchar(7),
    current_area_id integer,
    permanent_area_id integer,
    name varchar(100),
    FOREIGN KEY (gender_id) REFERENCES tl_gender (id),
    FOREIGN KEY (mobile_country_code_id) REFERENCES en_country (id),
    FOREIGN KEY (current_area_id) REFERENCES en_zipcode (id),
    FOREIGN KEY (permanent_area_id) REFERENCES en_zipcode (id)
);
CREATE UNIQUE INDEX autoindex_en_user_registration_1 ON en_user_registration (session_token);
CREATE UNIQUE INDEX autoindex_en_user_registration_2 ON en_user_registration (email_id);
CREATE INDEX en_user_registration_4f6a3ec6 ON en_user_registration (gender_id);
CREATE INDEX en_user_registration_1d9266a2 ON en_user_registration (mobile_country_code_id);
CREATE INDEX en_user_registration_c3b74141 ON en_user_registration (current_area_id);
CREATE INDEX en_user_registration_08358db8 ON en_user_registration (permanent_area_id);



CREATE TABLE en_contacts
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    mobile_number varchar(10) NOT NULL,
    secondary_number varchar(15),
    is_landline_number bool NOT NULL,
    email_id varchar(254),
    website varchar(100),
    publish_your_site bool NOT NULL,
    mobile_country_code_id integer NOT NULL,
    FOREIGN KEY (mobile_country_code_id) REFERENCES en_country (id)
);
CREATE UNIQUE INDEX autoindex_en_contacts_1 ON en_contacts (email_id);
CREATE INDEX en_contacts_5fd02f94 ON en_contacts (mobile_country_code_id);



CREATE TABLE en_users
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    product_id varchar(15) NOT NULL,
    name varchar(100) NOT NULL,
    date_of_birth date NOT NULL,
    display_picture varchar(100),
    newsletter_subscribe bool NOT NULL,
    account_status_id integer NOT NULL,
    contact_id integer NOT NULL,
    gender_id integer NOT NULL,
    activation_token varchar(200),
    FOREIGN KEY (account_status_id) REFERENCES tl_account_status (id),
    FOREIGN KEY (contact_id) REFERENCES en_contacts (id),
    FOREIGN KEY (gender_id) REFERENCES tl_gender (id)
);
CREATE UNIQUE INDEX autoindex_en_users_1 ON en_users (product_id);
CREATE UNIQUE INDEX autoindex_en_users_2 ON en_users (contact_id);
CREATE INDEX en_users_account_status_id_7119a9de ON en_users (account_status_id);
CREATE INDEX en_users_c9b8d30e ON en_users (gender_id);



CREATE TABLE en_address_book
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    house_name varchar(100) NOT NULL,
    street varchar(100),
    landmark varchar(100),
    is_current_address bool NOT NULL,
    is_permanent_address bool NOT NULL,
    user_id integer NOT NULL,
    zipcode_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES en_users (id),
    FOREIGN KEY (zipcode_id) REFERENCES en_zipcode (id)
);
CREATE UNIQUE INDEX en_address_book_e9f8f7b6_uniq ON en_address_book (user_id, house_name, zipcode_id, is_current_address, is_permanent_address);
CREATE INDEX en_address_book_d31bdb80 ON en_address_book (user_id);
CREATE INDEX en_address_book_51b1e17c ON en_address_book (zipcode_id);


CREATE TABLE en_login_credentials
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    username varchar(25) NOT NULL,
    password varchar(25) NOT NULL,
    password_history varchar(130),
    is_online bool NOT NULL,
    user_id integer NOT NULL,
    current_logged_in_time datetime NOT NULL,
    last_logged_in_time datetime,
    FOREIGN KEY (user_id) REFERENCES en_users (id)
);
CREATE UNIQUE INDEX autoindex_en_login_credentials_1 ON en_login_credentials (username);
CREATE UNIQUE INDEX autoindex_en_login_credentials_2 ON en_login_credentials (user_id);


CREATE TABLE en_message
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    send_datetime datetime NOT NULL,
    message varchar(500) NOT NULL,
    read_status bool NOT NULL,
    send_by_id integer NOT NULL,
    send_to_id integer NOT NULL,
    FOREIGN KEY (send_by_id) REFERENCES en_users (id),
    FOREIGN KEY (send_to_id) REFERENCES en_users (id)
);
CREATE INDEX en_message_bcec9baa ON en_message (send_by_id);
CREATE INDEX en_message_b8a227c6 ON en_message (send_to_id);




CREATE TABLE en_organization_group
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    product_id varchar(12) NOT NULL,
    group_name varchar(100) NOT NULL,
    logo varchar(100),
    website varchar(100),
    publish_your_site bool NOT NULL,
    account_status_id integer NOT NULL,
    FOREIGN KEY (account_status_id) REFERENCES tl_account_status (id)
);
CREATE UNIQUE INDEX autoindex_en_organization_group_1 ON en_organization_group (product_id);
CREATE UNIQUE INDEX en_organization_group_317f41b7_uniq ON en_organization_group (group_name, website);
CREATE INDEX en_organization_group_cd47a2be ON en_organization_group (account_status_id);



CREATE TABLE en_organization
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    product_id varchar(12) NOT NULL,
    school_name varchar(12) NOT NULL,
    started_date date NOT NULL,
    display_picture varchar(100),
    mobile_number_1 varchar(10) NOT NULL,
    mobile_number_2 varchar(10) NOT NULL,
    landline_number_1 varchar(13) NOT NULL,
    landline_number_2 varchar(13),
    email_id varchar(254),
    website varchar(100),
    publish_your_site bool NOT NULL,
    street varchar(100),
    registration_id varchar(100),
    account_status_id integer NOT NULL,
    affiliation_id integer,
    mobile_country_code_id integer NOT NULL,
    organization_group_id integer NOT NULL,
    organization_type_id integer,
    zipcode_id integer NOT NULL,
    FOREIGN KEY (account_status_id) REFERENCES tl_account_status (id),
    FOREIGN KEY (affiliation_id) REFERENCES tl_affiliation (id),
    FOREIGN KEY (mobile_country_code_id) REFERENCES en_country (id),
    FOREIGN KEY (organization_group_id) REFERENCES en_organization_group (id),
    FOREIGN KEY (organization_type_id) REFERENCES tl_institution_type (id),
    FOREIGN KEY (zipcode_id) REFERENCES en_zipcode (id)
);
CREATE UNIQUE INDEX autoindex_en_organization_1 ON en_organization (product_id);
CREATE UNIQUE INDEX en_organization_ec43b96d_uniq ON en_organization (school_name, zipcode_id, registration_id);
CREATE UNIQUE INDEX autoindex_en_organization_2 ON en_organization (registration_id);
CREATE INDEX en_organization_e572815f ON en_organization (account_status_id);
CREATE INDEX en_organization_0c967115 ON en_organization (affiliation_id);
CREATE INDEX en_organization_0b2fd651 ON en_organization (mobile_country_code_id);
CREATE INDEX en_organization_594153a4 ON en_organization (organization_group_id);
CREATE INDEX en_organization_7cb50d43 ON en_organization (organization_type_id);
CREATE INDEX en_organization_186b412f ON en_organization (zipcode_id);




CREATE TABLE en_user_roles
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    approved bool NOT NULL,
    request_approved_on datetime,
    request_raised_on datetime NOT NULL,
    is_selected_role bool NOT NULL,
    related_organization_id integer,
    related_organization_group_id integer,
    related_user_id integer,
    request_approved_by_id integer,
    request_raised_by_id integer NOT NULL,
    role_id integer NOT NULL,
    user_id integer NOT NULL,
    FOREIGN KEY (related_organization_id) REFERENCES en_organization (id),
    FOREIGN KEY (related_organization_group_id) REFERENCES en_organization_group (id),
    FOREIGN KEY (related_user_id) REFERENCES en_users (id),
    FOREIGN KEY (request_approved_by_id) REFERENCES en_users (id),
    FOREIGN KEY (request_raised_by_id) REFERENCES en_users (id),
    FOREIGN KEY (role_id) REFERENCES tl_roles (id),
    FOREIGN KEY (user_id) REFERENCES en_users (id)
);
CREATE UNIQUE INDEX en_user_roles_af9eacc2_uniq ON en_user_roles (user_id, role_id, related_organization_id, related_organization_group_id, related_user_id);
CREATE INDEX en_user_roles_e97ea84c ON en_user_roles (related_organization_id);
CREATE INDEX en_user_roles_13a80fb7 ON en_user_roles (related_organization_group_id);
CREATE INDEX en_user_roles_a7ab31e0 ON en_user_roles (related_user_id);
CREATE INDEX en_user_roles_03317323 ON en_user_roles (request_approved_by_id);
CREATE INDEX en_user_roles_ddfcd4b8 ON en_user_roles (request_raised_by_id);
CREATE INDEX en_user_roles_3cb1ae77 ON en_user_roles (role_id);
CREATE INDEX en_user_roles_54009231 ON en_user_roles (user_id);



CREATE TABLE en_retired_user_roles
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    user_role_id integer NOT NULL,
    request_approved_on datetime,
    request_raised_on datetime NOT NULL,
    related_organization_id integer,
    related_organization_group_id integer,
    related_user_id integer,
    request_approved_by_id integer,
    request_raised_by_id integer NOT NULL,
    role_id integer NOT NULL,
    user_id integer NOT NULL,
    FOREIGN KEY (related_organization_id) REFERENCES en_organization (id),
    FOREIGN KEY (related_organization_group_id) REFERENCES en_organization_group (id),
    FOREIGN KEY (related_user_id) REFERENCES en_users (id),
    FOREIGN KEY (request_approved_by_id) REFERENCES en_users (id),
    FOREIGN KEY (request_raised_by_id) REFERENCES en_users (id),
    FOREIGN KEY (role_id) REFERENCES tl_roles (id),
    FOREIGN KEY (user_id) REFERENCES en_users (id)
);
CREATE UNIQUE INDEX autoindex_en_retired_user_roles_1 ON en_retired_user_roles (user_role_id);
CREATE INDEX en_retired_user_roles_5d999827 ON en_retired_user_roles (related_organization_id);
CREATE INDEX en_retired_user_roles_2f6e13e3 ON en_retired_user_roles (related_organization_group_id);
CREATE INDEX en_retired_user_roles_38cd4297 ON en_retired_user_roles (related_user_id);
CREATE INDEX en_retired_user_roles_d8d96cbb ON en_retired_user_roles (request_approved_by_id);
CREATE INDEX en_retired_user_roles_7bc60e55 ON en_retired_user_roles (request_raised_by_id);
CREATE INDEX en_retired_user_roles_a0accc38 ON en_retired_user_roles (role_id);
CREATE INDEX en_retired_user_roles_7c47e4ce ON en_retired_user_roles (user_id);




CREATE TABLE en_activity_pattern
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    pattern_name varchar(100) NOT NULL,
    subject varchar(100) NOT NULL,
    description varchar(500) NOT NULL,
    priority integer NOT NULL,
    escalation_days integer NOT NULL
);
CREATE UNIQUE INDEX autoindex_en_activity_pattern_1 ON en_activity_pattern (pattern_name);


CREATE TABLE en_activity
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    created_on datetime NOT NULL,
    table_name varchar(100),
    read_status bool NOT NULL,
    can_change_read_status_direclty bool NOT NULL,
    created_by_id integer,
    created_to_id integer NOT NULL,
    en_user_role_id integer,
    escalated_from_id integer,
    pattern_id integer NOT NULL,
    FOREIGN KEY (created_by_id) REFERENCES en_users (id),
    FOREIGN KEY (created_to_id) REFERENCES en_users (id),
    FOREIGN KEY (en_user_role_id) REFERENCES en_user_roles (id),
    FOREIGN KEY (escalated_from_id) REFERENCES en_users (id),
    FOREIGN KEY (pattern_id) REFERENCES en_activity_pattern (id)
);
CREATE INDEX en_activity_d622181e ON en_activity (created_by_id);
CREATE INDEX en_activity_3ce86d40 ON en_activity (created_to_id);
CREATE INDEX en_activity_dc60cfc0 ON en_activity (en_user_role_id);
CREATE INDEX en_activity_05a1df8e ON en_activity (escalated_from_id);
CREATE INDEX en_activity_67903b40 ON en_activity (pattern_id);



CREATE TABLE en_school_timings
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    timing_name varchar(150) NOT NULL,
    school_starting_time time NOT NULL,
    school_closing_time time NOT NULL,
    no_of_periods integer NOT NULL,
    organization_id integer NOT NULL,
    assembly_duration integer,
    assembly_on_friday bool NOT NULL,
    assembly_on_monday bool NOT NULL,
    assembly_on_saturday bool NOT NULL,
    assembly_on_sunday bool NOT NULL,
    assembly_on_thursday bool NOT NULL,
    assembly_on_tuesday bool NOT NULL,
    assembly_on_wednesday bool NOT NULL,
    class_on_friday bool NOT NULL,
    class_on_monday bool NOT NULL,
    class_on_saturday bool NOT NULL,
    class_on_sunday bool NOT NULL,
    class_on_thursday bool NOT NULL,
    class_on_tuesday bool NOT NULL,
    class_on_wednesday bool NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES en_organization (id)
);
CREATE UNIQUE INDEX en_school_timings_3bd85b91_uniq ON en_school_timings (organization_id, timing_name);
CREATE INDEX en_school_timings_82efbc78 ON en_school_timings (organization_id);



CREATE TABLE en_school_timing_breakup
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    is_break bool NOT NULL,
    is_period bool NOT NULL,
    duration integer NOT NULL,
    description varchar(100),
    timing_id integer NOT NULL,
    FOREIGN KEY (timing_id) REFERENCES en_school_timings (id)
);
CREATE INDEX en_school_timing_c485ddfb ON en_school_timing_breakup (timing_id);




CREATE TABLE en_books
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name varchar(150) NOT NULL,
    volume integer NOT NULL,
    book_code varchar(100),
    author varchar(100),
    publisher varchar(100),
    published_year integer NOT NULL,
    category_id integer NOT NULL,
    sub_category_id integer,
    FOREIGN KEY (category_id) REFERENCES tl_books_category (id),
    FOREIGN KEY (sub_category_id) REFERENCES tl_books_sub_category (id)
);
CREATE UNIQUE INDEX en_books_b1680dfe_uniq ON en_books (name, volume, author, publisher, published_year, category_id);
CREATE INDEX en_books_1fd874be ON en_books (category_id);
CREATE INDEX en_books_72ab3fab ON en_books (sub_category_id);


CREATE TABLE en_classes
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    class_name varchar(100) NOT NULL,
    batch_nick_name varchar(100),
    academic_starting_year date NOT NULL,
    academic_ending_year date,
    batch_name varchar(100) NOT NULL,
    organization_id integer NOT NULL,
    organization_level_id integer NOT NULL,
    timing_id integer NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES en_organization (id),
    FOREIGN KEY (organization_level_id) REFERENCES tl_institution_levels (id),
    FOREIGN KEY (timing_id) REFERENCES en_school_timings (id)
);
CREATE UNIQUE INDEX en_classes_25e1c55c_uniq ON en_classes (organization_id, class_name, academic_starting_year);
CREATE INDEX en_classes_cf3ca0d4 ON en_classes (organization_id);
CREATE INDEX en_classes_430fccca ON en_classes (organization_level_id);
CREATE INDEX en_classes_14826e94 ON en_classes (timing_id);

CREATE TABLE en_class_subjects
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    subject_name varchar(100),
    duration integer,
    class_fk_id integer NOT NULL,
    FOREIGN KEY (class_fk_id) REFERENCES en_classes (id)
);
CREATE UNIQUE INDEX en_class_subjects_db1304f4_uniq ON en_class_subjects (class_fk_id, subject_name);
CREATE INDEX en_class_subjects_6ae73bc4 ON en_class_subjects (class_fk_id);



CREATE TABLE en_tasks
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    created_date datetime NOT NULL,
    to_be_done_on date NOT NULL,
    to_be_done_at time,
    priority integer NOT NULL,
    task varchar(200) NOT NULL,
    done_status bool NOT NULL,
    assigned_by_id integer NOT NULL,
    assigned_to_id integer,
    FOREIGN KEY (assigned_by_id) REFERENCES en_users (id),
    FOREIGN KEY (assigned_to_id) REFERENCES en_users (id)
);
CREATE UNIQUE INDEX en_tasks_ff0262be_uniq ON en_tasks (to_be_done_on, to_be_done_at, assigned_to_id, task);
CREATE INDEX en_tasks_8b845c58 ON en_tasks (assigned_by_id);
CREATE INDEX en_tasks_2080224c ON en_tasks (assigned_to_id);

