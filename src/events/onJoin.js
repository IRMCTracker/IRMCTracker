const { Events } = require("discord.js");

/**
 * Adding defualt role to newly joined members
 */
module.exports = {
    type: Events.GuildMemberAdd,
    async execute (e) {
        e.roles.add(e.guild.roles.cache.get(default_role))
    }
}
