import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { getServer } from '../../services/trackerService';
import { getServerMessage, checkChannelPermission } from '../../services/messagingService';


const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('server')
		.setDescription('💻 دریافت اطلاعات سرور مورد نظر')
		.addStringOption(option => option.setName('server').setDescription('اسم سرور').setRequired(true)),
	async execute(client, interaction) {
		if (!await checkChannelPermission(interaction, 'track')) return;

		const serverName: string = interaction.options.getString('server', true);

		await interaction.reply("🤔 چند لحظه صبر کن...");

		const server = await getServer(serverName);

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
