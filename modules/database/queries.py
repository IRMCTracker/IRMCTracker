CREATE_TABLES = """
    CREATE TABLE IF NOT EXISTS `servers`
    (
        `id`              INT(25) PRIMARY KEY,
        `name`            VARCHAR(50) NOT NULL UNIQUE,
        `current_players` INT(5) NOT NULL,
        `top_players`     INT(5) NOT NULL,
        `latest_version`  VARCHAR(200) NOT NULL,
        `discord`         VARCHAR(60) NOT NULL
    )"""