import { Client, Collection, GatewayIntentBits } from 'discord.js';
import { token } from './config.json';
import { getCommands, getEvents, getJobs } from './services/botService';
import { CronJob } from 'cron';


class TrackerClient extends Client {
    commands: Collection<any, any>;

    constructor(options?: any) {
        super(options);
        this.commands = new Collection();
    }
}

const client: TrackerClient = new TrackerClient({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.MessageContent, GatewayIntentBits.GuildMessages] });

// Register commands
console.log('[-] Registering commands...');
client.commands = getCommands();
console.log('[+] Registering commands completed.');

// Register events
console.log('[-] Registering events...');
getEvents().forEach((event: TrackerEvent<any>) => client.on(event.type, (...args) => event.execute(client, ...args)))
console.log('[+] Registering events completed.');

// Log in to Discord with your client's token
client.login(token);
