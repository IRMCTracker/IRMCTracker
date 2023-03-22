const { Client, Events, GatewayIntentBits, User } = require('discord.js');
const { token, default_role } = require('./config.json');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers] });


client.once(Events.ClientReady, c => {
	console.log(`Ready! Logged in as ${c.user.tag}`);
});

client.on(Events.GuildMemberAdd, e => e.roles.add([e.guild.roles.cache.get(default_role)]))

client.login(token);
