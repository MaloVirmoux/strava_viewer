SELECT
    email,
    new_activities,
    total_activities,
    last_task_id,
    last_start_date,
    last_end_date
FROM
    activities_imports
WHERE
    email = %(email)s
LIMIT
    1