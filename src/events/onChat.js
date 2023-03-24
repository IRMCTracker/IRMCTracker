const { Events, EmbedBuilder} = require("discord.js");

const INVITE_REGEX = /discord\.(gg|com\/invite)\//i;
const LINK_REGEX = /http(s)?:\/\/[^\s]+/i;
const IPV4_REGEX = /^(\d{1,3}\.){3}\d{1,3}$/;
const IGNORED_ROLES = ['root'];

/**
 * Handling Commands
 */
module.exports = {
    type: Events.MessageCreate,
    async execute(message) {
        if (message.author.bot) return;

        // Check if the message author has one of the ignored roles
        const ignoreRole = message.guild.roles.cache.find(role => IGNORED_ROLES.includes(role.name));

        if (ignoreRole && message.member.roles.cache.has(ignoreRole.id)) return;

        // Check for links and discord invite links in message content
        if (LINK_REGEX.test(message.content) || INVITE_REGEX.test(message.content) || IPV4_REGEX.test(message.content)) {
            // Delete the message
            message.delete();

            const embed = new EmbedBuilder().setTitle(`🔴 ${message.author.username}, لطفا از ارسال هرگونه لینک خودداری کنید.`).setColor("Red");

            // Send a warning message in the channel
            message.channel.send({embeds: [embed]})
                .then(warning => {
                    setTimeout(() => {
                        if (!warning.deleted) {
                            warning.delete();
                        }
                    }, 3000);
                });
        }
    }
}
