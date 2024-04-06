import { Client, TextChannel } from 'discord.js';
import { StatsResponse, getStats } from '../../services/trackerService';
import { trackerGuildId, channels } from '../../config.json';
import { formatNumber } from '../../services/messagingService';

async function getChannel(client: Client, id: string): Promise<TextChannel|null> {
    const channel = client.channels.cache.get(id) ?? await client.channels.fetch(id);

    if (! channel) return null;

    return channel as TextChannel;
}

const job: TrackerJob = {
	cronTime: '0 */5 * * * *',
	async execute(client: Client) {
        const stats: StatsResponse = await getStats();

        const membersCount = client.guilds.cache.get(trackerGuildId)?.memberCount ?? 0;

        const membersChannel = await getChannel(client, channels.membersCount);
        const votesChannel = await getChannel(client, channels.votesCount);
        const serversChannel = await getChannel(client, channels.serversCount);
        const tracksChannel = await getChannel(client, channels.recordsCount);
        const emptyChannel = await getChannel(client, channels.emptyCount);
        const totalChannel = await getChannel(client, channels.playersCount);

        await membersChannel?.setName(`👥・ Members「${formatNumber(membersCount)}」`);
        await votesChannel?.setName(`😄・Votes「${formatNumber(stats.counts.votes)}👥」`);
        await serversChannel?.setName(`💻・Servers「${formatNumber(stats.counts.servers)}👥」`);
        await tracksChannel?.setName(`🔗・Tracks「${formatNumber(stats.counts.records)}👥」`);

        await totalChannel?.setName(`💎・All「${formatNumber(stats.counts.players)}👥」`);
        await emptyChannel?.setName(`📈・Empty「${formatNumber(stats.counts.empty)}🔨」`);
	},
};

export default job;
