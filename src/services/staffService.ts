import { Client, Guild, GuildMember, Role } from 'discord.js';
import { isAxiosError } from 'axios';
import { staffRoles, trackerGuildId } from '../config.json';
import { tracker, apiKeyHeader } from './trackerService';
import { fetchAllMembers } from './botService';

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
  top: { name: string, color: string }[];
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

const sharedRoleIds = () => [staffRoles.owner, staffRoles.admin, staffRoles.developer, staffRoles.creator].filter(Boolean);

async function ensureStaffRole(guild: Guild, server: SyncState['top'][number]): Promise<void> {
  const color = server.color.toLowerCase();
  let role = findStaffRole(guild, server.name);

  if (!role) {
    role = await guild.roles.create({ name: staffRoleName(server.name), color, hoist: true, mentionable: true, reason: `Staff role for ${server.name}` });
  } else if (role.hexColor !== color || !role.hoist) {
    role = await role.edit({ color, hoist: true, reason: 'MCTracker staff sync' });
  }

  const sharedTop = Math.max(0, ...sharedRoleIds().map(id => guild.roles.cache.get(id)?.position ?? 0));
  if (role.position > sharedTop) return;

  if (sharedTop + 1 >= (guild.members.me?.roles.highest.position ?? 0)) {
    throw new Error('Move the bot\'s role above the shared staff roles so it can place staff roles above them');
  }

  // Only send this role: role.setPosition() renumbers every cached role, which breaks when the cache is stale.
  await guild.roles.setPositions([{ role, position: sharedTop + 1 }]);
  await guild.roles.fetch();
}

/**
 * Orders the staff roles just above the shared ones
 */
async function sortStaffRoles(guild: Guild, top: SyncState['top']): Promise<void> {
  await guild.roles.fetch();

  const staff = top
    .map(server => findStaffRole(guild, server.name))
    .filter((role): role is Role => role !== undefined)
    .reverse();
  const staffIds = new Set(staff.map(role => role.id));
  const sharedTop = Math.max(0, ...sharedRoleIds().map(id => guild.roles.cache.get(id)?.position ?? 0));

  // Bottom to top, without @everyone (always position 0).
  const current = [...guild.roles.cache.values()]
    .filter(role => role.id !== guild.id)
    .sort((a, b) => guild.roles.comparePositions(a, b));
  const others = current.filter(role => !staffIds.has(role.id));
  const cut = others.filter(role => role.position <= sharedTop).length;
  const wanted = [...others.slice(0, cut), ...staff, ...others.slice(cut)];

  const moves = wanted
    .map((role, i) => ({ role, position: i + 1 }))
    .filter(({ role }, i) => current[i] !== role);
  if (!moves.length) return;

  const botTop = guild.members.me?.roles.highest.position ?? 0;
  if (moves.some(({ role }) => role.position >= botTop)) {
    throw new Error('Move the bot\'s role above the staff roles so it can sort them');
  }

  await guild.roles.setPositions(moves);
}

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
    const role = findStaffRole(guild, entry.server);
    if (!role) throw new Error(`Missing staff role for ${entry.server}`);

    if (staffRoles[entry.role]) wanted.add(staffRoles[entry.role]);
    wanted.add(role.id);
  }

  if (member.roles.length > 0 && staffRoles.creator) wanted.add(staffRoles.creator);

  const current = discordMember.roles.cache;
  const staffRoleIds = [...state.top.map(server => server.name), ...state.retired]
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

  await guild.roles.fetch();

  for (const server of state.top) {
    try {
      await ensureStaffRole(guild, server);
    } catch (error) {
      ok = false;
      console.error(`[staff] Failed to set up the staff role for ${server.name}:`, error);
    }
  }

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
  await fetchAllMembers(guild);

  const listed = new Set(state.members.map(member => member.discord_id));

  for (const serverName of [...state.top.map(server => server.name), ...state.retired]) {
    for (const memberId of findStaffRole(guild, serverName)?.members.keys() ?? []) {
      if (listed.has(memberId)) continue;
      listed.add(memberId);
      state.members.push({ discord_id: memberId, roles: [] });
    }
  }

  const ok = await applyStaffState(client, state);

  try {
    await sortStaffRoles(guild, state.top);
  } catch (error) {
    console.error('[staff] Failed to sort staff roles:', error);
  }

  if (!ok) return;

  for (const serverName of state.retired) {
    const role = findStaffRole(guild, serverName);
    if (role) await role.delete('Server left the top').catch(error => console.error(`[staff] Failed to delete ${role.name}:`, error));
  }
}
