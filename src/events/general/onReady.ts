import { Events, Client } from 'discord.js';
import { getJobs } from '../../services/botService';
import { CronJob } from 'cron';

const event: TrackerEvent<Events.ClientReady> = {
	type: Events.ClientReady,
	async execute(client, readyClient: Client) {
		console.log(`[*] Ready! Logged in as ${readyClient.user?.tag}`);

		// Register jobs
		console.log('[-] Registering jobs...');
		getJobs().forEach((job: TrackerJob) => new CronJob(job.cronTime, () => job.execute(client), null, true, 'Asia/Tehran'))
		console.log('[+] Registering jobs completed.');

	},
};

export default event;
