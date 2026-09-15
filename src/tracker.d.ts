import { Client, SlashCommandBuilder, ChatInputCommandInteraction, AutocompleteInteraction } from 'discord.js';

declare global {
    interface TrackerJob {
        cronTime: string,
        execute: (client: Client) => any,
    }

    interface TrackerCommand {
        data: SlashCommandBuilder|Omit<SlashCommandBuilder>;
        execute: (client: Client, interaction: ChatInputCommandInteraction) => any,
        autocomplete?: (interaction: AutocompleteInteraction) => any,
    }

    interface TrackerEvent<Event extends keyof ClientEvents> {
        type: Event;
        execute: (...args: ClientEvents[Event]) => Awaitable<void>,
    }
}
