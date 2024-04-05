import { Client, Collection, GatewayIntentBits } from 'discord.js';
import { token } from './config.json';
import { getCommands, getEvents } from './services/botService';


class TrackerClient extends Client {
    commands: Collection<any, any>;

    constructor(options?: any) {
        super(options);
        this.commands = new Collection();
    }
}

const client: TrackerClient = new TrackerClient({ intents: [GatewayIntentBits.Guilds] });

// Register commands
client.commands = getCommands();

// Register events
getEvents().forEach((event: TrackerEvent<any>) => client.on(event.type, (...args) => event.execute(client, ...args)))

// Register jobs
// TODO

// Log in to Discord with your client's token
client.login(token);
