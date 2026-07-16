import axios, { AxiosError, AxiosRequestConfig, AxiosResponse } from 'axios';
import axiosRetry from 'axios-retry';
import { trackerApiUrl, trackerApiKey } from '../config.json';

// Dedicated client for the tracker site. The bot<->site link is shaky, so each
// attempt is bounded by a short timeout and transient failures are retried.
const tracker = axios.create({
    baseURL: trackerApiUrl,
    timeout: 5000,
    headers: { 'Accept-Encoding': 'gzip' },
});

const TRACKER_RETRIES = 5;

axiosRetry(tracker, {
    retries: TRACKER_RETRIES,
    // Give every attempt a fresh timeout instead of sharing one clock.
    shouldResetTimeout: true,
    retryCondition: (error: AxiosError) => {
        // Timeout or no response at all -> the request likely never landed.
        if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') return true;
        if (axiosRetry.isNetworkError(error)) return true;
        const status = error.response?.status;
        return status !== undefined && (status >= 500 || status === 429);
    },
    retryDelay: (retryCount: number) => {
        const base = Math.min(1000 * Math.pow(2, retryCount - 1), 8000);
        return base + Math.random() * 300;
    },
    onRetry: (retryCount: number, error: AxiosError, requestConfig: AxiosRequestConfig) => {
        const target = `${requestConfig.method?.toUpperCase()} ${requestConfig.url}`;
        const cause = error.code ?? error.response?.status ?? error.message;
        console.warn(`[tracker] retry ${retryCount}/${TRACKER_RETRIES} for ${target} - ${cause}`);
    },
});

export interface Server {
    name: string;
    type: 'java' | 'bedrock';
    description: string;
    favicon: string | null;
    motd: string | null;
    motd_text: string | null;
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
        const response: AxiosResponse<{data: StatsResponse}> = await tracker.get('/api/stats');

        // Return the response data
        return response.data.data;
    } catch (error) {
        // Handle any errors (retries already exhausted at this point)
        console.error('Error fetching stats:', error);
        throw error;
    }
}

export async function getServers(type?: 'java' | 'bedrock'): Promise<Server[] | null> {
    try {
        const url = type ? `/api/servers?type=${type}` : '/api/servers';
        const response: AxiosResponse<{ data: Server[] }> = await tracker.get(url);
        const serverData: Server[] = response.data.data;

        return serverData;
    } catch (error: any) {
        console.error('Error fetching servers data:', error.message);
        return null;
    }
}


export class TrackerUnavailableError extends Error {
    constructor(message: string) {
        super(message);
        this.name = 'TrackerUnavailableError';
    }
}

export async function getServer(name: String): Promise<Server | null> {
    try {
        const response: AxiosResponse<{ data: Server }> = await tracker.get(`/api/servers/${name}`);
        const serverData: Server = response.data.data;

        return serverData;
    } catch (error: any) {
        if (error?.response?.status === 404) {
            return null;
        }

        console.error('Error fetching server data:', error.message);
        throw new TrackerUnavailableError(error.message);
    }
}

export async function ask(question: String): Promise<string | null> {
    try {
        // AI generation is slow and non-idempotent, so give it a longer timeout
        // but never retry - a lost response could bill a duplicate generation.
        const response: AxiosResponse<{ answer: string }> = await tracker.post(
            '/api/ask',
            { question: question },
            {
                headers: { 'x-api-key': trackerApiKey },
                timeout: 30000,
                'axios-retry': { retries: 0 },
            }
        );
        const answer: string = response.data.answer;

        return answer;
    } catch (error: any) {
        console.error('Error asking ai:', error.message);
        return null;
    }
}
