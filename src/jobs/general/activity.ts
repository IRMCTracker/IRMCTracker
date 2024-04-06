import { Client } from 'discord.js';
import { StatsResponse, getStats } from '../../services/trackerService';

const activities = [
    "💎 Visit MCTracker.iR",
    "🤌🏻 You can vote to servers on our site!",
    "😎 Bishtar az %track_count% track",
    "🙄 Darhale track kardan %server_count% server"
];

const job: TrackerJob = {
	cronTime: '0 * * * * *',
	async execute(client: Client) {
        let newActivity = activities[Math.floor(Math.random() * activities.length)];

        // Means we need to replace stats
        if (newActivity.includes('%')) {
            const stats: StatsResponse = await getStats();
            newActivity = newActivity
                .replace('%track_count%', stats.counts.records.toString())
                .replace('%server_count%', stats.counts.servers.toString());
        }
        
        client.user?.setActivity(newActivity);
	},
};

export default job;
