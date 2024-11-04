import axios from 'axios';
import { Cache } from './cacheService';

axios.defaults.headers.common["Accept-Encoding"] = "gzip";

const uuidCache = new Cache<string>(300); // 5 minutes TTL
const profileCache = new Cache<MinecraftProfile>(300); // 5 minutes TTL

interface MinecraftProfile {
    username: string;
    history: Array<{
        username: string;
        changedAt?: string;
    }>;
    createdAt: string;
    uuid: string;
    isLegacy: boolean;
    isDemoAccount: boolean;
    profileUrl?: string;
    textures: {
        skin?: {
            url: string;
            slim: boolean;
            custom: boolean;
        };
        cape?: {
            url: string;
            type: string;
        };
    };
}

export async function userNameToUUID(userName: string): Promise<string | undefined> {
    const cachedUUID = uuidCache.get(userName.toLowerCase());
    if (cachedUUID) return cachedUUID;

    try {
        const response = await axios.get(`https://api.mojang.com/users/profiles/minecraft/${userName}`);
        const uuid = response.data.id;
        if (uuid) uuidCache.set(userName.toLowerCase(), uuid);
        return uuid;
    } catch (error: any) {
        console.warn('Error occurred during fetching UUID: ' + error.message);
        return undefined;
    }
}

export async function getMinecraftProfile(uuid: string): Promise<MinecraftProfile | undefined> {
    const cachedProfile = profileCache.get(uuid);
    if (cachedProfile) return cachedProfile;

    try {
        const [ashconResponse, mojangResponse] = await Promise.all([
            axios.get(`https://api.ashcon.app/mojang/v2/user/${uuid}`),
            axios.get(`https://sessionserver.mojang.com/session/minecraft/profile/${uuid}`)
        ]);

        const ashconData = ashconResponse.data;
        const mojangData = mojangResponse.data;

        if (ashconData) {
            const profile = {
                username: ashconData.username,
                history: ashconData.username_history.map((history: any) => ({
                    username: history.username,
                    changedAt: history.changed_at
                })),
                createdAt: ashconData.created_at,
                uuid: ashconData.uuid,
                isLegacy: ashconData.legacy || false,
                isDemoAccount: ashconData.demo || false,
                profileUrl: `https://namemc.com/profile/${uuid}`,
                textures: {
                    skin: ashconData.textures?.skin ? {
                        url: ashconData.textures.skin.url,
                        slim: ashconData.textures.skin.slim || false,
                        custom: ashconData.textures.skin.custom || false
                    } : undefined,
                    cape: ashconData.textures?.cape ? {
                        url: ashconData.textures.cape.url,
                        type: ashconData.textures.cape.type
                    } : undefined
                }
            };
            profileCache.set(uuid, profile);
            return profile;
        }
    } catch (error: any) {
        console.warn('Error occurred during fetching profile: ' + error.message);
    }
    return undefined;
}
