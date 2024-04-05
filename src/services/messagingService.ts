import { EmbedBuilder } from "discord.js";
import { Server } from "./serversService";

export function getServerEmbed(server: Server): EmbedBuilder {
    const embed = new EmbedBuilder()
        .setColor('#0099ff') // Set the embed color
        .setTitle('Server Information') // Set the embed title
        .setDescription('Here is some information about the server') // Set the embed description
        .setThumbnail(server.favicon) // Set the server favicon as the thumbnail
        .addFields(
            { name: 'Name', value: server.name, inline: true },
            { name: 'Description', value: server.description, inline: true },
            { name: 'Address', value: server.address, inline: true },
            { name: 'Players Online', value: `${server.players.online}/${server.players.max}`, inline: true },
            { name: 'Record Players', value: server.players.record.toString(), inline: true },
            { name: 'Country', value: `:flag_${server.country_code?.toLowerCase()}:`, inline: true },
            { name: 'Region', value: server.region ?? '-', inline: true },
            { name: 'Latency', value: `${server.latency}ms`, inline: true }
        );

    // Add dynamic gamemodes field
    if (server.gamemodes != null) {
        const gamemodesField = Object.entries(server.gamemodes)
            .map(([gamemode, value]) => ({ name: gamemode, value: `${value} ${getGamemodeEmoji(gamemode)}`, inline: true }));
        embed.addFields(gamemodesField);
    }

    // Add socials field
    const socialsField = Object.entries(server.socials)
        .map(([platform, link]) => ({ name: platform, value: `[${platform}](${link})`, inline: true }));
    embed.addFields(socialsField);

    return embed;
}

export function getGamemodeEmoji(gamemode: string) {
	const emojis: { [key: string]: string } = {
		bedwars: '🛏️',
		survival: '🏞️',
		oneblock: '🧱',
		kitpvp: '⚔️',
		arcade: '🎮'
	};
	return emojis[gamemode] || '';

}
