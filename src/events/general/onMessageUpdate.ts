import { Events, Message, PartialMessage } from 'discord.js';
import { moderateMessage } from '../../services/moderationService';

const event: TrackerEvent<Events.MessageUpdate> = {
    type: Events.MessageUpdate,
    async execute(_oldMessage: Message | PartialMessage, newMessage: Message | PartialMessage) {
        if (newMessage.partial) {
            try {
                newMessage = await newMessage.fetch();
            } catch {
                return;
            }
        }

        await moderateMessage(newMessage as Message);
    },
};

export default event;
