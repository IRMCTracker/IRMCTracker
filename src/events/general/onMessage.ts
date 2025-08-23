import { Events, Message } from 'discord.js';
import { moderateMessage } from '../../services/moderationService';

const event: TrackerEvent<Events.MessageCreate> = {
    type: Events.MessageCreate,
    async execute(_, message: Message) {
        await moderateMessage(message);
    },
};

export default event;
