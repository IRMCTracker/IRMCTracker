import axios from 'axios';
import { hypixelApiKey } from '../config.json';
import { Cache } from './cacheService';

const hypixelCache = new Cache<HypixelProfile>(60);

interface HypixelProfile {
    rank: string;
    level: number;
    karma: number;
    firstLogin: Date;
    lastLogin: Date;
    achievementPoints: number;
    stats: {
        bedwars?: {
            wins: number;
            losses: number;
            kills: number;
            deaths: number;
            finalKills: number;
            winstreak: number;
            level: number;
        };
        skywars?: {
            wins: number;
            losses: number;
            kills: number;
            deaths: number;
            level: number;
        };
        duels?: {
            wins: number;
            losses: number;
            kills: number;
            deaths: number;
        };
    };
    guildInfo?: {
        name: string;
        rank: string;
    };
    online: boolean;
}

export async function getHypixelProfile(uuid: string): Promise<HypixelProfile | undefined> {
    const cachedProfile = hypixelCache.get(uuid);
    if (cachedProfile) return cachedProfile;

    try {
        const [playerRes, statusRes] = await Promise.all([
            axios.get(`https://api.hypixel.net/player?uuid=${uuid}`, {
                headers: { 'API-Key': hypixelApiKey }
            }),
            axios.get(`https://api.hypixel.net/status?uuid=${uuid}`, {
                headers: { 'API-Key': hypixelApiKey }
            })
        ]);

        const player = playerRes.data.player;
        if (!player) return undefined;

        // Format stats
        const stats: HypixelProfile = {
            rank: getRank(player),
            level: getNetworkLevel(player.networkExp || 0),
            karma: player.karma || 0,
            firstLogin: new Date(player.firstLogin),
            lastLogin: new Date(player.lastLogin),
            achievementPoints: player.achievementPoints || 0,
            online: statusRes.data.session.online,
            stats: {
                bedwars: player.stats?.Bedwars ? {
                    wins: player.stats.Bedwars.wins_bedwars || 0,
                    losses: player.stats.Bedwars.losses_bedwars || 0,
                    kills: player.stats.Bedwars.kills_bedwars || 0,
                    deaths: player.stats.Bedwars.deaths_bedwars || 0,
                    finalKills: player.stats.Bedwars.final_kills_bedwars || 0,
                    winstreak: player.stats.Bedwars.winstreak || 0,
                    level: player.achievements?.bedwars_level || 0
                } : undefined,
                skywars: player.stats?.SkyWars ? {
                    wins: player.stats.SkyWars.wins || 0,
                    losses: player.stats.SkyWars.losses || 0,
                    kills: player.stats.SkyWars.kills || 0,
                    deaths: player.stats.SkyWars.deaths || 0,
                    level: getSkyWarsLevel(player.stats.SkyWars.skywars_experience || 0)
                } : undefined,
                duels: player.stats?.Duels ? {
                    wins: player.stats.Duels.wins || 0,
                    losses: player.stats.Duels.losses || 0,
                    kills: player.stats.Duels.kills || 0,
                    deaths: player.stats.Duels.deaths || 0
                } : undefined
            }
        };

        if (stats) {
            hypixelCache.set(uuid, stats);
        }
        return stats;
    } catch (error: any) {
        console.warn('Error fetching Hypixel data:', error.message);
        return undefined;
    }
}

function getRank(player: any): string {
    const ranks = [
        'ADMIN', 'GAME_MASTER', 'YT', 'STAFF', 'MOJANG', 'HELPER',
        'MVP_PLUS_PLUS', 'MVP_PLUS', 'MVP', 'VIP_PLUS', 'VIP'
    ];
    
    for (const rank of ranks) {
        if (player[`rank`] === rank || 
            player[`monthly_rank`] === rank || 
            player[`new_rank`] === rank ||
            player[`newPackageRank`] === rank) {
            return rank;
        }
    }
    return 'DEFAULT';
}

function getNetworkLevel(exp: number): number {
    return Number((Math.sqrt(2 * exp + 30625) / 50 - 2.5).toFixed(2));
}

function getSkyWarsLevel(exp: number): number {
    return Number(((exp - 15000) / 10000 + 12).toFixed(2));
}
