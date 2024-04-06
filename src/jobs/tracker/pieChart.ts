import { Client } from 'discord.js';
import { drawPieChart } from '../../services/chartService';

// Define your job object
const job: TrackerJob = {
    cronTime: '0 * * * * *',
    async execute(client: Client) {        
        try {
            // const chartFilePath = await drawPieChart();
            // TODO draw pie chart
            // TODO update pie chart channel
        } catch (error) {
            console.error('Error executing job:', error);
        }
    },
};

export default job;
