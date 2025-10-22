INSERT INTO
    activities_imports (
        email,
        new_activities,
        total_activities,
        last_task_id,
        last_start_date,
        last_end_date
    )
VALUES
    (
        %(email)s,
        %(new_activities)s,
        %(total_activities)s,
        %(last_task_id)s,
        %(last_start_date)s,
        %(last_end_date)s
    )
ON CONFLICT (email) DO NOTHING