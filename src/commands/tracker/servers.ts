import { SlashCommandBuilder, EmbedBuilder, AttachmentBuilder, APIEmbedField, RestOrArray, MessagePayload, ActionRowBuilder, ButtonBuilder, ButtonStyle, ComponentType } from 'discord.js';
import { Server, getServers } from '../../services/trackerService';
import { bannerUrl, logoUrl } from "../../config.json";
import { getMedal, checkChannelPermission } from '../../services/messagingService';

const command: TrackerCommand = {
    data: new SlashCommandBuilder()
        .setName('servers')
        .setDescription('💻 Retrieve a list of all available servers'),
    async execute(_, interaction) {
        if (!await checkChannelPermission(interaction, 'track')) return;
        
        await interaction.reply("🤔 Please wait a moment...");

        const servers: Server[] | null = await getServers();

        if (servers === null) {
            return await interaction.editReply('🔴 There was an issue retrieving the servers.');
        }

        const sortedServers = servers.slice().sort((a, b) => {
            if (b.players.online !== a.players.online) {
                return b.players.online - a.players.online;
            }
            if (a.up_from >= 0 && b.up_from < 0) {
                return -1;
            }
            if (a.up_from < 0 && b.up_from >= 0) {
                return 1;
            }
            return Math.abs(b.up_from) - Math.abs(a.up_from);
        });

        const embedFields: RestOrArray<APIEmbedField> = [];

        sortedServers.forEach((server: Server, index: number) => {
            if (server.up_from > 0) {
                embedFields.push({ name: `${getMedal(index)} ${server.name}`, value: `👥 ${server.players.online}`, inline: true });
            } else {
                embedFields.push({ name: `🔴 ${server.name}`, value: `👥 -`, inline: true });
            }
        });

        const chunkSize = 24;
        const embeds: EmbedBuilder[] = [];
        for (let i = 0; i < embedFields.length; i += chunkSize) {
            const chunk = embedFields.slice(i, i + chunkSize);
            const embed = new EmbedBuilder()
                .setColor(0x673AB7)
                .setTimestamp(Date.now())
                .setFooter({ text: 'Tracked by IRMCTracker' })
                .setTitle(`[${Math.floor(i / chunkSize) + 1}/${Math.ceil(embedFields.length / chunkSize)}] 📡 Servers List`)
                .setImage('attachment://banner.png');

            embed.addFields(chunk);
            embeds.push(embed);
        }
        
        let currentPage = 0;

        const row = new ActionRowBuilder<ButtonBuilder>()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId('previous')
                    .setLabel('◀ Previous Page')
                    .setStyle(ButtonStyle.Primary)
                    .setDisabled(true),
                new ButtonBuilder()
                    .setCustomId('next')
                    .setLabel('Next Page ▶')
                    .setStyle(ButtonStyle.Primary)
                    .setDisabled(embeds.length <= 1)
            );

        const response = await interaction.editReply({
            content: "",
            embeds: [embeds[0]],
            files: [{ name: "banner.png", attachment: bannerUrl }],
            components: [row]
        });

        const collector = response.createMessageComponentCollector({ 
            componentType: ComponentType.Button,
            time: 600000
        });

        collector.on('collect', async i => {
            if (i.user.id !== interaction.user.id) {
                return await i.reply({ content: "❌ Only the command executor can use these buttons!", ephemeral: true });
            }

            if (i.customId === 'previous') {
                currentPage--;
            } else if (i.customId === 'next') {
                currentPage++;
            }

            row.components[0].setDisabled(currentPage === 0);
            row.components[1].setDisabled(currentPage === embeds.length - 1);

            await i.update({
                embeds: [embeds[currentPage]],
                components: [row]
            });
        });

        collector.on('end', () => {
            row.components.forEach(button => button.setDisabled(true));
            interaction.editReply({ components: [row] }).catch(() => {});
        });
    },
};

export default command;
