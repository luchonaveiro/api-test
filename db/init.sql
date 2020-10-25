create schema users;

create table users.user
(
    id varchar(100) primary key,
    document int not null,
    name varchar(100) not null,
    email varchar(100) not null
);