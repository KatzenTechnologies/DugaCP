import SETTINGS
import GUNS
import NPC
import ITEMS
import katz
from os import *
import pygame
import copy
import random

#When creating guns, remember to create an item for the gun as well.

def init_dugacp_api(game_api):
    """Функция заглушка, нужна для возможности патчинга всего функционала игры"""
    global dugacp_api
    dugacp_api = game_api

def load_guns():
    #AK 47 - 0
    guns = {}
    guns.update({"ak47": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["ak_spritesheet"],
         'item': dugacp_api.paths["akitem"]
         },{
            'dmg' : 3,
            'spread' : 50,
            'hitchance': 80,
            'firerate': 0.08,
            'range': 10,
            'magsize': 30,
            'rlspeed': 1,
            'zoom': 6,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'AK-47'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7))})
    
    #Double Barrel Shotgun - 1
    guns.update({"shotgun": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["shotgun_spritesheet"],
         'item': dugacp_api.paths["shotgun"]
         },{
            'dmg' : 10,
            'spread' : 200,
            'hitchance': 65,
            'firerate': 0.3,
            'range': 7,
            'magsize': 2,
            'rlspeed': 1.4,
            'zoom': 8,
            'ammotype': 'shell',
            'guntype': 'primary',
            'name': 'DB Shotgun'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot4.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (34,10))})

    #Hand gun - 2
    guns.update({"pistol": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["pistol_spritesheet"],
         'item' : dugacp_api.paths["gun"]
         },{
             'dmg' : 2,
             'spread': 40,
             'hitchance': 90,
             'firerate': 0.25,
             'range': 8,
             'magsize': 10,
             'rlspeed': 0.8,
             'zoom': 2,
             'ammotype': 'bullet',
             'guntype': 'secondary',
             'name': 'Pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin2.ogg'))]
                }, (37,6))})

    #Knife - 3
    guns.update({"knife": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["knife_spritesheet"],
         'item' : dugacp_api.paths["knifeitem"]
         },{
             'dmg' : 2,
             'spread': 40, 
             'hitchance': 100,
             'firerate': 0.3,
             'range': 1.5,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Knife'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10))})

    #Brass Knuckles - 4
    guns.update({"brassknuckles": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["brass_spritesheet"],
         'item' : dugacp_api.paths["brassitem"]
         },{
             'dmg' : 1,
             'spread': 30, 
             'hitchance': 100,
             'firerate': 0.2,
             'range': 1.5,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Brass Knuckles'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10))})
    
   # Gauss - 5
    guns.update({"gauss": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["gauss_spritesheet"],
         'item': dugacp_api.paths["gaussitem"]
         },{
            'dmg' : 6,
            'spread' : 10,
            'hitchance': 85,
            'firerate': 0.5,
            'range': 15,
            'magsize': 8,
            'rlspeed': 1,
            'zoom': 8,
            'ammotype': 'ferromag',
            'guntype': 'primary',
            'name': 'Gauss rifle'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7))})

    #Shotgun pistol - 6
    guns.update({"shotgunpistol": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["sgp_spritesheet"],
         'item' : dugacp_api.paths["shotpistol"]
         },{
             'dmg' : 6,
             'spread': 100,
             'hitchance': 60,
             'firerate': 0.2,
             'range': 6,
             'magsize': 1,
             'rlspeed': 0.5,
             'zoom': 1,
             'ammotype': 'shell',
             'guntype': 'secondary',
             'name': 'SG Pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37,6))})
    
    # ------ SPECIAL WEAPONS ----------
    #Fast Brass Knuckles - 7
    guns.update({"lightbrassknuckles": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["brass_brass_spritesheet"],
         'item' : dugacp_api.paths["brassbrassitem"]
         },{
             'dmg' : 1,
             'spread': 30, 
             'hitchance': 100,
             'firerate': 0,
             'range': 2,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Light Knuckles'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10))})

    #Bloody Brass Knuckles - 8
    guns.update({"bloodybrassknuckles": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["blood_brass_spritesheet"],
         'item' : dugacp_api.paths["bloodbrassitem"]
         },{
             'dmg' : 20,
             'spread': 60, 
             'hitchance': 100,
             'firerate': 2,
             'range': 1,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Rampage Knuckles'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10))})
    
    #Sharp Knife - 9
    guns.update({"sharpknife": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["shiny_knife_spritesheet"],
         'item' : dugacp_api.paths["shinyknifeitem"]
         },{
             'dmg' : 3,
             'spread': 40, 
             'hitchance': 100,
             'firerate': 0.3,
             'range': 1.5,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Sharp Knife'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10))})

    #Fast Knife - 10
    guns.update({"lightknife": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["desert_knife_spritesheet"],
         'item' : dugacp_api.paths["desertknifeitem"]
         },{
             'dmg' : 2,
             'spread': 30, 
             'hitchance': 100,
             'firerate': 0.1,
             'range': 1.8,
             'magsize': 0,
             'rlspeed': 0,
             'zoom': 0,
             'ammotype': None,
             'guntype': 'melee',
             'name': 'Light Knife'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'knife_swing3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg'))]
                }, (37,10))})
    
    #Modded Double Barrel Shotgun - 11
    guns.update({"modifiedshotgun": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["modded_shotgun_spritesheet"],
         'item': dugacp_api.paths["moddedshotgun"]
         },{
            'dmg' : 15,
            'spread' : 220,
            'hitchance': 65,
            'firerate': 0.3,
            'range': 6,
            'magsize': 3.1415, #lol bad code.
            'rlspeed': 1.4,
            'zoom': 8,
            'ammotype': 'shell',
            'guntype': 'primary',
            'name': 'Modified Shotgun'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot4.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (34,10))})

    #Impossible Double Barrel Shotgun - 12
    guns.update({"tbshotgun": GUNS.Gun(
        {'spritesheet': path.join('graphics', 'weapon', 'shotgun_spritesheet.png'),
         'item': path.join('graphics', 'items', 'weirdshotgun.png')
         },{
            'dmg' : 8,
            'spread' : 200,
            'hitchance': 65,
            'firerate': 0.5,
            'range': 8,
            'magsize': 3,
            'rlspeed': 1.4,
            'zoom': 8,
            'ammotype': 'shell',
            'guntype': 'primary',
            'name': 'TB Shotgun'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_shot4.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (34,10))})

    #AK 74 - 13
    guns.update({"ak74": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["ak74_spritesheet"],
         'item': dugacp_api.paths["ak74item"]
         },{
            'dmg' : 4,
            'spread' : 30,
            'hitchance': 80,
            'firerate': 0.08,
            'range': 10,
            'magsize': 30,
            'rlspeed': 1,
            'zoom': 8,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'AK-74'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7))})

    #Extended mag AK - 14
    guns.update({"extmagak47": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["akext_spritesheet"],
         'item': dugacp_api.paths["akextitem"]
         },{
            'dmg' : 3,
            'spread' : 50,
            'hitchance': 80,
            'firerate': 0.08,
            'range': 10,
            'magsize': 40,
            'rlspeed': 1.2,
            'zoom': 6,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'Ext Mag AK-47'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7))})

    #Camo AK-47 - 15
    guns.update({"camoak47": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["camo_ak_spritesheet"],
         'item': dugacp_api.paths["camoakitem"]
         },{
            'dmg' : 3,
            'spread' : 50,
            'hitchance': 90,
            'firerate': 0.04,
            'range': 10,
            'magsize': 30,
            'rlspeed': 0.8,
            'zoom': 6,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'Camo AK-47'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7))})

    #Light AK-47 - 16
    guns.update({"lightak": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["lightak_spritesheet"],
         'item': dugacp_api.paths["lightakitem"]
         },{
            'dmg' : 3,
            'spread' : 60,
            'hitchance': 80,
            'firerate': 0.08,
            'range': 10,
            'magsize': 20,
            'rlspeed': 0.1,
            'zoom': 4,
            'ammotype': 'bullet',
            'guntype': 'primary',
            'name': 'Light AK-47'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot3.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot4.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_shot5.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7))})

    #Gauss Hand gun - 17
    guns.update({"anomalypistol": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["gauss_pistol_spritesheet"],
         'item' : dugacp_api.paths["gaussgun"]
         },{
             'dmg' : 9,
             'spread': 30,
             'hitchance': 98,
             'firerate': 0.25,
             'range': 12,
             'magsize': 10,
             'rlspeed': 0.8,
             'zoom': 8,
             'ammotype': 'ferromag',
             'guntype': 'secondary',
             'name': 'Anomaly Pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                }, (37,6))})

    #High power Hand gun - 18
    guns.update({"hppistol": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["hpgun_spritesheet"],
         'item' : dugacp_api.paths["hpgun"]
         },{
             'dmg' : 3,
             'spread': 40,
             'hitchance': 85,
             'firerate': 0.25,
             'range': 8,
             'magsize': 10,
             'rlspeed': 0.8,
             'zoom': 2,
             'ammotype': 'bullet',
             'guntype': 'secondary',
             'name': 'HP Pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'hpp_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'hpp_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'hpp_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin2.ogg'))]
                }, (37,6))})

    #Modded Gauss - 19
    guns.update({"moddedgauss": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["modded_gauss_spritesheet"],
         'item': dugacp_api.paths["moddedgaussitem"]
         },{
            'dmg' : 9,
            'spread' : 10,
            'hitchance': 85,
            'firerate': 0.5,
            'range': 15,
            'magsize': 12,
            'rlspeed': 1,
            'zoom': 9,
            'ammotype': 'ferromag',
            'guntype': 'primary',
            'name': 'Modded gauss'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7))})

    #bump Gauss - 20
    guns.update({"bumpgauss": GUNS.Gun(
        {'spritesheet': dugacp_api.paths["bump_gauss_spritesheet"],
         'item': dugacp_api.paths["bumpgaussitem"]
         },{
            'dmg' : 6,
            'spread' : 20,
            'hitchance': 70,
            'firerate': 0.15,
            'range': 15,
            'magsize': 8,
            'rlspeed': 1,
            'zoom': 7,
            'ammotype': 'ferromag',
            'guntype': 'primary',
            'name': 'Bump gauss'
            },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'gauss_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_click2.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'AK_magin2.ogg'))]
                },(35,7))})

    #Black Shotgun pistol - 21
    guns.update({"moddedsgp": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["black_sgp_spritesheet"],
         'item' : dugacp_api.paths["blackshotpistol"]
         },{
             'dmg' : 8,
             'spread': 100,
             'hitchance': 60,
             'firerate': 0.2,
             'range': 6,
             'magsize': 1,
             'rlspeed': 0.4,
             'zoom': 1,
             'ammotype': 'shell',
             'guntype': 'secondary',
             'name': 'Modded SGP'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37,6))})

    #TWO Shotgun pistol - 22
    guns.update({"wtfsgp": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["wtf_sgp_spritesheet"],
         'item' : dugacp_api.paths["wtfshotpistol"]
         },{
             'dmg' : 12,
             'spread': 150,
             'hitchance': 60,
             'firerate': 0.2,
             'range': 6,
             'magsize': 2,
             'rlspeed': 0.8,
             'zoom': 1,
             'ammotype': 'shell',
             'guntype': 'secondary',
             'name': 'What??'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'sgp_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'shotgun_magin2.ogg'))]
                }, (37,6))})

    #Auto Hand gun - 23
    guns.update({"autopistol": GUNS.Gun(
        {'spritesheet' : dugacp_api.paths["auto_pistol_spritesheet"],
         'item' : dugacp_api.paths["autogun"]
         },{
             'dmg' : 2,
             'spread': 40,
             'hitchance': 90,
             'firerate': 0.05,
             'range': 8,
             'magsize': 12,
             'rlspeed': 0.9,
             'zoom': 2,
             'ammotype': 'bullet',
             'guntype': 'secondary',
             'name': 'Auto pistol'
             },{
                'shot': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot2.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_shot3.ogg'))],
                'click': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'universal_click.ogg'))],
                'magout': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magout2.ogg'))],
                'magin': [pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin1.ogg')), pygame.mixer.Sound(path.join('sounds', 'weapons', 'pistol_magin2.ogg'))]
                }, (37,6))})

    guns = dugacp_api._ENTITIES_get_guns(guns)

    SETTINGS.gun_list += list(katz.inverse(guns))

def load_npc_types():
    SETTINGS.npc_types = [
        #soldier idle
        {
            'pos': [0,0],
            'face': 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(12,15),
            'speed': 40,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'hitscan',
            'atckrate': 1,
            'id': 0,
            'filepath' : ('graphics', 'npc', 'soldier_spritesheet.png'),
            'name' : 'idle soldier',
            'soundpack' : 'soldier',
            },
        
        #Soldier Patrolling
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(12,15),
            'speed': 40,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'hitscan',
            'atckrate': 1,
            'id': 1,
            'filepath' : ('graphics', 'npc', 'soldier_spritesheet.png'),
            'name' : 'patroul soldier',
            'soundpack' : 'soldier',
            },
            
        #Ninja idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.10,
            'dmg': 3,
            'health': 11,
            'speed': 60,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.8,
            'id': 2,
            'filepath' : ('graphics', 'npc', 'ninja_spritesheet.png'),
            'name' : 'idle ninja',
            'soundpack' : 'ninja',
            },

        #Ninja patrolling
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.10,
            'dmg': 3,
            'health': 12,
            'speed': 60,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'melee',
            'atckrate': 0.8,
            'id': 3,
            'filepath' : ('graphics', 'npc', 'ninja_spritesheet.png'),
            'name' : 'patroul ninja',
            'soundpack' : 'ninja',
            },

        #Zombie patroling hostile (no dmg?)
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 3.1415, #lol this is used to randomize dmg.
            'health': 6,
            'speed': 70,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'melee',
            'atckrate': 0.6,
            'id': 4,
            'filepath' : ('graphics', 'npc', 'zombie_spritesheet.png'),
            'name' : 'hostile zombie',
            'soundpack' : 'zombie hostile',
            },

        #Zombie idle shy 
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 0,
            'health': 6,
            'speed': 50,
            'mind': 'shy',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.6,
            'id': 5,
            'filepath' : ('graphics', 'npc', 'zombie_spritesheet.png'),
            'name' : 'shy zombie',
            'soundpack' : 'zombie shy',
            },

        #random NPC
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0,
            'dmg': 0,
            'health': 0,
            'speed': 0,
            'mind': None,
            'state': None,
            'atcktype': None,
            'atckrate': 0,
            'id': 6,
            'filepath' : ('graphics', 'npc', 'random_spritesheet.png'),
            'name' : 'random',
            'soundpack' : None,
            },

        #SPECIAL NPCS --------
        #Boss idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.10,
            'dmg': 5,
            'health': 40,
            'speed': 20,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'hitscan',
            'atckrate': 3,
            'id': 7,
            'filepath' : ('graphics', 'npc', 'red_soldier_spritesheet.png'),
            'name' : 'idle red',
            'soundpack' : 'red soldier',
            },
        
        #black soldier idle
        {
            'pos': [0,0],
            'face': 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(15,20),
            'speed': 30,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'hitscan',
            'atckrate': 0.5,
            'id': 8,
            'filepath' : ('graphics', 'npc', 'black_soldier_spritesheet.png'),
            'name' : 'black idle',
            'soundpack' : 'soldier',
            },
        

        #black soldier patroul
        {
            'pos': [0,0],
            'face': 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(15,20),
            'speed': 30,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'hitscan',
            'atckrate': 1.5,
            'id': 9,
            'filepath' : ('graphics', 'npc', 'black_soldier_spritesheet.png'),
            'name' : 'black patroul',
            'soundpack' : 'soldier',
            },

        #green ninja idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 3,
            'health': random.randint(8, 11),
            'speed': 100,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.5,
            'id': 10,
            'filepath' : ('graphics', 'npc', 'green_ninja_spritesheet.png'),
            'name' : 'idle green',
            'soundpack' : 'ninja',
            },

        #green ninja patrolling
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.12,
            'dmg': 2,
            'health': random.randint(8, 11),
            'speed': 100,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'melee',
            'atckrate': 0.5,
            'id': 11,
            'filepath' : ('graphics', 'npc', 'green_ninja_spritesheet.png'),
            'name' : 'idle green',
            'soundpack' : 'ninja',
            },

        #blue ninja idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.1,
            'dmg': 4,
            'health': 14,
            'speed': 35,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'melee',
            'atckrate': 1.1,
            'id': 12,
            'filepath' : ('graphics', 'npc', 'blue_ninja_spritesheet.png'),
            'name' : 'idle blue',
            'soundpack' : 'ninja',
            },

        #Zombie yellow patrolling
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 5, 
            'health': 20,
            'speed': 20,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'melee',
            'atckrate': 1,
            'id': 13,
            'filepath' : ('graphics', 'npc', 'sick_zombie_spritesheet.png'),
            'name' : 'patroul sick',
            'soundpack' : 'zombie hostile',
            },

        #zombie yellow idle
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 6,
            'health': 20,
            'speed': 20,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 0.8,
            'id': 14,
            'filepath' : ('graphics', 'npc', 'sick_zombie_spritesheet.png'),
            'name' : 'idle sick',
            'soundpack' : 'zombie hostile',
            },

        #zombie yellow idle shy
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 10,
            'health': 35,
            'speed': 20,
            'mind': 'hostile',
            'state': 'idle',
            'atcktype': 'melee',
            'atckrate': 1.2,
            'id': 15,
            'filepath' : ('graphics', 'npc', 'sick_zombie_spritesheet.png'),
            'name' : 'shy sick',
            'soundpack' : 'zombie hostile',
            },

        #blurry zombie hostile
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 8,
            'health': 5,
            'speed': 45,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'melee',
            'atckrate': 0.4,
            'id': 16,
            'filepath' : ('graphics', 'npc', 'blurry_zombie_spritesheet.png'),
            'name' : 'hostile blurry',
            'soundpack' : 'blurry zombie',
            },

        #blurry zombie hostile hitscan??
        {
            'pos' : [0,0],
            'face' : 0,
            'spf': 0.18,
            'dmg': 1,
            'health': 15,
            'speed': 45,
            'mind': 'hostile',
            'state': 'patrolling',
            'atcktype': 'hitscan',
            'atckrate': 0.4,
            'id': 17,
            'filepath' : ('graphics', 'npc', 'blurry_zombie_spritesheet.png'),
            'name' : 'hostile blurry',
            'soundpack' : 'blurry zombie',
            },
        ]

    load_npc_sounds()

def load_npc_sounds():
    SETTINGS.npc_soundpacks = [
        #Soldier soundpack
        {
            'name' : 'soldier',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_shoot.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_spot.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt3.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt4.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_die.ogg')),],
            },
        
        #boss soldier soundpack
        {
            'name' : 'red soldier',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_shoot_heavy.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_spot.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt3.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_hurt4.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'soldier_die.ogg')),],
            },
        
        #Ninja Soundpack
        {
            'name' : 'ninja',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_attack.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_hurt3.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_hurt4.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'ninja_die2.ogg'))],
            },

        #Zombie shy soundpack
        {
            'name' : 'zombie shy',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'other', 'none.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_spot2.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt3.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_die2.ogg'))],
            },

        #Zombie hostile soundpack
        {
            'name' : 'zombie hostile',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_attack.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_spot1.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_hurt3.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'zombie_die2.ogg'))],
            },

        #Zombie blurry soundpack
        {
            'name' : 'blurry zombie',
            'attack' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_attack.ogg')),
            'spot' : pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_spot.ogg')),
            'damage' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_hurt1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_hurt2.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_hurt3.ogg'))],
            'die' : [pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_die1.ogg')), pygame.mixer.Sound(path.join('sounds', 'npcs', 'blurry_zombie_die2.ogg'))],
            },
        ]


def spawn_npcs():
    seed = SETTINGS.current_level + SETTINGS.seed
    for npc in SETTINGS.levels_list[SETTINGS.current_level].npcs:
        if [x for x in SETTINGS.npc_types if x['id'] == npc[2]][0]['name'] == 'random':
            random.seed(seed)
            seed += 0.001
            stats = copy.deepcopy(random.choice([x for x in SETTINGS.npc_types if x['name'] != 'random']))
            print(stats['name'])
        else: 
            stats = copy.deepcopy([x for x in SETTINGS.npc_types if x['id'] == npc[2]][0])
            
        try:
            sounds = ([x for x in SETTINGS.npc_soundpacks if x['name'] == stats['soundpack']][0])
        except:
            print("Error loading NPC! No soundpack with name ", stats['soundpack'])
        stats['pos'] = npc[0]
        stats['face'] = npc[1]
        SETTINGS.npc_list.append(NPC.Npc(stats, sounds, path.join(*stats['filepath'])))


def load_item_types():
    print(SETTINGS.gun_list)
    SETTINGS.item_types = [
            #Health
            {
                'filepath' : ('graphics', 'items', 'firstaid.png'),
                'type' : 'health',
                'effect' : 10,
                'id' : 0,
                },
            #Armor
            {
                'filepath' : ('graphics', 'items', 'kevlar.png'),
                'type' : 'armor',
                'effect': 15,
                'id': 1,
                },
            #Bullet
            {
                'filepath' : ('graphics', 'items', 'bullet.png'),
                'type' : 'bullet',
                'effect': 10,
                'id': 2
                },
            #Shell
            {
                'filepath' : ('graphics', 'items', 'shell.png'),
                'type' : 'shell',
                'effect': 4,
                'id': 3
                },
            #ferromag ammo
            {
                'filepath' : ('graphics', 'items', 'ferromag.png'),
                'type' : 'ferromag',
                'effect': 6,
                'id': 4,
                },


            #Random any item
            {
                'filepath' : ('graphics', 'items', 'random.png'),
                'type' : 'random',
                'effect': ['health', 'armor', 'bullet', 'shell', 'ferromag',
                           'health', 'armor', 'bullet', 'shell', 'ferromag',
                           'melee', 'secondary', 'primary'],
                'id': 5,
                },


            #Random weapon
            {
                'filepath' : ('graphics', 'items', 'randomgun.png'),
                'type' : 'random',
                'effect': ['melee', 'secondary', 'primary'],
                'id': 6,
                },

            #Random item
            {
                'filepath' : ('graphics', 'items', 'randomitem.png'),
                'type' : 'random',
                'effect': ['health', 'armor', 'bullet', 'shell', 'ferromag'],
                'id': 7,
                },
            ]
    # Для возможности удалять/добавлять оружия
    for i in range(len(SETTINGS.gun_list)):
        SETTINGS.item_types.append({'filepath' : tuple(SETTINGS.gun_list[i].itemtexture.split('\\')),
                'type' : SETTINGS.gun_list[i].guntype,
                'effect': SETTINGS.gun_list[i],
                'id': 8+i})

def spawn_items():
    seed = SETTINGS.current_level + SETTINGS.seed
    for item in SETTINGS.levels_list[SETTINGS.current_level].items:
        stats = [x for x in SETTINGS.item_types if x['id'] == item[1]][0]
        if stats['type'] == 'random':
            random.seed(seed)
            possible_items = [x for x in SETTINGS.item_types if x['type'] in stats['effect']]
            stats = random.choice(possible_items)
            seed += 0.001
            
        elif stats['type'] not in ('primary', 'secondary', 'melee'):
            stats = copy.deepcopy([x for x in SETTINGS.item_types if x['id'] == item[1]][0])
        
        SETTINGS.all_items.append(ITEMS.Item(item[0], path.join(*stats['filepath']), stats['type'], stats['effect']))






