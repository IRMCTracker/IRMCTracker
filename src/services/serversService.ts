import axios, { AxiosResponse } from 'axios';
import { trackerUrl } from '../config.json';

export interface Server {
    name: string;
    description: string;
    favicon: string;
    motd: string;
    address: string;
    ip: string | null;
    country_code: string | null;
    region: string | null;
    up_from: number;
    latency: number | null;
    version: string | null;
    players: {
        online: number;
        max: number;
        record: number;
    };
    socials: {
        discord: string;
        telegram: string;
        website: string;
        instagram: string;
    };
    gamemodes: {
        [key: string]: number;
    } | null;

}

export async function getServers(): Promise<Server[]|null> {
    try {
        const response: AxiosResponse<{ data: Server[] }> = await axios.get(`${trackerUrl}/api/servers`);
        const serverData: Server[] = response.data.data;
        
        return serverData;
    } catch (error) {
        console.error('Error fetching server data:', error);
        return null;
    }
}


export async function getServer(name: String): Promise<Server|null> {
    try {
        const response: AxiosResponse<{ data: Server }> = await axios.get(`${trackerUrl}/api/servers/${name}`);
        const serverData: Server = response.data.data;

        return serverData;
    } catch (error) {
        console.error('Error fetching server data:', error);
        return null;
    }
}

