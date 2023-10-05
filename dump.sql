create table products
(
    id          int auto_increment
        primary key,
    name        varchar(128) not null,
    type        varchar(128) not null,
    size        varchar(128) not null,
    color       varchar(128) not null,
    sorting     varchar(128) not null,
    price       float        not null,
    description varchar(128) not null,
    quantity    int          not null
);

create table users
(
    guid     int auto_increment
        primary key,
    email    varchar(100) not null,
    name     varchar(128) not null,
    lastname varchar(128) not null,
    phone    varchar(32)  not null,
    type     varchar(32)  not null,
    company  varchar(128) null,
    password varchar(512) not null,
    constraint unq_email
        unique (email),
    constraint unq_phone
        unique (phone)
);

