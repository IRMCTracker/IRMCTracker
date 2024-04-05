export class Server {
    id: number
    name: string;
    favicon_url: string|null;
    banner_url: string|null;
    current_players: number;
    up_from: number;

    constructor(id: number, name: string, current_players: number, up_from: number, favicon_url: string|null, banner_url: string|null) {
        this.id = id;
        this.name = name;
        this.current_players = current_players;
        this.up_from = up_from;
        this.favicon_url = favicon_url;
        this.banner_url = banner_url;
    }
}

export async function getServers(): Promise<Server[]> {
    // TODO fetch from API
    return [new Server(1, 'foo', 10, 10, null, null)];
}


export async function getServer(name: String): Promise<Server|null> {
    // TODO fetch from API
    return new Server(1, 'foo', 10, 10, null, null);
}
