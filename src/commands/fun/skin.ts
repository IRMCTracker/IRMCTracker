import { SlashCommandBuilder, EmbedBuilder } from "discord.js";
import { userNameToUUID } from "../../services/playerService";

const command: TrackerCommand = {
  data: new SlashCommandBuilder()
    .setName("skin")
    .setDescription("🤌🏻 Retrieve an image of your Minecraft skin")
    .addStringOption((option) =>
      option.setName("name").setDescription("Your skin name").setRequired(true),
    ),
  async execute(_, interaction) {
    const userName: string = interaction.options.getString("name", true);

    await interaction.reply("Searching for your skin... 🤔");

    const uuid = await userNameToUUID(userName);

    if (!uuid) {
      return await interaction.editReply(
        "☹️ The skin name appears to be incorrect. Unable to find it.",
      );
    }

    const embed = new EmbedBuilder()
      .setTitle(`💎 Skin: ${userName}`)
      .setImage("attachment://skin.png");

    await interaction.editReply({
      embeds: [embed],
      content: "Found it! 😍\n",
      files: [
        {
          name: "skin.png",
          attachment: `https://crafatar.com/renders/body/${uuid}?size=512&default=MHF_Steve&overlay`,
        },
      ],
    });
  },
};

export default command;
