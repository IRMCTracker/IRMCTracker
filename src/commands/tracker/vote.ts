import { SlashCommandBuilder, EmbedBuilder } from "discord.js";
import { getServer } from "../../services/trackerService";

const command = {
  data: new SlashCommandBuilder()
    .setName("vote")
    .setDescription("💻 Vote for your favorite server")
    .addStringOption((option) =>
      option.setName("server").setDescription("Server name").setRequired(true),
    ),
  async execute(_, interaction) {
    const serverName = interaction.options.getString("server", true);

    await interaction.reply("🤔 Wait a moment...");

    const server = await getServer(serverName);

    if (!server) {
      setTimeout(() => {
        interaction.editReply({
          embeds: [
            new EmbedBuilder()
              .setColor("Red")
              .setTitle("🔴 The entered server does not exist!"),
          ],
        });
      }, 5000);
      return;
    }

    const embed = new EmbedBuilder()
      .setTitle(`💻 Vote for server ${server.name}`)
      .setDescription(
        "By voting for your favorite server daily, you can earn rewards in servers!",
      )
      .setURL(`https://mctracker.ir/server/${server.name}/vote`)
      .setColor(0x673ab7)
      .setTimestamp(Date.now())
      .setFooter({ text: "Tracked by IRMCTracker" });

    await interaction.editReply({ content: "", embeds: [embed] });
  },
};

export default command;
