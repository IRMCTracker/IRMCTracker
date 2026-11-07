import { Client } from 'discord.js';
import { syncStaffRoles } from '../../services/staffService';

const job: TrackerJob = {
  cronTime: '0 0 5 * * *',
  runOnStart: true,
  async execute(client: Client) {
    try {
      await syncStaffRoles(client);
    } catch (error) {
      console.error('[staff] Daily role sync failed:', error);
    }
  },
};

export default job;
