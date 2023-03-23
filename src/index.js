/**
 * Bootstrapping and running the bot
 */

const { Client, GatewayIntentBits } = require('discord.js');
const { token } = require('../config.json');

require('dotenv').config();

global.client = new Client({
	intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers]
});

require('./bootstrap');

client.login(token);
