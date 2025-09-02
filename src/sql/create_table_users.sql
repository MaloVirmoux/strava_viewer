CREATE TABLE
    users (
        email varchar NOT NULL,
        password varchar NOT NULL,
        session_key varchar,
        firstname varchar,
        lastname varchar,
        strava_user_id varchar,
        strava_access_token varchar,
        strava_expires_date timestamp,
        strava_refresh_token varchar,
        CONSTRAINT users_pk PRIMARY KEY (email)
    );