SELECT
    email,
    password,
    firstname,
    lastname,
    strava_user_id,
    strava_access_token,
    strava_expires_date,
    strava_refresh_token
FROM
    users
WHERE
    email = '{email}'
LIMIT
    1