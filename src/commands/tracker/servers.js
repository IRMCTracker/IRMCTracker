const { SlashCommandBuilder, EmbedBuilder } = require("discord.js");
const Server = require('../../models/Server');

function getMedal(index) {
	if (index === 0) {
		return '🥇';
	} else if (index === 1) {
		return '🥈';
	} else if (index === 2) {
		return '🥉';
	}

	return '🏅';
}

module.exports = {
	data: new SlashCommandBuilder()
		.setName('servers')
		.setDescription('💻 دریافت لیستی از تمام سرور های موجود'),
	async execute(interaction) {
		const embed = new EmbedBuilder()
			.setTitle('📡 Servers List | لیست سرور ها')
			.setColor(0x673AB7)
			.setTimestamp(Date.now())
			.setImage('attachment://banner.png')
			.setFooter({text: 'Tracked by IRMCTracker'})

		const servers = await Server.all();

		servers.forEach((server, index) => {
			if (server.up_from > 0) {
				embed.addFields([{ name: `${getMedal(index)} ${server.name}`, value: `👥 ${server.current_players}`, inline: true }]);
			} else {
				embed.addFields([{ name: `🔴 ${server.name}`, value: `👥 -`, inline: true }]);
			}
		})

		await interaction.reply({ embeds: [embed], files: ['./storage/static/banner.png'] });
	},
};
