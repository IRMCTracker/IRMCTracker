const { SlashCommandBuilder, EmbedBuilder } = require("discord.js");
const Server = require('../../models/Server');

module.exports = {
	data: new SlashCommandBuilder()
		.setName('vote')
		.setDescription('💻 رای دادن به سرور مورد علاقه')
		.addStringOption(option => option.setName('server').setDescription('اسم سرور').setRequired(true)),
	async execute(interaction) {
		const serverName = interaction.options.getString('server');

		const server = await Server.findLike(serverName);

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
			.setURL(`https://mctracker.ir/server/${server.id}/vote`)
			.setColor(0x673AB7)
			.setTimestamp(Date.now())
			.setFooter({text: 'Tracked by IRMCTracker'})

		const fav = server.favicon_path;
		let files = [];
		if (fav != null) {
			const favParts = fav.split('/');
			embed.setThumbnail('attachment://' + favParts[favParts.length - 1]);
			files.push(fav);
		}

		await interaction.reply({ embeds: [embed], files });
	},
};
