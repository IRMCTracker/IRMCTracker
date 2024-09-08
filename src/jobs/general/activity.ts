import { Client } from 'discord.js';
import { StatsResponse, getStats } from '../../services/trackerService';

const activities = [
  "💎 Visit MCTracker.iR",
  "📋 You can vote for servers on our site!",
  "😎 More than %track_count% tracked",
  "🙄 Currently tracking %server_count% servers"
];

const job = {
  cronTime: '0 * * * * *',
  async execute(client) {
    let newActivity = activities[Math.floor(Math.random() * activities.length)];

    // Replace placeholders with stats if needed
    if (newActivity.includes('%')) {
      const stats = await getStats();
      newActivity = newActivity
        .replace('%track_count%', stats.counts.records.toString())
        .replace('%server_count%', stats.counts.servers.toString());
    }

    client.user?.setActivity(newActivity);
  },
};

export default job;
