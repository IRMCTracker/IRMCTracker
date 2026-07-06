import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { getServer, TrackerUnavailableError } from '../../services/trackerService';
import { getServerMessage, getServerUnavailableMessage, checkChannelPermission } from '../../services/messagingService';


const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('server')
		.setDescription('💻 دریافت اطلاعات سرور مورد نظر')
		.addStringOption(option => option.setName('server').setDescription('اسم سرور').setRequired(true)),
	async execute(client, interaction) {
		if (!await checkChannelPermission(interaction, 'track')) return;

		const serverName: string = interaction.options.getString('server', true);

		await interaction.reply("🤔 چند لحظه صبر کن...");

		let server;
		try {
			server = await getServer(serverName);
		} catch (error) {
			if (error instanceof TrackerUnavailableError) {
				return await interaction.editReply(getServerUnavailableMessage(serverName));
			}
			throw error;
		}

		if (server == null) {
			return await interaction.editReply({
				content: '',
				embeds: [
					new EmbedBuilder()
						.setColor("Red")
						.setTitle('🔴 سرور وارد شده وجود نداره!')
				]
			});
		}

		const message = getServerMessage(client, server);

		await interaction.editReply(message);
	},

};

export default command
