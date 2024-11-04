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
        .setDescription('🦸 دریافت تصویری از کیپ شما')
        .addStringOption(option => 
            option.setName('name')
                .setDescription('نام اسکین شما')
                .setRequired(true)
        ),
    async execute(_, interaction) {
        if (!await checkChannelPermission(interaction, 'skin')) return;

        const userName: string = interaction.options.getString('name', true);
        
        await interaction.reply('دارم کیپت رو پیدا میکنم... 🤔');
        
        const uuid = await userNameToUUID(userName);

        if (!uuid) {
            return await interaction.editReply('☹️ فکر کنم اشتباه نوشتی اسم اسکین رو چون نمیتونم پیداش کنم');
        }

        const profile = await getMinecraftProfile(uuid);

        if (!profile?.textures.cape) {
            return await interaction.editReply('😔 این پلیر کیپ نداره!');
        }

        const capeOrigin = getCapeOrigin(profile.textures.cape.url);

        const embed = new EmbedBuilder()
            .setTitle(`🦸 Cape ${userName}`)
            .setDescription(`نوع: ${capeOrigin}`)
            .setImage('attachment://cape.png');
        
        await interaction.editReply({
            embeds: [embed],
            content: 'پیداش کردم 😍\n',
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