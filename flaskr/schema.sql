DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS proxy;
DROP TABLE IF EXISTS socks;

CREATE TABLE user (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE
                     NOT NULL,
    password TEXT    NOT NULL
);

CREATE TABLE proxy (
    id        INTEGER   PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER   NOT NULL,
    created   TIMESTAMP NOT NULL,
    updated   TIMESTAMP NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,
    ip        TEXT      NOT NULL
                        UNIQUE,
    port      TEXT      NOT NULL,
    FOREIGN KEY (
        author_id
    )
REFERENCES user (id));

CREATE TABLE socks (
    id        INTEGER   PRIMARY KEY AUTOINCREMENT,

    updated   TIMESTAMP NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,
    delay     TEXT,
    ip        TEXT      NOT NULL
                        UNIQUE,
    port      TEXT      NOT NULL,
    author_id INTEGER   NOT NULL,
    FOREIGN KEY (
        author_id
    )
REFERENCES user (id));



