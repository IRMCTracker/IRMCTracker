const { Events } = require("discord.js");

module.exports = {
    type: Events.ClientReady,
    execute: async (c) => {
        console.log(`Ready! Logged in as ${c.user.tag}`);
        
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
