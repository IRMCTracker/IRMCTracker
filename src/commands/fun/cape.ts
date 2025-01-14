import { SlashCommandBuilder, EmbedBuilder } from 'discord.js';
import { userNameToUUID, getMinecraftProfile } from '../../services/playerService';
import { checkChannelPermission } from '../../services/messagingService';

const getCapeOrigin = (url: string): string => {
    if (url.includes('minecraft.net/')) {
        if (url.includes('migrator')) return 'Migration Cape';
        if (url.includes('birthday')) return 'Birthday Cape';
        if (url.includes('founder')) return 'Founder Cape';
        return 'Mojang Cape';
    }
    if (url.includes('optifine.net/')) return 'OptiFine Cape';
    if (url.includes('minecraftcapes.net/')) return 'MinecraftCapes';
    return 'Special Cape';
};

const command: TrackerCommand = {
    data: new SlashCommandBuilder()
        .setName('cape')
        .setDescription('🦸 Get an image of your cape')
        .addStringOption(option => 
            option.setName('name')
                .setDescription('Your skin name')
                .setRequired(true)
        ),
    async execute(_, interaction) {
        if (!await checkChannelPermission(interaction, 'skin')) return;

        const userName: string = interaction.options.getString('name', true);
        
        await interaction.reply('Finding your cape... 🤔');
        
        const uuid = await userNameToUUID(userName);

        if (!uuid) {
            return await interaction.editReply('☹️ I think you entered the wrong skin name because I can\'t find it.');
        }

        const profile = await getMinecraftProfile(uuid);

        if (!profile?.textures.cape) {
            return await interaction.editReply('😔 This player doesn\'t have a cape!');
        }

        const capeOrigin = getCapeOrigin(profile.textures.cape.url);

        const embed = new EmbedBuilder()
            .setTitle(`🦸 Cape ${userName}`)
            .setDescription(`Type: ${capeOrigin}`)
            .setImage('attachment://cape.png');
        
        await interaction.editReply({
            embeds: [embed],
            content: 'I found it 😍\n',
            files: [
                {
                    name: 'cape.png',
                    attachment: profile.textures.cape.url
                }
            ]
        });
    }
};

export default command;
