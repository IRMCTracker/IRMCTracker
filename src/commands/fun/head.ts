import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { userNameToUUID } from '../../services/playerService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('head')
		.setDescription('🤌🏻 دریافت تصویری از کله شما')
		.addStringOption(option => option.setName('name').setDescription('نام اسکین شما').setRequired(true)),
	async execute(client, interaction) {
		const userName: string = interaction.options.getString('name', true).toLowerCase();

		await interaction.reply('دارم کلتو پیدا میکنم... 🤔');

		const uuid = await userNameToUUID(userName);

		if (uuid == null) {
			return await interaction.editReply('☹️ فکر کنم اشتباه نوشتی اسم اسکین رو چون نمیتونم پیداش کنم');
		}

		const embed = new EmbedBuilder()
			.setTitle(`💎 Skin ${userName}`)
			.setImage('attachment://head.png');

		await interaction.editReply({
			embeds: [embed],
			content: 'پیداش کردم 😍\n',
			files: [
				{
					attachment: `https://crafatar.com/renders/head/${uuid}?size=512&default=MHF_Steve&overlay`,
					name: 'head.png'
				}
			]
		});
	},
};

export default command
