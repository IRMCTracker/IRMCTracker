import { SlashCommandBuilder, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } from 'discord.js';
import { getServer } from '../../services/trackerService';
import { formatNumber, checkChannelPermission } from '../../services/messagingService';
import { bannerUrl } from '../../config.json';

interface ServerComparison {
    name: string;
    players: { online: number; record: number; };
    votes: number;
    latency: number|null;
}

const getComparisonStatus = (val1: number, val2: number): string => {
    if (val1 === val2) return "⚡";
    return val1 > val2 ? " (🏆)" : "";
};

const createServerField = (server: ServerComparison, otherServer: ServerComparison, color: '🔵' | '🔴') => ({
    name: `${color} ${server.name}`,
    value: [
        '\u200b',
        `👥 Players: **${server.players.online}** ${getComparisonStatus(server.players.online, otherServer.players.online)}`,
        `📊 Record: **${server.players.record}** ${getComparisonStatus(server.players.record, otherServer.players.record)}`,
        `🗳️ Votes: **${formatNumber(server.votes)}** ${getComparisonStatus(server.votes, otherServer.votes)}`,
        `📡 Ping: **${server.latency ?? 0}ms**`
    ].join('\n'),
    inline: true
});

const createComparisonEmbed = (server1: ServerComparison, server2: ServerComparison, clientAvatarUrl?: string) => {
    return new EmbedBuilder()
        .setTitle(`🏆 Comparing **${server1.name}** to **${server2.name}**`)
        .setColor('#90EE90')
        .setImage(bannerUrl)
        .addFields([
            createServerField(server1, server2, '🔵'),
            {
                name: '\u200b',
                value: ['\u200b', '┃', '⚔️', '┃', '\u200b'].join('\n'),
                inline: true
            },
            createServerField(server2, server1, '🔴')
        ])
        .setFooter({ 
            text: '📊 IRMCTracker Comparison System',
            iconURL: clientAvatarUrl
        })
        .setTimestamp();
};

const createServerButtons = (server1: ServerComparison, server2: ServerComparison) => {
    return new ActionRowBuilder<ButtonBuilder>()
        .addComponents(
            new ButtonBuilder()
                .setLabel(`View ${server1.name}`)
                .setStyle(ButtonStyle.Link)
                .setEmoji('🌐')
                .setURL(`https://mctracker.ir/servers/${server1.name}`),
            new ButtonBuilder()
                .setLabel(`View ${server2.name}`)
                .setStyle(ButtonStyle.Link)
                .setEmoji('🌐')
                .setURL(`https://mctracker.ir/servers/${server2.name}`)
        );
};

const command: TrackerCommand = {
    data: new SlashCommandBuilder()
        .setName('compare')
        .setDescription('🆚 مقایسه دو سرور با یکدیگر')
        .addStringOption(option => 
            option.setName('server1')
            .setDescription('نام سرور اول')
            .setRequired(true))
        .addStringOption(option => 
            option.setName('server2')
            .setDescription('نام سرور دوم')  
            .setRequired(true)),

    async execute(_, interaction) {
        if (!await checkChannelPermission(interaction, 'track')) return;

        const server1Name = interaction.options.getString('server1', true);
        const server2Name = interaction.options.getString('server2', true);

        await interaction.reply("🔄 در حال مقایسه سرور ها...");

        const [server1, server2] = await Promise.all([
            getServer(server1Name),
            getServer(server2Name)
        ]);

        if (!server1 || !server2) {
            return await interaction.editReply({
                content: '',
                embeds: [
                    new EmbedBuilder()
                        .setColor("Red")
                        .setTitle('❌ یکی از سرور های وارد شده وجود نداره!')
                ]
            });
        }

        const embed = createComparisonEmbed(server1, server2, interaction.client.user?.avatarURL() || undefined);
        const buttons = createServerButtons(server1, server2);

        await interaction.editReply({
            content: '',
            embeds: [embed],
            components: [buttons]
        });
    }
};

export default command;