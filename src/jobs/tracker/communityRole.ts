import { Client } from 'discord.js';
import { communityRoleId, trackerGuildId } from '../../config.json';
import { fetchAllMembers } from '../../services/botService';

const job: TrackerJob = {
  cronTime: '0 30 5 * * *',
  runOnStart: true,
  async execute(client: Client) {
    if (!communityRoleId) return;

    try {
      const guild = client.guilds.cache.get(trackerGuildId);
      if (!guild) throw new Error('Home guild not in cache');

      const members = await fetchAllMembers(guild);
      const missing = members.filter(member => !member.user.bot && !member.roles.cache.has(communityRoleId));

      let given = 0;
      for (const member of missing.values()) {
        try {
          await member.roles.add(communityRoleId, 'Community role');
          given++;
        } catch (error) {
          console.error(`[community] Failed to give role to ${member.id}:`, error);
        }
      }

      if (missing.size) console.log(`[community] Gave the role to ${given}/${missing.size} members.`);
    } catch (error) {
      console.error('[community] Role sync failed:', error);
    }
  },
};

export default job;
