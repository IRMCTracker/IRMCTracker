const { Events } = require("discord.js");

module.exports = {
    type: Events.ClientReady,
    execute: async (c) => console.log(`Ready! Logged in as ${c.user.tag}`)
};
