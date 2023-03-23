const { Collection } = require('discord.js');
const fs = require('node:fs');
const path = require('node:path');
const { findJSFiles } = require('../src/utils');

client.commands = new Collection();

/* Loading Commands */
console.log(`Loading commands...`);

const commandsPath = path.join(__dirname, 'commands');

for (const filePath of findJSFiles(commandsPath)) {
	const command = require(filePath);

    if ('data' in command && 'execute' in command) {
        console.log(`» [Command Loaded] ${command.data.name}`);

		client.commands.set(command.data.name, command);
	} else {
		console.warn(`The command at ${filePath} is missing a required "data" or "execute" property.`);
	}
}

/* Loading Events */
console.log(`\nLoading events...`);

const eventsPath = path.join(__dirname, 'events');

for (const filePath of findJSFiles(eventsPath)) {
	const event = require(filePath);

    if ('type' in event && 'execute' in event) {
        console.log(`» [Event Loaded] ${path.basename(filePath)}`);

        client.on(event.type, e => event.execute(e, client));
	} else {
		console.warn(`The command at ${filePath} is missing a required "data" or "execute" property.`);
	}
};
