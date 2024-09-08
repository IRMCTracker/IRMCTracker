import { EmbedBuilder, Events, Message } from "discord.js";
import { channels } from "../../config.json";
import { ask } from "../../services/trackerService";

const event = {
  type: Events.MessageCreate,
  async execute(_, message) {
    // Ignore messages from bots or not in the specified channel
    if (
      message.author.bot ||
      !message.guild ||
      message.channel.id !== channels.aiChat
    )
      return;

    // Check message length
    if (message.content.length < 5 || message.content.length > 100) {
      return message.reply({
        embeds: [
          new EmbedBuilder()
            .setColor("Red")
            .setTitle(
              "Your message must be between 5 and 100 characters to get help 😎",
            ),
        ],
      });
    }

    const answer = await ask(message.content);

    if (answer === null) {
      return message.reply({
        embeds: [
          new EmbedBuilder()
            .setColor("Red")
            .setTitle("Unfortunately, I have no answer 🥹"),
        ],
      });
    }

    const embed = new EmbedBuilder().setColor("Green");
    if (answer.length <= 256) {
      embed.setTitle(answer);
    } else {
      embed.setDescription(answer);
    }

    message.reply({ embeds: [embed] });
  },
};

export default event;
