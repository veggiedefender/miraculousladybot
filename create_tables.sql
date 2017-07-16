SET client_encoding = 'UTF8';

CREATE TABLE fics (
    id bigint NOT NULL UNIQUE,
    body text NOT NULL,
    date bigint NOT NULL
);
