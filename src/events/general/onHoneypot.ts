import { EmbedBuilder, Events, Message } from 'discord.js';
import { channels } from '../../config.json';

const TIMEOUT_MS = 24 * 60 * 60 * 1000;

export const honeypotEmbed = new EmbedBuilder()
	.setColor('Red')
	.setTitle('⛔ به هیچ عنوان در این چنل پیام ندهید')
	.setDescription('این چنل برای شناسایی اکانت‌ های هک‌ شده و اسپمرها ساخته شده.\nهر کسی اینجا پیام بفرستد **به صورت خودکار میوت** می‌شود.')
	.setFooter({ text: 'MCTracker Anti-Spam' });

const event: TrackerEvent<Events.MessageCreate> = {
	type: Events.MessageCreate,
	async execute(_, message: Message) {
		if (!channels.honeypot || message.channel.id != channels.honeypot) return;
		if (message.author.bot || !message.guild) return;

		await message.delete().catch(() => {});

		if (!message.member?.moderatable) return;

		await message.member.timeout(TIMEOUT_MS, 'Honeypot channel')
			.then(() => console.log(`[honeypot] Timed out ${message.author.tag} (${message.author.id})`))
			.catch(error => console.error('[honeypot] Timeout failed:', error));
	},
};

export default event;
