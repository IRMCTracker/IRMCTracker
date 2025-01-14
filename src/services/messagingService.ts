import { ActionRowBuilder, AttachmentPayload, ButtonBuilder, ButtonStyle, ChatInputCommandInteraction, Client, EmbedBuilder, Emoji, InteractionEditReplyOptions, MessagePayload, TextChannel } from 'discord.js';
import { Server } from './trackerService';
import { trackerUrl, bannerUrl, logoUrl, trackerGuildId, channels } from '../config.json';

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
            .setDescription('The given server is currently offline.');
    } else {
        embed = new EmbedBuilder()
            .setColor('Random')
            .setTitle(`💎 ${server.name}`)
            .setURL(`${trackerUrl}/servers/${server.name}/vote`)
            .setDescription(server.description)
            .setImage('attachment://motd.png')
            .addFields(
            { name: '「🌐」Address »', value: server.ip ? `${server.address} (**${server.ip}**)` : server.address, inline: false },
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

export async function checkChannelPermission(interaction: ChatInputCommandInteraction, requiredChannel: keyof typeof channels): Promise<boolean> {
    if (interaction.channelId !== channels[requiredChannel]) {
        await interaction.reply({ content: `❌ در چنل اشتباهی هستید! لطفا به <#${channels[requiredChannel]}> برید.`, ephemeral: true });
        return false;
    }
    return true;
}
