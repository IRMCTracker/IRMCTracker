import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { userNameToUUID } from '../../services/playerService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('head')
		.setDescription('🤌🏻 Get an image of your head')
		.addStringOption(option => option.setName('name').setDescription('Your skin name').setRequired(true)),
	async execute(client, interaction) {
		const userName: string = interaction.options.getString('name', true).toLowerCase();

		await interaction.reply('Finding your head... 🤔');

		const uuid = await userNameToUUID(userName);

		if (uuid == null) {
			return await interaction.editReply('☹️ I think you entered the wrong skin name because I can\'t find it.');
		}

		const embed = new EmbedBuilder()
			.setTitle(`💎 Skin ${userName}`)
			.setImage('attachment://head.png');

		await interaction.editReply({
			embeds: [embed],
			content: 'I found it 😍\n',
			files: [
				{
					attachment: `https://crafatar.com/renders/head/${uuid}?size=512&default=MHF_Steve&overlay`,
					name: 'head.png'
				}
			]
		});
	},
};

export default command;
