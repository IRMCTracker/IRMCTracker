const { SlashCommandBuilder, EmbedBuilder } = require("discord.js");
const Server = require('../../models/Server');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('servers')
		.setDescription('💻 دریافت لیستی از تمام سرور های موجود'),
	async execute(interaction) {
	},
};
