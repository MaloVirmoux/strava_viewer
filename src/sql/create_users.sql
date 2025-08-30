CREATE TABLE users (
	user_id int8 NOT NULL,
	user_name varchar NULL,
	access_token varchar NULL,
	expires_date timestamp NULL,
	refresh_token varchar NULL,
	last_connection timestamp NULL,
	CONSTRAINT users_pk PRIMARY KEY (user_id)
);
