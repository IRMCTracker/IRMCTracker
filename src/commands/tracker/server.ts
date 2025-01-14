import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { getServer } from '../../services/trackerService';
import { getServerMessage, checkChannelPermission } from '../../services/messagingService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('server')
		.setDescription('💻 Retrieve information about the specified server')
		.addStringOption(option => option.setName('server').setDescription('Server name').setRequired(true)),
	async execute(client, interaction) {
		if (!await checkChannelPermission(interaction, 'track')) return;

		const serverName: string = interaction.options.getString('server', true);

		await interaction.reply("🤔 Hold on for a moment...");

		const server = await getServer(serverName);

		if (!server) {
			return await interaction.editReply({
				content: '',
				embeds: [
					new EmbedBuilder()
						.setColor("Red")
						.setTitle('🔴 The specified server does not exist!')
				]
			});
		}

		const message = getServerMessage(client, server);

		await interaction.editReply(message);
	},
};

export default command;
