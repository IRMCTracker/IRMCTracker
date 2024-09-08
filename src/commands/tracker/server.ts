import { SlashCommandBuilder, EmbedBuilder } from "discord.js";
import { getServer } from "../../services/trackerService";
import { getServerMessage } from "../../services/messagingService";

const command: TrackerCommand = {
  data: new SlashCommandBuilder()
    .setName("server")
    .setDescription("💻 Retrieve information about the specified server")
    .addStringOption((option) =>
      option.setName("server").setDescription("Server name").setRequired(true),
    ),
  async execute(client, interaction) {
    const serverName: string = interaction.options.getString("server", true);

    await interaction.reply("🤔 Please wait a moment...");

    const server = await getServer(serverName);

    if (!server) {
      const reply = await interaction.editReply({
        embeds: [
          new EmbedBuilder()
            .setColor("Red")
            .setTitle("🔴 The specified server does not exist!"),
        ],
      });

      // Delete the message after 5 seconds
      setTimeout(() => {
        reply
          .delete()
          .catch((err) => console.error("Failed to delete message:", err));
      }, 5000);

      return;
    }

    const message = getServerMessage(client, server);

    await interaction.editReply(message);
  },
};

export default command;
