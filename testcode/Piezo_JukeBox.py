from machine import Pin, PWM
import utime

Buzzer_system = 6  # Port GP6 pour votre piezo

# --- DICTIONNAIRE GLOBAL DES FRÉQUENCES ---
NOTES = {
    'LA3': 220, 'SI3': 247,
    'DO4': 262, 'RE4': 294, 'MI4': 330, 'FA4': 349, 'SOL4': 392, 'LA4': 440, 'SIB4': 466, 'SI4': 494,
    'DO5': 523, 'RE5': 587, 'MI5': 659, 'FA5': 698, 'SOL5': 784, 'LA5': 880, 'SI5': 988,
    'DO6': 1047, 'MI6': 1319,
    'FA#4': 370, 'SOL#4': 415, 'SI#4': 512, 'DO#5': 554, 'RE#5': 622, 'FA#5': 740,
    'SIB5': 932, 'FA5_MARIO': 698, 'SOL5_MARIO': 784, 'LA5_MARIO': 880,
    'SILENCE': 0
}

# --- FONCTION UNIVERSELE POUR JOUER UNE PARTITION ---
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

# --- BASE DE DONNÉES DES MORCEAUX (JUKEBOX) ---

def track_mario_coin():
    print("🪙 Bruitage : Mario Coin")
    Buzzer = PWM(Pin(Buzzer_system))
    Buzzer.freq(988)
    Buzzer.duty_u16(3000)
    utime.sleep(0.08)
    Buzzer.freq(1319)
    utime.sleep(0.35)
    Buzzer.duty_u16(0)

def track_mario():
    print("🎮 Musique : Mario Bros Theme")
    part = ['MI5', 'MI5', 'SILENCE', 'MI5', 'SILENCE', 'DO5', 'MI5', 'SILENCE', 'SOL5', 'SILENCE', 'SOL4', 'SILENCE']
    temp = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.36, 0.12, 0.36]
    play_track(part, temp, volume=1500, pause=0.03)

def track_zelda():
    print("⚔️ Musique : The Legend of Zelda")
    part = ['SIB4', 'SILENCE', 'FA4', 'SILENCE', 'SIB4', 'SIB4', 'DO5', 'RE5', 'MI5', 'FA5']
    temp = [0.4, 0.05, 0.4, 0.05, 0.15, 0.15, 0.15, 0.15, 0.15, 0.6]
    play_track(part, temp, volume=2000, pause=0.02)

def track_mission():
    print("💣 Musique : Mission Impossible")
    part = ['SOL4', 'SOL4', 'SIB4', 'DO5', 'SOL4', 'SOL4', 'FA4', 'FA#4']
    temp = [0.3, 0.3, 0.15, 0.15, 0.3, 0.3, 0.15, 0.15]
    play_track(part, temp, volume=2000, pause=0.04)

def track_bond():
    print("🍸 Musique : James Bond 007")
    part = ['MI4', 'SILENCE', 'FA4', 'FA4', 'SILENCE', 'FA#4', 'FA#4', 'SILENCE', 'FA4', 'MI4', 'SI4', 'SOL4', 'MI4']
    temp = [0.3, 0.1, 0.15, 0.15, 0.1, 0.15, 0.15, 0.1, 0.15, 0.15, 0.15, 0.15, 0.6]
    play_track(part, temp, volume=2200, pause=0.03)

def track_axel():
    print("🎷 Musique : Axel F (Beverly Hills Cop)")
    part = ['FA4', 'SILENCE', 'SIB4', 'SILENCE', 'FA4', 'FA4', 'SILENCE', 'SIB4', 'FA4', 'DO5']
    temp = [0.2, 0.1, 0.25, 0.05, 0.15, 0.15, 0.05, 0.2, 0.2, 0.2]
    play_track(part, temp, volume=2500, pause=0.02)

def track_pacman():
    print("👾 Musique : Pac-Man Intro")
    part = ['SI4', 'SI5', 'FA#5', 'RE#5', 'SI5', 'FA#5', 'RE#5', 'DO5', 'DO6', 'SOL5', 'MI5', 'DO6']
    temp = [0.08] * 11 + [0.3]
    play_track(part, temp, volume=2000, pause=0.0)

def track_tetris():
    print("🧱 Musique : Tetris (Korobeiniki)")
    part = ['MI5', 'SI4', 'DO5', 'RE5', 'DO5', 'SI4', 'LA4', 'LA4', 'DO5', 'MI5', 'RE5', 'DO5', 'SI4']
    temp = [0.3, 0.15, 0.15, 0.3, 0.15, 0.15, 0.3, 0.15, 0.15, 0.3, 0.15, 0.15, 0.45]
    play_track(part, temp, volume=1800, pause=0.02)

def track_blinding():
    print("⚡ Musique : Blinding Lights")
    part = ['FA5', 'FA5', 'MI5', 'MI5', 'RE5', 'DO5', 'RE5', 'MI5', 'FA5']
    temp = [0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.18, 0.36]
    play_track(part, temp, volume=2200, pause=0.02)

def track_seven():
    print("🎸 Musique : Seven Nation Army")
    part = ['MI4', 'SILENCE', 'MI4', 'SOL5', 'MI4', 'RE4', 'DO4', 'SI3']
    temp = [0.45, 0.05, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5]
    play_track(part, temp, volume=3000, pause=0.03)

def track_pirates():
    print("🏴‍☠️ Musique : Pirates des Caraïbes")
    part = ['LA3', 'DO4', 'RE4', 'RE4', 'SILENCE', 'RE4', 'MI4', 'FA4', 'FA4', 'SILENCE', 'RE4']
    temp = [0.15, 0.15, 0.30, 0.15, 0.05, 0.15, 0.15, 0.30, 0.15, 0.05, 0.45]
    play_track(part, temp, volume=2200, pause=0.02)

# --- BOUCLE PRINCIPALE DU JUKEBOX ---
while True:
    print("\n" + "="*30)
    print("      MICRO-JUKEBOX GP6      ")
    print("="*30)
    print("1  - Mario (Coin)")
    print("2  - Mario Bros (Thème)")
    print("3  - Zelda (Thème)")
    print("4  - Mission Impossible")
    print("5  - James Bond 007")
    print("6  - Axel F (Beverly Hills)")
    print("7  - Pac-Man (Intro)")
    print("8  - Tetris")
    print("9  - Blinding Lights")
    print("10 - Seven Nation Army")
    print("11 - Pirates des Caraïbes")
    print("="*30)
    
    choix = input("Choisissez un numéro (1-11) : ")
    print("-"*30)
    
    if choix == "1": track_mario_coin()
    elif choix == "2": track_mario()
    elif choix == "3": track_zelda()
    elif choix == "4": track_mission()
    elif choix == "5": track_bond()
    elif choix == "6": track_axel()
    elif choix == "7": track_pacman()
    elif choix == "8": track_tetris()
    elif choix == "9": track_blinding()
    elif choix == "10": track_seven()
    elif choix == "11": track_pirates()
    else:
        print("❌ Choix invalide, réessayez.")
    
    utime.sleep(1)
