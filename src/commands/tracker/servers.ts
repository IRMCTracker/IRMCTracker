import { SlashCommandBuilder, EmbedBuilder, AttachmentBuilder, APIEmbedField, RestOrArray, MessagePayload } from 'discord.js';
import { Server, getServers } from '../../services/serversService';
import { bannerUrl, trackerUrl } from "../../config.json";

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
		await interaction.reply("🤔 چند لحظه صبر کن...");

		const servers: Server[] | null = await getServers();

		if (servers === null) {
			return await interaction.editReply('🔴 مشکلی در دریافت سرور ها بوجود آمده.');
		}


		const embedFields: RestOrArray<APIEmbedField> = [];

		servers.forEach((server: Server, index: number) => {
			if (server.up_from > 0) {
				embedFields.push({ name: `${getMedal(index)} ${server.name}`, value: `👥 ${server.players.online}`, inline: true });
			} else {
				embedFields.push({ name: `🔴 ${server.name}`, value: `👥 -`, inline: true });
			}
		});

		const chunkSize = 24;
		const embeds = [];
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
		embeds[0]
			.setTitle('📡 Servers List | لیست سرور ها')
			.setThumbnail('attachment://logo.png')

		// Setting banner/footer on last embed
		embeds[embeds.length - 1].setImage('attachment://banner.png');

		// Loop through each embed and send them
		let firstEmbed: boolean = true;
		for (const embed of embeds) {
			const files = [];

			if (embed.toJSON().thumbnail) files.push({ name: "logo.png", attachment: `${trackerUrl}/img/logo.png` });
			if (embed.toJSON().image) files.push({ name: "banner.png", attachment: bannerUrl })

			if (firstEmbed) {
				await interaction.editReply({
					content: "",
					embeds: [embed],
					files: files
				});
				firstEmbed = false;
			} else {
				await interaction.followUp({
					embeds: [embed],
					files: files
				});
			}
			
		}
	},
};

export default command
