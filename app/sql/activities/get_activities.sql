SELECT
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
FROM
    activities
WHERE
    email = %(email)s