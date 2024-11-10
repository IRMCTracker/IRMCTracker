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

            // Update all channels concurrently
            await Promise.all(
                sortedServers
                    .slice(0, Math.min(sortedServers.length, topVotesChannels.length))
                    .map((server, index) => 
                        updateStatsChannel(client, topVotesChannels[index], server, index)
                            .catch(err => console.error(`Failed to update channel ${topVotesChannels[index]}:`, err))
                    )
            );
        } catch (error) {
            console.error('Error executing job:', error);
        }
    },
};

export default job;
