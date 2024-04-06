import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { getServer } from '../../services/trackerService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('vote')
		.setDescription('💻 رای دادن به سرور مورد علاقه')
		.addStringOption(option => option.setName('server').setDescription('اسم سرور').setRequired(true)),
	async execute(_, interaction) {
		const serverName: string = interaction.options.getString('server', true);

		await interaction.reply("🤔 چند لحظه صبر کن...");

		const server = await getServer(serverName);

		if (server == null) {
			return await interaction.reply({embeds: [
				new EmbedBuilder()
					.setColor("Red")
					.setTitle('🔴 سرور وارد شده وجود نداره!')
			]});
		}

		let embed = new EmbedBuilder()
			.setTitle(`💻 رای دادن به سرور ${server.name}`)
			.setDescription('با هرروز رای دادن به سرور مورد علاقتون میتونید داخل سرور ها جایزه دریافت کنید!')
			.setURL(`https://mctracker.ir/server/${server.name}/vote`)
			.setColor(0x673AB7)
			.setTimestamp(Date.now())
			.setFooter({text: 'Tracked by IRMCTracker'})

		await interaction.editReply({ embeds: [embed] });
	},

};

export default command
