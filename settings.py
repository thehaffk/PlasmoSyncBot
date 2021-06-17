config = {
    'token': 'ODQxMDI5NjExMzUzODAwNzA1.YJgz3A.NqTDgLNj0yRH0xlpe2Pnpr2LtOk',
    'prefix': 'ps.',
    'db': 'servers.db',  # sudo chmod 777 не забудь
}
admins = [191836876980748298, 737501414141591594, 222718720127139840]

rp = {
    'id': 672312131760291842,  # 672312131760291842
    'player': 746628733452025866,  # 746628733452025866
    'fusion': 751722994170331136,  # 751722994170331136
    'helper': 751723033357451335  # 751723033357451335
}
smp = {
    'id': 841024625102422016,
    'player': 841056589234700329,
    'fusion': 841056624915513385,
    'helper': 841056667503296512
}
texts = {
    # Общие приколы
    'activity': 'rp.plo.su',
    'settings color': 0x00ff00,
    'settings': 'Настройки PlasmoSync | ',
    'settingsOnJoin': 'Синхронизация при входе',
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

    'syncing': 'Синхронизация...',  # Текст в embed'e во время everyone_sync
    'everyone_sync done': 'Дело сделано :+1:',  # Текст в embed'e после выполнения everyone_sync

    # Приколы из setdonor
    'setdonor color': 0x00ff00,
    'setdonor title': 'Изменены настройки',  # см. скрин в ноушне
    'setdonor name': 'Подробнее:',  # см. скрин в ноушне
    'setdonor text': 'Сервер донор {guild} установлен',  # см. скрин в ноушне

    'ArgumentsError (setdonor)': 'Usage: RP/SMP',  # Долбаеб написал что-то в роде /setdonor 123

    # Приколы из onJoin
    'onJoin color': 0x00ff00,
    'onJoin title': 'Изменены настройки',
    'onJoin name': 'Подробнее:',
    'onJoin text true': 'Синхронизация при входе включена',
    'onJoin text false': 'Синхронизация при входе отключена',

    # Приколы из sync-nicknames
    'syncNick color': 0x00ff00,
    'syncNick title': 'Изменены настройки',
    'syncNick name': 'Подробнее:',
    'syncNick text true': 'Синхронизация ников включена',
    'syncNick text false': 'Синхронизация ников отключена',


    # Приколы из sync-roles
    'syncRoles color': 0x00ff00,
    'syncRoles title': 'Изменены настройки',
    'syncRoles name': 'Подробнее:',
    'syncRoles text true': 'Синхронизация ролей включена',
    'syncRoles text false': 'Синхронизация ролей отключена',

    # Приколы из help
    'help': 'Тебе только бог поможет',  # Сам хелп


    'wrongRolename': 'Usage: Player/Fusion/Helper',

    'setrole color': 0x00ff00,
    'setrole title': 'Настройки ролей обновлены',
    'setrole name': 'Подробнее:',
    'setrole text': 'Роль {role} установлена как {name}',

    'remrole color': 0x00ff00,
    'remrole title': 'Настройки ролей обновлены',
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
    'plasmoHelper': 'Хелпер',
    'connected': 'Подключено',
    'connection err': 'Помянем',
}
