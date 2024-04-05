import fs from 'fs';
import path from 'path';

import { Collection } from "discord.js";

export function getCommands(): Collection<String, TrackerCommand> {
    const commands = new Collection<String, TrackerCommand>();

    const foldersPath = path.join(__dirname, '../commands');
    const commandFolders = fs.readdirSync(foldersPath);

    for (const folder of commandFolders) {
        const commandsPath = path.join(foldersPath, folder);
        const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.ts'));
        for (const file of commandFiles) {
            const filePath = path.join(commandsPath, file);
            const command: TrackerCommand = require(filePath).default;
            
            // Set a new item in the Collection with the key as the command name and the value as the exported module
            if ('data' in command && 'execute' in command) {
                commands.set(command.data.name, command);
            }
            else {
                console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
            }
        }
    }

    return commands;
}


export function getEvents(): TrackerEvent<any>[] {
    const events: TrackerEvent<any>[] = [];

    const foldersPath = path.join(__dirname, '../events');
    const eventFolders = fs.readdirSync(foldersPath);

    for (const folder of eventFolders) {
        const eventsPath = path.join(foldersPath, folder);
        const eventFiles = fs.readdirSync(eventsPath).filter(file => file.endsWith('.ts'));
        for (const file of eventFiles) {
            const filePath = path.join(eventsPath, file);
            const event: TrackerEvent<any> = require(filePath).default;
            
            if ('type' in event && 'execute' in event) {
                events.push(event)
            }
            else {
                console.log(`[WARNING] The command at ${filePath} is missing a required "type" or "execute" property.`);
            }
        }
    }

    return events;
}
