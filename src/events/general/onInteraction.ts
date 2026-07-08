import { Events, Interaction, CacheType, InteractionReplyOptions } from 'discord.js';
import { TrackerUnavailableError } from '../../services/trackerService';
import { getServerUnavailableMessage } from '../../services/messagingService';

const event: TrackerEvent<Events.InteractionCreate> = {
	type: Events.InteractionCreate,
	async execute(client, interaction: Interaction<CacheType>) {
        if (!interaction.isChatInputCommand()) return;

        const command = (interaction.client as any).commands.get(interaction.commandName);
    
        if (!command) {
            console.error(`No command matching ${interaction.commandName} was found.`);
            return;
        }
    
        try {
            await command.execute(client, interaction);
        }
        catch (error) {
            console.error(error);

            // tracker outages hit every command that calls getServer/getServers;
            // catch once here instead of a try/catch per command.
            const reply: InteractionReplyOptions = error instanceof TrackerUnavailableError
                ? { ...getServerUnavailableMessage(), ephemeral: true } as InteractionReplyOptions
                : { content: 'There was an error while executing this command!', ephemeral: true };

            if (interaction.replied || interaction.deferred) {
                await interaction.editReply(reply);
            }
            else {
                await interaction.reply(reply);
            }
        }
	},
};

export default event;
