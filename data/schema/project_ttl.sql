USE schoolms;

CREATE TABLE tl_account_status
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(10) NOT NULL,
    name varchar(10) NOT NULL,
    description text
);
CREATE UNIQUE INDEX autoindex_tl_account_status_1 ON tl_account_status (code);


CREATE TABLE tl_affiliation
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(40) NOT NULL,
    name varchar(40) NOT NULL,
    description text
);
CREATE UNIQUE INDEX autoindex_tl_affiliation_1 ON tl_affiliation (code);


CREATE TABLE tl_books_category
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(60) NOT NULL,
    name varchar(60) NOT NULL,
    description text
);
CREATE UNIQUE INDEX autoindex_tl_books_category_1 ON tl_books_category (code);


CREATE TABLE tl_books_sub_category
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(60) NOT NULL,
    name varchar(60) NOT NULL,
    description text,
    category_id integer NOT NULL,
    FOREIGN KEY (category_id) REFERENCES tl_books_category (id)
);
CREATE UNIQUE INDEX autoindex_tl_books_sub_category_1 ON tl_books_sub_category (code);
CREATE INDEX tl_books_sub_category_category_id_f52358d3 ON tl_books_sub_category (category_id);


CREATE TABLE tl_gender
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(10) NOT NULL,
    name varchar(10) NOT NULL,
    description text
);
CREATE UNIQUE INDEX autoindex_tl_gender_1 ON tl_gender (code);


CREATE TABLE tl_institution_levels
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(40) NOT NULL,
    name varchar(40) NOT NULL,
    description text
);
CREATE UNIQUE INDEX autoindex_tl_institution_levels_1 ON tl_institution_levels (code);


CREATE TABLE tl_institution_type
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(40) NOT NULL,
    name varchar(40) NOT NULL,
    description varchar(100)
);
CREATE UNIQUE INDEX autoindex_tl_institution_type_1 ON tl_institution_type (code);


CREATE TABLE tl_roles
(
    id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,
    code varchar(30) NOT NULL,
    name varchar(30) NOT NULL,
    description text
);
CREATE UNIQUE INDEX autoindex_tl_roles_1 ON tl_roles (code)



