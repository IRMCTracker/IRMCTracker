import { SlashCommandBuilder, EmbedBuilder, ChatInputCommandInteraction, hyperlink } from 'discord.js';
import { getMinecraftProfile, userNameToUUID, skinRenderUrl } from '../../services/playerService';
import { bannerUrl } from '../../config.json';
import { checkChannelPermission } from '../../services/messagingService';
import { getHypixelProfile } from '../../services/hypixelService';

const command: TrackerCommand = {
    data: new SlashCommandBuilder()
        .setName('profile')
        .setDescription('🔥 دریافت اطلاعات حساب ماینکرفت شما')
        .addStringOption(option => option.setName('username').setDescription('یوزرنیم پلیر').setRequired(true)),

    async execute(_, interaction: ChatInputCommandInteraction) {
        if (!await checkChannelPermission(interaction, 'profile')) return;

        const userName: string = interaction.options.getString('username', true);
        await interaction.reply({
            content: `در حال جستجوی پروفایل ${userName}...`,
            embeds: [new EmbedBuilder()
                .setDescription('🔄 لطفا صبر کنید...')
                .setColor('#FFA500')]
        });

        const uuid = await userNameToUUID(userName);

        if (!uuid) {
            return await interaction.editReply({
                content: '',
                embeds: [new EmbedBuilder()
                    .setDescription('❌ پلیر مورد نظر پیدا نشد!')
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
                    .setDescription('⚠️ خطا در دریافت اطلاعات پروفایل')
                    .setColor('#FF0000')]
            });
        }

        const namemcLink = hyperlink('NameMC', minecraftProfile.profileUrl || '');
        const skinViewerLink = hyperlink('Skin Viewer', `https://namemc.com/skin/${uuid}`);
        
        const historyFormatted = minecraftProfile.history
            .map((entry, index) => {
                const date = entry.changedAt ? 
                    `(${new Date(entry.changedAt).toLocaleDateString()})` : 
                    '';
                return `${index + 1}. ${entry.username} ${date}`;
            })
            .join('\n');

        const accountBadges = [
            minecraftProfile.isLegacy ? '👑 Legacy Account' : '',
            minecraftProfile.isDemoAccount ? '🎮 Demo Account' : '',
            minecraftProfile.textures.cape ? '🦸 Has Cape' : '',
            minecraftProfile.textures.skin ? '🎨 Custom Skin' : '⚪ Default Skin',
            minecraftProfile.textures.skin?.slim ? '💃 Slim Model' : '🧍 Classic Model'
        ].filter(badge => badge).join(' | ');

		const embed = new EmbedBuilder()
			.setTitle(`🎮 پروفایل ${minecraftProfile.username}`)
			.setColor("#00FF00")
			.setDescription(accountBadges)
			.setTimestamp(Date.now())
			.setThumbnail('attachment://profile.png')
			.setImage('attachment://banner.png')
			.setFooter({ text: 'Tracked by IRMCTracker', iconURL: 'attachment://profile.png' })
			.addFields([
			{ 
				name: '📋 اطلاعات اصلی', 
				value: [
				`🔹 نام: \`${minecraftProfile.username}\``,
				`🔹 UUID: \`${minecraftProfile.uuid}\``,
				`🔹 تاریخ ساخت: ${minecraftProfile.createdAt ? `<t:${Math.floor(new Date(minecraftProfile.createdAt).getTime() / 1000)}:R>` : 'مخفی'}`,
				`🔹 لینک‌ها: ${namemcLink} | ${skinViewerLink}`
				].join('\n'),
				inline: false 
			},
			{ 
				name: '📝 تاریخچه نام‌ ها', 
				value: `\`\`\`${historyFormatted}\`\`\``, 
				inline: false 
			}
			]);

        // Add Hypixel stats if available
        if (hypixelProfile) {
            const formatRatio = (a: number, b: number) => (b === 0 ? a : (a / b).toFixed(2));
            
            embed.addFields([
                {
                    name: '🌟 Hypixel Stats',
                    value: [
                        `${hypixelProfile.online ? '🟢 Online' : '🔴 Offline'}`,
                        `👑 Rank: ${hypixelProfile.rank}`,
                        `📊 Network Level: ${hypixelProfile.level.toFixed(2)}`,
                        `✨ Karma: ${hypixelProfile.karma.toLocaleString()}`,
                        `🏆 Achievement Points: ${hypixelProfile.achievementPoints.toLocaleString()}`,
                        `📅 First Login: ${hypixelProfile.firstLogin.getTime() > 0 ? `<t:${Math.floor(hypixelProfile.firstLogin.getTime() / 1000)}:R>` : '-'}`,
                        `📅 Last Login: ${hypixelProfile.lastLogin.getTime() > 0 ? `<t:${Math.floor(hypixelProfile.lastLogin.getTime() / 1000)}:R>` : '-'}`
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
                    attachment: skinRenderUrl(uuid, 'head')
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
