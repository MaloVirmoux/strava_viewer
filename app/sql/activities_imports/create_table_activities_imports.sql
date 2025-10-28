CREATE TABLE
    imports (
        email varchar NOT NULL,
        last_task_id varchar,
        last_start_date timestamp,
        last_end_date timestamp,
        CONSTRAINT imports_pk PRIMARY KEY (email)
    );