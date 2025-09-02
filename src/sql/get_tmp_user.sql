SELECT
    strava_user_id,
    strava_access_token,
    strava_expires_date,
    strava_refresh_token
FROM
    tmp_users
WHERE
    strava_user_id = '{strava_user_id}'
LIMIT
    1