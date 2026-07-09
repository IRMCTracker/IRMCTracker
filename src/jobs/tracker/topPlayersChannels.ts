import { Client } from 'discord.js';
import { Server, getServers } from '../../services/trackerService';
import { statsChannels, bedrockStatsChannels } from '../../config.json';
import { updateStatsChannel } from '../../services/messagingService';

async function updateTopChannels(client: Client, type: 'java' | 'bedrock', channelIds: string[]) {
    if (channelIds.length === 0) return;

    const servers = await getServers(type);

    if (servers == null) {
        return console.error(`[!] Fetching ${type} servers failed`);
    }

    // Sort the servers based on players
    const sortedServers = servers.slice().sort((a: Server, b: Server) => {
        // Sort by players.online (descending)
        if (b.players.online !== a.players.online) {
            return b.players.online - a.players.online;
        }
        // If players.online is the same, sort by up_from (positive values first)
        if (a.up_from >= 0 && b.up_from < 0) {
            return -1; // a comes before b
        }
        if (a.up_from < 0 && b.up_from >= 0) {
            return 1; // b comes before a
        }
        // If up_from values are both positive or both negative, sort by their absolute values
        return Math.abs(b.up_from) - Math.abs(a.up_from);
    });

    // Update all channels concurrently
    await Promise.all(
        sortedServers
            .slice(0, Math.min(sortedServers.length, channelIds.length))
            .map((server, index) =>
                updateStatsChannel(client, channelIds[index], server, index)
                    .catch(err => console.error(`Failed to update channel ${channelIds[index]}:`, err))
            )
    );
}

// Define your job object
const job: TrackerJob = {
    cronTime: '0 */5 * * * *',
    async execute(client: Client) {
        try {
            await Promise.all([
                updateTopChannels(client, 'java', statsChannels),
                updateTopChannels(client, 'bedrock', bedrockStatsChannels),
            ]);
        } catch (error) {
            console.error('Error executing job:', error);
        }
    },
};

export default job;
