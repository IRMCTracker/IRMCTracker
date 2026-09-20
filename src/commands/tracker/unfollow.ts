import { EmbedBuilder, GuildMember, InteractionContextType, SlashCommandBuilder } from 'discord.js';
import { syncFollow } from '../../services/trackerService';
import { getFollowEmbed } from '../../services/messagingService';
import { findFollowRole, findServerByName, respondWithServerNames } from '../../services/followService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('unfollow')
		.setDescription('🔕 لغو دنبال کردن یک سرور')
		.addStringOption(option => option.setName('server').setDescription('اسم سرور').setRequired(true).setAutocomplete(true))
		.setContexts(InteractionContextType.Guild) as SlashCommandBuilder,

	autocomplete: respondWithServerNames,

	async execute(client, interaction) {
		if (!interaction.guild) return;

		await interaction.deferReply();

		const server = await findServerByName(interaction.options.getString('server', true));

		if (!server) {
			return await interaction.editReply({ embeds: [errorEmbed('سرور وارد شده توی MCTracker پیدا نشد!')] });
		}

		const member = interaction.member as GuildMember;
		const role = findFollowRole(interaction.guild, server.name);

		if (!role || !member.roles.cache.has(role.id)) {
			return await interaction.editReply({
				embeds: [getFollowEmbed(
					server,
					'ℹ️ در حال حاضر دنبال نمی‌کنید',
					`**${server.name}** رو دنبال نمی‌کنید.\nبرای دنبال کردن: \`/follow ${server.name}\``,
				)]
			});
		}

		try {
			await member.roles.remove(role);
		} catch (error) {
			console.error(`Unfollow failed for ${server.name}:`, error);

			return await interaction.editReply({
				embeds: [errorEmbed('انگار یه مشکلی وجود داره. لطفا با مدیر های سرور در ارتباط باشید 🥲')]
			});
		}

		await syncFollow(server.name, member.id, false);

		return await interaction.editReply({
			embeds: [getFollowEmbed(
				server,
				'🔕 لغو شد',
				`دیگه خبر های **${server.name}** براتون ارسال نمیشه.`,
			)]
		});
	},
};

function errorEmbed(description: string): EmbedBuilder {
	return new EmbedBuilder().setColor('Red').setTitle('❌ خطا').setDescription(description);
}

export default command;
