const { Events } = require("discord.js");

/**
 * Handling Commands
 */
module.exports = {
    type: Events.InteractionCreate,
    async execute(interaction) {
        if (!interaction.isChatInputCommand()) return;
    
        const command = interaction.client.commands.get(interaction.commandName);
    
        if (!command) {
            return;
        }
    
        try {
            await command.execute(interaction);
        } catch (error) {
            console.error('Error while handling command ' + interaction.commandName, error);
            if (interaction.replied || interaction.deferred) {
                await interaction.followUp({ content: 'There was an error while executing this command!', ephemeral: true });
            } else {
                await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true });
            }
        }    
    }
}
