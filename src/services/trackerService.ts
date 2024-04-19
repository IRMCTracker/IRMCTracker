import axios, { AxiosError, AxiosResponse } from 'axios';
import { trackerUrl, trackerApiKey } from '../config.json';

export interface Server {
    name: string;
    description: string;
    favicon: string | null;
    motd: string | null;
    address: string;
    ip: string | null;
    country_code: string | null;
    region: string | null;
    up_from: number;
    uptime: string;
    latency: number | null;
    version: string | null;
    votes: number;
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

export interface StatsResponse {
    counts: {
        servers: number;
        records: number;
        players: number;
        empty: number;
        votes: number;
    };
}

export async function getStats(): Promise<StatsResponse> {
    try {
        // Make the GET request using Axios
        const response: AxiosResponse<{data: StatsResponse}> = await axios.get(`${trackerUrl}/api/stats`);

        // Return the response data
        return response.data.data;
    } catch (error) {
        // Handle any errors
        console.error('Error fetching stats:', error);
        throw error;
    }
}

export async function getServers(): Promise<Server[] | null> {
    try {
        const response: AxiosResponse<{ data: Server[] }> = await axios.get(`${trackerUrl}/api/servers`);
        const serverData: Server[] = response.data.data;

        return serverData;
    } catch (error: any) {
        console.warn('Error fetching servers data:', error.message);
        return null;
    }
}


export async function getServer(name: String): Promise<Server | null> {
    try {
        const response: AxiosResponse<{ data: Server }> = await axios.get(`${trackerUrl}/api/servers/${name}`);
        const serverData: Server = response.data.data;

        return serverData;
    } catch (error: any) {
        console.warn('Error fetching server data:', error.message);
        return null;
    }
}

export async function ask(question: String): Promise<string | null> {
    try {
        const response: AxiosResponse<{ answer: string }> = await axios.post(`${trackerUrl}/api/ask`, {question: question}, {headers: {'x-api-key': trackerApiKey}});
        const answer: string = response.data.answer;

        return answer;
    } catch (error: any) {
        console.warn('Error asking ai:', error.message);
        return null;
    }
}
