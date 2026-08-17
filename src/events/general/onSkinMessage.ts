import { Events, Message, MessageCreateOptions } from 'discord.js';
import { channels } from '../../config.json';
import { userNameToUUID } from '../../services/playerService';
import { getSkinMessage } from '../../services/messagingService';

export const usernameRegex = /^[A-Za-z0-9_]{3,16}$/;

const event: TrackerEvent<Events.MessageCreate> = {
    type: Events.MessageCreate,
    async execute(_, message: Message) {
        if (message.author.bot || !message.guild || message.channel.id !== channels.skin) return;

        const userName = message.content.trim();
        if (!usernameRegex.test(userName)) return;

        const uuid = await userNameToUUID(userName);

        if (!uuid) return;

        await message.reply(getSkinMessage(userName, uuid) as MessageCreateOptions);
    },
};

export default event;
