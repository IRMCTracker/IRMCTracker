import { EmbedBuilder, InteractionContextType, SlashCommandBuilder } from 'discord.js';
import { channels, ownerId } from '../../config.json';
import {
  StaffRole, StaffServer, addStaff, applyStaffState, getStaffServer, removeStaff, staffErrorCode,
} from '../../services/staffService';

const ROLE_LABELS: Record<StaffRole, string> = {
  owner: 'اونر',
  admin: 'ادمین',
  developer: 'دولوپر',
};

const ERRORS: Record<string, string> = {
  no_active_server: 'شما اونر هیچ سرور فعالی توی ترکر نیستید، پس استفی برای مدیریت ندارید.',
  staff_limit: 'هر سرور حداکثر ۶ استف (ادمین یا دولوپر) میتونه داشته باشه. لطفا اول یکی رو حذف کنید.',
  cannot_change_owner: 'نقش اونر ها رو نمیشه تغییر داد. لطفا با تیم ترکر در ارتباط باشید.',
  cannot_remove_owner: 'اونر ها رو نمیشه حذف کرد. لطفا با تیم ترکر در ارتباط باشید.',
  not_staff: 'این کاربر جزو استف های این سرور نیست.',
};

const command: TrackerCommand = {
  data: new SlashCommandBuilder()
    .setName('staff')
    .setDescription('👥 مدیریت استف های سرور شما')
    .addSubcommand(sub => sub
      .setName('add')
      .setDescription('➕ اضافه کردن یا تغییر نقش یک استف')
      .addUserOption(option => option.setName('user').setDescription('کاربر').setRequired(true))
      .addStringOption(option => option.setName('role').setDescription('نقش').setRequired(true).addChoices(
        { name: ROLE_LABELS.admin, value: 'admin' },
        { name: ROLE_LABELS.developer, value: 'developer' },
      )))
    .addSubcommand(sub => sub
      .setName('remove')
      .setDescription('➖ حذف یک استف')
      .addUserOption(option => option.setName('user').setDescription('کاربر').setRequired(true)))
    .addSubcommand(sub => sub
      .setName('list')
      .setDescription('📋 لیست استف های سرور'))
    .setContexts(InteractionContextType.Guild) as SlashCommandBuilder,

  async execute(client, interaction) {
    if (channels.staff && interaction.channelId !== channels.staff) {
      return await interaction.reply({ content: '❌', ephemeral: true });
    }

    const subcommand = interaction.options.getSubcommand();
    const user = interaction.options.getUser('user');

    if (user && user.id === ownerId && interaction.user.id !== ownerId) {
      return await interaction.reply({ embeds: [errorEmbed('این کاربر رو نمیشه به استف ها اضافه یا ازشون حذف کرد.')], ephemeral: true });
    }

    if (user?.bot) {
      return await interaction.reply({ embeds: [errorEmbed('ربات ها نمیتونن استف باشن.')], ephemeral: true });
    }

    const isPublic = subcommand !== 'list';
    await interaction.deferReply({ ephemeral: !isPublic });

    try {
      if (!user) {
        return await interaction.editReply({ embeds: [listEmbed(await getStaffServer(interaction.user.id))] });
      }

      const server = subcommand === 'add'
        ? await addStaff(user.id, interaction.options.getString('role', true) as StaffRole, interaction.user.id)
        : await removeStaff(user.id, interaction.user.id);

      let rolesApplied = false;
      try {
        rolesApplied = await applyStaffState(client, server.sync);
      } catch (error) {
        console.error(`[staff] Immediate role sync failed for ${user.id}:`, error);
      }

      const rolesNote = !rolesApplied
        ? '\n\n⚠️ تغییرات ذخیره شد اما بدلیل اختلالات موجود ممکنه کمی اعمال تغییرات زمان ببره.'
        : subcommand === 'add' && !server.top
          ? '\n\nℹ️ رول های استف فقط وقتی داده میشه که سرور جزو ۵۰ سرور برتر ترکر باشه.'
          : '';

      const description = subcommand === 'add'
        ? `${user} به عنوان **${ROLE_LABELS[server.staff.find(row => row.discord_id === user.id)!.role]}** سرور **${server.name}** ثبت شد.`
        : `${user} از استف های سرور **${server.name}** حذف شد.`;

      return await interaction.editReply({
        embeds: [new EmbedBuilder().setColor('Green').setTitle('✅ انجام شد').setDescription(description + rolesNote)],
      });
    } catch (error) {
      const code = staffErrorCode(error);

      if (!code || !ERRORS[code]) {
        console.error(`[staff] /staff ${subcommand} failed:`, error);
      }

      const embeds = [errorEmbed(ERRORS[code ?? ''] ?? 'انگار یک مشکلی وجود داره. لطفا کمی بعد دوباره امتحان کنید 🥲')];

      if (!isPublic) return await interaction.editReply({ embeds });

      // A deferred public reply can't become ephemeral, so replace it with a private follow-up.
      await interaction.deleteReply().catch(() => null);
      return await interaction.followUp({ embeds, ephemeral: true });
    }
  },
};

function listEmbed(server: StaffServer): EmbedBuilder {
  const lines = (['owner', 'admin', 'developer'] as StaffRole[]).map(role => {
    const people = server.staff.filter(row => row.role === role).map(row => `<@${row.discord_id}>`);
    return `**${ROLE_LABELS[role]}:** ${people.length ? people.join(' ') : '-'}`;
  });

  const staffCount = server.staff.filter(row => row.role !== 'owner').length;

  return new EmbedBuilder()
    .setColor('Blue')
    .setTitle(`👥 استف های ${server.name}`)
    .setDescription(lines.join('\n') + `\n\nظرفیت: ${staffCount} از ۶` + (server.top ? '' : '\n\n⚠️ این سرور الان جزو ۵۰ سرور برتر نیست.'));
}

function errorEmbed(description: string): EmbedBuilder {
  return new EmbedBuilder().setColor('Red').setTitle('❌ خطا').setDescription(description);
}

export default command;
