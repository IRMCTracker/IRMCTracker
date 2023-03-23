const { Events } = require("discord.js");
const path = require("node:path");
const {findJSFiles} = require("../utils");
const {Sequelize} = require("sequelize");

/**
 * Handling jobs
 */
module.exports = {
    type: Events.ClientReady,
    async execute (c) {
        console.log(`\nReady! Logged in as ${c.user.tag}`);
        
        let counter = 0;
        setInterval(() => {
            client.jobs.forEach((job) => {
                if (counter % job.interval === 0) {
                    job.execute();
                }
            });
            counter += 1000;
        }, 1000);

        /* Connecting to database */
        const sequelize = new Sequelize(process.env.MARIADB_DATABASE, process.env.MARIADB_USERNAME, process.env.MARIADB_PASSWORD, {
            host: process.env.MARIADB_HOST,
            dialect: 'mariadb'
        });

        try {
            await sequelize.authenticate();
            console.log('Database connection has been established successfully.');
        } catch (error) {
            console.error('Unable to connect to the database:', error);
        }

        const modelsPath = path.join(__dirname, '../models');

        for (const modelPath of findJSFiles(modelsPath)) {
            const model = require(modelPath);
            model.init(sequelize);
            model.sync();
        }
    }
};
