import { Events, Message } from "discord.js";

const event: TrackerEvent<Events.MessageCreate> = {
  type: Events.MessageCreate,
  async execute(_, message: Message) {
    // Check if the message is from a bot or not in a guild
    if (message.author.bot || !message.guild) return;

    // Define patterns to match invites and IPs
    const inviteRegex = /(discord\.(gg|io|me|li|com|net)\/[^\s]+)/g;
    const ipRegex = /\b(?:\d{1,3}\.){3}\d{1,3}\b/g;

    // Check if the message contains any invite or IP
    if (inviteRegex.test(message.content) || ipRegex.test(message.content)) {
      await message.delete();
      return;
    }

    // Extract and check URLs in the message content
    const urls = message.content.match(/\bhttps?:\/\/\S+/gi);
    if (urls) {
      const allLinksAreClean: boolean = urls.every((url: string) => {
        try {
          return new URL(url).hostname.endsWith("mctracker.ir");
        } catch (error) {
          // Ignore invalid URLs
          return true;
        }
      });

      if (!allLinksAreClean) {
        await message.delete();
      }
    }
  },
};

export default event;
