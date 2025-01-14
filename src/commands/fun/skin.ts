import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { userNameToUUID } from '../../services/playerService';
import { checkChannelPermission } from '../../services/messagingService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('skin')
		.setDescription('🤌🏻 Get an image of your skin')
			.addStringOption(option => option.setName('name').setDescription('Your skin name').setRequired(true)),
	async execute(_, interaction) {
		if (!await checkChannelPermission(interaction, 'skin')) return;

		const userName: string = interaction.options.getString('name', true);
		
		await interaction.reply('Searching for your skin... 🤔');
		
		const uuid = await userNameToUUID(userName);

		if (!uuid) {
			return await interaction.editReply('☹️ I think you entered the skin name incorrectly because I can’t find it.');
		}

		const embed = new EmbedBuilder()
			.setTitle(`💎 Skin ${userName}`)
			.setImage('attachment://skin.png');
		
		await interaction.editReply({
			embeds: [embed],
			content: 'I found it! 😍\n',
			files: [
				{
					name: 'skin.png',
					attachment: `https://crafatar.com/renders/body/${uuid}?size=512&default=MHF_Steve&overlay`
				}
			]
		});
	},
};

export default command;
