import { Client, Colors, EmbedBuilder, TextChannel } from 'discord.js';
import { getServers, Server } from '../../services/trackerService';
import AlertStateManager, { AlertType } from '../../services/alertService';
import { channels } from '../../config.json';

const getAlertEmbed = (server: Server, alertType: AlertType, data: any = {}) => {
    const alerts = {
        went_online: {
            color: Colors.Green,
            title: '🟢 Server is Online',
            description: `Server **${server.name}** is now online! ✨`
        },
        went_offline: {
            color: Colors.Red,
            title: '🔴 Server is Offline',
            description: `Server **${server.name}** is now offline. ⚡`
        },
        new_record: {
            color: Colors.Yellow,
            title: '🏆 New record!',
            description: `Server **${server.name}** registered a record of **${data.record}** player(s)!`
        },
        high_latency: {
            color: Colors.Orange,
            title: '⚠️ High latency warning',
            description: `Server **${server.name}** is currently experincing high latency. \nProbably DDoS or network problems.`
        },
        player_spike: {
            color: Colors.Purple,
            title: '📈 High player spike!',
            description: `Server **${server.name}** got a high player spike!\n` +
                `Before: ${data.previous} ← Current: ${data.current} player(s)\n` +
                `This might be a sign of botting or fake memberships.`
        }
    };

    const alert = alerts[alertType];
    return new EmbedBuilder()
        .setColor(alert.color)
        .setTitle(alert.title)
        .setDescription(alert.description)
        .setThumbnail(server.favicon)
        .setTimestamp()
        .setFooter({ text: 'IRMCTracker Alert System' });
};

const job: TrackerJob = {
    cronTime: '0 * * * * *',

    async execute(client: Client) {
        if (!channels.alerts) return;

        try {
            const alertChannel = await client.channels.fetch(channels.alerts) as TextChannel;
            if (!alertChannel) return;

            const servers = await getServers();
            if (!servers) return;

            const alertManager = AlertStateManager.getInstance();
            
            for (const server of servers) {
                const previousState = alertManager.getServerState(server.name);
                const alerts = alertManager.updateServerState(server);
                
                for (const alertType of alerts) {
                    const alertData = {
                        record: server.players.record,
                        latency: server.latency,
                        previous: previousState?.lastPlayerCount,
                        current: server.players.online
                    };

                    const embed = getAlertEmbed(server, alertType, alertData);
                    await alertChannel.send({ embeds: [embed] });
                }
            }
        } catch (error) {
            console.error('Error in alerts job:', error);
        }
    }
};

export default job;
