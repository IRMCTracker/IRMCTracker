/**
 * Bootstrapping and running the bot
 */

const { Client, GatewayIntentBits } = require('discord.js');
const { token } = require('../config.json');

require('dotenv').config();

global.client = new Client({
	intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMembers, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent]
});

require('./bootstrap');

client.login(token);
