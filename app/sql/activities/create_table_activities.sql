CREATE TABLE
    activities (
        email varchar NOT NULL,
        id varchar NOT NULL,
        sport varchar,
        name varchar,
        description text,
        track text,
        start_date timestamp,
        distance float,
        duration interval,
        speed float,
        elevation float,
        CONSTRAINT activities_pk PRIMARY KEY (id)
    );