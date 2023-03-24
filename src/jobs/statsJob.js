
const Server = require('../models/Server');
const Record = require('../models/Record');
const Vote = require('../models/Vote');

const guild_id = require('../../config.json').guild_id;
const {
    members_count,
    servers_count,
    votes_count,
    tracks_count,
    total_count,
    empty_count,
} = require('../../config.json').channels;

/**
 * Updating stats channels
 */
module.exports = {
    interval: 30_000,
    async execute() {
        const membersCount = client.guilds.cache.get(guild_id).memberCount;
        const votesCount = await Vote.count();
        const serversCount = await Server.count();
        const recordsCount = await Record.count();
        const totalCount = await Server.totalPlayersCount();
        const emptyCount = await Server.emptyServersCount();

        const membersChannel = await getChannel(members_count);
        const votesChannel = await getChannel(votes_count);
        const serversChannel = await getChannel(servers_count);
        const tracksChannel = await getChannel(tracks_count);
        const emptyChannel = await getChannel(empty_count);
        const totalChannel = await getChannel(total_count);

        await membersChannel.setName(`👥・ Members「${membersCount}」`);
        await votesChannel.setName(`😄・Votes「${votesCount}👥」`);
        await serversChannel.setName(`💻・Servers「${serversCount}👥」`);
        await tracksChannel.setName(`🔗・Tracks「${recordsCount}👥」`);

        await totalChannel.setName(`💎・All「${totalCount}👥」`);
        await emptyChannel.setName(`📈・Empty「${emptyCount}🔨」`);
    }
}

async function getChannel(id) {
    return client.channels.cache.get(id) ?? await client.channels.fetch(id);
}
