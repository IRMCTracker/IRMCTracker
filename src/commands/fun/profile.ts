import { SlashCommandBuilder, EmbedBuilder, ChatInputCommandInteraction } from 'discord.js';
import { getMinecraftProfile, userNameToUUID } from '../../services/playerService';
import { checkChannelPermission, getProfileMessage } from '../../services/messagingService';
import { getHypixelProfile } from '../../services/hypixelService';

const command: TrackerCommand = {
    data: new SlashCommandBuilder()
        .setName('profile')
        .setDescription('🔥 دریافت اطلاعات حساب ماینکرفت شما')
        .addStringOption(option => option.setName('username').setDescription('یوزرنیم پلیر').setRequired(true)),

    async execute(_, interaction: ChatInputCommandInteraction) {
        if (!await checkChannelPermission(interaction, 'profile')) return;

        const userName: string = interaction.options.getString('username', true);
        await interaction.reply({
            content: `در حال جستجوی پروفایل ${userName}...`,
            embeds: [new EmbedBuilder()
                .setDescription('🔄 لطفا صبر کنید...')
                .setColor('#FFA500')]
        });

        const uuid = await userNameToUUID(userName);

        if (!uuid) {
            return await interaction.editReply({
                content: '',
                embeds: [new EmbedBuilder()
                    .setDescription('❌ پلیر مورد نظر پیدا نشد!')
                    .setColor('#FF0000')]
            });
        }

        // Fetch both profiles in parallel
        const [minecraftProfile, hypixelProfile] = await Promise.all([
            getMinecraftProfile(uuid),
            getHypixelProfile(uuid)
        ]);

        if (!minecraftProfile) {
            return await interaction.editReply({
                content: '',
                embeds: [new EmbedBuilder()
                    .setDescription('⚠️ خطا در دریافت اطلاعات پروفایل')
                    .setColor('#FF0000')]
            });
        }

        await interaction.editReply(getProfileMessage(uuid, minecraftProfile, hypixelProfile));
    },
};

export default command;
