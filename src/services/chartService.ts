// TODO this file is not production ready will be fixed ASAP

import { Server, getServers } from "./trackerService";
import { ChartJSNodeCanvas } from "chartjs-node-canvas";
import fs from 'fs';

// Function to fetch top 8 servers data
export async function drawPieChart() {
    async function fetchTopServersData() {
        try {
            // Make an API call to fetch server data
            const servers: Server[]|null = await getServers();

            if (servers == null) {
                throw Error('Invalid response from site while drawing chart.');
            }

            // Sort the server data by players online and select the top 8
            const sortedServers = servers.sort((a: Server, b: Server) => b.players.online - a.players.online).slice(0, 8);

            return sortedServers;
        } catch (error) {
            console.error('Error fetching server data:', error);
            throw error;
        }
    }

    // Function to generate and save pie chart image
    async function generatePieChartImage(serversData: Server[]) {
        const width = 800;
        const height = 600;

        // Create ChartJSNodeCanvas instance
        const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });

        // Render chart to an image
        const image = await chartJSNodeCanvas.renderToBuffer({
            type: 'pie',
            data: {
                labels: serversData.map(server => server.name),
                datasets: [{
                    data: serversData.map(server => server.players.online),
                    backgroundColor: [
                        'red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta'
                    ],
                }]
            },
            options: {
                // title: {
                //     display: true,
                //     text: 'Top 8 Servers Players',
                // },
            },
        });

        // Save the image to a file
        fs.writeFileSync('pie_chart.png', image);
        console.log('The PNG file was created.');
    }

    console.log('Generating pie chart image...');
    try {
        // Fetch top 8 servers data
        const topServersData = await fetchTopServersData();

        // Generate and save pie chart image
        await generatePieChartImage(topServersData);
    } catch (error) {
        console.error('Error generating pie chart image:', error);
    }


}

drawPieChart()
