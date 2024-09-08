import { SlashCommandBuilder, EmbedBuilder } from "discord.js";
import { userNameToUUID } from "../../services/playerService";

const command: TrackerCommand = {
  data: new SlashCommandBuilder()
    .setName("head")
    .setDescription("🤌🏻 Retrieve an image of your character's head")
    .addStringOption((option) =>
      option
        .setName("name")
        .setDescription("Your character's skin name")
        .setRequired(true),
    ),
  async execute(client, interaction) {
    const userName: string = interaction.options
      .getString("name", true)
      .toLowerCase();

    await interaction.reply("Searching for your character's head... 🤔");

    const uuid = await userNameToUUID(userName);

    if (!uuid) {
      return await interaction.editReply(
        "☹️ Could not find the skin name. Please check for any mistakes.",
      );
    }

    const embed = new EmbedBuilder()
      .setTitle(`💎 Skin: ${userName}`)
      .setImage("attachment://head.png");

    await interaction.editReply({
      embeds: [embed],
      content: "Found it! 😍\n",
      files: [
        {
          attachment: `https://crafatar.com/renders/head/${uuid}?size=512&default=MHF_Steve&overlay`,
          name: "head.png",
        },
      ],
    });
  },
};

export default command;
