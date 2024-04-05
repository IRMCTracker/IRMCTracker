import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { getMinecraftProfile, userNameToUUID } from '../../services/playerService';
import { bannerUrl } from '../../config.json';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('profile')
		.setDescription('🔥 دریافت اطلاعات حساب ماینکرفت شما')
		.addStringOption(option => option.setName('username').setDescription('یوزرنیم پلیر').setRequired(true)),
	async execute(_, interaction) {
		const userName: string = interaction.options.getString('username', true);
		
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
			.setThumbnail('attachment://profile.png')
			.setImage('attachment://banner.png')
			.setFooter({text: 'Tracked by IRMCTracker'})
			.addFields([
				{name: '💻 • UserNames', value: profile.history.join(' - '), inline: true},
				{name: '📆 • Created', value: profile.createdAt ?? 'مخفی', inline: true}
			]);

		await interaction.editReply({
			embeds: [embed],
			content: '',
			files: [
				{
					name: 'profile.png',
					attachment: `https://crafatar.com/renders/head/${uuid}?size=512&default=MHF_Steve&overlay`
				},
				{
					name: 'banner.png',
					attachment: bannerUrl
				}
			]
		});
	},

};

export default command
