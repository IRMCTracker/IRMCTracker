import { AttachmentPayload, EmbedBuilder, Emoji, Guild, InteractionEditReplyOptions, MessagePayload } from 'discord.js';
import { Server } from './trackerService';
import { trackerUrl, bannerUrl, logoUrl } from '../config.json';

export function getServerMessage(guild: Guild, server: Server): MessagePayload | InteractionEditReplyOptions {
    let embed: EmbedBuilder;
    const files: AttachmentPayload[] = [];

    if (server.up_from < 0) {
        // Server morede nazar shoma dar hale hazer offline hast : (
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
        if (server.gamemodes != null) {
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
        const socialsFieldValue = Object.entries(server.socials)
            .map(([platform, link]) => {
                const platformName = platform.charAt(0).toUpperCase() + platform.slice(1);
                return `${guild.emojis.cache.find((emoji: Emoji) => emoji.name === platform)} [${platformName}](${link})`;
            })
            .join('\n');

        embed.addFields({ name: '「👥」Socials', value: socialsFieldValue, inline: true });

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
