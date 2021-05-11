import discord
from discord.ext import commands
from settings import config, rp, smp, texts
import sqlite3

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')


# Synchronization
@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def sync(ctx=None, member: discord.Member = None, do_not_reply=False):
    global user_plasmo
    if member is None:  # sync без аргументов - вызывается на того, кто вызвал
        member = ctx.author
    if member.bot:
        return None
    db_result = cursor.execute(f''' SELECT * FROM servers WHERE guild_id = {member.guild.id}''').fetchall()
    if len(db_result) == 0:
        if not do_not_reply:
            ctx.send(texts['err'])
        print(f'Сервера {member.guild} нет в {config["db"]}')
        return None
    if db_result[0][3] == 'RP':
        plasmo_guild = rp_guild
        plasmo_player = rp_player
        plasmo_fusion = rp_fusion
        plasmo_helper = rp_helper
    elif db_result[0][3] == 'SMP':
        plasmo_guild = smp_guild
        plasmo_player = smp_player
        plasmo_fusion = smp_fusion
        plasmo_helper = smp_helper
    else:
        await ctx.send(texts['err'])
        return False
    if plasmo_guild is None:
        print(f'Ошибка подключения к серверу Plasmo -> {db_result[0][3]}')
        if not do_not_reply:
            ctx.send(texts['err'])
        return None

    user_plasmo = plasmo_guild.get_member(member.id)
    if user_plasmo is None:  # Снимает роли плазмы если игрока нет на сервере-доноре
        if not do_not_reply:
            await ctx.send(f'{texts["memberNotFound"]}{plasmo_guild}')
        print(f'[FAILED]  to: {member.guild} -> {member} from {plasmo_guild}')
        try:
            guild_roles = member.guild.get_member(member.id).roles
            if db_result[0][6] != 'NULL':  # Проходка
                player_role = member.guild.get_role(db_result[0][6])
                if player_role in guild_roles:
                    await member.remove_roles(player_role)

            if db_result[0][7] != 'NULL':  # Роль фужона
                fusion_role = member.guild.get_role(db_result[0][7])
                if fusion_role in guild_roles:
                    await member.remove_roles(fusion_role)

            if db_result[0][8] != 'NULL':  # Роль хелпера
                helper_role = member.guild.get_role(db_result[0][8])
                if helper_role in guild_roles:
                    await member.remove_roles(helper_role)
        except Exception:
            return False
        return False

    try:
        # Синхронизация ника
        if bool(db_result[0][
                    5]) and user_plasmo.display_name is not None and member.display_name != user_plasmo.display_name:
            await member.edit(nick=user_plasmo.display_name)
    except Exception as e:
        if not do_not_reply:
            await ctx.send(texts["missingPermissions"])
        return e
    try:
        #  Синхронизация ролей
        if bool(db_result[0][4]):
            user_plasmo_roles = user_plasmo.roles
            guild_roles = member.guild.get_member(member.id).roles

            if db_result[0][6] != 'NULL':  # Проходка
                player_role = member.guild.get_role(db_result[0][6])
                if plasmo_player in user_plasmo_roles:
                    await member.add_roles(player_role)
                elif player_role in guild_roles:
                    await member.remove_roles(player_role)

            if db_result[0][7] != 'NULL':  # Роль фужона
                fusion_role = member.guild.get_role(db_result[0][7])
                if plasmo_fusion in user_plasmo_roles:
                    await member.add_roles(fusion_role)
                elif fusion_role in guild_roles:
                    await member.remove_roles(fusion_role)

            if db_result[0][8] != 'NULL':  # Роль хелпера
                helper_role = member.guild.get_role(db_result[0][8])
                if plasmo_helper in user_plasmo_roles:
                    await member.add_roles(helper_role)
                elif helper_role in guild_roles:
                    await member.remove_roles(helper_role)

    except Exception as e:
        print('Exception:', e)
        return None
        # Ну не работает и не работает, че бубнить то
    if not do_not_reply:
        await ctx.send(f'{ctx.author.mention}{texts["done"]}')
    print(f'[SUCCESS] to: {member.guild} -> {member} from {plasmo_guild}')  # Debug


@sync.error
async def sync_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        pass


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def settings(ctx):
    print('Settings:', ctx.guild)
    result = cursor.execute(f'''SELECT * FROM servers WHERE guild_id = {ctx.guild.id}''').fetchall()
    if len(result) == 0 and ctx.guild != rp_guild and ctx.guild != smp_guild:
        await ctx.send(f'{ctx.guild} отсутствует в базе данных, сейчас починим')
        await on_guild_join(ctx.guild)
        await ctx.send(f'Починил Pepega')
        return None
    elif ctx.guild == rp_guild or ctx.guild == smp_guild:
        return None
    embedSettings = discord.Embed(title=(texts['settings'] + str(ctx.guild)), color=0x00ff00)
    embedSettings.add_field(name=texts['settingsOnJoin'], value=f"{result[0][1]}", inline=False)
    # embedSettings.add_field(name=texts['settingsEveryone'], value=f"{result[0][2]}", inline=False)
    embedSettings.add_field(name=texts['settingsDonor'], value=f"Plasmo {result[0][3]}", inline=False)
    embedSettings.add_field(name=texts['settingsSyncRoles'], value=f"{result[0][4]}", inline=False)
    embedSettings.add_field(name=texts['settingsSyncNicknames'], value=f"{result[0][5]}", inline=False)
    if bool(result[0][4]):
        try:
            embedSettings.add_field(name=texts['settingsPlayerRole'],
                                    value=f"{ctx.guild.get_role(result[0][6]).mention}", inline=False)
        except Exception:
            embedSettings.add_field(name=texts['settingsPlayerRole'], value=f"Не задано", inline=False)
        try:
            embedSettings.add_field(name=texts['settingsFusionRole'],
                                    value=f"{ctx.guild.get_role(result[0][7]).mention}", inline=False)
        except Exception:
            embedSettings.add_field(name=texts['settingsFusionRole'], value=f"Не задано", inline=False)
        try:
            embedSettings.add_field(name=texts['settingsHelperRole'],
                                    value=f"{ctx.guild.get_role(result[0][8]).mention}", inline=False)
        except Exception:
            embedSettings.add_field(name=texts['settingsHelperRole'], value=f"Не задано", inline=False)
    await ctx.send(embed=embedSettings)


@settings.error
async def settings_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        pass


# TODO: Help - список всех комманд и помощь по установке
@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def help(ctx):
    await ctx.send('Тебе только бог поможет')


@help.error
async def help_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        pass


# Синхронизация всех пользователей на сервере разом - done
@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def everyone_sync(ctx):  # TODO НЕ ЗАБУДЬ СМЕНИТЬ НАЗВАНИЕ СУКА
    members = ctx.guild.members
    embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0xffff00)
    embedCounter.add_field(name=f'Синхронизация...', value=f'{0}/{len(members)}')
    message = await ctx.send(embed=embedCounter)
    for counter in range(len(members)):
        embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0xffff00)
        embedCounter.add_field(name='Синхронизация...', value=f'{counter}/{len(members)}')
        await message.edit(embed=embedCounter)
        member = members[counter]
        if not member.bot:
            await sync(ctx, member=member, do_not_reply=True)
    embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0x00ff00)
    embedCounter.add_field(name='Дело сделано :+1:', value=f'{len(members)}/{len(members)}')
    await message.edit(embed=embedCounter)


@everyone_sync.error
async def everyone_sync_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        pass
    else:
        print(ctx.author, ctx.guild, error)  # Debug


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def setrole(ctx, rolename: str, role: discord.Role):
    embedSetrole = discord.Embed(title='Роли обновлены', color=0x00ff00)
    if rolename.lower() == 'player' or rolename.lower() == 'игрок':
        cursor.execute(f'''UPDATE servers SET player_role = {role.id} WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name='Подробнее:', value=f'{role.mention} установлена как {texts["plasmoPlayer"]}')

    elif rolename.lower() == 'fusion' or rolename.lower() == 'фужон':
        cursor.execute(f'''UPDATE servers SET fusion_role = {role.id} WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name='Подробнее:', value=f' {role.mention} установлена как {texts["plasmoFusion"]}')

    elif rolename.lower() == 'helper' or rolename.lower() == 'хелпер':
        cursor.execute(f'''UPDATE servers SET fusion_role = {role.id} WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name='Подробнее:', value=f' {role.mention} установлена как {texts["plasmoHelper"]}')

    else:
        await ctx.send(texts['wrongRolename'])
        return False

    await ctx.send(embed=embedSetrole)


@setrole.error
async def setrole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(texts['MissingRequiredArgument'])
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send(texts['roleNotFound'])


# Events:

@bot.event
async def on_ready():
    global rp_guild, rp_fusion, rp_player, rp_helper, rp_error
    rp_guild = bot.get_guild(rp['id'])
    if rp_guild is None:
        rp_error = True
        rp_fusion = None
        rp_player = None
        rp_helper = None
    else:
        rp_error = False
        rp_fusion = rp_guild.get_role(rp['fusion'])
        rp_player = rp_guild.get_role(rp['player'])
        rp_helper = rp_guild.get_role(rp['helper'])

    global smp_guild, smp_fusion, smp_player, smp_helper, smp_error
    smp_guild = bot.get_guild(smp['id'])
    if smp_guild is None:
        smp_error = True
        smp_fusion = None
        smp_player = None
        smp_helper = None
    else:
        smp_error = False
        smp_fusion = smp_guild.get_role(smp['fusion'])
        smp_player = smp_guild.get_role(smp['player'])
        smp_helper = smp_guild.get_role(smp['helper'])

    global cursor, conn
    conn = sqlite3.connect(config['db'])
    cursor = conn.cursor()

    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(f'Plasmo | {config["prefix"]}help'))
    print(f'{smp_guild}  - {"connected" if not smp_error else "roflanPominki"} (as SMP) \
\n{rp_guild}  - {"connected" if not rp_error else "roflanPominki"} (as RP)')
    print(f'Located at {len(bot.guilds)} servers(including donors).')
    # Проверка гильдов на наличие в бд и вызов on_guild_join если нет.


@bot.event
async def on_guild_join(guild):
    if guild == rp_guild or guild == smp_guild:
        print(f'Joined a PLASMO guild {guild.name}')
        return None
    result = cursor.execute(f'''SELECT everyone FROM servers WHERE guild_id = {guild.id}''').fetchall()
    if len(result) > 0:
        print(f'Joined an old guild {guild.name}')
    else:
        cursor.execute(f"""INSERT INTO servers VALUES ({guild.id}, 'True', 'False', 'RP', 'False', 'True', 'NULL', 
        'NULL', 'NULL')""")
        conn.commit()
        print(f'Joined a new guild {guild.name}')



@bot.event
async def on_member_update(before, after):
    if (before.guild != rp_guild and before.guild != smp_guild) or (before.roles == after.roles and
                                                                    before.display_name == after.display_name):
        return None
    # print(before.display_name, '->', after.display_name)
    # print(before.roles, '->', after.roles)

    for guild in bot.guilds:
        if guild != rp_guild and guild != smp_guild:
            user = guild.get_member(before.id)
            if user is not None:
                await sync(member=user, do_not_reply=True)


@bot.event
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def on_member_join(member):
    if member.guild == rp_guild or member.guild == smp_guild:
        return None
    db_result = cursor.execute(f''' SELECT on_join FROM servers WHERE guild_id = {member.guild.id}''').fetchone()
    if db_result is None:
        return None
    elif db_result[0] == 'True':
        await sync(member, member=member, do_not_reply=True)
    return None


if __name__ == '__main__':
    bot.run(config['token'])
