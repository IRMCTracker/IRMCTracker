import { Client, Events, GuildMember } from 'discord.js';
import { communityRoleId, trackerGuildId } from '../../config.json';

const event: TrackerEvent<Events.GuildMemberAdd> = {
	type: Events.GuildMemberAdd,
	async execute(client: Client, member: GuildMember) {
		if (!communityRoleId || member.guild.id !== trackerGuildId || member.user.bot) return;

		await member.roles.add(communityRoleId, 'Community role')
			.catch(error => console.error(`[community] Failed to give role to ${member.id}:`, error));
	},
};

export default event;
