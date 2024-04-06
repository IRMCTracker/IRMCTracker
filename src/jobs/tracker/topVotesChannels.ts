import { Client } from 'discord.js';
import { getServers } from '../../services/trackerService';
import { topVotesChannels } from '../../config.json';
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

            // Sort the servers based on votes
            const sortedServers = servers.slice().sort((a, b) => b.votes - a.votes);

            // Iterate over the sorted servers and update embeds in all channels
            for (let i = 0; i < Math.min(sortedServers.length, topVotesChannels.length); i++) {
                const server = sortedServers[i];
                const channelId = topVotesChannels[i];
                await updateStatsChannel(client, channelId, server, i);
            }
        } catch (error) {
            console.error('Error executing job:', error);
        }
    },
};

export default job;
