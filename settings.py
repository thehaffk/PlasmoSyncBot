config = {
    'token': 'ODQyMzAxODc3NDAwMjQwMTQw.YJzUwA.1hr1tXBNSG_QLpcGoFP0jUGAu20',
    'prefix': 'ps.',
    'db': 'servers.db',  # sudo chmod 777 не забудь
}
admins = [191836876980748298, 737501414141591594, 222718720127139840]

rp = {
    'id': 672312131760291842,  # 672312131760291842
    'player': 746628733452025866,  # 746628733452025866
    'fusion': 751722994170331136,  # 751722994170331136
    'helper': 751723033357451335,  # 751723033357451335
    'banker': 826367015014498314,
    'mko_head': 810492714235723777,
    'mko_helper': 826366703591620618,
    'mko_member': 844507728671277106,
}
smp = {
    'id': 385007717623922688,
    'player': 626887926373941258,
    'fusion': 626887902953209866,
    'helper': 626887908946739200
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
    'player': 'Игрок Plasmo',
    'fusion': 'Fusion',
    'helper': 'Интерпол',
    'banker': 'Банкир',
    'mko_head': 'Член Совета Глав МКО',
    'mko_helper': 'Помощник Совета Глав МКО',
    'mko_member': 'Участник Совета МКО',

    'connected': 'Подключено',
    'connection err': 'Помянем',
}
