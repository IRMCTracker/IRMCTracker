import { ActionRowBuilder, AttachmentPayload, BaseMessageOptions, ButtonBuilder, ButtonStyle, ChatInputCommandInteraction, Client, EmbedBuilder, Emoji, hyperlink, InteractionEditReplyOptions, MessageCreateOptions, MessagePayload, TextChannel } from 'discord.js';
import { Server } from './trackerService';
import { trackerUrl, bannerUrl, logoUrl, botInviteUrl, trackerGuildId, channels } from '../config.json';
import { MinecraftProfile, skinRenderUrl } from './playerService';
import { HypixelProfile } from './hypixelService';

export function getSkinMessage(userName: string, uuid: string): InteractionEditReplyOptions {
    return {
        content: 'پیداش کردم 😍',
        embeds: [new EmbedBuilder().setTitle(`💎 Skin ${userName}`).setImage('attachment://skin.png')],
        files: [{ name: 'skin.png', attachment: skinRenderUrl(uuid) }],
    };
}

export function getProfileMessage(uuid: string, minecraftProfile: MinecraftProfile, hypixelProfile?: HypixelProfile): InteractionEditReplyOptions {
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

    return {
        content: '',
        embeds: [embed],
        files: [
            { name: 'profile.png', attachment: skinRenderUrl(uuid, 'head') },
            { name: 'banner.png', attachment: bannerUrl },
        ],
    };
}

export function getServerMessage(client: Client, server: Server): MessagePayload | InteractionEditReplyOptions {
    let embed: EmbedBuilder;
    const files: AttachmentPayload[] = [];

    const guild = client.guilds.cache.get(trackerGuildId);

    if (guild == null) {
        throw Error('Tracker guild is not properly set.');
    }

    if (server.up_from < 0) {
        embed = new EmbedBuilder()
            .setColor('Red')
            .setTitle(`🔴 ${server.name}`)
            .setDescription('سرور وارد شده درحال حاضر آفلاین هست!');
    } else {
        embed = new EmbedBuilder()
            .setColor('Random')
            .setTitle(`💎 ${server.name}`)
            .setURL(`${trackerUrl}/servers/${server.name}/vote`)
            .setDescription(server.description)
            .setImage('attachment://motd.png')
            .addFields(
            { name: '「🌐」Address »', value: server.ip ? `${server.address} (**${server.ip}**)` : server.address, inline: false },
            { name: '「🧱」Edition »', value: server.type === 'bedrock' ? 'Bedrock' : 'Java', inline: false },
            { name: '「👥」Online Players »', value: `${server.players.online}`, inline: true },
            { name: '「🥇」Top Record »', value: server.players.record.toString(), inline: true },
            { name: '「📈」Uptime »', value: `${server.uptime}`, inline: false },
            { name: '「📌」Version »', value: `${server.version}`, inline: true },
            { name: '「📡」Latency »', value: `${server.latency}ms`, inline: true },
            { name: '「🌎」Country »', value: `:flag_${server.country_code?.toLowerCase() ?? 'ir'}: ${server.region ?? 'Iran Tehran'}`, inline: false },
            );

        // Add dynamic gamemodes field
        if (server.gamemodes != null && Object.entries(server.gamemodes).length > 0) {
            const gamemodesFieldValue = Object.entries(server.gamemodes)
                .sort((a, b) => b[1] - a[1]) // Sort by players in descending order
                .map(([gamemode, value]) => {
                    const emoji = guild.emojis.cache.find((emoji: Emoji) => emoji.name === gamemode);
                    const gamemodeEmoji = emoji ? emoji.toString() : guild.emojis.cache.find((emoji: Emoji) => emoji.name === 'barrier')?.toString();
                    const gamemodeName = gamemode.charAt(0).toUpperCase() + gamemode.slice(1);
                    return `${gamemodeEmoji} ${gamemodeName}: ${value}`;
                })
                .join('\n');


            embed.addFields({ name: '「🎮」Games Status', value: gamemodesFieldValue, inline: true });
        }

        // Add socials field
        if (server.socials && Object.entries(server.socials).length > 0) {
            const socialsFieldValue = Object.entries(server.socials)
                .map(([platform, link]) => {
                    const platformName = platform.charAt(0).toUpperCase() + platform.slice(1);
                    return `${guild.emojis.cache.find((emoji: Emoji) => emoji.name === platform)} [${platformName}](${link})`;
                })
                .join('\n');

            embed.addFields({ name: '「👥」Socials', value: socialsFieldValue, inline: true });
        }


        files.push({ name: "motd.png", attachment: server.motd ? server.motd : bannerUrl })
    }

    // Setting Favicon in embed
    embed.setThumbnail('attachment://favicon.png')
    files.push({ name: "favicon.png", attachment: server.favicon ? server.favicon : logoUrl })

    const openTrackerButton = new ButtonBuilder()
        .setLabel('Open on MCTracker.iR')
        .setURL('https://mctracker.ir/server/' + server.name)
        .setEmoji("🌐")
        .setStyle(ButtonStyle.Link);

    const voteButton = new ButtonBuilder()
        .setLabel('Vote for ' + server.name)
        .setURL('https://mctracker.ir/server/' + server.name + '/vote')
        .setEmoji("👍🏻")
        .setStyle(ButtonStyle.Link);

    const row = new ActionRowBuilder<ButtonBuilder>()
        .addComponents(openTrackerButton, voteButton);

    // Setting footer
    embed
        .setTimestamp(Date.now())
        .setFooter({ text: 'Tracked by IRMCTracker' });

    return {
        content: '',
        embeds: [embed],
        files: files,
        components: [row]
    };
}

function socialUrl(link: string): string | null {
    if (!link) return null;

    const url = /^https?:\/\//i.test(link) ? link : `https://${link}`;

    try {
        new URL(url);
        return url;
    } catch {
        return null;
    }
}

export function getServerCardMessage(server: Server, card: Buffer): InteractionEditReplyOptions {
    const components = [
        new ActionRowBuilder<ButtonBuilder>().addComponents(
            new ButtonBuilder()
                .setLabel('Open on MCTracker.iR')
                .setURL(`${trackerUrl}/server/${server.name}`)
                .setEmoji('🌐')
                .setStyle(ButtonStyle.Link),
            new ButtonBuilder()
                .setLabel(`Vote for ${server.name}`)
                .setURL(`${trackerUrl}/server/${server.name}/vote`)
                .setEmoji('👍🏻')
                .setStyle(ButtonStyle.Link),
        ),
    ];

    const socials = Object.entries(server.socials ?? {})
        .map(([platform, link]) => ({ platform, url: socialUrl(link) }))
        .filter(social => social.url !== null)
        .slice(0, 5);

    if (socials.length > 0) {
        components.push(
            new ActionRowBuilder<ButtonBuilder>().addComponents(
                socials.map(({ platform, url }) =>
                    new ButtonBuilder()
                        .setLabel(platform.charAt(0).toUpperCase() + platform.slice(1))
                        .setURL(url!)
                        .setStyle(ButtonStyle.Link)
                )
            )
        );
    }

    const embed = new EmbedBuilder()
        .setColor(server.up_from < 0 ? 'Red' : 'Green')
        .setImage('attachment://card.png');

    return {
        content: '',
        embeds: [embed],
        files: [{ name: 'card.png', attachment: card }],
        components,
    };
}

export function getServerUnavailableMessage(serverName?: string): InteractionEditReplyOptions {
    const serverUrl = serverName ? `${trackerUrl}/servers/${serverName}` : trackerUrl;

    const embed = new EmbedBuilder()
        .setColor('Orange')
        .setTitle('⚠️ اختلال در دریافت اطلاعات')
        .setDescription(
            `بدلیل اختلالات موجود نتونستیم اطلاعات سرور شما رو اینجا ارسال کنیم، اما میتونید از سایت اطلاعات رو مشاهده کنید:`
        )
        .setThumbnail('attachment://favicon.png')
        .setTimestamp(Date.now())
        .setFooter({ text: 'Tracked by IRMCTracker' });

    const openTrackerButton = new ButtonBuilder()
        .setLabel('مشاهده در سایت')
        .setURL(serverUrl)
        .setEmoji('🌐')
        .setStyle(ButtonStyle.Link);

    const row = new ActionRowBuilder<ButtonBuilder>()
        .addComponents(openTrackerButton);

    return {
        content: '',
        embeds: [embed],
        files: [{ name: 'favicon.png', attachment: logoUrl }],
        components: [row],
    };
}

export function formatNumber(number: number, decPlaces: number = 0): string {
    // 2 decimal places => 100, 3 => 1000, etc
    decPlaces = Math.pow(10, decPlaces)

    // Enumerate number abbreviations
    var abbrev = ['k', 'm', 'b', 't']
    let abbr = '';

    // Go through the array backwards, so we do the largest first
    for (var i = abbrev.length - 1; i >= 0; i--) {
        // Convert array index to "1000", "1000000", etc
        var size = Math.pow(10, (i + 1) * 3)

        // If the number is bigger or equal do the abbreviation
        if (size <= number) {
            // Here, we multiply by decPlaces, round, and then divide by decPlaces.
            // This gives us nice rounding to a particular decimal place.
            number = Math.round((number * decPlaces) / size) / decPlaces

            // Handle special case where we round up to the next abbreviation
            if (number == 1000 && i < abbrev.length - 1) {
                number = 1
                i++
            }

            // Add the letter for the abbreviation
            abbr = abbrev[i]

            // We are done... stop
            break
        }
    }

    return number.toString() + abbr

}

export function getMedal(index: number): string {
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

export async function updateStatsChannel(client: Client, channelId: string, server: Server, index: number): Promise<void> {
    try {
        const channel = await client.channels.fetch(channelId) as TextChannel;

        channel.setName(`${server.up_from > 0 ? getMedal(index) : '❌'}・${server.name}「${server.up_from > 0 ? server.players.online : '-'}👥」`)

        if (channel) {
            const message = getServerMessage(client, server);
            const lastMessage = (await channel.messages.fetch({ limit: 1 })).first();

            // The bot can only edit its own messages; seed one the first time.
            if (lastMessage && lastMessage.author.id === client.user?.id && lastMessage.embeds.length > 0) {
                await lastMessage.edit(message);
            } else {
                await channel.send(message as MessageCreateOptions);
            }
        }
    } catch (error) {
        console.error(`Error updating embed in channel ${channelId}:`, error);
    }
}

export async function checkChannelPermission(interaction: ChatInputCommandInteraction, requiredChannel: keyof typeof channels): Promise<boolean> {
    if (interaction.channelId !== channels[requiredChannel]) {
        await interaction.reply({ content: `❌ در چنل اشتباهی هستید! لطفا به <#${channels[requiredChannel]}> برید.`, ephemeral: true });
        return false;
    }
    return true;
}

const LIVE_OFFLINE = 'این سرور در حال حاضر آفلاین هست!';
const LIVE_DELISTED = 'این سرور دیگه روی MCTracker ترک نمیشه.';
const LIVE_FOOTER = 'MCTracker Live • آخرین بروزرسانی';
const LIVE_INVITE_LABEL = 'Add MCTracker to your server';

export function getDelistedEmbed(serverName: string): BaseMessageOptions {
    return {
        content: '',
        embeds: [
            new EmbedBuilder()
                .setColor('Grey')
                .setTitle(`⚪ ${serverName}`)
                .setDescription(LIVE_DELISTED)
        ],
        components: [],
    };
}

/**
 * Standalone from getServerMessage, for community servers
 */
export function getLiveEmbed(client: Client, server: Server): BaseMessageOptions {
    const online = server.up_from > 0;

    const embed = new EmbedBuilder()
        .setColor(online ? 'Green' : 'Red')
        .setTitle(`${online ? '💎' : '🔴'} ${server.name}`)
        .setURL(`${trackerUrl}/server/${server.name}`)
        .setTimestamp(Date.now())
        .setFooter({ text: LIVE_FOOTER, iconURL: logoUrl });

    if (server.favicon) embed.setThumbnail(server.favicon);

    if (!online) {
        embed.setDescription(LIVE_OFFLINE);
    } else {
        embed.addFields(
            { name: '「🌐」Address »', value: server.address, inline: false },
            { name: '「👥」Online Players »', value: `${server.players.online}/${server.players.max}`, inline: true },
            { name: '「🥇」Top Record »', value: `${server.players.record}`, inline: true },
            { name: '「📌」Version »', value: `${server.version}`, inline: false },
            { name: '「📡」Latency »', value: `${server.latency}ms`, inline: true },
            { name: '「📈」UpTime »', value: `${server.uptime}`, inline: true },
        );

        // Gamemode emoji live in the tracker's guild
        const home = client.guilds.cache.get(trackerGuildId);
        const fallback = home?.emojis.cache.find((emoji: Emoji) => emoji.name === 'barrier')?.toString() ?? '';

        const gamemodes = Object.entries(server.gamemodes ?? {})
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10)
            .map(([gamemode, value]) => {
                const icon = home?.emojis.cache.find((emoji: Emoji) => emoji.name === gamemode)?.toString() ?? fallback;

                return `${icon} ${gamemode.charAt(0).toUpperCase() + gamemode.slice(1)}: ${value}`.trim();
            })
            .join('\n');

        if (gamemodes) embed.addFields({ name: '「🎮」Games Status', value: gamemodes, inline: false });
    }

    return {
        content: '',
        embeds: [embed],
        components: [
            new ActionRowBuilder<ButtonBuilder>().addComponents(
                new ButtonBuilder()
                    .setLabel('Open on MCTracker.iR')
                    .setURL(`${trackerUrl}/server/${server.name}`)
                    .setEmoji('🌐')
                    .setStyle(ButtonStyle.Link),
                new ButtonBuilder()
                    .setLabel(`Vote for ${server.name}`)
                    .setURL(`${trackerUrl}/server/${server.name}/vote`)
                    .setEmoji('👍🏻')
                    .setStyle(ButtonStyle.Link),
                new ButtonBuilder()
                    .setLabel(LIVE_INVITE_LABEL)
                    .setURL(botInviteUrl)
                    .setEmoji('➕')
                    .setStyle(ButtonStyle.Link),
            ),
        ],
    };
}


export async function syncNickname(client: Client, guildId: string, server?: Server): Promise<void> {
    const me = client.guilds.cache.get(guildId)?.members.me;
    if (!me) return;

    const nickname = server && server.up_from > 0
        ? `MCTracker | ${server.players.online} online`
        : 'MCTracker';

    if (me.nickname === nickname) return;

    try {
        await me.setNickname(nickname);
    } catch (error) {
        console.error(`Failed to set nickname in guild ${guildId}:`, error);
    }
}

export function getFollowEmbed(server: Server, title: string, description: string): EmbedBuilder {
    const embed = new EmbedBuilder()
        .setColor('#90EE90')
        .setTitle(title)
        .setURL(`${trackerUrl}/server/${server.name}`)
        .setDescription(description)
        .setFooter({ text: 'MCTracker Follow', iconURL: logoUrl })
        .setTimestamp();

    if (server.favicon) embed.setThumbnail(server.favicon);

    return embed;
}
