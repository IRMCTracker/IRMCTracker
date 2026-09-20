import { Client, Colors, EmbedBuilder, TextChannel } from 'discord.js';
import { getServers, Server } from '../../services/trackerService';
import AlertStateManager, { AlertType } from '../../services/alertService';
import { findFollowRole } from '../../services/followService';
import { channels } from '../../config.json';

// player_spike usually means a bot attack, not news a follower wants.
const SILENT_ALERTS: AlertType[] = ['player_spike'];

const getAlertEmbed = (server: Server, alertType: AlertType, data: any = {}) => {
    const alerts = {
        went_online: {
            color: Colors.Green,
            title: '🟢 سرور آنلاین شد',
            description: `سرور **${server.name}** آنلاین شده است! ✨`
        },
        went_offline: {
            color: Colors.Red,
            title: '🔴 سرور آفلاین شد',
            description: `سرور **${server.name}** آفلاین شده است! ⚡`
        },
        new_record: {
            color: Colors.Yellow,
            title: '🏆 رکورد جدید',
            description: `سرور **${server.name}** رکورد جدیدی از تعداد بازیکنان را ثبت کرده است: **${data.record}** بازیکن!`
        },
        high_latency: {
            color: Colors.Orange,
            title: '⚠️ هشدار پینگ بالا',
            description: `سرور **${server.name}** پینگ بالایی را تجربه می‌کند (\`${data.latency}ms\`)\nاحتمال حمله DDoS یا مشکلات شبکه وجود دارد`
        },
        player_spike: {
            color: Colors.Purple,
            title: '📈 افزایش ناگهانی بازیکنان',
            description: `سرور **${server.name}** افزایش ناگهانی در تعداد بازیکنان داشته است\n` +
                `قبلی: ${data.previous} ← فعلی: ${data.current} بازیکن\n` +
                `این ممکن است نشان‌دهنده حمله ربات باشد`
        }
    };

    const alert = alerts[alertType];
    return new EmbedBuilder()
        .setColor(alert.color)
        .setTitle(alert.title)
        .setDescription(alert.description)
        .setThumbnail(server.favicon)
        .setTimestamp()
        .setFooter({ text: `/follow ${server.name} • IRMCTracker Alert System` });
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
                        previous: previousState?.lastPlayerCount, // Use previous state before update
                        current: server.players.online
                    };

                    const embed = getAlertEmbed(server, alertType, alertData);

                    const role = !SILENT_ALERTS.includes(alertType)
                        ? findFollowRole(alertChannel.guild, server.name)
                        : undefined;

                    await alertChannel.send({
                        content: role ? `${role}` : undefined,
                        embeds: [embed],
                        allowedMentions: { roles: role ? [role.id] : [] },
                    });
                }
            }
        } catch (error) {
            console.error('Error in alerts job:', error);
        }
    }
};

export default job;