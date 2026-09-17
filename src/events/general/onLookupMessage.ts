import { Events, InteractionEditReplyOptions, Message, MessageCreateOptions } from 'discord.js';
import { channels } from '../../config.json';
import { getMinecraftProfile, userNameToUUID } from '../../services/playerService';
import { getHypixelProfile } from '../../services/hypixelService';
import { getServer, getServerCard, TrackerUnavailableError } from '../../services/trackerService';
import { getProfileMessage, getServerCardMessage, getServerUnavailableMessage, getSkinMessage } from '../../services/messagingService';

export const usernameRegex = /^[A-Za-z0-9_]{3,16}$/;
const serverNameRegex = /^[A-Za-z0-9_.-]{3,32}$/;

const lookups: Record<string, (query: string) => Promise<InteractionEditReplyOptions | null>> = {
    [channels.skin]: async userName => {
        if (!usernameRegex.test(userName)) return null;

        const uuid = await userNameToUUID(userName);

        return uuid ? getSkinMessage(userName, uuid) : null;
    },

    [channels.profile]: async userName => {
        if (!usernameRegex.test(userName)) return null;

        const uuid = await userNameToUUID(userName);
        if (!uuid) return null;

        const [minecraftProfile, hypixelProfile] = await Promise.all([
            getMinecraftProfile(uuid),
            getHypixelProfile(uuid)
        ]);

        return minecraftProfile ? getProfileMessage(uuid, minecraftProfile, hypixelProfile) : null;
    },

    [channels.track]: async serverName => {
        if (!serverNameRegex.test(serverName)) return null;

        try {
            const server = await getServer(serverName);
            if (server == null) return null;

            return getServerCardMessage(server, await getServerCard(serverName));
        } catch (error) {
            if (error instanceof TrackerUnavailableError) return getServerUnavailableMessage(serverName);
            throw error;
        }
    },
};

const event: TrackerEvent<Events.MessageCreate> = {
    type: Events.MessageCreate,
    async execute(_, message: Message) {
        if (message.author.bot || !message.guild) return;

        const lookup = lookups[message.channel.id];
        if (!lookup) return;

        const reply = await lookup(message.content.trim());

        if (reply) await message.reply(reply as MessageCreateOptions);
    },
};

export default event;
