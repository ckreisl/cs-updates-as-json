from __future__ import annotations

import json

import pytest

from src.utils.csgo import CSGODataUtils


@pytest.fixture
def data() -> dict:
    return json.loads(r'''[{
            "id": "1443641916898851208",
            "timestamp": "16 Mar, 2012",
            "link": "http://store.steampowered.com/news/7552/",
            "entry": "\r\n\t\tMaps:\u2022 Added St. Marc to Demolition mode.\u2022 Added and set quick match to cs_Italy\u2022 Added de_dust2_se. See blog for details.Gameplay:\u2022 New weapons: Famas, Galil AR, P250, Dual Berettas\u2022 Demolition mode update\u2022 Match now consists of two 10 round halves\u2022 Weapon progression updated: - CTs: m4a4, p90, ump45, deagle, nova, fiveseven, hkp2000, ssg08, awp, awp - Ts: ak47, p90, bison, deagle, nova, tec9, glock, ssg08, awp, awpUI\u2022 Added My Awards \u2013 Achievements & Stats\u2022 Updated alerts animation\u2022 Games with a half-time now display that it\u2019s the last round before halftime\u2022 Fixed final round not being called out in games with two halves\u2022 Fixed player getting a weapon upgrade on the last round before half-time/teamswap\u2022 Fixed some bugs where involving bot takeover scenarios\u2022 Fixed death message icon order - not penetration icon show up before the headshot so it makes sense in chronological order\u2022 Fixed some bad defusing text when spectating\u2022 Fixed \"YOU ARE ON TEAM\" panels not fading out properly\u2022 Fixed same panels not toggling visibility properly when toggling the scoreboard\u2022 When a CT is defusing, his ID shows the defuse icon now\u2022 Fixed scoreboard not showing from team selection menu\u2022 Restored ability to see when you unlocked an achievement on PC\u2022 Along with the hint, weapons now click when you change modes\u2022 Fix to not display the cash award message in the following cases:\u2022 The round just prior to halftime has ended.\u2022 It is not currently halftime \u2022 It is not the last round of the match (including the clinch victory early situation)\u2022 Space bar now changes camera mode and navigation text has been updated accordingly\u2022 Update to Match Set Up screen\u2022 Fix for PC video settings defaulting to COUCH\u2022 Modified \"Playing on Team...\" panel.\u2022 Visual update to mini-scoreboardMaps\u2022 Dust   - Fix bug that allowed player to hop near wall and see into inaccessible area - replaced some nodraw brushes with textures to help fix these holes. - Fixed bug where player clip limits jumping  -removed player clip that was preventing them from jumping the full height.\u2022 Dust 2 - Fixed bug where player can toss bomb out of reach. - Fixed bug where clip preventing jumping.  - Fixed bug where player was able to see out of map. -added some simple tops to this geometry. - Fixed bug where player can hop near wall and see into inaccessible area. - Fixed bug where clip limits jumping. \u2022 Lake  - Tree models were optimized - Fixed bug where player gets stuck on the physics prop model of lumber, changed this to static props - Increased the fade distance at which some of the bushes fade - Nav fixes - Fixed being able to get stuck between rock & shed.  - Adjusted start position of the upstairs doors into the bedroom and bathroom so there is better flow into those spaces. - Adjusted some tree cards in the skybox, and perimeter. - Pulled out a couple unneeded tree models in the 3dskybox to help with perf. - Draw distance for the floaties in the water seems too near. \u2022 Train  - Adjusted fog per community feedback. - Inferno - Tightened up collision volumes for Inferno Objects bomb crate, bomb crate stack, and bomb tanksAudio\u2022 Disabled unused sound entries.  Adding back in two sets of bullet surface impacts.\u2022 Added semi-auto to auto switch sound \u2022 Ambient sound adjustments for dust, dust2, and Italy \u2022 Sound effects tuning \u2022 Pulled down volume of ammo pickup that's played at round start. \u2022 Pulled bell attenuation back to normal levels, only hear in and around terrorist spawn, no longer level wide.\u2022 Increased life on helicopter from 15 to 25 seconds, for chopper fade out.\u2022 UI timer click down to .35 volumeEffects\u2022 Grenade visibility - added self illum to colored stripe on thrown flashbang.\u2022 Tune effect for the C4's flashing indicator light.Animations\u2022 Removed forearm slap, times and remixed clip out wave\u2022 Tune Terrorist run - Work on the arms and weapon. \u2022 Fix crouch fire leg wiggle in Terrorist aim\u2022 Fix for crouchwalk finger popping, found that stand had a sliding finger, now stabilized in Terrorist aimOther Bug Fixes\u2022 Fix for spawning inside another player after halftime. \u2022 Fixing CSM entity related bug that could cause CSM shadows to be disabled when toggling between fullscreen and windowed when connected to a dedicated server. \u2022 Fixing red console errors with props that were set to use VPhysics, but have no collision hull. \u2022 Fixed bug where the main menu could be clicked through the custom game menu (resulting in both being drawn)\u2022 Cleaned up warnings in single player screen\t\t\n",
            "tags": "maps,gameplay,ui,d2,lake,train,audio,effects,animations,bug fixes",
            "chars": 3674
        },
        {
            "id": "1f253bd200cf59a21c520babad746c696dde7e827517ce5dfc7ae62971835769",
            "timestamp": "13 Jan, 2020",
            "link": "https://blog.counter-strike.net/index.php/2020/01/28044/",
            "entry": "\nRelease Notes for 1/13/2020\n2020.01.13   - \n[ MISC ]\n\u2013 Fixed Operation Shattered Web sometimes not appearing on main menu player profiles.\n\u2013 Added an experimental search bar allowing users to find and purchase any specific coupon item in game.\n\u2013 Guardian encouragement voice radio lines will no longer play when there are enemies still alive.\n\u2013 Fixed a regression with Storage Units in Perfect World version of the game.\n\u2013 Fixed a UI bug when activating some Bonus Rank XP items.\n[ MAPS ]\n\u2013 Studio has been updated with the latest changes from Steam Workshop:\n\u2014 Middle has had a complete re-design.\n\u2014 CT / T streets have been reduced in size.\n\u2014 CT Spawn have been reduced in size.\n\u2014 B Upper have been reduced in size.\n\u2014 T Spawn alley has been removed.\n\u2014 B connectors to middle have been updated.\n\u2014 3D Skybox has been updated.\n\u2014 T spawn geometry has received minor update.\n\u2014 B Site catwalk has been widened and updated for smoother gameplay when dropping into site.\n\u2014 B site cover has been changed to give player better colour callouts.\n\u2014 Updated soundscapes.\n\u2014 Removed the ability to throw weapons into unintended areas / out of map.\n\u2014 Fixed many community bug reports.\n\u2014 Improved clipping across the map.\n\nTweet\n \u00a0 \n\t\t\t\t\t\t\t\t\t\t\n\n",
            "tags": "misc,maps",
            "chars": 971
        }]'''.encode())


def test_csgo_updates_per_year(data):
    csgo_histogram = CSGODataUtils.updates_per_year(data)
    assert csgo_histogram['2012'] == 1
    assert csgo_histogram['2013'] == 0
    assert csgo_histogram['2020'] == 1

    with pytest.raises(KeyError):
        csgo_histogram['2011']


def test_csgo_updates_per_month_of_year(data):
    csgo_data = CSGODataUtils.updates_per_month_of_year(data, 2012)
    assert len(csgo_data) == 12
    assert csgo_data['Mar'] == 1
    assert csgo_data['Jan'] == 0


def test_csgo_updates_tags_histogram(data):
    csgo_data = CSGODataUtils.tags_histogram(data)
    assert len(csgo_data) == 11
    assert csgo_data['maps'] == 2
    assert csgo_data['bug fixes'] == 1

    with pytest.raises(KeyError):
        csgo_data['bug']

    csgo_data = CSGODataUtils.tags_histogram({})
    assert len(csgo_data) == 0
