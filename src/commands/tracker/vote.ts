import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { getServer } from '../../services/trackerService';

const command: TrackerCommand = {
	data: new SlashCommandBuilder()
		.setName('vote')
		.setDescription('💻 Vote for your Favourite server!')
		.addStringOption(option => option.setName('server').setDescription('Name').setRequired(true)),
	async execute(_, interaction) {
		const serverName: string = interaction.options.getString('server', true);

		await interaction.reply("🤔 Please wait a moment...");

		const server = await getServer(serverName);

		if (server == null) {
			return await interaction.editReply({embeds: [
				new EmbedBuilder()
					.setColor("Red")
					.setTitle(`🔴 The given server doesn't exist on our database.`)
			]});
		}

		let embed = new EmbedBuilder()
			.setTitle(`💻 Vote for ${server.name}`)
			.setDescription('You can vote everyday to gain great gifts from the server!')
			.setURL(`https://mctracker.ir/server/${server.name}/vote`)
			.setColor(0x673AB7)
			.setTimestamp(Date.now())
			.setFooter({text: 'Tracked by IRMCTracker'})

		await interaction.editReply({ content: '', embeds: [embed] });
	},

};

export default command
