config = {
    'token': 'ODQxMDI5NjExMzUzODAwNzA1.YJgz3A.jfaWIR36s0Cmd9eMSPwMqSROFP4',
    'prefix': 'apehumlox.',
    'db': 'servers.db',  # sudo chmod 777 не забудь
    'everyone_sync cooldown': 6000  # кулдаун синхронизации всего сервера (в секундах)
}
admins = [191836876980748298, 737501414141591594, 222718720127139840]
# Могут юзать бота даже если нет пермишенсов, работает через жопу поэтому функции с аргументами не работают
rp = {
    'id': 672312131760291842,  # 672312131760291842
    'player': 746628733452025866,  # 746628733452025866
    'fusion': 751722994170331136,  # 751722994170331136
    'helper': 751723033357451335  # 751723033357451335
}
smp = {
    'id': 385007717623922688,
    'player': 626887926373941258,
    'fusion': 626887902953209866,
    'helper': 626887908946739200
}
texts = {
    # Общие приколы
    'activity': 'PlasmoSync v.0.9',
    # Приколы из settings
    'settings color': 0x00ff00,
    'settings': 'Настройки PlasmoSync | ',
    'settingsOnJoin': 'Синхронизация при входе',
    'хуй': 'wtf',  # не нужный прикол, хз зачем добавил но пусть будет Kappa
    'settingsDonor': 'Сервер-донор',
    'settingsSyncRoles': 'Синхронизировать роли',
    'settingsSyncNicknames': 'Синхронизировать ники',
    'settingsPlayerRole': 'Роль Plasmo Player',
    'settingsFusionRole': 'Роль Plasmo Fusion',
    'settingsHelperRole': 'Роль Plasmo Helper',

    'on': 'Включено',
    'off': 'Выключено',

    'databaseGuildNotFound': '{guild} отсутствует в базе данных, сейчас починим',
    'databaseFixed': 'Сервер добавлен в базу данных',
    # Приколы из sync
    'done': '{mention} дело сделано',
    'memberNotFound (sync | guild)': 'Пользователя нет на сервере {guild}',  # Не нашел юзера на плазмо
    'err': 'Пососи, я не могу подключиться к серверу донору',  # Нет подключения к Plasmo,
    'missingPermissions': 'У бота нет прав на это действие',  # нет прав у бота
    'everyone_sync': 'Синхронизация всех пользователей | ',  # заголовок embed'a
    'MemberNotFound (sync | argument)': 'ты еблан? пингани чела',  # Долбаеб написал что-то в роде ps.sync 123

    'syncing': 'Синхронизация...',  # Текст в embed'e во время everyone_sync
    'everyone_sync done': 'Дело сделано :+1:',  # Текст в embed'e после выполнения everyone_sync

    # Приколы из setdonor
    'setdonor color': 0x00ff00,
    'setdonor title': 'Изменены настройки',  # см. скрин в ноушне
    'setdonor name': 'Подробнее:',  # см. скрин в ноушне
    'setdonor text': 'Сервер донор {guild} установлен',  # см. скрин в ноушне

    'MissingRequiredArgument (setdonor)': 'Пример использования: `ps.setdonor RP`',
    'ArgumentsError (setdonor)': 'Usage: RP/SMP',  # Долбаеб написал что-то в роде ps.setdonor 123

    # Приколы из onJoin
    'onJoin color': 0x00ff00,
    'onJoin title': 'Изменены настройки',
    'onJoin name': 'Подробнее:',
    'onJoin text true': 'Синхронизация при входе включена',
    'onJoin text false': 'Синхронизация при входе отключена',

    'MissingRequiredArgument (onJoin)': 'Пример использования: `ps.onJoin True`',  # onJoin был c рофлан аргументом
    'ArgumentsError (onJoin)': 'Usage: True/False',  # Долбаеб написал что-то в роде ps.onJoin 123

    # Приколы из syncNick
    'syncNick color': 0x00ff00,
    'syncNick title': 'Изменены настройки',
    'syncNick name': 'Подробнее:',
    'syncNick text true': 'Синхронизация ников включена',
    'syncNick text false': 'Синхронизация ников отключена',

    'MissingRequiredArgument (syncNick)': 'Пример использования: `ps.syncNick True`',
    'ArgumentsError (syncNick)': 'Usage: True/False',  # Долбаеб написал что-то в роде ps.syncNick 123


    # Приколы из syncRoles
    'syncRoles color': 0x00ff00,
    'syncRoles title': 'Изменены настройки',
    'syncRoles name': 'Подробнее:',
    'syncRoles text true': 'Синхронизация ролей включена',
    'syncRoles text false': 'Синхронизация ролей отключена',

    'MissingRequiredArgument (syncRoles)': 'Пример использования: `ps.syncRoles True`',
    'ArgumentsError (syncRoles)': 'Usage: True/False',  # Долбаеб написал что-то в роде ps.syncRoles 123


    # Приколы из help
    'help': 'Тебе только бог поможет',  # Сам хелп


    # Приколы из setrole/remrole
    'MissingRequiredArgument (roles)': 'Argument Missing',
    'wrongRolename': 'Usage: Player/Fusion/Helper',
    'roleNotFound': 'Роль не найдена',

    'setrole color': 0x00ff00,
    'setrole title': 'Роли обновлены',
    'setrole name': 'Подробнее:',
    'setrole text': '{role} установлена как {name}',

    'remrole color': 0x00ff00,
    'remrole title': 'Роли обновлены',
    'remrole name': 'Подробнее:',
    'remrole text': 'Роль {name} сброшена',


    # Приколы из status
    'botStatus': 'Состояние бота',
    'guilds_installed': 'Сервера, на которых установлен PlasmoSync',
    'rp_status': 'Состояние донора RP',
    'smp_status': 'Состояние донора SMP',

    'db_lines': 'Серверов в базе данных',


    # Общие приколы
    'plasmoPlayer': 'Игрок Plasmo',
    'plasmoFusion': 'Fusion',
    'plasmoHelper': 'Интерпол',
    'connected': 'connected',
    'connection err': 'roflanPominki',
}
