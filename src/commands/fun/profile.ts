import { SlashCommandBuilder, EmbedBuilder, ChatInputCommandInteraction, hyperlink } from 'discord.js';
import { getMinecraftProfile, userNameToUUID } from '../../services/playerService';
import { bannerUrl } from '../../config.json';
import { checkChannelPermission } from '../../services/messagingService';
import { getHypixelProfile } from '../../services/hypixelService';

function formatRatio(a, b) {
    return b === 0 ? `${a}` : (a / b).toFixed(2);
}

function formatDate(timestamp) {
    return timestamp ? `<t:${Math.floor(timestamp.getTime() / 1000)}:R>` : 'Unknown';
}

function generateAccountBadges(profile) {
    return [
        profile.isLegacy ? '👑 Legacy Account' : '',
        profile.isDemoAccount ? '🎮 Demo Account' : '',
        profile.textures.cape ? '🦸 Has Cape' : '',
        profile.textures.skin ? '🎨 Custom Skin' : '⚪ Default Skin',
        profile.textures.skin?.slim ? '💃 Slim Model' : '🧍 Classic Model'
    ].filter(Boolean).join(' | ');
}

const command = {
    data: new SlashCommandBuilder()
        .setName('profile')
        .setDescription('🔥 Recive your Minecraft Account Information')
        .addStringOption(option => option.setName('username').setDescription(`Player's username`).setRequired(true)),

    async execute(_, interaction) {
        if (!await checkChannelPermission(interaction, 'profile')) return;

        const userName = interaction.options.getString('username', true);
        await interaction.reply({
            content: `Searching for ${userName}'s profile...`,
            embeds: [new EmbedBuilder()
                .setDescription('🔄 a moment...')
                .setColor('#FFA500')]
        });

        const uuid = await userNameToUUID(userName);

        if (!uuid) {
            return await interaction.editReply({
                content: '',
                embeds: [new EmbedBuilder()
                    .setDescription('❌ I cannot find the given player.')
                    .setColor('#FF0000')]
            });
        }

        // Fetch both profiles in parallel
        const [minecraftProfile, hypixelProfile] = await Promise.all([
            getMinecraftProfile(uuid),
            getHypixelProfile(uuid)
        ]);

        if (!minecraftProfile) {
            return await interaction.editReply({
                content: '',
                embeds: [new EmbedBuilder()
                    .setDescription('⚠️ Fatal Error occurred when I was trying to recive the information.')
                    .setColor('#FF0000')]
            });
        }

        const namemcLink = hyperlink('NameMC', minecraftProfile.profileUrl || '');
        const skinViewerLink = hyperlink('Skin Viewer', `https://namemc.com/skin/${uuid}`);

        const historyFormatted = minecraftProfile.history
            .map((entry, index) => {
                const date = entry.changedAt ? `(${new Date(entry.changedAt).toLocaleDateString()})` : '';
                return `${index + 1}. ${entry.username} ${date}`;
            })
            .join('\n');

        const accountBadges = generateAccountBadges(minecraftProfile);

        const embed = new EmbedBuilder()
            .setTitle(`🎮 ${minecraftProfile.username}'s Profile`)
            .setColor("#00FF00")
            .setDescription(accountBadges)
            .setTimestamp(Date.now())
            .setThumbnail('attachment://profile.png')
            .setImage('attachment://banner.png')
            .setFooter({ text: 'Tracked by IRMCTracker', iconURL: 'attachment://profile.png' })
            .addFields([
                {
                    name: '📋 Main Information',
                    value: [
                        `🔹 Username: \`${minecraftProfile.username}\``,
                        `🔹 UUID: \`${minecraftProfile.uuid}\``,
                        `🔹 Date of creation: ${formatDate(new Date(minecraftProfile.createdAt))}`,
                        `🔹 Links: ${namemcLink} | ${skinViewerLink}`
                    ].join('\n'),
                    inline: false
                },
                {
                    name: '📝 Name history',
                    value: `\`\`\`${historyFormatted}\`\`\``,
                    inline: false
                }
            ]);

        if (hypixelProfile) {
            embed.addFields([
                {
                    name: '🌟 Hypixel Stats',
                    value: [
                        `${hypixelProfile.online ? '🟢 Online' : '🔴 Offline'}`,
                        `👑 Rank: ${hypixelProfile.rank}`,
                        `📊 Network Level: ${hypixelProfile.level.toFixed(2)}`,
                        `✨ Karma: ${hypixelProfile.karma.toLocaleString()}`,
                        `🏆 Achievement Points: ${hypixelProfile.achievementPoints.toLocaleString()}`,
                        `📅 First Login: ${formatDate(hypixelProfile.firstLogin)}`,
                        `📅 Last Login: ${formatDate(hypixelProfile.lastLogin)}`
                    ].join('\n'),
                    inline: false
                }
            ]);

            if (hypixelProfile.stats.bedwars) {
                const bw = hypixelProfile.stats.bedwars;
                embed.addFields({
                    name: '🛏️ Bedwars Stats',
                    value: [
                        `⭐ Level: ${bw.level}`,
                        `🏆 Wins: ${bw.wins.toLocaleString()} (W/L: ${formatRatio(bw.wins, bw.losses)})`,
                        `💀 Finals: ${bw.finalKills.toLocaleString()} (K/D: ${formatRatio(bw.finalKills, bw.deaths)})`,
                        `🔥 Current Winstreak: ${bw.winstreak}`
                    ].join('\n'),
                    inline: true
                });
            }

            if (hypixelProfile.stats.skywars) {
                const sw = hypixelProfile.stats.skywars;
                embed.addFields({
                    name: '🌟 Skywars Stats',
                    value: [
                        `⭐ Level: ${sw.level}`,
                        `🏆 Wins: ${sw.wins.toLocaleString()} (W/L: ${formatRatio(sw.wins, sw.losses)})`,
                        `⚔️ Kills: ${sw.kills.toLocaleString()} (K/D: ${formatRatio(sw.kills, sw.deaths)})`
                    ].join('\n'),
                    inline: true
                });
            }
        }

        await interaction.editReply({
            embeds: [embed],
            content: '',
            files: [
                {
                    name: 'profile.png',
                    attachment: `https://crafatar.com/renders/head/${uuid}?size=512&default=MHF_Steve&overlay`
                },
                {
                    name: 'banner.png',
                    attachment: bannerUrl
                }
            ]
        });
    },
};

export default command;
