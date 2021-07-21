CREATE_SERVERS_TABLE = """
    CREATE TABLE IF NOT EXISTS `servers`
    (
        `id`              INT(25) PRIMARY KEY,
        `name`            VARCHAR(50) NOT NULL UNIQUE,
        `current_players` INT(5) NOT NULL,
        `top_players`     INT(5) NOT NULL,
        `latest_version`  VARCHAR(200) NOT NULL,
        `discord`         VARCHAR(60) NOT NULL
    )"""

INSERT_SERVER = """
    INSERT INTO `servers`(
        name,
        current_players,
        top_players, 
        latest_version,
        discord
    ) 
    VALUES 
    (
        '%name%',
        %current_players%,
        %top_players%, 
        '%latest_version%',
        '%discord%'
    )
"""