const { REST, Routes } = require('discord.js');
const { client_id, token } = require('../config.json');
const { findJSFiles } = require('../src/utils');
const path = require('node:path');

const commands = [];

const commandsPath = path.join(__dirname, 'commands');

// Grab the SlashCommandBuilder#toJSON() output of each command's data for deployment
for (const filePath of findJSFiles(commandsPath)) {
	const command = require(filePath);
	commands.push(command.data.toJSON());
}

const rest = new REST({ version: '10' }).setToken(token);

(async () => {
	try {
		console.log(`Started refreshing ${commands.length} application (/) commands.`);
				
		const data = await rest.put(
			Routes.applicationCommands(client_id),
			{ body: commands },
		);

		console.log(`Successfully reloaded ${data.length} application (/) commands.`);
	} catch (error) {
		console.error(error);
	}
})();
