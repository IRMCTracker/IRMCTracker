import { EmbedBuilder, Events, Message } from 'discord.js';
import { channels } from '../../config.json';
import { ask } from '../../services/trackerService';

const event: TrackerEvent<Events.MessageCreate> = {
	type: Events.MessageCreate,
	async execute(_, message: Message) {
		// Check if the message is from a bot or not in a guild
		if (message.author.bot || !message.guild || message.channel.id != channels.aiChat) return;

		if (message.content.length < 5 || message.content.length > 100) {
			return message.reply({
				embeds: [
					new EmbedBuilder().setColor('Red').setTitle('I only answer to questions which have atleast 5 and atlast 100 characters. 😎')
				]
			});
		}

		const answer: string|null = await ask(message.content);

		if (answer == null) {
			return message.reply({
				embeds: [
					new EmbedBuilder().setColor('Red').setTitle('No answers 🥹')
				]
			});
		}

		if (answer.length <= 256) {
			message.reply({
				embeds: [
					new EmbedBuilder().setColor('Green').setTitle(answer)
				]
			})
		} else {
			message.reply({
				embeds: [
					new EmbedBuilder().setColor('Green').setDescription(answer)
				]
			})
		}
	},
};

export default event;
