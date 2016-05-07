SET client_encoding = 'UTF8';

CREATE TABLE logs (
    id bigint NOT NULL UNIQUE,
    blog character varying(50) NOT NULL,
    content text NOT NULL,
    date bigint NOT NULL
);