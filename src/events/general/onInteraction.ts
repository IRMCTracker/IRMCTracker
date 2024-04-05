import { Events, Interaction, CacheType } from 'discord.js';

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
            if (interaction.replied || interaction.deferred) {
                await interaction.followUp({ content: 'There was an error while executing this command!', ephemeral: true });
            }
            else {
                await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
            }
        }    
	},
};

export default event;
