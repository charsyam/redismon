CREATE TABLE `monitoring_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `seed` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `is_cluster` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_name` (`name`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE `unit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `addr` varchar(255) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  `role` varchar(16) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `failure_count` int DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_addr` (`addr`),
  KEY `idx_group_id` (`group_id`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE metric (
    id int not null auto_increment,
    unit_id int,
    value text,
    created_at timestamp,
    PRIMARY KEY(id),
    KEY `idx_unit_id` (`unit_id`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;

CREATE TABLE event (
    id int not null auto_increment,
    unit_id int,
    value text,
    last_metric_created_at timestamp,
    created_at timestamp,
    PRIMARY KEY(id),
    KEY `idx_unit_id` (`unit_id`),
    KEY `idx_last_metric_created_at` (`created_at`),
    KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
