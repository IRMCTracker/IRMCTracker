import axios from 'axios';
axios.defaults.headers.common["Accept-Encoding"] = "gzip";

interface MinecraftProfile {
    username: string;
    history: string[];
    createdAt: string;
}

export async function userNameToUUID(userName: string): Promise<string | undefined> {
    try {
        const response = await axios.get(`https://api.mojang.com/users/profiles/minecraft/${userName}`);
        return response.data.id;
    } catch (error: any) {
        console.warn('Error occurred during fetching UUID: ' + error.message);
        return undefined;
    }
}

export async function getMinecraftProfile(uuid: string): Promise<MinecraftProfile | undefined> {
    try {
        const response = await axios.get(`https://api.ashcon.app/mojang/v2/user/${uuid}`);
        const json = response.data;
        if (json) {
            return {
                username: json.username,
                history: json.username_history.map((history: any) => history.username),
                createdAt: json.created_at
            };
        }
    } catch (error: any) {
        console.warn('Error occurred during fetching profile: ' + error.message);
    }
    return undefined;
}
