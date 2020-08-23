CREATE TABLE monitoring_group (
    id int not null auto_increment,
    name varchar(255),
    seed varchar(255),
    is_cluster tinyint(1),
    created_at timestamp,
    PRIMARY KEY(id),
    KEY `idx_name` (`name`)
);

CREATE TABLE unit (
    id int not null auto_increment,
    addr varchar(255),
    group_id int,
    created_at timestamp,
    is_master tinyint(1),
    PRIMARY KEY(id),
    KEY `idx_addr` (`addr`),
    KEY `idx_group_id` (`group_id`)
);

CREATE TABLE metric (
    id int not null auto_increment
    unit_id int,
    value varchar(255),
    created_at timestamp,
    PRIMARY KEY(id),
    KEY `idx_unit_id` (`unit_id`)
);
