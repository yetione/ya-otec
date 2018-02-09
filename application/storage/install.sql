CREATE TABLE urls
(
	id INTEGER PRIMARY KEY AUTOINCREMENT ,
	address VARCHAR(255) not null,
	headers TEXT,
	cookies TEXT,
	date_add INT NOT NULL,
	last_visit INT NOT NULL,
	request_type VARCHAR(10) DEFAULT 'GET' NOT NULL,
	is_active INT DEFAULT 1 NOT NULL,
	add_by VARCHAR(100)
);

CREATE TABLE options
(
    option_key VARCHAR(100) PRIMARY KEY NOT NULL,
    option_value BLOB
);
CREATE UNIQUE INDEX options_option_key_uindex ON options (option_key);

