const { Events } = require("discord.js");

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
    }
};
