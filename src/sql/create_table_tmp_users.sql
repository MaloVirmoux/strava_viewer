CREATE TABLE
    tmp_users (
        strava_user_id varchar,
        strava_access_token varchar,
        strava_expires_date timestamp,
        strava_refresh_token varchar,
        CONSTRAINT tmp_users_pk PRIMARY KEY (strava_user_id)
    );