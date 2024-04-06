import { Client } from 'discord.js';
import { getServers } from '../../services/trackerService';
import { statsChannels } from '../../config.json';
import { updateStatsChannel } from '../../services/messagingService';

// Define your job object
const job: TrackerJob = {
    cronTime: '0 */5 * * * *',
    async execute(client: Client) {        
        try {
            // Fetch the servers
            const servers = await getServers();

            if (servers == null) {
                return console.error("[!] Fetching servers failed");
            }

            // Sort the servers based on players
            const sortedServers = servers.slice().sort((a, b) => b.players.online - a.players.online);

            // Iterate over the sorted servers and update embeds in all channels
            for (let i = 0; i < Math.min(sortedServers.length, statsChannels.length); i++) {
                const server = sortedServers[i];
                const channelId = statsChannels[i];
                await updateStatsChannel(client, channelId, server, i);
            }
        } catch (error) {
            console.error('Error executing job:', error);
        }
    },
};

export default job;
