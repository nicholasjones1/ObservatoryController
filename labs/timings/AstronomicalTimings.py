import ephem

sun = ephem.Sun()
astroTerip = ephem.Observer()
astroTerip.lat = '-37.02'
astroTerip.long = '145.12'

astroTerip.date = '2018/05/18 17:00'
risingDateTime = astroTerip.next_rising(ephem.Sun())
settingDateTime = astroTerip.next_setting(ephem.Sun())

print('The Sun sets today at %s' % ephem.localtime(settingDateTime))
astroTerip.horizon = '-12'
print('Naughtical twilight ends  at %s' % ephem.localtime(settingDateTime))


astroTerip.horizon = '-18'
astroTwilightlightEnds = astroTerip.next_setting(ephem.Sun(), use_center=True)
print('Astronomical twilight ends at %s' % ephem.localtime(astroTwilightlightEnds))



