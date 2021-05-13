import discord
from discord.ext import commands
from settings import config, rp, smp, texts, admins
import sqlite3

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def sync(ctx=None, member: discord.Member = None, do_not_reply=False):
    if member is None:  # sync без аргументов - вызывается на того, кто вызвал
        member = ctx.author
    if member.bot:
        return None
    db_result = cursor.execute(f''' SELECT * FROM servers WHERE guild_id = {member.guild.id}''').fetchall()

    if len(db_result) == 0:
        if not do_not_reply:
            ctx.send(texts['err'])
            await settings(ctx)
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
        if not do_not_reply:
            await ctx.send(texts['err'])
        return False
    if plasmo_guild is None:
        print(f'Ошибка подключения к серверу Plasmo -> {db_result[0][3]}')
        if not do_not_reply:
            await ctx.send(texts['err'])
        return None

    user_plasmo = plasmo_guild.get_member(member.id)  # Получаем пользователя на доноре Pepega
    if user_plasmo is None:  # Пользователя нет на доноре. Если есть роли плазмы - они снимаются Kappa
        if not do_not_reply:
            await ctx.send(texts["memberNotFound (sync | guild)"].format(guild=plasmo_guild))

        guild_roles = member.guild.get_member(member.id).roles

        if db_result[0][6] != 'NULL':  # Проверка проходки и её снятие
            player_role = member.guild.get_role(db_result[0][6])
            if player_role is not None and player_role in guild_roles:
                await member.remove_roles(player_role)

        if db_result[0][7] != 'NULL':  # Проверка фужона и его снятие
            fusion_role = member.guild.get_role(db_result[0][7])
            if fusion_role is not None and fusion_role in guild_roles:
                await member.remove_roles(fusion_role)

        if db_result[0][8] != 'NULL':  # Проверка хелпера и его снятие
            helper_role = member.guild.get_role(db_result[0][8])
            if helper_role is not None and helper_role in guild_roles:
                await member.remove_roles(helper_role)
        return False  # Пользователя нет на доноре - конец sync

    try:
        # Синхронизация ника
        if db_result[0][5] == 'True' \
                and user_plasmo.display_name is not None and member.display_name != user_plasmo.display_name:
            await member.edit(nick=user_plasmo.display_name)
    except Exception as e:
        if not do_not_reply:
            await ctx.send(texts["missingPermissions"])  # У бота нет прав на смену ника peepoSad
        print('Exception:', e)
        return None

    #  Синхронизация ролей
    if db_result[0][4] == 'True':
        user_plasmo_roles = user_plasmo.roles
        guild_roles = member.guild.get_member(member.id).roles

        if db_result[0][6] != 'NULL':
            player_role = member.guild.get_role(db_result[0][6])
            if player_role is not None:  # Проходка
                if plasmo_player in user_plasmo_roles:
                    await member.add_roles(player_role)
                elif player_role in guild_roles:
                    await member.remove_roles(player_role)

        if db_result[0][7] != 'NULL':
            fusion_role = member.guild.get_role(db_result[0][7])
            if fusion_role is not None:  # Роль фужона
                if plasmo_fusion in user_plasmo_roles:
                    await member.add_roles(fusion_role)
                elif fusion_role in guild_roles:
                    await member.remove_roles(fusion_role)

        if db_result[0][8] != 'NULL':
            helper_role = member.guild.get_role(db_result[0][8])
            if helper_role is not None:  # Роль хелпера
                if plasmo_helper in user_plasmo_roles:
                    await member.add_roles(helper_role)
                elif helper_role in guild_roles:
                    await member.remove_roles(helper_role)

        # Ну не работает и не работает, че бубнить то
    if not do_not_reply:
        await ctx.send(texts["done"].format(mention=ctx.author.mention))
    print(f'[Synced] to: {member.guild} -> {member} from {plasmo_guild}')  # Debug


@sync.error
async def sync_error(ctx, error):
    if ctx is not None:
        await log(f'sync_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'sync_error -> {error}')

    if isinstance(error, commands.MissingPermissions):
        pass
    elif isinstance(error, commands.CommandInvokeError):
        pass
    elif isinstance(error, commands.errors.MemberNotFound):
        if ctx is not None:
            await ctx.send(texts['MemberNotFound (sync | argument)'])


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def settings(ctx):
    print('Settings:', ctx.guild)
    result = cursor.execute(f'''SELECT * FROM servers WHERE guild_id = {ctx.guild.id}''').fetchall()
    if len(result) == 0 and ctx.guild != rp_guild and ctx.guild != smp_guild:
        await ctx.send(texts['databaseGuildNotFound'].format(guild=ctx.guild))
        await on_guild_join(ctx.guild)
        await ctx.send(texts['databaseFixed'])
        return None
    elif ctx.guild == rp_guild or ctx.guild == smp_guild:
        return None
    embedSettings = discord.Embed(title=(texts['settings'] + str(ctx.guild)), color=texts['settings color'])
    embedSettings.add_field(name=texts['settingsOnJoin'],
                            value=f"{texts['on'] if result[0][1] == 'True' else texts['off']}", inline=False)
    embedSettings.add_field(name=texts['settingsDonor'], value=f"Plasmo {result[0][3]}", inline=False)
    embedSettings.add_field(name=texts['settingsSyncNicknames'],
                            value=f"{texts['on'] if result[0][5] == 'True' else texts['off']}", inline=False)
    embedSettings.add_field(name=texts['settingsSyncRoles'],
                            value=f"{texts['on'] if result[0][4] == 'True' else texts['off']}", inline=False)
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
    if ctx is not None:
        await log(f'settings_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')

    if isinstance(error, commands.MissingPermissions):
        if ctx is not None:
            if ctx.author.id in admins:
                await settings(ctx)
    elif isinstance(error, commands.CommandInvokeError):
        pass


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def help(ctx):
    await ctx.send('Руководство пользования ботом -> http://gg.gg/PlasmoSync')


@help.error
async def help_error(ctx, error):
    if ctx is not None:
        await log(f'help_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')

    if isinstance(error, commands.MissingPermissions):
        if ctx is not None:
            if ctx.author.id in admins:
                await help(ctx)
    elif isinstance(error, commands.CommandInvokeError):
        if ctx is not None:
            if ctx.author.id in admins:
                await help(ctx)


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
@commands.cooldown(rate=1, per=config['everyone_sync cooldown'], type=commands.BucketType.guild)
async def everyone_sync(ctx, rcd: str = 'хуй', with_logs=True):
    if ctx is not None:
        if rcd.lower() == 'rcd' and ctx.author.id in admins:
            commands.Command.reset_cooldown(everyone_sync, ctx=ctx)
            await ctx.send('Кулдаун команды сброшен.')
            return None

    members = ctx.guild.members
    message = None
    if with_logs:
        embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0xffff00)
        embedCounter.add_field(name=texts['syncing'], value=f'{0}/{len(members)}')
        message = await ctx.send(embed=embedCounter)
    for counter in range(len(members)):
        if with_logs:
            embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0xffff00)
            embedCounter.add_field(name=texts['syncing'], value=f'{counter}/{len(members)}')
            await message.edit(embed=embedCounter)
        member = members[counter]
        if not member.bot:
            await sync(ctx, member=member, do_not_reply=True)
    if with_logs:
        embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0x00ff00)
        embedCounter.add_field(name=texts['everyone_sync done'], value=f'{len(members)}/{len(members)}')
        await message.edit(embed=embedCounter)


@everyone_sync.error
async def everyone_sync_error(ctx, error):
    if ctx is not None:
        await log(f'everyone_sync_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')

    if isinstance(error, commands.MissingPermissions):
        if ctx is not None:
            if ctx.author.id in admins:
                await everyone_sync(ctx)

    elif isinstance(error, commands.CommandOnCooldown):
        if ctx is not None:
            if ctx.author in admins:
                await everyone_sync(ctx)
                return None
        print(f'у {ctx.guild} кулдаун на everyone_sync, да и похуй')
        if ctx is not None:
            ctx.send(f'Пока что неьлзя выполнить эту команду. На сервере не прошел кулдаун.')
    elif isinstance(error, commands.CommandInvokeError):
        print(ctx.guild, error)
    else:
        print(ctx.guild, error)


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def setrole(ctx, rolename: str, role: discord.Role):
    embedSetrole = discord.Embed(title=texts['setrole title'], color=texts['setrole color'])
    if rolename.lower() == 'player' or rolename.lower() == 'игрок':
        cursor.execute(f'''UPDATE servers SET player_role = {role.id} WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name=texts['setrole name'],
                               value=texts['setrole text'].format(role=role.mention, name=texts["plasmoPlayer"]))

    elif rolename.lower() == 'fusion' or rolename.lower() == 'фужон':
        cursor.execute(f'''UPDATE servers SET fusion_role = {role.id} WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name=texts['setrole name'],
                               value=texts['setrole text'].format(role=role.mention, name=texts["plasmoFusion"]))

    elif rolename.lower() == 'helper' or rolename.lower() == 'хелпер':
        cursor.execute(f'''UPDATE servers SET helper_role = {role.id} WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name=texts['setrole name'],
                               value=texts['setrole text'].format(role=role.mention, name=texts["plasmoHelper"]))

    else:
        await ctx.send(texts['wrongRolename'])
        return False

    await ctx.send(embed=embedSetrole)


@setrole.error
async def setrole_error(ctx, error):
    if ctx is not None:
        await log(f'setrole_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')

    if isinstance(error, commands.MissingPermissions):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(texts['MissingRequiredArgument (roles)'])
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send(texts['roleNotFound'])
    elif isinstance(error, commands.CommandInvokeError):
        pass


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def remrole(ctx, rolename: str):
    embedSetrole = discord.Embed(title=texts['remrole title'], color=texts['remrole color'])
    if rolename.lower() == 'player' or rolename.lower() == 'игрок':
        cursor.execute(f'''UPDATE servers SET player_role = 'NULL' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name=texts['remrole name'],
                               value=texts['remrole text'].format(name=texts["plasmoPlayer"]))

    elif rolename.lower() == 'fusion' or rolename.lower() == 'фужон':
        cursor.execute(f'''UPDATE servers SET fusion_role = 'NULL' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name=texts['remrole name'],
                               value=texts['remrole text'].format(name=texts["plasmoFusion"]))

    elif rolename.lower() == 'helper' or rolename.lower() == 'хелпер':
        cursor.execute(f'''UPDATE servers SET helper_role = 'NULL' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetrole.add_field(name=texts['remrole name'],
                               value=texts['remrole text'].format(name=texts["plasmoHelper"]))

    else:
        await ctx.send(texts['wrongRolename'])
        return False

    await ctx.send(embed=embedSetrole)


@remrole.error
async def remrole_error(ctx, error):
    if ctx is not None:
        await log(f'remrole_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')

    if isinstance(error, commands.MissingPermissions):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(texts['MissingRequiredArgument (roles)'])
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send(texts['roleNotFound'])
    elif isinstance(error, commands.CommandInvokeError):
        pass


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def setdonor(ctx, donor: str):
    embedSetdonor = discord.Embed(title=texts['setdonor title'], color=texts['setdonor color'])
    if donor.lower() == 'rp' or donor.lower() == 'рп':
        cursor.execute(f'''UPDATE servers SET server = 'RP' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetdonor.add_field(name=texts['setdonor name'], value=texts['setdonor text'].format(guild='RP'))

    elif donor.lower() == 'smp' or donor.lower() == 'смп':
        cursor.execute(f'''UPDATE servers SET server = 'SMP' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedSetdonor.add_field(name=texts['setdonor name'], value=texts['setdonor text'].format(guild='SMP'))
    else:
        await ctx.send(texts['ArgumentsError (setdonor)'])
        return False

    await ctx.send(embed=embedSetdonor)


@setdonor.error
async def setdonor_error(ctx, error):
    if ctx is not None:
        await log(f'setdonor_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')

    if isinstance(error, commands.MissingPermissions):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(texts['MissingRequiredArgument (setdonor)'])
    elif isinstance(error, commands.CommandInvokeError):
        pass


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def onJoin(ctx, value: str):
    embedOnJoin = discord.Embed(title=texts['onJoin title'], color=texts['onJoin color'])
    if value.lower() == 'true':
        cursor.execute(f'''UPDATE servers SET on_join = 'True' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['onJoin name'], value=texts['onJoin text true'])

    elif value.lower() == 'false':
        cursor.execute(f'''UPDATE servers SET on_join = 'False' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['onJoin name'], value=texts['onJoin text false'])
    else:
        await ctx.send(texts['ArgumentsError (onJoin)'])
        return False

    await ctx.send(embed=embedOnJoin)


@onJoin.error
async def onJoin_error(ctx, error):
    if ctx is not None:
        await log(f'onJoin_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')

    if isinstance(error, commands.MissingPermissions):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(texts['MissingRequiredArgument (onJoin)'])
    elif isinstance(error, commands.CommandInvokeError):
        pass


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def syncNick(ctx, value: str):
    embedOnJoin = discord.Embed(title=texts['syncNick title'], color=texts['syncNick color'])
    if value.lower() == 'true':
        cursor.execute(f'''UPDATE servers SET sync_nick = 'True' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['syncNick name'], value=texts['syncNick text true'])

    elif value.lower() == 'false':
        cursor.execute(f'''UPDATE servers SET sync_nick = 'False' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['syncNick name'], value=texts['syncNick text false'])
    else:
        await ctx.send(texts['ArgumentsError (syncNick)'])
        return False

    await ctx.send(embed=embedOnJoin)


@syncNick.error
async def syncNick_error(ctx, error):
    if ctx is not None:
        await log(f'syncNick_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')
    if isinstance(error, commands.MissingPermissions):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(texts['MissingRequiredArgument (syncNick)'])
    elif isinstance(error, commands.CommandInvokeError):
        pass


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def syncRoles(ctx, value: str):
    embedOnJoin = discord.Embed(title=texts['syncRoles title'], color=texts['syncRoles color'])
    if value.lower() == 'true':
        cursor.execute(f'''UPDATE servers SET sync_roles = 'True' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['syncRoles name'], value=texts['syncRoles text true'])

    elif value.lower() == 'false':
        cursor.execute(f'''UPDATE servers SET sync_roles = 'False' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['syncRoles name'], value=texts['syncRoles text false'])
    else:
        await ctx.send(texts['ArgumentsError (syncRoles)'])
        return False

    await ctx.send(embed=embedOnJoin)


@syncRoles.error
async def syncRoles_error(ctx, error):
    if ctx is not None:
        await log(f'syncRoles_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')
    if isinstance(error, commands.MissingPermissions):
        pass
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(texts['MissingRequiredArgument (syncRoles)'])
    elif isinstance(error, commands.CommandInvokeError):
        pass


@bot.command()
@commands.has_permissions(manage_roles=True, manage_nicknames=True)
@commands.bot_has_permissions(manage_roles=True, manage_nicknames=True)
async def status(ctx):
    status_ = discord.Embed(title=texts['botStatus'], color=0x00ff00)
    status_.add_field(name=texts['guilds_installed'], value=f'{len(bot.guilds)}', inline=False)
    status_.add_field(name=texts['rp_status'],
                      value=f'{texts["connected"] if not rp_error else texts["connection err"]}',
                      inline=False)
    status_.add_field(name=texts['smp_status'],
                      value=f'{texts["connected"] if not smp_error else texts["connection err"]}',
                      inline=False)
    status_.add_field(name=texts['db_lines'],
                      value=str(len(cursor.execute('SELECT guild_id from servers').fetchall())), inline=False)

    await ctx.send(embed=status_)


@status.error
async def status_error(ctx, error):
    if ctx is not None:
        await log(f'status_error -> {error} by {ctx.author} in {ctx.guild}')
    else:
        await log(f'status_error -> {error}')
    if isinstance(error, commands.MissingPermissions):
        if ctx is not None:
            if ctx.author.id in admins:
                await status(ctx)
                return None

    elif isinstance(error, commands.CommandInvokeError):
        if ctx is not None:
            if ctx.author.id in admins:
                await status(ctx)


async def log(message):
    log_channel = bot.get_channel(842391326607540265)
    await log_channel.send(message)



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

    all_guilds = bot.guilds
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(texts['activity']))
    print(f'{smp_guild} - {texts["connected"] if not smp_error else texts["connection err"]} (as SMP)')
    print(f'{rp_guild} - {texts["connected"] if not rp_error else texts["connection err"]} (as RP)')
    print(f'Located at {len(all_guilds)} servers(including donors).')

    guilds_ids = cursor.execute('SELECT guild_id FROM servers').fetchall()
    for guild in all_guilds:
        if (guild.id,) not in guilds_ids and guild is not rp_guild and guild is not smp_guild:
            print(f'Fixed downtime join - ', end="")
            await on_guild_join(guild)


@bot.event
async def on_guild_join(guild):
    if guild == rp_guild or guild == smp_guild:
        print(f'Joined a PLASMO guild {guild.name}')
        return None
    result = cursor.execute(f'''SELECT everyone FROM servers WHERE guild_id = {guild.id}''').fetchall()
    if len(result) > 0:
        print(f'Joined an old guild {guild.name}')
    else:
        cursor.execute(f"""INSERT INTO servers VALUES ({guild.id}, 'True', 'False', 'RP', 'True', 'True', 'NULL', 
        'NULL', 'NULL')""")
        conn.commit()
        print(f'Joined a new guild {guild.name}')


@bot.event
async def on_member_update(before, after):
    if (before.guild != rp_guild and before.guild != smp_guild) or (before.roles == after.roles and
                                                                    before.display_name == after.display_name):
        return None

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
