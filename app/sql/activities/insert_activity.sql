INSERT INTO
    activities (
        email,
        id,
        sport,
        name,
        description,
        track,
        start_date,
        distance,
        duration,
        speed,
        elevation
    )
VALUES
    (
        %(email)s,
        %(id)s,
        %(sport)s,
        %(name)s,
        %(description)s,
        %(track)s,
        %(start_date)s,
        %(distance)s,
        %(duration)s,
        %(speed)s,
        %(elevation)s
    )
ON CONFLICT (id) DO NOTHING