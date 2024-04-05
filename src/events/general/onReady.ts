import { Events, Client } from 'discord.js';

const event: TrackerEvent<Events.ClientReady> = {
	type: Events.ClientReady,
	async execute(client, readyClient: Client) {
		console.log(`Ready! Logged in as ${readyClient.user?.tag}`);
	},
};

export default event;
