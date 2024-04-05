import { SlashCommandBuilder, EmbedBuilder, AttachmentBuilder } from 'discord.js';
import { Server, getServers } from '../../services/serversService';
import { bannerUrl } from "../../config.json";

function getMedal(index: number): string {
    switch (index) {
        case 0:
            return '🥇';
        case 1:
            return '🥈';
        case 2:
            return '🥉';
        default:
            return '🏅';
    }
}

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('servers')
		.setDescription('💻 دریافت لیستی از تمام سرور های موجود'),
	async execute(_, interaction) {
		const embed = new EmbedBuilder()
			.setTitle('📡 Servers List | لیست سرور ها')
			.setColor(0x673AB7)
			.setTimestamp(Date.now())
			.setImage('attachment://banner.png')
			.setFooter({text: 'Tracked by IRMCTracker'})

		await interaction.reply("🤔 چند لحظه صبر کن...");

		const servers: Server[] = await getServers();

		servers.forEach((server: Server, index: number) => {
			if (server.up_from > 0) {
				embed.addFields([{ name: `${getMedal(index)} ${server.name}`, value: `👥 ${server.current_players}`, inline: true }]);
			} else {
				embed.addFields([{ name: `🔴 ${server.name}`, value: `👥 -`, inline: true }]);
			}
		})

		await interaction.editReply({ 
			embeds: [embed], 
			files: [{name: "banner.png",attachment: bannerUrl}]
		});
	},
};

export default command
