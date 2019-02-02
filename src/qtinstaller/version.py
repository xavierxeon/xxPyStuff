#!/usr/bin/env python3

class Version:

    def __init__(self, settings, key, baseVersion):

        self._settings = settings
        self._key = key
        self._baseVersion = baseVersion
        self._current = 0

        if not 'versions' in settings.data:
            settings.data['versions'] = dict()
            settings.save()

        if not key in settings.data['versions']:
            settings.data['versions'][key] = baseVersion + '.' + str(self._current)
            settings.save()
        else:
            content = settings.data['versions'][key]
            if content.startswith(baseVersion):
                value = content.replace(baseVersion + '.', '')
                self._current = int(value)

    def update(self):

        self._current += 1
        value = self._baseVersion + '.' + str(self._current)

        self._settings.data['versions'][self._key] = value
        self._settings.save()

        return value
