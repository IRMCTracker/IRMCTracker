import { AutocompleteInteraction, Guild, Role } from 'discord.js';
import { getServers, Server } from './trackerService';

// Role membership is the source of truth; server_followers on the site is a mirror.
export const followRoleName = (serverName: string) => `🔔 ${serverName}`.slice(0, 100);

export const findFollowRole = (guild: Guild, serverName: string): Role | undefined =>
    guild.roles.cache.find(role => role.name === followRoleName(serverName));

// Lazy creation keeps unfollowed servers out of the guild's 250-role budget. (no atomic prevention for now)
export async function ensureFollowRole(guild: Guild, serverName: string): Promise<Role> {
    return findFollowRole(guild, serverName) ?? await guild.roles.create({
        name: followRoleName(serverName),
        mentionable: false,
        reason: `Follower role for ${serverName}`,
    });
}

// Shared by /follow and /unfollow.
export async function respondWithServerNames(interaction: AutocompleteInteraction): Promise<void> {
    const typed = interaction.options.getFocused().toLowerCase();
    const servers = await getServers() ?? [];

    await interaction.respond(
        servers
            .filter(server => server.name.toLowerCase().includes(typed))
            .slice(0, 25)
            .map(server => ({ name: server.name, value: server.name }))
    );
}

export async function findServerByName(name: string): Promise<Server | null> {
    const servers = await getServers();

    return servers?.find(candidate => candidate.name.toLowerCase() === name.toLowerCase()) ?? null;
}
