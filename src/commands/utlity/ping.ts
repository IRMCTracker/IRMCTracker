import { SlashCommandBuilder } from "discord.js";

const command = {
  data: new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Replies with the bot's latency"),
  async execute(_, interaction) {
    const sent = await interaction.reply({
      content: "Calculating ping...",
      fetchReply: true,
    });
    const latency = sent.createdTimestamp - interaction.createdTimestamp;
    await interaction.editReply(`Bot latency is ${latency}ms.`);
  },
};

export default command;
