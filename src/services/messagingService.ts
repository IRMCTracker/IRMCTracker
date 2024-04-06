import { AttachmentPayload, Client, EmbedBuilder, Emoji, InteractionEditReplyOptions, MessagePayload, TextChannel } from 'discord.js';
import { Server } from './trackerService';
import { trackerUrl, bannerUrl, logoUrl, trackerGuildId } from '../config.json';

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
                { name: '「🌐」Address »', value: `${server.address} (**${server.ip}**)`, inline: false },
                { name: '「👥」Online Players »', value: `${server.players.online}/${server.players.max}`, inline: true },
                { name: '「🥇」Top Record »', value: server.players.record.toString(), inline: true },
                { name: '「📈」Uptime »', value: `${server.uptime}`, inline: false },
                { name: '「📌」Version »', value: `${server.version}`, inline: true },
                { name: '「📡」Latency »', value: `${server.latency}ms`, inline: true },
                { name: '「🌎」Country »', value: `:flag_${server.country_code?.toLowerCase()}: ${server.region}`, inline: false },
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



    // Setting footer
    embed
        .setTimestamp(Date.now())
        .setFooter({ text: 'Tracked by IRMCTracker' });

    return {
        content: '',
        embeds: [embed],
        files: files
    };
}

export function formatNumber(num: number): string {
    const suffixes = ['', 'k', 'M', 'B', 'T']; // Array of suffixes for thousand, million, billion, etc.

    // Determine the appropriate suffix based on the magnitude of the number
    const magnitude = Math.floor(Math.log10(num) / 3);
    const suffix = suffixes[magnitude];

    // Calculate the shortened number
    const shortNum = num / Math.pow(10, magnitude * 3);

    // Use toFixed to limit the number of decimal places
    const shortNumStr = shortNum.toFixed(1);

    return shortNumStr + suffix;
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
            const lastMessage = await channel.messages.fetch({ limit: 1 });
            if (lastMessage.size > 0) {
                const lastEmbed = lastMessage.first()?.embeds[0];
                if (lastEmbed) {
                    const message = getServerMessage(client, server);
                    await lastMessage.first()?.edit(message);
                }
            }
        }
    } catch (error) {
        console.error(`Error updating embed in channel ${channelId}:`, error);
    }
}
