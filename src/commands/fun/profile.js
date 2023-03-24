const { SlashCommandBuilder, EmbedBuilder } = require("discord.js");

const { userNameToUUID, getMinecraftProfile } = require('../../utils');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('profile')
		.setDescription('🔥 دریافت اطلاعات حساب ماینکرفت شما')
		.addStringOption(option => option.setName('username').setDescription('یوزرنیم پلیر').setRequired(true)),
	async execute(interaction) {
		const userName = interaction.options.getString('username');
		
		await interaction.reply(`دارم حساب ${userName} پیدا میکنم... 🤔`);
		
		const uuid = await userNameToUUID(userName);

		if (uuid == null) {
			return await interaction.editReply('☹️ فکر کنم اشتباه نوشتی اسم پلیر رو چون نمیتونم پیداش کنم');
		}

		const profile = await getMinecraftProfile(uuid);

		if (profile == null) {
			return await interaction.editReply('☹️ مشکلی تو دریافت اطلاعات پیش اومد. لطفا بعدا دوباره تلاش کن');
		}

		const embed = new EmbedBuilder()
			.setTitle(`⌠・Player Profile ${userName}・⌡`)
			.setColor("Random")
			.setTimestamp(Date.now())
			.setThumbnail(`https://crafatar.com/renders/head/${uuid}?size=512&default=MHF_Steve&overlay`)
			.setImage('attachment://banner.png')
			.setFooter({text: 'Tracked by IRMCTracker'})
			.addFields([
				{name: '💻 • UserNames', value: profile.history.join(' - '), inline: true},
				{name: '📆 • Created', value: profile.createdAt ?? 'مخفی', inline: true}
			]);

		await interaction.editReply({embeds: [embed], content: '', files: ['./storage/static/banner.png']});
	},
};
