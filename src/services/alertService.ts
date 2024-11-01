import { Server } from './trackerService';

interface ServerState {
    name: string;
    up_from: number;
    lastCheck: number;
    lastRecord: number;
    lastPlayerCount: number;
    lastLatency: number | null;
    recentLatencies: number[]; // Store last 5 latency readings
    recentPlayerCounts: number[]; // Store last 5 player counts
}

type AlertType = 'went_online' | 'went_offline' | 'new_record' | 'high_latency' | 'player_spike';

class AlertStateManager {
    private static instance: AlertStateManager;
    private serverStates: Map<string, ServerState>;
    private readonly LATENCY_THRESHOLD = 500; // ms
    private readonly PLAYER_SPIKE_THRESHOLD = 50; // Minimum increase in players
    private readonly PLAYER_SPIKE_PERCENTAGE = 0.5; // 50% increase
    private readonly HISTORY_SIZE = 5;
    private readonly RECORD_MINIMUM_PLAYERS = 50; // Only record if above 100 players

    private constructor() {
        this.serverStates = new Map();
    }

    static getInstance(): AlertStateManager {
        if (!AlertStateManager.instance) {
            AlertStateManager.instance = new AlertStateManager();
        }
        return AlertStateManager.instance;
    }

    private detectPlayerSpike(current: number, history: number[]): boolean {
        if (history.length < 2) return false;
        
        const lastCount = history[history.length - 1];
        const increase = current - lastCount;
        
        // Only alert if:
        // 1. The absolute increase is at least PLAYER_SPIKE_THRESHOLD
        // 2. The percentage increase is at least PLAYER_SPIKE_PERCENTAGE
        // 3. The current count is different from the last count
        return increase >= this.PLAYER_SPIKE_THRESHOLD && 
               current !== lastCount &&
               current > lastCount * (1 + this.PLAYER_SPIKE_PERCENTAGE);
    }

    private detectHighLatency(current: number | null, history: number[]): boolean {
        if (!current || history.length < 3) return false;
        const average = history.reduce((a, b) => a + b, 0) / history.length;
        return current > this.LATENCY_THRESHOLD && current > average * 1.5;
    }

    private updateMetricHistory<T>(current: T, history: T[]): T[] {
        const newHistory = [...history, current];
        return newHistory.slice(-this.HISTORY_SIZE);
    }

    updateServerState(server: Server): AlertType[] {
        const alerts: AlertType[] = [];
        const now = Date.now();
        const currentState = this.serverStates.get(server.name);

        // Initialize new state if none exists
        if (!currentState) {
            this.serverStates.set(server.name, {
                name: server.name,
                up_from: server.up_from,
                lastCheck: now,
                lastRecord: server.players.record,
                lastPlayerCount: server.players.online,
                lastLatency: server.latency,
                recentLatencies: server.latency ? [server.latency] : [],
                recentPlayerCounts: [server.players.online]
            });
            return alerts;
        }

        // Status change checks
        if (currentState.up_from < 0 && server.up_from > 0) {
            alerts.push('went_online');
        } else if (currentState.up_from > 0 && server.up_from < 0) {
            alerts.push('went_offline');
        }

        // New record check - only if above minimum threshold
        if (server.players.record > currentState.lastRecord && 
            server.players.record >= this.RECORD_MINIMUM_PLAYERS) {
            alerts.push('new_record');
        }

        // Update and check latency
        if (server.latency) {
            const newLatencies = this.updateMetricHistory(server.latency, currentState.recentLatencies);
            if (this.detectHighLatency(server.latency, currentState.recentLatencies)) {
                alerts.push('high_latency');
            }
            currentState.recentLatencies = newLatencies;
        }

        // Update and check player count
        const newPlayerCounts = this.updateMetricHistory(server.players.online, currentState.recentPlayerCounts);
        if (this.detectPlayerSpike(server.players.online, currentState.recentPlayerCounts)) {
            alerts.push('player_spike');
        }
        currentState.recentPlayerCounts = newPlayerCounts;

        // Update state
        this.serverStates.set(server.name, {
            ...currentState,
            up_from: server.up_from,
            lastCheck: now,
            lastRecord: server.players.record,
            lastPlayerCount: server.players.online,
            lastLatency: server.latency
        });

        return alerts;
    }

    getServerState(serverName: string): ServerState | undefined {
        return this.serverStates.get(serverName);
    }
}

export type { AlertType, ServerState };
export default AlertStateManager;