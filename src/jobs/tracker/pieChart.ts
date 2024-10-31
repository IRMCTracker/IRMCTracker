import { Client, TextChannel, AttachmentBuilder, EmbedBuilder } from 'discord.js';
import { drawPieChart } from '../../services/chartService';
import { channels, logoUrl } from '../../config.json';

// Define your job object
const job: TrackerJob = {
    cronTime: '0 * * * * *',
    async execute(client: Client) {        
        try {
            const chartFilePath = await drawPieChart();
            const pieChartChannel = await client.channels.fetch(channels.pieChart) as TextChannel;
            if (pieChartChannel) {
                const attachment = new AttachmentBuilder(chartFilePath);
                
                const embed = new EmbedBuilder()
                    .setColor('#90EE90') // lite green color
                    .setTitle('🥧 Pie Chart - Players of top Iranian servers')
                    .setURL('https://mctracker.ir')
                    .setImage('attachment://' + chartFilePath.split(/[/\\]/).pop())
                    .setFooter({ 
                        text: 'Tracked by IRMCTracker',
                        iconURL: logoUrl 
                    })
                    .setTimestamp();

                await pieChartChannel.send({ 
                    embeds: [embed],
                    files: [attachment]
                });
            }
        } catch (error) {
            console.error('Error executing job:', error);
        }
    },
};

export default job;
