import { Client, TextChannel, EmbedBuilder } from 'discord.js';
import { getServers } from '../../services/trackerService';
import { channels, logoUrl } from '../../config.json';
import { getMedal } from '../../services/messagingService';

const job: TrackerJob = {
    cronTime: '0 * * * * *',
    async execute(client: Client) {        
        try {
            const servers = await getServers();
            if (servers == null) {
                return console.error("[!] Fetching servers failed");
            }

            // Sort servers by record count
            const sortedServers = servers
                .slice()
                .sort((a, b) => b.players.record - a.players.record)
                .slice(0, 15); // Take top 15 servers

            const recordsChannel = await client.channels.fetch(channels.recordsChannel) as TextChannel;
            if (!recordsChannel) return;

            // Build the records list with enhanced formatting
            const recordsList = sortedServers
                .map((server, index) => {
                    const statusEmoji = server.up_from > 0 ? '🟢' : '🔴';
                    
                    return `${getMedal(index)} ${statusEmoji} **${server.name}**\n` +
                           `┗━ ${server.players.record}👥 Players`;
                })
                .join('\n\n');

            const embed = new EmbedBuilder()
                .setColor('#673AB7')
                .setTitle('💎 Top Records | رکورد سرور های ایرانی')
                .setDescription('لیست بالا ترین رکورد سرور های ایرانی بر اساس تعداد پلیر\n\n' + recordsList)
                .setThumbnail(logoUrl)
                .setTimestamp()
                .setFooter({ text: 'Tracked by IRMCTracker • هردقیقه بروزرسانی میشود' });

            // Get last message and update it
            const lastMessage = await recordsChannel.messages.fetch({ limit: 1 });
            if (lastMessage.size > 0) {
                await lastMessage.first()?.edit({ embeds: [embed] });
            } else {
                await recordsChannel.send({ embeds: [embed] });
            }

        } catch (error) {
            console.error('Error executing records channel job:', error);
        }
    }
};

export default job;
