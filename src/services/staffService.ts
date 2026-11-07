import { Client, Guild, GuildMember, Role } from 'discord.js';
import { isAxiosError } from 'axios';
import { staffRoles, trackerGuildId } from '../config.json';
import { tracker, apiKeyHeader } from './trackerService';

export type StaffRole = 'owner' | 'admin' | 'developer';

export interface StaffServer {
  name: string;
  top: boolean;
  staff: { discord_id: string, role: StaffRole }[];
}

export interface StaffChange extends StaffServer {
  sync: SyncState;
}

interface SyncState {
  top: string[];
  retired: string[];
  members: { discord_id: string, roles: { server: string, role: StaffRole }[] }[];
}

export async function getStaffServer(actorId: string): Promise<StaffServer> {
  const response = await tracker.get('/api/staff', { ...apiKeyHeader, params: { actor: actorId } });
  return response.data.data;
}

export async function addStaff(discordId: string, role: StaffRole, actorId: string): Promise<StaffChange> {
  const response = await tracker.put(`/api/staff/${discordId}`, { role, actor: actorId }, apiKeyHeader);
  return response.data.data;
}

export async function removeStaff(discordId: string, actorId: string): Promise<StaffChange> {
  const response = await tracker.delete(`/api/staff/${discordId}`, { ...apiKeyHeader, data: { actor: actorId } });
  return response.data.data;
}

export function staffErrorCode(error: unknown): string | null {
  return isAxiosError(error) ? error.response?.data?.message ?? null : null;
}

export const staffRoleName = (serverName: string) => `${serverName} Staff`.slice(0, 100);

const findStaffRole = (guild: Guild, serverName: string): Role | undefined =>
  guild.roles.cache.find(role => role.name === staffRoleName(serverName));

async function ensureStaffRole(guild: Guild, serverName: string): Promise<Role> {
  return findStaffRole(guild, serverName) ?? await guild.roles.create({
    name: staffRoleName(serverName),
    mentionable: true,
    reason: `Staff role for ${serverName}`,
  });
}

const sharedRoleIds = () => [staffRoles.owner, staffRoles.admin, staffRoles.developer, staffRoles.creator].filter(Boolean);

/**
 * Shared roles are only removed alongside a "{server} Staff" role, so ones
 * given by hand are left alone.
 */
async function applyMember(guild: Guild, state: SyncState, member: SyncState['members'][number]): Promise<void> {
  let discordMember: GuildMember;

  try {
    discordMember = await guild.members.fetch(member.discord_id);
  } catch {
    return;
  }

  const wanted = new Set<string>();

  for (const entry of member.roles) {
    if (staffRoles[entry.role]) wanted.add(staffRoles[entry.role]);
    wanted.add((await ensureStaffRole(guild, entry.server)).id);
  }

  if (member.roles.length > 0 && staffRoles.creator) wanted.add(staffRoles.creator);

  const current = discordMember.roles.cache;
  const staffRoleIds = [...state.top, ...state.retired]
    .map(serverName => findStaffRole(guild, serverName)?.id)
    .filter((id): id is string => id !== undefined);

  const toAdd = [...wanted].filter(id => !current.has(id));
  const toRemove = staffRoleIds.filter(id => current.has(id) && !wanted.has(id));

  if (toRemove.length) {
    toRemove.push(...sharedRoleIds().filter(id => current.has(id) && !wanted.has(id)));
  }

  if (toAdd.length) await discordMember.roles.add(toAdd, 'MCTracker staff sync');
  if (toRemove.length) await discordMember.roles.remove(toRemove, 'MCTracker staff sync');
}

function homeGuild(client: Client): Guild {
  const guild = client.guilds.cache.get(trackerGuildId);
  if (!guild) throw new Error('Home guild not in cache');
  return guild;
}

export async function applyStaffState(client: Client, state: SyncState): Promise<boolean> {
  const guild = homeGuild(client);
  let ok = true;

  for (const member of state.members) {
    try {
      await applyMember(guild, state, member);
    } catch (error) {
      ok = false;
      console.error(`[staff] Failed to sync roles for ${member.discord_id}:`, error);
    }
  }

  return ok;
}

/**
 * Members holding a staff role the site no longer lists are synced with no
 * roles. Retired roles are deleted only after a clean run, since deleting one
 * first would skip removing the shared roles that came with it.
 */
export async function syncStaffRoles(client: Client): Promise<void> {
  const response = await tracker.get('/api/staff/sync', apiKeyHeader);
  const state: SyncState = response.data.data;

  const guild = homeGuild(client);
  await guild.members.fetch();

  const listed = new Set(state.members.map(member => member.discord_id));

  for (const serverName of [...state.top, ...state.retired]) {
    for (const memberId of findStaffRole(guild, serverName)?.members.keys() ?? []) {
      if (listed.has(memberId)) continue;
      listed.add(memberId);
      state.members.push({ discord_id: memberId, roles: [] });
    }
  }

  if (!await applyStaffState(client, state)) return;

  for (const serverName of state.retired) {
    const role = findStaffRole(guild, serverName);
    if (role) await role.delete('Server left the top').catch(error => console.error(`[staff] Failed to delete ${role.name}:`, error));
  }
}
