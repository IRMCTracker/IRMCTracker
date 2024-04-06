import { SlashCommandBuilder, EmbedBuilder, AttachmentBuilder, APIEmbedField, RestOrArray, MessagePayload } from 'discord.js';
import { Server, getServers } from '../../services/trackerService';
import { bannerUrl, logoUrl } from "../../config.json";
import { getMedal } from '../../services/messagingService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('servers')
		.setDescription('💻 دریافت لیستی از تمام سرور های موجود'),
	async execute(_, interaction) {
		await interaction.reply("🤔 چند لحظه صبر کن...");

		const servers: Server[] | null = await getServers();

		if (servers === null) {
			return await interaction.editReply('🔴 مشکلی در دریافت سرور ها بوجود آمده.');
		}

		const sortedServers = servers.slice().sort((a, b) => {
			// Sort by players.online (descending)
			if (b.players.online !== a.players.online) {
				return b.players.online - a.players.online;
			}
			// If players.online is the same, sort by up_from (positive values first)
			if (a.up_from >= 0 && b.up_from < 0) {
				return -1; // a comes before b
			}
			if (a.up_from < 0 && b.up_from >= 0) {
				return 1; // b comes before a
			}
			// If up_from values are both positive or both negative, sort by their absolute values
			return Math.abs(b.up_from) - Math.abs(a.up_from);
		});
		

		const embedFields: RestOrArray<APIEmbedField> = [];

		sortedServers.forEach((server: Server, index: number) => {
			if (server.up_from > 0) {
				embedFields.push({ name: `${getMedal(index)} ${server.name}`, value: `👥 ${server.players.online}`, inline: true });
			} else {
				embedFields.push({ name: `🔴 ${server.name}`, value: `👥 -`, inline: true });
			}
		});

		const chunkSize = 24;
		const embeds: EmbedBuilder[] = [];
		for (let i = 0; i < embedFields.length; i += chunkSize) {
			const chunk = embedFields.slice(i, i + chunkSize);
			const embed = new EmbedBuilder()
				.setColor(0x673AB7)
				.setTimestamp(Date.now())
				.setFooter({ text: 'Tracked by IRMCTracker' });

			embed.addFields(chunk);
			embeds.push(embed);
		}

		// Setting title on first embed
		embeds[0].setTitle('📡 Servers List | لیست سرور ها')

		embeds.forEach((embed: EmbedBuilder, index: number) => {
			if (index != embeds.length - 1) {
				embeds[index].setThumbnail('attachment://logo.png')
			}
		})
		
			

		// Setting banner/footer on last embed
		embeds[embeds.length - 1].setImage('attachment://banner.png');

		await interaction.editReply({
			content: "",
			embeds: embeds,
			files: [{ name: "logo.png", attachment: logoUrl }, { name: "banner.png", attachment: bannerUrl }]
		});
	},
};

export default command
