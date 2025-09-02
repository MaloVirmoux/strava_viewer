INSERT INTO
    users (
        email,
        password,
        session_key,
        firstname,
        lastname,
        strava_user_id,
        strava_access_token,
        strava_expires_date,
        strava_refresh_token
    )
VALUES
    (
        '{email}',
        '{password}',
        '{session_key}',
        '{firstname}',
        '{lastname}',
        '{strava_user_id}',
        '{strava_access_token}',
        '{strava_expires_date}',
        '{strava_refresh_token}'
    ) ON CONFLICT (email) DO
UPDATE
SET
    strava_access_token = excluded.strava_access_token,
    strava_expires_date = excluded.strava_expires_date,
    strava_refresh_token = excluded.strava_refresh_token