drop table if exists tasks;
create table tasks (
    id integer primary key autoincrement,
    name string not null,
    description string not null
);
insert into tasks (name, description) values ('Heat ovens', 'Make ovens very hot');
insert into tasks (name, description) values ('Forge', 'Create some iron stuff');
insert into tasks (name, description) values ('Pack', 'Put iron parts in to boxes');
drop table if exists maschines;
create table maschines (
    id integer primary key autoincrement,
    ip string not null,
    name string not null
);
insert into maschines (ip, name) values ('100.0.1.1', 'LoverCraft 1000');
insert into maschines (ip, name) values ('100.0.1.2', 'Master See');
insert into maschines (ip, name) values ('100.0.1.3', 'Master See 2');
insert into maschines (ip, name) values ('100.0.1.4', 'Guy 5000');
drop table if exists task_maschines;
create table task_maschines (
    id integer primary key autoincrement,
    maschine_id integer not null,
    task_id integer not null,
    stage integer not null,
    end_time datetime not null
);