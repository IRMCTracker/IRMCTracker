const { Events } = require("discord.js");

module.exports = {
    type: Events.GuildMemberAdd,
    execute: async (e) => {
        const role = e.guild.roles.cache.get(default_role);
        
        if (role) {
            e.roles.add(role);
        } else {
            console.warn('Invalid default role');
        }
    }
}
