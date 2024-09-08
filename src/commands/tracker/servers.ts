import {
  SlashCommandBuilder,
  EmbedBuilder,
  AttachmentBuilder,
  APIEmbedField,
  RestOrArray,
  MessagePayload,
} from "discord.js";
import { Server, getServers } from "../../services/trackerService";
import { bannerUrl, logoUrl } from "../../config.json";
import { getMedal } from "../../services/messagingService";

const command = {
  data: new SlashCommandBuilder()
    .setName("servers")
    .setDescription("💻 Get a list of all available servers"),
  async execute(_, interaction) {
    await interaction.reply("🤔 Wait a moment...");

    const servers = await getServers();

    if (!servers) {
      setTimeout(() => {
        interaction.editReply("🔴 There was a problem retrieving servers.");
      }, 5000);
      return;
    }

    const sortedServers = servers.slice().sort((a, b) => {
      if (b.players.online !== a.players.online) {
        return b.players.online - a.players.online;
      }
      if (a.up_from >= 0 && b.up_from < 0) {
        return -1;
      }
      if (a.up_from < 0 && b.up_from >= 0) {
        return 1;
      }
      return Math.abs(b.up_from) - Math.abs(a.up_from);
    });

    const embedFields = sortedServers.map((server, index) => ({
      name: `${server.up_from > 0 ? getMedal(index) : "🔴"} ${server.name}`,
      value: server.up_from > 0 ? `👥 ${server.players.online}` : `👥 -`,
      inline: true,
    }));

    const chunkSize = 24;
    const embeds = [];
    for (let i = 0; i < embedFields.length; i += chunkSize) {
      const chunk = embedFields.slice(i, i + chunkSize);
      const embed = new EmbedBuilder()
        .setColor(0x673ab7)
        .setTimestamp(Date.now())
        .setFooter({ text: "Tracked by IRMCTracker" });

      embed.addFields(chunk);
      embeds.push(embed);
    }

    embeds[0].setTitle("📡 Servers List | لیست سرور ها");
    embeds.forEach((embed, index) => {
      if (index !== embeds.length - 1) {
        embed.setThumbnail("attachment://logo.png");
      }
    });
    embeds[embeds.length - 1].setImage("attachment://banner.png");

    await interaction.editReply({
      content: "",
      embeds: embeds,
      files: [
        { name: "logo.png", attachment: logoUrl },
        { name: "banner.png", attachment: bannerUrl },
      ],
    });
  },
};

export default command;
