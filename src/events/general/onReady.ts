import { Events, Client, TextChannel } from 'discord.js';
import { channels } from '../../config.json';
import { honeypotEmbed } from './onHoneypot';
import { getJobs } from '../../services/botService';
import { CronJob } from 'cron';

const event: TrackerEvent<Events.ClientReady> = {
	type: Events.ClientReady,
	async execute(client, readyClient: Client) {
		console.log(`[*] Ready! Logged in as ${readyClient.user?.tag}`);

		// Register jobs
		console.log('[-] Registering jobs...');
		getJobs().forEach((job: TrackerJob) => new CronJob(job.cronTime, () => job.execute(client), null, true, 'Asia/Tehran', null, job.runOnStart ?? false))
		console.log('[+] Registering jobs completed.');

		// Everyone else's messages get deleted, so any message from us means the warning is already up.
		if (channels.honeypot) {
			try {
				const channel = await client.channels.fetch(channels.honeypot) as TextChannel;
				const recent = await channel.messages.fetch({ limit: 10 });
				if (!recent.some(message => message.author.id == client.user?.id)) {
					await channel.send({ embeds: [honeypotEmbed] });
				}
			} catch (error) {
				console.error('[honeypot] Failed to post warning:', error);
			}
		}

	},
};

export default event;
