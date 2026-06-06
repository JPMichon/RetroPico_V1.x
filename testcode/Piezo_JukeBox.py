from machine import Pin, PWM
import utime

Buzzer_system = 6  # Port GP6

# --- DICTIONNAIRE GLOBAL DES FRÉQUENCES ---
NOTES = {
    'DO3': 131, 'DO#3': 139, 'RE3': 147, 'RE#3': 156, 'MI3': 165, 'FA3': 175, 'FA#3': 185, 'SOL3': 196, 'SOL#3': 208, 'LA3': 220, 'LA#3': 233, 'SI3': 247,
    'DO4': 262, 'DO#4': 277, 'RE4': 294, 'RE#4': 311, 'MI4': 330, 'FA4': 349, 'FA#4': 370, 'SOL4': 392, 'SOL#4': 415, 'LA4': 440, 'SIB4': 466, 'SI4': 494,
    'DO5': 523, 'DO#5': 554, 'RE5': 587, 'RE#5': 622, 'MI5': 659, 'FA5': 698, 'FA#5': 740, 'SOL5': 784, 'SOL#5': 831, 'LA5': 880, 'SIB5': 932, 'SI5': 988,
    'DO6': 1047, 'DO#6': 1109, 'RE6': 1175, 'MI6': 1319, 'SOL6': 1568,
    'SILENCE': 0
}

# --- FONCTION UNIVERSELLE DE LECTURE ---
def play_track(partition, tempos, volume=2000, pause=0.02):
    Buzzer = PWM(Pin(Buzzer_system))
    for note, duree in zip(partition, tempos):
        frequence = NOTES.get(note, 0)
        if frequence == 0:
            Buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            Buzzer.freq(frequence)
            Buzzer.duty_u16(volume)
            utime.sleep(duree)
        Buzzer.duty_u16(0)
        utime.sleep(pause)
    Buzzer.duty_u16(0)

# --- BASE DE DONNÉES EXTENDUE DU JUKEBOX ---

def play_summer_storm():
    Buzzer = PWM(Pin(Buzzer_system))
    
    # Extrait de la descente et de la montée frénétique de l'Orage (Presto)
    partition = [
        # Descente rapide
        'RE5', 'DO5', 'SI4', 'LA4', 'SOL4', 'FA4', 'MI4', 'RE4',
        'LA4', 'SOL4', 'FA4', 'MI4', 'RE4', 'DO4', 'SI3', 'LA3', # SI3 et LA3 simulés par octave 4
        
        # Motif de la tempête (alternance rapide)
        'RE5', 'LA4', 'RE5', 'LA4', 'RE5', 'LA4', 'RE5', 'LA4',
        'MI5', 'LA4', 'MI5', 'LA4', 'MI5', 'LA4', 'MI5', 'LA4',
        'FA5', 'LA4', 'FA5', 'LA4', 'SOL5', 'LA4', 'SOL5', 'LA4',
        
        # Accord final puissant
        'RE5', 'SILENCE'
    ]
    
    # Remplacement des notes trop graves hors dictionnaire pour le buzzer
    partition = ['RE4' if n == 'SI3' else 'MI4' if n == 'LA3' else n for n in partition]
    
    # Notes très courtes pour l'effet de vitesse (Presto)
    tempos = [
        0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10,
        0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10,
        0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08,
        0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08,
        0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08,
        0.40, 0.20
    ]
    
    for note, duree in zip(partition, tempos):
        frequence = NOTES[note]
        
        if frequence == 0:
            Buzzer.duty_u16(0)
            utime.sleep(duree)
        else:
            Buzzer.freq(frequence)
            Buzzer.duty_u16(4000) # Volume élevé pour l'intensité de l'orage
            utime.sleep(duree)
            
        # Pause ultra-courte pour enchaîner les notes sans perdre le rythme
        Buzzer.duty_u16(0)
        utime.sleep(0.02)
        
    Buzzer.duty_u16(0)
    
def track_mario():
    print("🎮 Musique : Mario Bros Theme (Long)")
    part = [
        'MI5', 'MI5', 'SILENCE', 'MI5', 'SILENCE', 'DO5', 'MI5', 'SILENCE', 'SOL5', 'SILENCE', 'SOL4', 'SILENCE',
        'DO5', 'SILENCE', 'SOL4', 'SILENCE', 'MI4', 'SILENCE', 'LA4', 'SILENCE', 'SI4', 'SILENCE', 'SIB4', 'LA4', 'SILENCE',
        'SOL4', 'MI5', 'SOL5', 'LA5', 'SILENCE', 'FA5', 'SOL5', 'SILENCE', 'MI5', 'SILENCE', 'DO5', 'RE5', 'SI4', 'SILENCE',
        'SILENCE', 'SOL5', 'FA#5', 'FA5', 'RE#5', 'SILENCE', 'MI5', 'SILENCE', 'GSL4', 'LA4', 'DO5', 'SILENCE', 'LA4', 'DO5', 'RE5'
    ]
    temp = [
        0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.36, 0.12, 0.36,
        0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12,
        0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.24, 0.12,
        0.24, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.24
    ]
    NOTES['GSL4'] = 415
    play_track(part, temp, volume=1500, pause=0.03)

def track_zelda():
    print("⚔️ Musique : The Legend of Zelda (Long)")
    part = [
        'SIB4', 'SILENCE', 'FA4', 'SILENCE', 'SIB4', 'SIB4', 'DO5', 'RE5', 'MI5', 'FA5', 'SILENCE',
        'FA5', 'FA5', 'SOL5', 'LA5', 'SIB5', 'SILENCE', 'SIB5', 'SIB5', 'LA5', 'SOL5', 'FA5', 'SOL5', 'FA5', 'MI5', 'SILENCE',
        'MI5', 'FA5', 'SOL5', 'FA5', 'MI5', 'RE5', 'MI5', 'RE5', 'DO5', 'SILENCE',
        'DO5', 'RE5', 'MI5', 'RE5', 'DO5', 'SI4', 'DO5', 'SI4', 'LA4', 'FA4', 'SOL4', 'LA4', 'SIB4'
    ]
    temp = [
        0.4, 0.05, 0.4, 0.05, 0.15, 0.15, 0.15, 0.15, 0.15, 0.6, 0.05,
        0.15, 0.15, 0.15, 0.15, 0.6, 0.05, 0.15, 0.15, 0.15, 0.15, 0.4, 0.15, 0.15, 0.5, 0.05,
        0.15, 0.15, 0.4, 0.15, 0.15, 0.4, 0.15, 0.15, 0.5, 0.05,
        0.15, 0.15, 0.4, 0.15, 0.15, 0.4, 0.15, 0.15, 0.4, 0.15, 0.15, 0.15, 0.6
    ]
    play_track(part, temp, volume=2000, pause=0.02)

def track_mission():
    print("💣 Musique : Mission Impossible (Extended)")
    part = [
        'SOL4', 'SOL4', 'SIB4', 'DO5', 'SOL4', 'SOL4', 'FA4', 'FA#4',
        'SOL4', 'SOL4', 'SIB4', 'DO5', 'SOL4', 'SOL4', 'FA4', 'FA#4',
        'SI4', 'LA4', 'SOL4', 'MI4', 'SILENCE', 'SI4', 'LA4', 'FA#4', 'MI4',
        'SILENCE', 'SI4', 'LA4', 'FA4', 'MI4', 'SILENCE', 'RE4', 'RE#4', 'MI4'
    ]
    temp = [
        0.25, 0.25, 0.12, 0.12, 0.25, 0.25, 0.12, 0.12,
        0.25, 0.25, 0.12, 0.12, 0.25, 0.25, 0.12, 0.12,
        0.4, 0.4, 0.4, 0.6, 0.1, 0.4, 0.4, 0.4, 0.6,
        0.1, 0.4, 0.4, 0.4, 0.6, 0.1, 0.15, 0.15, 0.5
    ]
    play_track(part, temp, volume=2000, pause=0.03)

def track_bond():
    print("🍸 Musique : James Bond 007 (Extended)")
    part = [
        'MI4', 'SILENCE', 'FA4', 'FA4', 'SILENCE', 'FA#4', 'FA#4', 'SILENCE', 'FA4',
        'MI4', 'SILENCE', 'FA4', 'FA4', 'SILENCE', 'FA#4', 'FA#4', 'SILENCE', 'FA4',
        'MI4', 'SI4', 'SOL4', 'MI4', 'SILENCE',
        'MI4', 'FA4', 'FA#4', 'SOL4', 'LA4', 'SI4', 'DO5', 'RE5', 'DO#5', 'DO5', 'SI4'
    ]
    temp = [
        0.3, 0.1, 0.15, 0.15, 0.1, 0.15, 0.15, 0.1, 0.15,
        0.3, 0.1, 0.15, 0.15, 0.1, 0.15, 0.15, 0.1, 0.15,
        0.15, 0.15, 0.15, 0.6, 0.2,
        0.1, 0.1, 0.1, 0.1, 0.15, 0.15, 0.15, 0.3, 0.15, 0.15, 0.6
    ]
    play_track(part, temp, volume=2200, pause=0.03)

def track_axel():
    print("🎷 Musique : Axel F (Extended)")
    part = [
        'FA4', 'SILENCE', 'SIB4', 'SILENCE', 'FA4', 'FA4', 'SILENCE', 'SIB4', 'FA4', 'DO5',
        'FA4', 'SILENCE', 'DO5', 'SILENCE', 'FA4', 'FA4', 'SILENCE', 'REB5', 'DO5', 'LA4',
        'FA4', 'DO5', 'FA5', 'FA4', 'SILENCE', 'MIB4', 'MIB4', 'SILENCE', 'DO4', 'SOL4', 'FA4',
        'SILENCE', 'FA5', 'RE5', 'DO5', 'LA4', 'FA4', 'DO5', 'FA5', 'FA4', 'REB5', 'DO5', 'SOL5', 'FA5'
    ]
    temp = [
        0.2, 0.1, 0.25, 0.05, 0.15, 0.15, 0.05, 0.2, 0.2, 0.2,
        0.2, 0.1, 0.25, 0.05, 0.15, 0.15, 0.05, 0.2, 0.2, 0.2,
        0.15, 0.15, 0.2, 0.15, 0.05, 0.15, 0.15, 0.05, 0.15, 0.15, 0.4,
        0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.5
    ]
    play_track(part, temp, volume=2500, pause=0.02)

def track_tetris():
    print("🧱 Musique : Tetris (Full Main Verse)")
    part = [
        'MI5', 'SI4', 'DO5', 'RE5', 'DO5', 'SI4', 'LA4', 'LA4', 'DO5', 'MI5', 'RE5', 'DO5', 'SI4',
        'DO5', 'RE5', 'MI5', 'DO5', 'LA4', 'LA4', 'SILENCE',
        'RE5', 'FA5', 'LA5', 'SOL5', 'FA5', 'MI5', 'DO5', 'MI5', 'RE5', 'DO5', 'SI4',
        'SI4', 'DO5', 'RE5', 'MI5', 'DO5', 'LA4', 'LA4', 'SILENCE',
        'DO5', 'MI5', 'DO5', 'MI5', 'LA4', 'LA4', 'SI4', 'RE4', 'SI4', 'RE4', 'MI4', 'MI4'
    ]
    temp = [
        0.3, 0.15, 0.15, 0.3, 0.15, 0.15, 0.3, 0.15, 0.15, 0.3, 0.15, 0.15, 0.45,
        0.15, 0.3, 0.3, 0.3, 0.3, 0.3, 0.15,
        0.45, 0.15, 0.3, 0.15, 0.15, 0.45, 0.15, 0.3, 0.15, 0.15, 0.3,
        0.15, 0.15, 0.3, 0.3, 0.3, 0.3, 0.45, 0.2,
        0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.6
    ]
    play_track(part, temp, volume=1800, pause=0.02)

def track_blinding():
    print("⚡ Musique : Blinding Lights (Chorus & Verse)")
    part = [
        'FA5', 'FA5', 'MI5', 'MI5', 'RE5', 'DO5', 'RE5', 'MI5', 'FA5', 'SILENCE', 'RE5', 'MI5', 'FA5', 'RE5', 'DO5',
        'FA5', 'FA5', 'MI5', 'MI5', 'RE5', 'DO5', 'RE5', 'MI5', 'FA5', 'SILENCE', 'RE5', 'MI5', 'FA5', 'RE5', 'SOL5',
        'SILENCE', 'RE5', 'RE5', 'RE5', 'MI5', 'DO5', 'SILENCE', 'RE5', 'RE5', 'RE5', 'MI5', 'LA4'
    ]
    temp = [
        0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.05, 0.18, 0.18, 0.18, 0.18, 0.36,
        0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.05, 0.18, 0.18, 0.18, 0.18, 0.54,
        0.2, 0.18, 0.18, 0.18, 0.18, 0.36, 0.1, 0.18, 0.18, 0.18, 0.18, 0.54
    ]
    play_track(part, temp, volume=2200, pause=0.02)

def track_seven():
    print("🎸 Musique : Seven Nation Army (Main + Chorus)")
    part = [
        'MI4', 'SILENCE', 'MI4', 'SOL5', 'MI4', 'RE4', 'DO4', 'SI3',
        'MI4', 'SILENCE', 'MI4', 'SOL5', 'MI4', 'RE4', 'DO4', 'RE4', 'DO4', 'SI3',
        'SOL4', 'SOL4', 'SOL4', 'SOL4', 'SOL4', 'SOL4', 'SOL4', 'SOL4', 'LA4', 'LA4', 'LA4', 'LA4', 'LA4', 'LA4', 'LA4', 'LA4'
    ]
    temp = [
        0.45, 0.05, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5,
        0.45, 0.05, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.5,
        0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15
    ]
    play_track(part, temp, volume=3000, pause=0.03)

def track_pirates():
    print("🏴‍☠️ Musique : Pirates des Caraïbes (Epic Long)")
    part = [
        'LA3', 'DO4', 'RE4', 'RE4', 'SILENCE', 'RE4', 'MI4', 'FA4', 'FA4', 'SILENCE',
        'FA4', 'SOL4', 'MI4', 'MI4', 'SILENCE', 'RE4', 'DO4', 'DO4', 'RE4', 'SILENCE',
        'LA3', 'DO4', 'RE4', 'RE4', 'SILENCE', 'RE4', 'MI4', 'FA4', 'FA4', 'SILENCE',
        'FA4', 'SOL4', 'MI4', 'MI4', 'SILENCE', 'RE4', 'DO4', 'RE4', 'SILENCE',
        'LA3', 'DO4', 'RE4', 'FA4', 'SOL4', 'LA4', 'LA4', 'SILENCE', 'SIB4', 'DO5', 'LA4', 'LA4', 'RE4', 'MI4', 'FA4', 'SOL4', 'LA4'
    ]
    temp = [
        0.15, 0.15, 0.30, 0.15, 0.05, 0.15, 0.15, 0.30, 0.15, 0.05,
        0.15, 0.15, 0.30, 0.15, 0.05, 0.15, 0.15, 0.15, 0.45, 0.10,
        0.15, 0.15, 0.30, 0.15, 0.05, 0.15, 0.15, 0.30, 0.15, 0.05,
        0.15, 0.15, 0.30, 0.15, 0.05, 0.15, 0.15, 0.45, 0.15,
        0.15, 0.15, 0.30, 0.30, 0.30, 0.30, 0.15, 0.05, 0.15, 0.15, 0.30, 0.15, 0.15, 0.15, 0.15, 0.15, 0.60
    ]
    play_track(part, temp, volume=2200, pause=0.02)

def track_pink_panther():
    print("🐆 Musique : La Panthère Rose (Extended)")
    part = [
        'RE#4', 'MI4', 'SILENCE', 'FA#4', 'SOL4', 'SILENCE',
        'RE#4', 'MI4', 'FA#4', 'SOL4', 'DO5', 'SI4', 'MI4', 'SOL4', 'SI4', 'LA#4', 'LA4', 'SILENCE',
        'SOL4', 'MI4', 'RE4', 'MI4', 'SILENCE', 'RE#4', 'MI4', 'FA#4', 'SOL4', 'DO5', 'SI4', 'SOL5', 'SI5', 'MI6'
    ]
    temp = [
        0.15, 0.45, 0.10, 0.15, 0.45, 0.10,
        0.15, 0.15, 0.15, 0.15, 0.30, 0.30, 0.15, 0.15, 0.15, 0.60, 0.60, 0.20,
        0.15, 0.15, 0.15, 0.45, 0.10, 0.15, 0.15, 0.15, 0.15, 0.30, 0.30, 0.15, 0.15, 0.80
    ]
    play_track(part, temp, volume=1800, pause=0.04)
    
def track_star_wars():
    print("🚀 Musique : Star Wars (Extended)")
    part = [
        'DO4', 'SOL4', 'SILENCE', 'FA4', 'MI4', 'RE4', 'DO5', 'SOL4', 'SILENCE', 
        'FA4', 'MI4', 'RE4', 'DO5', 'SOL4', 'SILENCE', 'FA4', 'MI4', 'FA4', 'RE4', 'SILENCE',
        'SOL4', 'SOL4', 'SOL4', 'DO5', 'SOL5', 'SILENCE', 'FA5', 'MI5', 'RE5', 'DO6', 'SOL5'
    ]
    temp = [
        0.4, 0.4, 0.05, 0.13, 0.13, 0.13, 0.4, 0.2, 0.05,
        0.13, 0.13, 0.13, 0.4, 0.2, 0.05, 0.13, 0.13, 0.13, 0.5, 0.2,
        0.13, 0.13, 0.13, 0.4, 0.4, 0.05, 0.13, 0.13, 0.13, 0.4, 0.4
    ]
    play_track(part, temp, volume=2200, pause=0.03)

def track_pulp_fiction():
    print("🕶️ Musique : Pulp Fiction - Misirlou (Fast Tremolo)")
    # Riff oriental ultra rapide nécessitant des notes dupliquées serrées
    part = [
        'MI4', 'MI4', 'MI4', 'MI4', 'FA4', 'FA4', 'SOL#4', 'SOL#4', 'LA4', 'LA4', 'SI4', 'SI4',
        'DO5', 'DO5', 'SI4', 'SI4', 'LA4', 'LA4', 'SOL#4', 'SOL#4', 'FA4', 'FA4', 'MI4', 'MI4',
        'MI4', 'MI4', 'MI4', 'MI4', 'RE4', 'RE4', 'DO4', 'DO4', 'SI3', 'SI3', 'SI3', 'SI3'
    ]
    temp = [0.06] * 36  # Succession ultra-rapide de notes de 60ms
    play_track(part, temp, volume=2600, pause=0.01) # Micro-pause ultra courte
    
    
# --- BOUCLE PRINCIPALE DU JUKEBOX ---
while True:
    print("\n" + "="*35)
    print("   JUKEBOX ")
    print("="*35)
    print("1 - Mario Bros")
    print("2 - The Legend of Zelda")
    print("3 - Mission Impossible")
    print("4 - James Bond 007")
    print("5 - Axel F (Beverly Hills)")
    print("6 - Tetris")
    print("7 - Blinding Lights")
    print("8 - Seven Nation Army")
    print("9 - Pirates des Caraïbes")
    print("10 - La Panthère Rose")
    print("11 - Star Wars 🚀")
    print("12 - Pulp Fiction 🕶️")
    print("13 - L'Été (L'Orage)️")
    print("="*35)
    
    choix = input("Choisissez un numéro (1-13) : ")
    print("-"*35)
    
    if choix == "1": track_mario()
    elif choix == "2": track_zelda()
    elif choix == "3": track_mission()
    elif choix == "4": track_bond()
    elif choix == "5": track_axel()
    elif choix == "6": track_tetris()
    elif choix == "7": track_blinding()
    elif choix == "8": track_seven()
    elif choix == "9": track_pirates()
    elif choix == "10": track_pink_panther()
    elif choix == "11": track_star_wars()
    elif choix == "12": track_pulp_fiction()
    elif choix == "13": play_summer_storm()
    else:print("❌ Choix invalide, réessayez.")
    utime.sleep(1)