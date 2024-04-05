import { SlashCommandBuilder } from 'discord.js';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('ping')
		.setDescription('Replies with Pong!'),
	async execute(_, interaction) {
		await interaction.reply('Pong!');
	},
};

export default command
