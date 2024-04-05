import { REST, RESTPostAPIChatInputApplicationCommandsJSONBody } from 'discord.js';
import { Routes } from 'discord-api-types/v9';
import { clientId, token } from './config.json';
import { getCommands } from './services/botService';

const commands: RESTPostAPIChatInputApplicationCommandsJSONBody[] = getCommands().map((command: TrackerCommand) => command.data.toJSON());

// Construct and prepare an instance of the REST module
const rest = new REST({ version: '9' }).setToken(token);

// and deploy your commands!
(async () => {
    try {
        console.log(`Started refreshing ${commands.length} application (/) commands.`);

        // The put method is used to fully refresh all commands in the guild with the current set
        const data: any = await rest.put(
            Routes.applicationCommands(clientId),
            { body: commands },
        );

        console.log(`Successfully reloaded ${data.length} application (/) commands.`);
    } catch (error) {
        // And of course, make sure you catch and log any errors!
        console.error(error);
    }
})();
