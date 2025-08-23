import { Message, PermissionFlagsBits, TextChannel, ThreadChannel } from 'discord.js';

export async function moderateMessage(message: Message): Promise<void> {
    if (message.author.bot || !message.guild) return;

    const channel = message.channel;
    if (
        (channel instanceof TextChannel || channel instanceof ThreadChannel) &&
        channel.name.startsWith('ticket-')
    ) {
        return;
    }

    if (message.member?.permissions.has(PermissionFlagsBits.Administrator)) return;

    const inviteRegex = /(?:https?:\/\/)?(?:www\.)?discord(?:\.gg|\.io|\.me|\.li|\.com|\.net)\/[^\s]+/i;
    const ipRegex = /\b(?:\d{1,3}\.){3}\d{1,3}\b/;

    if (inviteRegex.test(message.content) || ipRegex.test(message.content)) {
        await message.delete();
        return;
    }

    const urls = message.content.match(/\bhttps?:\/\/\S+/gi);
    if (urls) {
        const allLinksAreClean: boolean = urls.every((url: string) => {
            try {
                return new URL(url).hostname.endsWith('mctracker.ir');
            } catch {
                return true;
            }
        });

        if (!allLinksAreClean) {
            await message.delete();
        }
    }
}
