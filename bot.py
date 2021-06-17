import discord
from discord.ext import commands
from settings import config, rp, smp, texts, admins
import sqlite3
from discord_slash import SlashCommand, SlashContext

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')

slash = SlashCommand(bot, sync_commands=True)


def is_admin():
    async def predicate(ctx):
        return ctx.author.id in admins

    return commands.check(predicate)


@bot.command(name='eval')
@is_admin()
async def _eval(ctx, *, code):
    resp = eval(code)
    await ctx.send(resp if bool(resp) else 'None')


@slash.slash(name='sync', description='Синхронизировать конкретного игрока', options=[
    {
        'name': 'user',
        'description': 'User to sync',
        'required': True,
        'type': 6  # string 3, user 6, int 4
    }
])
async def _sync(ctx: SlashContext, user: discord.Member = None):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
    if user.bot:
        return None
    await sync(ctx=ctx, member=user)


async def sync(ctx=None, member: discord.Member = None, do_not_reply=False):
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
        await log(f'Ошибка подключения к серверу Plasmo -> {db_result[0][3]}')
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
        await log(f'** {member.guild} ** {e}')
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


@slash.slash(name='settings', description='Выводит настройки Plasmo Sync в чат')
async def settings(ctx):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
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


@slash.slash(name='help', description='Выводит руководство пользования ботом')
async def help(ctx):
    if ctx.guild is not rp_guild and ctx.guild is not rp_guild:
        await ctx.send('Руководство пользования ботом -> http://gg.gg/PlasmoSync')


@slash.slash(name='everyone-sync', description='Синхронизировать весь сервер')
async def everyone_sync(ctx):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
    members = ctx.guild.members
    embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0xffff00)
    embedCounter.add_field(name=texts['syncing'], value=f'{0}/{len(members)}')
    message = await ctx.send(embed=embedCounter)
    for counter in range(len(members)):
        embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0xffff00)
        embedCounter.add_field(name=texts['syncing'], value=f'{counter}/{len(members)}')
        await message.edit(embed=embedCounter)
        member = members[counter]
        if not member.bot:
            await sync(ctx, member=member, do_not_reply=True)
    embedCounter = discord.Embed(title=(texts['everyone_sync'] + str(ctx.guild)), color=0x00ff00)
    embedCounter.add_field(name=texts['everyone_sync done'], value=f'{len(members)}/{len(members)}')
    await message.edit(embed=embedCounter)


@slash.slash(name='setrole', description='Настроить синхронизацию ролей',
             options=[
                 {
                     'name': 'rolename',
                     'description': 'Player / Fusion / Helper',
                     'required': True,
                     'type': 3  # string 3, user 6, int 4
                 },
                 {
                     'name': 'role',
                     'description': 'Роль',
                     'required': True,
                     'type': 8  # string 3, user 6, int 4
                 }
             ])
async def setrole(ctx, rolename, role):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
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


@slash.slash(name='resetrole', description='Сбросить настройку синхронизации для конкретной роли', options=[
    {
        'name': 'rolename',
        'description': 'Player / Fusion / Helper',
        'required': True,
        'type': 3  # string 3, user 6, int 4
    }
])
async def remrole(ctx, rolename):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
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


@slash.slash(name='setdonor', description='Установить локальный сервер-донор для синхронизации', options=[
    {
        'name': 'donor',
        'description': 'RP / SMP',
        'required': True,
        'type': 3  # string 3, user 6, int 4
    }
])
async def setdonor(ctx, donor: str):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
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


@slash.slash(name='on-join', description='Синхронизировать ли новых пользователей при входе', options=[
    {
        'name': 'value',
        'description': 'Синхронизировать ли новых пользователей при входе',
        'required': True,
        'type': 5  # string 3, user 6, int 4
    }
])
async def onJoin(ctx, value):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
    embedOnJoin = discord.Embed(title=texts['onJoin title'], color=texts['onJoin color'])
    if value:
        cursor.execute(f'''UPDATE servers SET on_join = 'True' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['onJoin name'], value=texts['onJoin text true'])
    else:
        cursor.execute(f'''UPDATE servers SET on_join = 'False' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['onJoin name'], value=texts['onJoin text false'])

    await ctx.send(embed=embedOnJoin)


@slash.slash(name='sync-nicknames', description='Синхронизировать ли ники пользователей', options=[
    {
        'name': 'value',
        'description': 'Синхронизировать ли ники пользователей',
        'required': True,
        'type': 5  # string 3, user 6, int 4
    }
])
async def syncNick(ctx, value):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
    embedOnJoin = discord.Embed(title=texts['syncNick title'], color=texts['syncNick color'])
    if value:
        cursor.execute(f'''UPDATE servers SET sync_nick = 'True' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['syncNick name'], value=texts['syncNick text true'])

    else:
        cursor.execute(f'''UPDATE servers SET sync_nick = 'False' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()
        embedOnJoin.add_field(name=texts['syncNick name'], value=texts['syncNick text false'])

    await ctx.send(embed=embedOnJoin)


@slash.slash(name='sync-roles', description='Синхронизировать ли роли пользователей', options=[
    {
        'name': 'value',
        'description': 'Синхронизировать ли роли пользователей',
        'required': True,
        'type': 5  # string 3, user 6, int 4
    }
])
async def syncRoles(ctx, value):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
    embedOnJoin = discord.Embed(title=texts['syncRoles title'], color=texts['syncRoles color'])
    if value:
        cursor.execute(f'''UPDATE servers SET sync_roles = 'True' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['syncRoles name'], value=texts['syncRoles text true'])

    else:
        cursor.execute(f'''UPDATE servers SET sync_roles = 'False' WHERE guild_id = {ctx.guild.id}''')
        conn.commit()

        embedOnJoin.add_field(name=texts['syncRoles name'], value=texts['syncRoles text false'])

    await ctx.send(embed=embedOnJoin)


@slash.slash(name='status', description='Выводит краткую сводку по состоянию Plasmo Sync')
async def status(ctx):
    if not ctx.author.guild_permissions.manage_nicknames or not ctx.author.guild_permissions.manage_roles:
        return False
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
    await log('Starting ** Plasmo Sync **')
    print(f'{smp_guild} - {texts["connected"] if not smp_error else texts["connection err"]} (as SMP)')
    await log(f'{smp_guild} - {texts["connected"] if not smp_error else texts["connection err"]} (as SMP)')
    print(f'{rp_guild} - {texts["connected"] if not rp_error else texts["connection err"]} (as RP)')
    await log(f'{rp_guild} - {texts["connected"] if not rp_error else texts["connection err"]} (as RP)')
    print(f'Located at {len(all_guilds)} servers(including donors).')
    await log(f'Located at **{len(all_guilds)}** servers.')

    guilds_ids = cursor.execute('SELECT guild_id FROM servers').fetchall()
    for guild in all_guilds:
        if (guild.id,) not in guilds_ids and guild is not rp_guild and guild is not smp_guild:
            print(f'Fixed (downtime join) - ', end="")
            await log(f'Fixed (downtime join) - {guild}')
            await on_guild_join(guild)
        await log(guild)


@bot.event
async def on_guild_join(guild):
    if guild == rp_guild or guild == smp_guild:
        print(f'Joined a PLASMO guild {guild.name}')
        await log(f'Joined a PLASMO guild {guild.name}')
        return None
    result = cursor.execute(f'''SELECT everyone FROM servers WHERE guild_id = {guild.id}''').fetchall()
    if len(result) > 0:
        print(f'Joined an old guild {guild.name}')
        await log(f'Joined an old guild {guild.name}')
    else:
        cursor.execute(f"""INSERT INTO servers VALUES ({guild.id}, 'True', 'False', 'RP', 'True', 'True', 'NULL', 
        'NULL', 'NULL')""")
        conn.commit()
        print(f'Joined a new guild {guild.name}')
        await log(f'Joined a new guild {guild.name}')


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
async def on_member_ban(guild, _user):
    if guild != rp_guild and guild != smp_guild:
        return None

    for guild in bot.guilds:
        if guild != rp_guild and guild != smp_guild:
            user = guild.get_member(_user.id)
            if user is not None:
                await sync(member=user, do_not_reply=True)

    await log(f'<@{_user}> get banned on {guild}')


@bot.event
async def on_member_join(member):
    if member.guild == rp_guild or member.guild == smp_guild:
        return None
    db_result = cursor.execute(f''' SELECT on_join FROM servers WHERE guild_id = {member.guild.id}''').fetchone()
    if db_result is None:
        return None
    elif db_result[0] == 'True':
        await sync(member, member=member, do_not_reply=True)
    return None


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        cmds = [f'{config["prefix"]}sync',
                f'{config["prefix"]}everyone_sync',
                f'{config["prefix"]}help',
                f'{config["prefix"]}onJoin',
                f'{config["prefix"]}status',
                f'{config["prefix"]}syncRoles',
                f'{config["prefix"]}syncNick',
                f'{config["prefix"]}settings',
                f'{config["prefix"]}remrole',
                f'{config["prefix"]}setrole',
                f'{config["prefix"]}setdonor']
        raw = ctx.message.content
        if raw.split()[0] in cmds and ctx.guild != rp_guild and ctx.guild != smp_guild:
            await ctx.send('** ⚠️ Недавно Plasmo Sync обновился до версии 2.0 и теперь использует слеш-команды, '
                           'которые '
                           'требуют определенного доступа к серверам. Если вы установили Plasmo Sync до 19 июня - '
                           'установите заново по ссылке: **'
                           'https://discord.com/oauth2/authorize?client_id=842301877400240140&permissions=402655232'
                           '&redirect_uri=https%3A%2F%2Fwww.notion.so%2FDiscord-9827cd8b10ee4c33920d9c973ad90a6a'
                           '&scope=bot%20applications.commands')


if __name__ == '__main__':
    bot.run(config['token'])
