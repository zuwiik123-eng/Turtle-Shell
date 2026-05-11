#!/usr/bin/env python3
import os, sys, random, time, string, subprocess, platform, pyperclip, curses, pygame

# os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
# os.environ["SDL_VIDEODRIVER"]            = "dummy"
# os.environ["SDL_AUDIODRIVER"]            = "pulse"
# import pygame

# Kolorki
def zielony(tekst):
	return f"\033[32m{tekst}\033[0m"
def czerwony(tekst):
	return f"\033[31m{tekst}\033[0m"
def zolty(tekst):
	return f"\033[33m{tekst}\033[0m"
def cyan(tekst):
	return f"\033[36m{tekst}\033[0m"

def wyczysc_ekran():
	os.system('clear')

def get_os_info():
	info = {}
	try:
		with open("/etc/os-release") as f:
			for line in f:
				if "=" in line:
					k, v = line.rstrip().split("=", 1)
					info[k] = v.strip('"')
	except FileNotFoundError:
		return None
	return info

def pobierz_baze_komendy(akcja):
	os_info = get_os_info()
	if not os_info:
		return None

	os_id = os_info.get("ID", "").lower()
	os_like = os_info.get("ID_LIKE", "").lower().split()

	systemy = {
		"fedora": {
			"install": ["sudo", "dnf", "install", "-y"],
			"remove": ["sudo", "dnf", "remove", "-y"],
			"reinstall": ["sudo", "dnf", "reinstall", "-y"],
			"update": ["sudo", "dnf", "upgrade", "-y"],
			"clean": ["sudo", "dnf", "autoremove", "-y"]
		},
		"debian": {
			"install": ["sudo", "apt", "install", "-y"],
			"remove": ["sudo", "apt", "remove", "-y"],
			"reinstall": ["sudo", "apt", "install", "--reinstall", "-y"],
			"update": ["sudo", "apt", "update", "&&", "sudo", "apt", "upgrade", "-y"],
			"clean": ["sudo", "apt", "autoremove", "-y"]
		},
		"arch": { #you use arch btw
			"install": ["sudo", "pacman", "-S", "--noconfirm"],
			"remove": ["sudo", "pacman", "-Rs", "--noconfirm"],
			"reinstall": ["sudo", "pacman", "-S", "--noconfirm"],
			"update": ["sudo", "pacman", "-Syu", "--noconfirm"],
			"clean": ["sudo", "pacman", "-Rns", "$(pacman -Qtdq)"]
		}
	}

	target = None
	if os_id in systemy:
		target = systemy[os_id]
	else:
		for like in os_like:
			if like in systemy:
				target = systemy[like]
				break

	return target.get(akcja) if target else None

def pokaz_distro():
    try:
        info = platform.freedesktop_os_release()
        print(f"Siedzisz na: {info['PRETTY_NAME']}")
    except (AttributeError, FileNotFoundError):
        print(f"System: {platform.system()} {platform.release()}")

def wylacz_komputer():
	print("pa pa")
	time.sleep(1)
	os.system('shutdown now')

def swylacz_komputer():
	os.system('sudo shutdown now')

def zrestartuj_komputer():
	print("papa")
	time.sleep(1)
	os.system('reboot now')

def szrestartuj_komputer():
	os.system('sudo reboot now')

def update_and_clean():
	update_cmd = pobierz_baze_komendy("update")
	clean_cmd = pobierz_baze_komendy("clean")

	if update_cmd and clean_cmd:
		print("--- Aktualizacja systemu ---")
		subprocess.run(update_cmd)
		print("--- Czyszczenie zbędnych pakietów ---")
		subprocess.run(clean_cmd)
	else:
		print("Twoja dystrybuja nie jest obsługiwana")

def zainstaluj(package):
	cmd = pobierz_baze_komendy("install")
	if cmd:
		subprocess.run(cmd + [package])
	else:
		print("Twoja dystrybuja nie jest obsługiwana")

def odinstaluj(package):
	cmd = pobierz_baze_komendy("remove")
	if cmd:
		print(f"--- Usuwanie: {package} ---")

def przeinstaluj(package):
	cmd = pobierz_baze_komendy("reinstall")
	if cmd:
		print(f"--- Przeinstalowywanie: {package} ---")
		subprocess.run(cmd + [package])
	else:
		print("Twoja dystrybuja nie jest obsługiwana")

def gambling():
	wyczysc_ekran()

	kosci = [random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), random.randint(1, 6)]

	def rzuc_kosci(nkosci):
		for i in nkosci:
			index = int(i) - 1
			kosci[index] = random.randint(1, 6)

	def pokaz_kosci():
		print(czerwony("----------------------------------"))
		for i in range(5):
			print(zielony(f"kosc nr{i + 1}. {kosci[i]}"))
		print(czerwony("----------------------------------"))

	def sprawdz_czy_przerzucamy():
		odp = input("Czy chcesz przerzucic kosci? (y/n)")
		return odp.lower() == "y"

	rzuc_kosci("12345")
	pokaz_kosci()

	for i in range(2):
		czy_przerzut = sprawdz_czy_przerzucamy()
		if czy_przerzut:
			kosci_do_przezutu = input("Wpisz numery kosci, ktore chcesz przerzucic: ")
			kosci_do_przezutubs = kosci_do_przezutu.replace(" ", "")
			rzuc_kosci(kosci_do_przezutubs)
			pokaz_kosci()
		else:
			break

def moj_kalkulator():
	wyczysc_ekran()
	print("--- URUCHAMIAM KALKULATOR ---")
	kalkulacja = ""
	def help_kalkulator():
		print(zielony("Napisz enter aby obliczyc dzialanie "))
		print(zielony("Napisz exit aby wyjsc"))
		print(zielony("Podaj liczbę, znak dzialania, albo cale dzialanie"))
		print(zielony("'clear' czysci ekran i dzialanie"))

		print(czerwony("""+ dodawanie
- odejmowanie
* mnozenie
/ dzielenie
** potęgowanie"""))
	help_kalkulator()
	while True:
		wejscie = input(">> ")
		wejscie_bs = wejscie.replace(" ", "")
		wejscie_pop = wejscie_bs.replace(",", ".")

		if wejscie == "enter":
			# try:
			wynik = eval(kalkulacja)
			print(float(wynik))
			print(zielony("(skopiowano!)"))
			pyperclip.copy(wynik)
			kalkulacja = ""
			# except:
			# 	print(czerwony("nie mozna obliczyc"))
		elif wejscie == "clear":
			wyczysc_ekran()
			help_kalkulator()
		elif wejscie == "exit":
			input(czerwony("\nNaciśnij Enter, aby wrócić do Zuwiika..."))
			break
		else:
			kalkulacja += wejscie_pop

def generator_hasel():
	wyczysc_ekran()
	print("--- URUCHAMIAM GENERATOR ---")
	znak = 0
	asd = None
	while znak <= 1:
		try:
			ilosc_znakow = int(input("ile chcesz, aby twoje haslo mialo znakow?: "))
		except ValueError:
			print("Musi być to znak całkowity!")
			continue
		if ilosc_znakow <= 3:
			print(czerwony("Zla ilosc znakow!"))
			asd = 1
			break
		znak = 2

	haslo = ""
	male_litery = string.ascii_lowercase
	duze_litery = string.ascii_uppercase
	znaki_specjalne = string.punctuation

	stare_z = -1
	start = time.time()

	for a in range(ilosc_znakow):
		z = random.randint(0, 2)
		if z == 0:
			haslo += random.choice(znaki_specjalne)
		elif z == 1:
			haslo += random.choice(duze_litery)
		else:
			haslo += random.choice(male_litery)

	if asd == 1:
		input("\nNaciśnij Enter, aby wrócić do Zuwiika...")
		exit
	print(zielony(f"Twoje haslo to: {czerwony(haslo)} (skopiowalo sie do schowka)"))
	pyperclip.copy(haslo)
	end = time.time()
	print(f"wygenerowanie zajelo {end - start:.2f} sekund/y")
	input("\nNaciśnij Enter, aby wrócić do Zuwiika...")

def gra_w_zgadywanie():
	wyczysc_ekran()
	print("--- URUCHAMIAM GRE---")
	losowa_liczba = random.randint(1, 100)
	while True:
		zgadywana_liczba = int(input("Zgadnij liczbe: "))
		if losowa_liczba == zgadywana_liczba:
			print("Zgadles! Brawo!")
			print("-----------------------------")
			input("\nNaciśnij Enter, aby wrócić do Zuwiika...")
			break
		if losowa_liczba > zgadywana_liczba:
			print("Twoja liczba jest za mała!")
			if 10 >= losowa_liczba - zgadywana_liczba >= 0:
				print("jesteś blisko!")
			if 5 >= losowa_liczba - zgadywana_liczba >= 0:
				print("nawet BARDZO BARDZO blisko!")
			print("-----------------------------")
			continue
		if losowa_liczba < zgadywana_liczba:
			print("Twoja liczba jest za duza!")
			if 10 >= zgadywana_liczba - losowa_liczba >= 0:
				print("jesteś blisko!")
			if 5 >= zgadywana_liczba - losowa_liczba >= 0:
				print("nawet BARDZO BARDZO blisko!")
			print("-----------------------------")
			continue

def gra_wyscig():
	wyczysc_ekran()
	print("--- URUCHAMIAM GRE---")
	kroki = 0
	kroki2 = 0
	tura = 0
	tura2 = 0
	META = 20
	print(f"Wyścig do {META}")
	while kroki < META and kroki2 < META:
		input(cyan("Nacisnij ENTER aby rzucic kostka (Gracz 1)"))
		kroki += random.randint(1, 5)
		kroki2 += random.randint(1, 5)
		print("*rzucasz...*")
		time.sleep(1)
		print(cyan(f"(Gracz 1)- wyrzucił {kroki}/{META}"))
		tura += 1
		if kroki < META:
			input(czerwony("Nacisnij ENTER aby rzucic kostka (Gracz 2)"))
			kroki += random.randint(1, 5)
			print("*rzucasz...*")
			time.sleep(1)
			print(czerwony(f"(Gracz 2)- wyrzucił {kroki2}/{META}"))
			tura2 += 1
	if kroki > META:
		print("----------------------")
		print(cyan(f"Gracz 1 Dobiegł, zajeło to {tura} tur/y!"))
		input("\nNaciśnij Enter, aby wrócić do Zuwiika...")
	if kroki2 > META:
		print("----------------------")
		print(czerwony(f"Gracz 2 Dobiegł, zajeło to {tura2} tur/y!"))
		input("\nNaciśnij Enter, aby wrócić do Zuwiika...")

def info():
	print("To jest Zuwiik shell v1.1")
	print("Jesli znajdziesz buga, wyslij na zuwiik@proton.me")

def start():
	print(zielony("==================================================================="))
	print(zielony(" 	Witaj w systemie ZUWIIK's TURTLE SHELL (Fedora 42) "))
	print(czerwony(" 		Wpisz 'help', aby zobaczyć opcje "))
	print(zielony("==================================================================="))

def Antosify():
	"""
	Terminal Music Player
	Wymagania: pip install pygame mutagen
	Użycie: python player.py [katalog_z_mp3]
	"""

	# Ucisz wszelkie pozostałe wydruki SDL na stderr podczas initu
	import io as _io
	_devnull = open(os.devnull, "w")

	try:
		from mutagen.mp3 import MP3
		HAS_MUTAGEN = True
	except ImportError:
		HAS_MUTAGEN = False

	# ──────────────────────────────────────────────
	#  Logika gracza
	# ──────────────────────────────────────────────

	class MusicPlayer:
		def __init__(self, music_dir="."):
			self.music_dir = music_dir
			self.playlist = []
			self.current_index = 0
			self.volume = 0.3
			self.paused = True
			self.running = True
			self.current_duration = 0
			self.message = ""
			self.message_until = 0

			_old_stderr, sys.stderr = sys.stderr, _devnull
			try:
				pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
			finally:
				sys.stderr = _old_stderr
			pygame.mixer.music.set_volume(self.volume)

			self._scan_files()

		# ── skanowanie ──────────────────────────────

		def _scan_files(self):
			found = []
			for root, _, files in os.walk(self.music_dir):
				for f in files:
					if f.lower().endswith(".mp3"):
						found.append(os.path.join(root, f))
			random.shuffle(found)
			self.playlist = found

		# ── playback ────────────────────────────────

		def play_current(self):
			if not self.playlist:
				return
			path = self.playlist[self.current_index]
			self.current_duration = self._get_duration(path)
			try:
				pygame.mixer.music.load(path)
				pygame.mixer.music.play()
				self.paused = False
			except Exception as e:
				self.set_message(f"Błąd: {e}")

		def next_track(self):
			self.current_index = (self.current_index + 1) % len(self.playlist)
			self.play_current()

		def prev_track(self):
			self.current_index = (self.current_index - 1) % len(self.playlist)
			self.play_current()

		def toggle_pause(self):
			if self.paused:
				pygame.mixer.music.unpause()
				self.paused = False
			else:
				pygame.mixer.music.pause()
				self.paused = True

		# ── narzędzia ───────────────────────────────

		def set_volume(self, vol_pct: int):
			self.volume = max(0.0, min(1.0, vol_pct / 100.0))
			pygame.mixer.music.set_volume(self.volume)

		def set_message(self, msg: str, seconds: float = 3.0):
			self.message = msg
			self.message_until = time.time() + seconds

		def get_position(self) -> float:
			"""Pozycja w sekundach (pygame zwraca ms)."""
			return max(0.0, pygame.mixer.music.get_pos() / 1000.0)

		def _get_duration(self, path: str) -> float:
			if HAS_MUTAGEN:
				try:
					return MP3(path).info.length
				except Exception:
					pass
			return 0.0

		def shuffle_playlist(self):
			current_path = self.playlist[self.current_index] if self.playlist else None
			random.shuffle(self.playlist)
			if current_path in self.playlist:
				self.current_index = self.playlist.index(current_path)
			else:
				self.current_index = 0

		@property
		def current_name(self) -> str:
			if not self.playlist:
				return ""
			return os.path.splitext(os.path.basename(self.playlist[self.current_index]))[0]

	# ──────────────────────────────────────────────
	#  Interfejs curses
	# ──────────────────────────────────────────────

	def _fmt_time(seconds: float) -> str:
		s = int(seconds)
		return f"{s // 60}:{s % 60:02d}"

	def _bar(filled: int, total: int, char_full="█", char_empty="░") -> str:
		if total <= 0:
			return char_empty * 1
		f = max(0, min(filled, total))
		return char_full * f + char_empty * (total - f)

	def draw_ui(stdscr, player: MusicPlayer):
		# ── ustawienia curses ──
		curses.curs_set(1)
		stdscr.nodelay(True)
		stdscr.keypad(True)

		if curses.has_colors():
			curses.start_color()
			curses.use_default_colors()
			curses.init_pair(1, curses.COLOR_GREEN, -1)  # zielony – nagłówek
			curses.init_pair(2, curses.COLOR_CYAN, -1)  # cyan – aktywny utwór
			curses.init_pair(3, curses.COLOR_BLUE, -1)  # żółty – pasek/głośność
			curses.init_pair(4, curses.COLOR_RED, -1)  # czerwony – błąd
			curses.init_pair(5, curses.COLOR_WHITE, -1)  # biały – normalny tekst
			curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)  # odwrócony

		C_GREEN = curses.color_pair(1) | curses.A_BOLD
		C_CYAN = curses.color_pair(2) | curses.A_BOLD
		C_YELLOW = curses.color_pair(3)
		C_RED = curses.color_pair(4)
		C_WHITE = curses.color_pair(5)
		C_TITLE = curses.color_pair(1)

		input_buf = ""

		def safe_addstr(y, x, text, attr=0):
			"""Bezpieczne addstr – ignoruje wychodzenie poza ekran."""
			h, w = stdscr.getmaxyx()
			if y < 0 or y >= h or x >= w:
				return
			text = text[: w - x - 1]  # zostaw 1 znak na margines
			if text:
				try:
					stdscr.addstr(y, x, text, attr)
				except curses.error:
					pass

		def hline(y, attr=0):
			h, w = stdscr.getmaxyx()
			if 0 <= y < h:
				try:
					stdscr.hline(y, 0, curses.ACS_HLINE, w, attr)
				except curses.error:
					pass

		def wyszukiwarka(komenda):
			if len(komenda) < 2:
				player.set_message("❌  Użycie: search <nazwa>")
				return []
			szukana = komenda[1]
			wyniki = []
			for p in player.playlist:
				if szukana in p.lower():
					wyniki.append(p)
			return wyniki

		while player.running:
			try:
				h, w = stdscr.getmaxyx()
				stdscr.erase()

				# ── auto-next ──────────────────────────────
				if (player.playlist
						and not player.paused
						and not pygame.mixer.music.get_busy()):
					player.next_track()

				# ── nagłówek (wiersze 0-1) ─────────────────
				title = "♫  Antosify  ♫"
				safe_addstr(0, max(0, (w - len(title)) // 2), title, C_TITLE)
				hline(1, C_GREEN)

				# ── informacje o utworze (2-4) ─────────────
				if player.playlist:
					status_icon = "⏸" if player.paused else "▶"
					now_playing = f" {status_icon}  {player.current_name}"
					safe_addstr(2, 0, now_playing, C_CYAN)

					track_info = f" Utwór {player.current_index + 1} / {len(player.playlist)}"
					safe_addstr(3, 0, track_info, C_WHITE)

					vol_pct = int(player.volume * 100)
					vol_bar = _bar(vol_pct // 5, 20)
					safe_addstr(4, 0, f" 🔊 [{vol_bar}] {vol_pct}%", C_YELLOW)
				else:
					safe_addstr(2, 0, " ⚠  Brak plików MP3 w katalogu!", C_RED)

				hline(5, C_GREEN)

				# ── lista playlist (6 … h-7) ───────────────
				list_top = 6
				list_bot = h - 7
				list_h = max(0, list_bot - list_top)

				if player.playlist and list_h > 0:
					half = list_h // 2
					start = max(0, player.current_index - half)
					end = min(len(player.playlist), start + list_h)
					# korekta gdy jesteśmy blisko końca
					if end - start < list_h:
						start = max(0, end - list_h)

					for row_i, idx in enumerate(range(start, end)):
						y = list_top + row_i
						if y >= list_bot:
							break
						name = os.path.splitext(
							os.path.basename(player.playlist[idx])
						)[0]
						if idx == player.current_index:
							line = f" ► {name}"
							safe_addstr(y, 0, line, C_CYAN)
						else:
							num = f"{idx + 1:>3}."
							line = f" {num} {name}"
							safe_addstr(y, 0, line, C_WHITE)

				# ── separator + pasek postępu (h-6 … h-4) ──
				hline(h - 6, C_GREEN)

				if player.playlist and player.current_duration > 0:
					pos = player.get_position()
					bar_w = max(0, w - 16)
					filled = int(pos / player.current_duration * bar_w)
					progress = _bar(filled, bar_w)
					pos_str = _fmt_time(pos)
					dur_str = _fmt_time(player.current_duration)
					safe_addstr(h - 5, 0,
								f" {pos_str} [{progress}] {dur_str}",
								C_YELLOW)
				elif player.playlist:
					safe_addstr(h - 5, 0, " (czas nieznany – zainstaluj mutagen)", C_WHITE)

				# ── komunikat systemowy (h-4) ──────────────
				if player.message and time.time() < player.message_until:
					safe_addstr(h - 4, 0, f" ▸ {player.message}", C_YELLOW)

				# ── pomoc (h-3) ────────────────────────────
				help_txt = " next | prev | pause | volume 0-100 | shuffle | goto * | quit | search"
				safe_addstr(h - 3, 0, help_txt[: w - 1], C_WHITE)

				# ── linia wejścia (h-2, h-1) ──────────────
				hline(h - 2, C_GREEN)
				prompt = f" > {input_buf}"
				safe_addstr(h - 1, 0, prompt, C_CYAN)
				# przesuń kursor na koniec inputa
				cur_x = min(len(prompt), w - 2)
				try:
					stdscr.move(h - 1, cur_x)
				except curses.error:
					pass

				stdscr.refresh()

				# ── obsługa klawiatury ─────────────────────
				key = stdscr.getch()

				if key == -1:
					time.sleep(0.05)
					continue

				if key in (curses.KEY_BACKSPACE, 127, 8):
					input_buf = input_buf[:-1]

				elif key in (10, 13):  # Enter
					cmd = input_buf.strip().lower()
					input_buf = ""

					if not cmd:
						pass
					elif cmd in ("q", "quit", "exit", "wyjdz", "spierdalaj"):
						player.running = False

					elif cmd in ("n", "next", "nastepny"):
						player.next_track()
						player.set_message("⏭  Następny utwór")

					elif cmd in ("p", "prev", "previous", "poprzedni"):
						player.prev_track()
						player.set_message("⏮  Poprzedni utwór")

					elif cmd in ("pause", "play", "pp", "pauza"):
						player.toggle_pause()
						player.set_message("⏸  Pauza" if player.paused else "▶  Odtwarzanie")

					elif cmd == "shuffle":
						player.shuffle_playlist()
						player.set_message("🔀  Playlista przetasowana")

					elif cmd.startswith(("search ", "sr ", "szukaj")):
						parts = cmd.split()
						wyniki = wyszukiwarka(parts)
						if len(wyniki) == 0:
							player.set_message("❌  Nic nie znaleziono")
						else:
							nazwy = ", ".join([os.path.splitext(os.path.basename(p))[0] for p in wyniki])
							player.set_message(f"🔍  Znaleziono {len(wyniki)}: {nazwy}")
						# if len(wyniki) == 1:
						#     player.current_index =

					elif cmd.startswith(("volume ", "vol ")):
						parts = cmd.split()
						if len(parts) == 2:
							try:
								v = int(parts[1])
								player.set_volume(v)
								player.set_message(f"🔊  Głośność: {v}%")
							except ValueError:
								player.set_message("❌  Podaj liczbę 0–100, np.: volume 60")
						else:
							player.set_message(f"🔊  Aktualna głośność: {int(player.volume * 100)}%")

					elif cmd.startswith("goto "):
						parts = cmd.split()
						if len(parts) == 2:
							try:
								idx = int(parts[1]) - 1
								if 0 <= idx < len(player.playlist):
									player.current_index = idx
									player.play_current()
									player.set_message(f"⏩  Przeskoczono do #{idx + 1}")
								else:
									player.set_message(f"❌  Numer spoza zakresu (1–{len(player.playlist)})")
							except ValueError:
								player.set_message("❌  Składnia: goto <numer>")
						else:
							player.set_message("❌  Składnia: goto <numer>")

					else:
						player.set_message(f"❓  Nieznana komenda: {cmd!r}")

				elif 32 <= key <= 126:  # drukowalne ASCII
					input_buf += chr(key)

			except curses.error:
				pass

			time.sleep(0.05)

	# ──────────────────────────────────────────────
	#  Punkt wejścia
	# ──────────────────────────────────────────────

	def main():
		base_dir = os.path.dirname(os.path.abspath(__file__))
		music_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base_dir, "muzyka")

		if not os.path.isdir(music_dir):
			print(f"Błąd: '{music_dir}' nie jest katalogiem.")
			sys.exit(1)

		if not os.path.isdir(music_dir):
			print(f"Błąd: '{music_dir}' nie jest katalogiem.")
			sys.exit(1)

		if not HAS_MUTAGEN:
			print("Uwaga: mutagen nie zainstalowany – czas trwania piosenek niedostępny.")
			print("       pip install mutagen")
			time.sleep(2)

		player = MusicPlayer(music_dir)

		if not player.playlist:
			print(f"Nie znaleziono plików MP3 w: {os.path.abspath(music_dir)}")
			sys.exit(1)

		print(f"Znaleziono {len(player.playlist)} pliku/ów MP3. Uruchamianie...")
		# player.play_current()
		time.sleep(0.3)

		try:
			curses.wrapper(lambda stdscr: draw_ui(stdscr, player))
		except KeyboardInterrupt:
			pass
		finally:
			pygame.mixer.music.stop()
			pygame.mixer.quit()
			print("\nDo widzenia! 🎵")

	if __name__ == "__main__":
		main()

def main():
	wyczysc_ekran()
	start()
	while True:
		komenda = input(zielony("Zuwiik > ")).strip().lower()
		czesc = komenda.split()

		if komenda == "help":
			print(czerwony("\nDostępne komendy:"))
			print(czerwony(" bash           - wraca do podstawowego terminala"))
			print(zolty(" clear          - czyści ekran"))
			print(zolty(" exit           - zamyka Zuwiika"))
			print(zolty(" start          - odpala startową informacje"))
			print(zolty(" info           - daje informacje o shellu"))
			print(zolty(" shutdown       - wyłącze cały komputer"))
			print(zolty(" sshutdown      - robi to, ale jako Super user (potrzeba hasla roota) "))
			print(zolty(" reboot         - restartuje caly komputer"))
			print(zolty(" sreboot        - robi to, ale jako Super user (potrzeba hasla roota)"))
			print(zielony(" zainstaluj     - mozesz zainstalowac dowolną apliakcje z repozytorium (potrzeba hasla roota)"))
			print(zielony(" przeinstaluj   - mozesz przeinstalowac aplikacje z repozytorium (potrzeba hasla roota)"))
			print(zielony(" odinstaluj     - mozesz odinstalowac aplikacje z repozytorium (potrzeba hasla roota)"))
			print(zielony(" uac            - (update and clean) aktualizuje aplikacje i czysci niepotrzebne pliki (potrzeba hasla roota)"))
			print(zielony(" distro         - pokazuje jakiego distro uzywasz"))
			print(cyan(" kalkulator     - odpala kalkulator"))
			print(cyan(" gen hasel      - odpala generator hasel"))
			print(cyan(" gra zgad       - odpala gre z zgadywaniem liczby"))
			print(cyan(" gra wyscig     - odpala gre z wyscigiem"))
			print(cyan(" kosci          - odpala gre w Yahtzee"))
			print(cyan(" antosify       - odpala media player"))
			print("")

		elif komenda == "bash":
			os.system("/bin/bash")

		elif komenda == "distro":
			pokaz_distro()

		elif komenda == "antosify":
			Antosify()

		elif komenda == "kosci":
			gambling()

		elif komenda == "uac":
			update_and_clean()

		elif czesc[0] == "zainstaluj":
			package = czesc[1]
			zainstaluj(package)


		elif czesc[0] == "przeinstaluj":
			package = czesc[1]
			przeinstaluj(package)

		elif czesc[0] == "odinstaluj":
			package = czesc[1]
			odinstaluj(package)

		elif komenda == "shutdown":
			wylacz_komputer()

		elif komenda == "sshutdown":
			swylacz_komputer()

		elif komenda == "reboot":
			zrestartuj_komputer()

		elif komenda == "sreboot":
			szrestartuj_komputer()

		elif komenda == "gen hasel":
			generator_hasel()
			wyczysc_ekran()
			print("Jesteś z powrotem w Zuwiik. Siema!, co teraz?")

		elif komenda == "kalkulator":
			moj_kalkulator()
			wyczysc_ekran()
			print("Jesteś z powrotem w Zuwiik. Siema! co teraz?")

		elif komenda == "gra zgad":
			gra_w_zgadywanie()
			wyczysc_ekran()
			print("Jesteś z powrotem w Zuwiik. Siema! co teraz?")

		elif komenda == "gra wyscig":
			gra_wyscig()
			wyczysc_ekran()
			print("Jesteś z powrotem w Zuwiik. Siema! co teraz?")

		elif komenda == "clear":
			wyczysc_ekran()

		elif komenda == "start":
			start()

		elif komenda == "info":
			info()

		elif komenda == "exit" or komenda == "wyjdz":
			print("Zamykanie Zuwiika... Do zobaczenia!")
			sys.exit()

		elif komenda == "":
			continue

		elif komenda == "ustawienia":
			pass

		else:
			print(f"Nie znam komendy '{komenda}'. Wpisz 'help' po listę.")

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Użycie: zainstaluj <pakiety>")
	else:
		zainstaluj(sys.argv[1:])
	main()