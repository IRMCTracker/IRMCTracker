import { Client, Events, Guild } from 'discord.js';
import { removeConfig } from '../../services/guildConfigService';

const event: TrackerEvent<Events.GuildDelete> = {
	type: Events.GuildDelete,
	async execute(client: Client, guild: Guild) {
		await removeConfig(guild.id).catch(error => console.error(`Failed to remove config for ${guild.id}:`, error));
	},
};

export default event;
