import { REST, RESTPostAPIChatInputApplicationCommandsJSONBody } from 'discord.js';
import { Routes } from 'discord-api-types/v9';
import { clientId, token, trackerGuildId } from './config.json';
import { getCommands } from './services/botService';

const PUBLIC_COMMANDS = ['setup'];

const commands: RESTPostAPIChatInputApplicationCommandsJSONBody[] = getCommands().map((command: TrackerCommand) => command.data.toJSON());

const publicCommands = commands.filter(command => PUBLIC_COMMANDS.includes(command.name));
const homeCommands = commands.filter(command => !PUBLIC_COMMANDS.includes(command.name));

// Construct and prepare an instance of the REST module
const rest = new REST({ version: '9' }).setToken(token);

// and deploy your commands!
(async () => {
    try {
        console.log(`Started refreshing ${publicCommands.length} global and ${homeCommands.length} guild (/) commands.`);

        await rest.put(Routes.applicationCommands(clientId), { body: publicCommands });
        await rest.put(Routes.applicationGuildCommands(clientId, trackerGuildId), { body: homeCommands });

        console.log('Successfully reloaded application (/) commands.');
    } catch (error) {
        // And of course, make sure you catch and log any errors!
        console.error(error);
    }
})();
