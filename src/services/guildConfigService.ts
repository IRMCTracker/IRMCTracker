import { GuildConfig, deleteGuildConfig, fetchGuildConfigs, patchGuildConfig, putGuildConfig } from './trackerService';

const REFRESH_INTERVAL = 5 * 60_000;

let cache = new Map<string, GuildConfig>();
let lastRefresh = 0;

export async function getConfigs(): Promise<GuildConfig[]> {
    if (Date.now() - lastRefresh >= REFRESH_INTERVAL) {
        const fresh = await fetchGuildConfigs();

        // A failed refresh keeps the previous cache
        if (fresh) {
            cache = new Map(fresh.map(config => [config.guild_id, config]));
            lastRefresh = Date.now();
        }
    }

    return [...cache.values()];
}

export async function saveConfig(guildId: string, body: Record<string, unknown>): Promise<GuildConfig> {
    const config = await putGuildConfig(guildId, body);
    cache.set(guildId, config);

    return config;
}

export async function setMessageId(guildId: string, messageId: string | null): Promise<void> {
    await patchGuildConfig(guildId, { message_id: messageId });

    const config = cache.get(guildId);
    if (config) config.message_id = messageId;
}

export async function disableConfig(guildId: string): Promise<void> {
    await patchGuildConfig(guildId, { disabled: true });
    cache.delete(guildId);
}

export async function removeConfig(guildId: string): Promise<void> {
    await deleteGuildConfig(guildId);
    cache.delete(guildId);
}
