import { SlashCommandBuilder, EmbedBuilder, AttachmentBuilder, APIEmbedField, RestOrArray, MessagePayload, ActionRowBuilder, ButtonBuilder, ButtonStyle, ComponentType } from 'discord.js';
import { Server, getServers } from '../../services/trackerService';
import { bannerUrl, logoUrl } from "../../config.json";
import { getMedal, checkChannelPermission } from '../../services/messagingService';

const command: TrackerCommand = {
    data: new SlashCommandBuilder()
        .setName('servers')
        .setDescription('💻 دریافت لیستی از تمام سرور های موجود')
        .addStringOption(option =>
            option.setName('type')
                .setDescription('نسخه سرور ها (پیش‌ فرض: جاوا)')
                .addChoices(
                    { name: 'Java', value: 'java' },
                    { name: 'Bedrock', value: 'bedrock' },
                )),
    async execute(_, interaction) {
        if (!await checkChannelPermission(interaction, 'track')) return;

        await interaction.reply("🤔 چند لحظه صبر کن...");

        const type = (interaction.options.getString('type') as 'java' | 'bedrock') ?? 'java';
        const servers: Server[] | null = await getServers(type);

        if (servers === null) {
            return await interaction.editReply('🔴 مشکلی در دریافت سرور ها بوجود آمده.');
        }

        const sortedServers = servers.slice().sort((a, b) => {
            // Sort by players.online (descending)
            if (b.players.online !== a.players.online) {
                return b.players.online - a.players.online;
            }
            // If players.online is the same, sort by up_from (positive values first)
            if (a.up_from >= 0 && b.up_from < 0) {
                return -1; // a comes before b
            }
            if (a.up_from < 0 && b.up_from >= 0) {
                return 1; // b comes before a
            }
            // If up_from values are both positive or both negative, sort by their absolute values
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
				.setTitle(`[${Math.floor(i / chunkSize) + 1}/${Math.ceil(embedFields.length / chunkSize)}] 📡 Servers List | لیست سرور ها`)
				.setImage('attachment://banner.png');

            embed.addFields(chunk);
            embeds.push(embed);
        }
        
        let currentPage = 0;

        const row = new ActionRowBuilder<ButtonBuilder>()
            .addComponents(
                new ButtonBuilder()
                    .setCustomId('previous')
                    .setLabel('◀ صفحه قبل')
                    .setStyle(ButtonStyle.Primary)
                    .setDisabled(true),
                new ButtonBuilder()
                    .setCustomId('next')
                    .setLabel('صفحه بعد ▶')
                    .setStyle(ButtonStyle.Primary)
                    .setDisabled(embeds.length <= 1)
            );

        const response = await interaction.editReply({
            content: "",
            embeds: [embeds[0]],
            files: [{ name: "banner.png", attachment: bannerUrl }],
            components: [row]
        });

        // Create a collector for button interactions
        const collector = response.createMessageComponentCollector({ 
            componentType: ComponentType.Button,
            time: 600000 // 10 minutes
        });

        collector.on('collect', async i => {
            if (i.user.id !== interaction.user.id) {
                return await i.reply({ content: "❌ فقط کسی که دستور رو اجرا کرده میتونه از این دکمه ها استفاده کنه!", ephemeral: true });
            }

            if (i.customId === 'previous') {
                currentPage--;
            } else if (i.customId === 'next') {
                currentPage++;
            }

            // Update button states
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
