import { SlashCommandBuilder, EmbedBuilder } from "discord.js";
import {
  getMinecraftProfile,
  userNameToUUID,
} from "../../services/playerService";
import { bannerUrl } from "../../config.json";

const command: TrackerCommand = {
  data: new SlashCommandBuilder()
    .setName("profile")
    .setDescription("🔥 Retrieve your Minecraft account information")
    .addStringOption((option) =>
      option
        .setName("username")
        .setDescription("Player username")
        .setRequired(true),
    ),
  async execute(_, interaction) {
    const userName: string = interaction.options.getString("username", true);

    await interaction.reply(`Searching for the account of ${userName}... 🤔`);

    const uuid = await userNameToUUID(userName);

    if (!uuid) {
      return await interaction.editReply(
        "☹️ It seems the player name is incorrect. Unable to find it.",
      );
    }

    const profile = await getMinecraftProfile(uuid);

    if (!profile) {
      return await interaction.editReply(
        "☹️ There was an issue retrieving the profile information. Please try again later.",
      );
    }

    const embed = new EmbedBuilder()
      .setTitle(`⌠・Player Profile: ${userName}・⌡`)
      .setColor("Random")
      .setTimestamp()
      .setThumbnail("attachment://profile.png")
      .setImage("attachment://banner.png")
      .setFooter({ text: "Tracked by IRMCTracker" })
      .addFields([
        {
          name: "💻 • Usernames",
          value: profile.history.join(" - "),
          inline: true,
        },
        {
          name: "📆 • Created",
          value: profile.createdAt ?? "Hidden",
          inline: true,
        },
      ]);

    await interaction.editReply({
      embeds: [embed],
      content: "",
      files: [
        {
          name: "profile.png",
          attachment: `https://crafatar.com/renders/head/${uuid}?size=512&default=MHF_Steve&overlay`,
        },
        {
          name: "banner.png",
          attachment: bannerUrl,
        },
      ],
    });
  },
};

export default command;
