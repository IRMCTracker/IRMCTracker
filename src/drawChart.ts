import { drawPieChart } from './services/chartService';

async function main() {
    const args = process.argv.slice(2);
    const chartType = args[0]?.toLowerCase();

    try {
        if (chartType === 'pie') {
            const filePath = await drawPieChart();
            console.log(`Chart generated successfully: ${filePath}`);
        } else {
            console.error('Usage: node drawChart.js pie');
            process.exit(1);
        }
    } catch (error) {
        console.error('Error generating chart:', error);
        process.exit(1);
    }
}

main();
