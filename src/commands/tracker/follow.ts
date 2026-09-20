import { EmbedBuilder, GuildMember, InteractionContextType, SlashCommandBuilder } from 'discord.js';
import { syncFollow } from '../../services/trackerService';
import { ensureFollowRole, findFollowRole, findServerByName, respondWithServerNames } from '../../services/followService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('follow')
		.setDescription('🔔 دنبال کردن یه سرور - هر وقت آنلاین/آفلاین شد یا رکورد زد و خبر جدیدی اتفاق افتاد خبرتون میکنم')
		.addStringOption(option => option.setName('server').setDescription('اسم سرور').setRequired(true).setAutocomplete(true))
		.setContexts(InteractionContextType.Guild) as SlashCommandBuilder,

	autocomplete: respondWithServerNames,

	async execute(client, interaction) {
		if (!interaction.guild) return;

		await interaction.deferReply({ ephemeral: true });

		const server = await findServerByName(interaction.options.getString('server', true));

		if (!server) {
			return await interaction.editReply({ embeds: [errorEmbed('سرور وارد شده توی MCTracker پیدا نشد!')] });
		}

		const member = interaction.member as GuildMember;
		const existing = findFollowRole(interaction.guild, server.name);

		if (existing && member.roles.cache.has(existing.id)) {
			return await interaction.editReply({
				embeds: [
					new EmbedBuilder()
						.setColor('Blue')
						.setTitle('ℹ️ از قبل دنبالش میکنید')
						.setDescription(`**${server.name}** رو از قبل دنبال میکنید.\nبرای لغو از \`/unfollow\` استفاده کنید.`)
				]
			});
		}

		try {
			await member.roles.add(await ensureFollowRole(interaction.guild, server.name));
		} catch (error) {
			console.error(`Follow failed for ${server.name}:`, error);

			return await interaction.editReply({
				embeds: [errorEmbed('انگار یه مشکلی وجود داره. لطفا با مدیر های سرور در ارتباط باشید 🥲')]
			});
		}

		const followers = await syncFollow(server.name, member.id, true);

		return await interaction.editReply({
			embeds: [
				new EmbedBuilder()
					.setColor('Green')
					.setTitle('🔔 دنبال شد')
					.setDescription(
						`از این به بعد هر وقت **${server.name}** آنلاین/آفلاین بشه، رکورد بزنه یا پینگش بره بالا و هر خبر جدید دیگه‌ای اتفاق بیوفته تگ میشید.\n` +
						(followers ? `در حال حاضر **${followers}** نفر این سرور رو دنبال میکنن.\n` : '') +
						`برای لغو: \`/unfollow ${server.name}\``
					)
			]
		});
	},
};

function errorEmbed(description: string): EmbedBuilder {
	return new EmbedBuilder().setColor('Red').setTitle('❌ خطا').setDescription(description);
}

export default command;
