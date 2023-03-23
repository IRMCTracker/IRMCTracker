const { SlashCommandBuilder, EmbedBuilder } = require("discord.js");

const { userNameToUUID } = require('../../utils');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('skin')
		.setDescription('🤌🏻 دریافت تصویری از اسکین شما')
		.addStringOption(option => option.setName('name').setDescription('نام اسکین شما').setRequired(true)),
	async execute(interaction) {
		const userName = interaction.options.getString('name');
		
		await interaction.reply('دارم اسکینتو پیدا میکنم... 🤔');
		
		const uuid = await userNameToUUID(userName);

		if (uuid == null) {
			return await interaction.editReply('☹️ فکر کنم اشتباه نوشتی اسم اسکین رو چون نمیتونم پیداش کنم');
		}

		const embed = new EmbedBuilder()
			.setTitle(`💎 Skin ${userName}`)
			.setImage(`https://crafatar.com/renders/body/${uuid}?size=512&default=MHF_Steve&overlay`);
		
		await interaction.editReply({embeds: [embed], content: 'پیداش کردم 😍\n'});
	},
};
