import { Client, DiscordAPIError, RESTJSONErrorCodes, TextChannel } from 'discord.js';
import { GuildConfig, Server, getServers } from '../../services/trackerService';
import { disableConfig, getConfigs, removeConfig, setMessageId } from '../../services/guildConfigService';
import { getDelistedEmbed, getLiveEmbed, syncNickname } from '../../services/messagingService';

const PERMISSION_FAILURE_LIMIT = 3;
const NICKNAME_INTERVAL = 15 * 60_000;

const signatures = new Map<string, { messageId: string | null, sig: string }>();
const permissionFailures = new Map<string, number>();
const nicknameUpdatedAt = new Map<string, number>();

let running = false;

function signature(server?: Server): string {
    if (!server) return 'delisted';

    return [
        server.up_from > 0,
        server.players.online,
        server.players.max,
        server.players.record,
        server.version,
        server.latency,
        server.uptime,
        JSON.stringify(server.gamemodes ?? {}),
    ].join('|');
}

async function sync(client: Client, config: GuildConfig, server?: Server): Promise<void> {
    const current = signature(server);
    const previous = signatures.get(config.guild_id);

    // A different message id means the panel was reposted or reinstalled.
    if (previous?.messageId === config.message_id && previous.sig === current) return;

    const channel = await client.channels.fetch(config.channel_id) as TextChannel | null;
    if (!channel) return;

    const payload = server ? getLiveEmbed(server) : getDelistedEmbed(config.server);

    let messageId = config.message_id;

    if (messageId) {
        await channel.messages.edit(messageId, payload);
    } else {
        messageId = (await channel.send(payload)).id;
        await setMessageId(config.guild_id, messageId);
    }

    signatures.set(config.guild_id, { messageId, sig: current });
    permissionFailures.delete(config.guild_id);
}

async function handleFailure(config: GuildConfig, error: unknown): Promise<void> {
    const code = error instanceof DiscordAPIError ? error.code : null;

    switch (code) {
        case RESTJSONErrorCodes.UnknownMessage:
            // Someone deleted the panel, drop the id and the next cycle reposts.
            await setMessageId(config.guild_id, null);
            break;

        case RESTJSONErrorCodes.UnknownChannel:
        case RESTJSONErrorCodes.MissingAccess:
            await removeConfig(config.guild_id);
            break;

        case RESTJSONErrorCodes.MissingPermissions: {
            const failures = (permissionFailures.get(config.guild_id) ?? 0) + 1;
            permissionFailures.set(config.guild_id, failures);

            if (failures >= PERMISSION_FAILURE_LIMIT) {
                permissionFailures.delete(config.guild_id);
                await disableConfig(config.guild_id);
            }
            break;
        }

        default:
            console.error(`Live embed failed for guild ${config.guild_id}:`, error);
    }
}

const job: TrackerJob = {
    cronTime: '0 * * * * *',

    async execute(client: Client) {
        if (running) return;
        running = true;

        try {
            const configs = await getConfigs();
            if (configs.length === 0) return;

            const servers = await getServers();
            if (!servers) return;

            const byName = new Map(servers.map(server => [server.name.toLowerCase(), server]));

            // sequential for now, might switch to concurrent pools later
            for (const config of configs) {
                const server = byName.get(config.server?.toLowerCase() ?? '');

                try {
                    await sync(client, config, server);
                } catch (error) {
                    await handleFailure(config, error);
                }

                const nicknameAge = Date.now() - (nicknameUpdatedAt.get(config.guild_id) ?? 0);

                if (config.nickname_enabled && nicknameAge >= NICKNAME_INTERVAL) {
                    nicknameUpdatedAt.set(config.guild_id, Date.now());
                    await syncNickname(client, config.guild_id, server);
                }
            }
        } finally {
            running = false;
        }
    },
};

export default job;
