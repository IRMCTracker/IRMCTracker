import { Chart, ArcElement, Legend, Tooltip } from 'chart.js';
import ChartDataLabels from 'chartjs-plugin-datalabels';
import { ChartJSNodeCanvas } from "chartjs-node-canvas";
import { getServers } from "./trackerService";
import { getAverageColor } from 'fast-average-color-node';
import fetch from 'node-fetch';
import fs from 'fs';
import path from 'path';

// Register Chart.js components and plugins once at the module level
Chart.register(ArcElement, Legend, Tooltip, ChartDataLabels);

// Create a singleton ChartJSNodeCanvas instance
const chartCanvas = new ChartJSNodeCanvas({ 
    width: 800, 
    height: 600, 
    backgroundColour: 'transparent'
});

// Cleanup function for proper resource management
export function cleanup() {
    Object.keys(Chart.instances).forEach((key) => {
        Chart.instances[key].destroy();
    });
}

const fallbackColors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];

async function getColorFromFavicon(faviconUrl: string, fallbackIndex: number): Promise<string> {
    if (!faviconUrl) return fallbackColors[fallbackIndex % fallbackColors.length];
    
    try {
        const response = await fetch(faviconUrl);
        if (!response.ok) throw new Error('Failed to fetch favicon');
        
        const buffer = await response.buffer();
        const color = await getAverageColor(buffer, {algorithm: "dominant", mode: "precision", silent: true, ignoredColor: [[0, 0, 0]]});
        return color.hex;
    } catch (error) {
        console.error(`Error extracting color from favicon: ${error}`);
        return fallbackColors[fallbackIndex % fallbackColors.length];
    }
}

export async function drawPieChart(): Promise<string> {
    const servers = await getServers();
    if (!servers) throw new Error("Failed to fetch server data");
    
    // Get top 6 servers by player count
    const topServers = servers
        .filter(s => s.up_from > 0)
        .sort((a, b) => b.players.online - a.players.online)
        .slice(0, 6);

    // Extract colors from favicons
    const serverColors = await Promise.all(
        topServers.map((server, index) => 
            getColorFromFavicon(server.favicon || '', index)
        )
    );

    const totalPlayers = topServers.reduce((sum, s) => sum + s.players.online, 0);

    const configuration = {
        type: 'pie' as const,
        data: {
            labels: topServers.map(s => `${s.name} (${s.players.online} players)`),
            datasets: [{
                data: topServers.map(s => s.players.online),
                backgroundColor: serverColors,
                borderColor: '#FFFFFF',
                borderWidth: 1
            }]
        },
        options: {
            layout: {
                padding: 20
            },
            responsive: true,
            plugins: {
                datalabels: {
                    display: true,
                    color: '#FFFFFF',
                    textAlign: 'center' as 'center',
                    font: {
                        size: 12
                    },
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                    borderRadius: 4,
                    padding: 4,
                    formatter: (value: number, ctx: any) => {
                        const percentage = ((value / totalPlayers) * 100).toFixed(1);
                        const label = ctx.chart.data.labels[ctx.dataIndex].split(' (')[0];
                        return `${label} » ${percentage}%`;
                    },
                    anchor: 'end',  // Changed from 'center' to 'end'
                    align: (ctx: any) => {
                        const value = ctx.dataset.data[ctx.dataIndex];
                        return value / totalPlayers > 0.10 ? 'start' : 'end';
                    },
                    offset: (ctx: any) => {
                        const value = ctx.dataset.data[ctx.dataIndex];
                        return value / totalPlayers > 0.10 ? 75 : -110;  // Increased offset for better visibility
                    },
                    rotation: (ctx: any) => {
                        const value = ctx.dataset.data[ctx.dataIndex];
                        if (value / totalPlayers > 0.10) return 0;
                        
                        const angle = ctx.chart.getDatasetMeta(0).data[ctx.dataIndex].startAngle + 
                            (ctx.chart.getDatasetMeta(0).data[ctx.dataIndex].endAngle - 
                             ctx.chart.getDatasetMeta(0).data[ctx.dataIndex].startAngle) / 2;
                        
                        // Convert angle to degrees and keep text horizontal
                        let degrees = (angle * 180 / Math.PI - 90) % 360;
                        
                        // Adjust text to be right-side up
                        if (degrees < -90 || degrees > 90) {
                            degrees -= 90;
                        }
                        
                        return degrees;
                    }
                },
                legend: {
                    display: true,
                    position: 'right' as const,
                    labels: {
                        color: '#FFFFFF',
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        boxWidth: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: (context: any) => {
                            const value = context.raw;
                            const percentage = ((value / totalPlayers) * 100).toFixed(1);
                            return `${context.label}: ${percentage}%`;
                        }
                    }
                }
            }
        }
    };

    // Use the singleton instance
    const image = await chartCanvas.renderToBuffer(configuration);
    const storageDir = path.join(process.cwd(), 'storage');
    if (!fs.existsSync(storageDir)) {
        fs.mkdirSync(storageDir, { recursive: true });
    }

    const filePath = path.join(storageDir, 'pie_chart.png');
    fs.writeFileSync(filePath, new Uint8Array(image));
    
    return filePath;
}

