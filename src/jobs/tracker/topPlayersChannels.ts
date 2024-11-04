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
            const sortedServers = servers.slice().sort((a, b) => {
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
