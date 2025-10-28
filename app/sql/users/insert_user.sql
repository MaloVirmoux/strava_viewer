INSERT INTO
    users (
        email,
        password,
        firstname,
        lastname,
        strava_user_id,
        profile_picture_url,
        strava_access_token,
        strava_expires_date,
        strava_refresh_token,
        import_task_id
    )
VALUES
    (
        %(email)s,
        %(password)s,
        %(firstname)s,
        %(lastname)s,
        %(strava_user_id)s,
        %(profile_picture_url)s,
        %(strava_access_token)s,
        %(strava_expires_date)s,
        %(strava_refresh_token)s,
        %(import_task_id)s
    )
ON CONFLICT (email) DO NOTHING