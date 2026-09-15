import { ChannelType, EmbedBuilder, PermissionFlagsBits, SlashCommandBuilder, TextChannel } from 'discord.js';
import { getServers } from '../../services/trackerService';
import { getLiveEmbed, syncNickname } from '../../services/messagingService';
import { saveConfig } from '../../services/guildConfigService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('setup')
		.setDescription('💎 نصب ترکر زنده سرور توی این دیسکورد')
		.addStringOption(option => option.setName('server').setDescription('اسم سرور').setRequired(true).setAutocomplete(true))
		.addChannelOption(option => option.setName('channel').setDescription('چنل نمایش ترکر').addChannelTypes(ChannelType.GuildText))
		.addBooleanOption(option => option.setName('nickname').setDescription('نمایش تعداد پلیر روی اسم ربات'))
		.setDefaultMemberPermissions(PermissionFlagsBits.ManageGuild)
		.setDMPermission(false) as SlashCommandBuilder,

	async autocomplete(interaction) {
		const typed = interaction.options.getFocused().toLowerCase();
		const servers = await getServers() ?? [];

		const matches = servers
			.filter(server => server.name.toLowerCase().includes(typed))
			.slice(0, 25)
			.map(server => ({ name: server.name, value: server.name }));

		await interaction.respond(matches);
	},

	async execute(client, interaction) {
		if (!interaction.guild) return;

		await interaction.deferReply({ ephemeral: true });

		const name = interaction.options.getString('server', true);
		const servers = await getServers();

		const server = servers?.find(candidate => candidate.name.toLowerCase() === name.toLowerCase());

		if (!server) {
			return await interaction.editReply({ embeds: [errorEmbed('سرور وارد شده توی MCTracker پیدا نشد!')] });
		}

		const channel = (interaction.options.getChannel('channel') ?? interaction.channel) as TextChannel;

		const permissions = channel.permissionsFor(client.user!);

		if (!permissions?.has(PermissionFlagsBits.SendMessages) || !permissions.has(PermissionFlagsBits.EmbedLinks)) {
			return await interaction.editReply({ embeds: [errorEmbed(`توی ${channel} دسترسی ارسال پیام یا Embed ندارم!`)] });
		}

		const nicknameEnabled = interaction.options.getBoolean('nickname') ?? false;

		const message = await channel.send(getLiveEmbed(client, server));

		await saveConfig(interaction.guild.id, {
			server: server.name,
			channel_id: channel.id,
			message_id: message.id,
			nickname_enabled: nicknameEnabled,
		});

		if (nicknameEnabled) await syncNickname(client, interaction.guild.id, server);

		await interaction.editReply({
			embeds: [
				new EmbedBuilder()
					.setColor('Green')
					.setTitle('✅ انجام شد')
					.setDescription(`ترکر زنده **${server.name}** توی ${channel} نصب شد و هر دقیقه بروز میشه.`)
			]
		});
	},
};

function errorEmbed(description: string): EmbedBuilder {
	return new EmbedBuilder().setColor('Red').setTitle('❌ خطا').setDescription(description);
}

export default command;
