import random
import pygame
from tkinter import *
import time

pygame.font.init()

WIDTH, HEIGHT = 360, 360
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (211, 211, 211)
FPS = 10

FONT = pygame.font.SysFont('comicsans', 30)


class Aloitus:
    """Piirtää aloitusnäytön, jossa pystyy valitsemaan vaikeustason"""

    def __init__(self):
        self.window = Tk()
        self.taso = None

        self.vaikeus_taso_teksti = Label(self.window, text=f"Valitse vaikeustaso", relief=FLAT)
        self.vaikeus_taso_teksti.grid(row=0, columnspan=6)

        self.helppo_teksti = Button(self.window, text="Helppo", relief=RAISED, background="green",
                                    fg="white", command=self.helppo)
        self.helppo_teksti.grid(row=1, column=0, columnspan=2)

        self.keskitaso_teksti = Button(self.window, text="Keskitaso", relief=RAISED, background="blue",
                                       fg="white", command=self.keskitaso)
        self.keskitaso_teksti.grid(row=1, column=2, columnspan=2)

        self.vaikea_teksti = Button(self.window, text="Vaikea", relief=RAISED, background="red",
                                    fg="white", command=self.vaikea)
        self.vaikea_teksti.grid(row=1, column=4, columnspan=2)

        self.window.mainloop()

    def helppo(self):
        self.window.destroy()
        self.taso = "H"
        return self.taso

    def keskitaso(self):
        self.window.destroy()
        self.taso = "K"
        return self.taso

    def vaikea(self):
        self.window.destroy()
        self.taso = "V"
        return self.taso


class Lopetus:
    """Piirtää lopetusruudun, jossa näkyy suorituksen aika ja virheiden määrä.
        Mahdollisuus aloittaa uusi peli tai poistua."""

    def __init__(self, virheet, aika):
        self.window = Tk()
        self.virheet = virheet
        self.aika = aika
        self.lopetus = None

        self.onnittelu_teksti = Label(self.window, text=f"Onnittelut voitit pelin!", relief=FLAT)
        self.onnittelu_teksti.grid(row=0, columnspan=6)

        self.virhe_teksti = Label(self.window, text=f"Sinulla oli {self.virheet} virhettä.", relief=FLAT, fg="red")
        self.virhe_teksti.grid(row=1, columnspan=6)

        self.aika = Label(self.window, text=f"Pelin suoritus kesti {self.aika: .0f} sekuntia.", relief=FLAT)
        self.aika.grid(row=2, columnspan=6)

        self.paina = Label(self.window, text=f"Paina", relief=FLAT)
        self.paina.grid(row=3, column=0)

        self.uudestaan = Button(self.window, text="tästä", relief=FLAT, command=self.new_game, background="green")
        self.uudestaan.grid(row=3, column=1)

        self.loppu = Label(self.window, text=", jos haluat pelata uudelleen.", relief=FLAT)
        self.loppu.grid(row=3, column=2)

        self.lopeta = Button(self.window, text="Quit", relief=FLAT, command=self.quit, background="red")
        self.lopeta.grid(row=4, column=5)

        self.window.mainloop()

    def new_game(self):
        self.window.destroy()
        self.lopetus = True
        return self.lopetus

    def quit(self):
        self.window.destroy()
        self.lopetus = False
        return self.lopetus


def lauta(taso):
    """Määrittää pelilaudan, sekä siirtää tiedon vaikeustasosta taytto -funktiolle"""

    summa = 0

    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]

    game_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    ratkaisu(board)

    if taso == "V":
        vaikeus = 45
        game_board, summa = taytto(board, game_board, vaikeus, summa)
    elif taso == "K":
        vaikeus = 30
        game_board, summa = taytto(board, game_board, vaikeus, summa)
    elif taso == "H":
        vaikeus = 10
        game_board, summa = taytto(board, game_board, vaikeus, summa)

    return board, game_board, summa


def taytto(board, game_board, vaikeus, summa):
    """Luo sattumanvaraisesti lukuja pelilaudalle vaikeustason antaman määrän."""

    count = 0
    while 81 - count > vaikeus:
        rivi = random.randint(0, 8)
        luku = random.randint(0, 8)
        game_board[rivi].pop(luku)
        game_board[rivi].insert(luku, board[rivi][luku])
        count += 1

    for rivi in game_board:
        for luku in rivi:
            if luku == 0:
                summa += 1
    return game_board, summa


def ratkaisu(board):

    """Luo sattumanvaraisesti oikean ratkaisun laudalle logiikka -funktion avulla."""

    for rivi in board:

        while rivi.count(0) > 0:

            muunnettava_luku = random.randint(0, 8)
            valinta = logiikka(board, rivi, muunnettava_luku)

            if len(valinta) == 0:
                continue
            board[board.index(rivi)].pop(muunnettava_luku)
            board[board.index(rivi)].insert(muunnettava_luku, random.choice(valinta))

    return board


def logiikka(board, muunnettava_rivi, muunnettava_luku):

    """Tämä funktio vastaa laudan täyttämisestä sudokun logiikan ehdoilla."""

    valinta = []
    laatikko_vaaka = []
    laatikko = []
    pysty_rivi = []

    if muunnettava_luku == 0 or muunnettava_luku == 1 or muunnettava_luku == 2:
        laatikko_vaaka = [0, 3]
    elif muunnettava_luku == 3 or muunnettava_luku == 4 or muunnettava_luku == 5:
        laatikko_vaaka = [3, 6]
    elif muunnettava_luku == 6 or muunnettava_luku == 7 or muunnettava_luku == 8:
        laatikko_vaaka = [6, 9]

    if board.index(muunnettava_rivi) == 0 or board.index(muunnettava_rivi) == 1 or board.index(muunnettava_rivi) == 2:
        laatikko = [board[0][laatikko_vaaka[0]: laatikko_vaaka[1]],
                    board[1][laatikko_vaaka[0]: laatikko_vaaka[1]],
                    board[2][laatikko_vaaka[0]: laatikko_vaaka[1]]]
    elif board.index(muunnettava_rivi) == 3 or board.index(muunnettava_rivi) == 4 or board.index(muunnettava_rivi) == 5:
        laatikko = [board[3][laatikko_vaaka[0]: laatikko_vaaka[1]],
                    board[4][laatikko_vaaka[0]: laatikko_vaaka[1]],
                    board[5][laatikko_vaaka[0]: laatikko_vaaka[1]]]
    elif board.index(muunnettava_rivi) == 6 or board.index(muunnettava_rivi) == 7 or board.index(muunnettava_rivi) == 8:
        laatikko = [board[6][laatikko_vaaka[0]: laatikko_vaaka[1]],
                    board[7][laatikko_vaaka[0]: laatikko_vaaka[1]],
                    board[8][laatikko_vaaka[0]: laatikko_vaaka[1]]]

    uusi_laatikko = []
    for kolmikko in laatikko:
        for numero in kolmikko:
            uusi_laatikko.append(numero)

    for rivi in board:
        pysty_rivi.append(rivi[muunnettava_luku])

    for luku in range(1, 10):
        if luku not in board[board.index(muunnettava_rivi)] and luku not in uusi_laatikko and luku not in pysty_rivi:
            valinta.append(luku)

    return valinta


def draw_rectangles(game_board, board, sijainti, uusi, toimii, location, text, summa):

    """Piirtää pelilaudan ja luvut näkyviin."""

    WIN.fill(WHITE)
    neliot = {}
    # Vasen yläkulma joka toinen harmaa
    rivi = -2
    for y in range(0, 360, 80):
        rivi += 2
        luku = 0
        for x in range(0, 360, 80):
            pygame.draw.rect(WIN, LIGHT_GRAY, pygame.Rect(x, y, 40, 40))
            neliot[(x, y)] = board[rivi][luku]
            if game_board[rivi][luku] == 0:
                WIN.blit(FONT.render("", True, BLACK), (x + 11, y - 1))
                luku += 2

            else:
                WIN.blit(FONT.render(str(game_board[rivi][luku]), True, BLACK), (x + 11, y - 1))
                luku += 2
    # Toinen rivi, toinen harmaa
    rivi = -1
    for y in range(40, 320, 80):
        rivi += 2
        luku = 1
        for x in range(40, 320, 80):
            pygame.draw.rect(WIN, LIGHT_GRAY, pygame.Rect(x, y, 40, 40))
            neliot[(x, y)] = board[rivi][luku]
            if game_board[rivi][luku] == 0:
                WIN.blit(FONT.render("", True, BLACK), (x + 11, y - 1))
                luku += 2
            else:
                WIN.blit(FONT.render(str(game_board[rivi][luku]), True, BLACK), (x + 11, y - 1))
                luku += 2
    # Toinen rivi, valkoinen
    rivi = -1
    for y in range(40, 360, 80):
        rivi += 2
        luku = 0
        for x in range(0, 360, 80):
            pygame.draw.rect(WIN, WHITE, pygame.Rect(x, y, 40, 40))
            neliot[(x, y)] = board[rivi][luku]
            if game_board[rivi][luku] == 0:
                WIN.blit(FONT.render("", True, BLACK), (x + 11, y - 1))
                luku += 2
            else:
                WIN.blit(FONT.render(str(game_board[rivi][luku]), True, BLACK), (x + 11, y - 1))
                luku += 2
    # Ensimmäinen rivi, valkoinen
    rivi = -2
    for y in range(0, 360, 80):
        rivi += 2
        luku = 1
        for x in range(40, 360, 80):
            pygame.draw.rect(WIN, WHITE, pygame.Rect(x, y, 40, 40))
            neliot[x, y] = board[rivi][luku]
            if game_board[rivi][luku] == 0:
                WIN.blit(FONT.render("", True, BLACK), (x + 11, y - 1))
                luku += 2
            else:
                WIN.blit(FONT.render(str(game_board[rivi][luku]), True, BLACK), (x + 11, y - 1))
                luku += 2
    if toimii:
        muutettava_teksti = FONT.render(text, True, BLACK)
        pygame.draw.rect(WIN, LIGHT_BLUE, pygame.Rect(location[0], location[1], 40, 40))
        WIN.blit(muutettava_teksti, (location[0] + 11, location[1] + 1))

        # Viivat pelilautaan
    for x in range(40, 360, 40):
        if x % 120 == 0:
            pygame.draw.rect(WIN, BLACK, pygame.Rect(x, 0, 4, HEIGHT))
        else:
            pygame.draw.rect(WIN, BLACK, pygame.Rect(x, 0, 2, HEIGHT))
    for y in range(40, 360, 40):
        if y % 120 == 0:
            pygame.draw.rect(WIN, BLACK, pygame.Rect(0, y, WIDTH, 4))
        else:
            pygame.draw.rect(WIN, BLACK, pygame.Rect(0, y, WIDTH, 2))

    if sijainti != ():
        summa -= 1
        uusi.update({sijainti: neliot[sijainti]})

    for paikka in uusi.keys():
        WIN.blit(FONT.render(str(uusi[paikka]), True, BLACK), (paikka[0] + 11, paikka[1] - 1))
    sijainti = ()
    pygame.display.update()
    return neliot, summa, sijainti


def testaus(location, neliot, virheet, text):

    """Tarkistaa onko syötetty luku oikein vai väärin."""

    oikein = []

    if text == str(neliot[location]):
        oikea = 1
        oikein.append(oikea)
        return oikein, virheet

    elif text != str(neliot[location]):
        virheet += 1
        WIN.blit(FONT.render(text, True, RED), (location[0] + 11, location[1] + 1))
        pygame.display.update()
        pygame.time.wait(2000)
        return oikein, virheet


def main():
    aloitus = Aloitus()
    text = ""
    board, game_board, summa = lauta(aloitus.taso)
    clock = pygame.time.Clock()
    virheet = 0
    run = True
    sijainti = ()
    uusi = {(-40, -40): 0}
    aktiivinen = False
    toimii = False
    start_time = time.time()
    location = ()
    while run:
        aika = time.time() - start_time
        clock.tick(FPS)
        neliot, summa, sijainti = draw_rectangles(game_board, board, sijainti, uusi, toimii, location, text, summa)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

                # TAB -näppäintä painamalla saat oikean vastauksen näkyviin 3 sekunniksi
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    draw_rectangles(board, board, sijainti, uusi, toimii, location, text, summa)
                    pygame.time.delay(3000)
                # Jos painat pelilaudan neliötä pystyt kirjoittamaan kyseiseen neliöön
            if event.type == pygame.MOUSEBUTTONDOWN:
                for nelio in neliot.keys():
                    if pygame.mouse.get_pressed()[0] and \
                            pygame.draw.rect(WIN, WHITE, pygame.Rect(nelio[0], nelio[1],
                                                                     40, 40)).collidepoint(pygame.mouse.get_pos()):
                        aktiivinen = True
                        location = (nelio[0], nelio[1])
                        toimii = True
                # Kun olet syöttänyt luvun ja painat Enter -näppäintä vastaus tallentuu ruudulle
            if event.type == pygame.KEYDOWN:
                if aktiivinen:
                    if event.key == pygame.K_RETURN:
                        oikein, virheet = testaus(location, neliot, virheet, text)
                        try:
                            if len(oikein) != 0:
                                sijainti = location
                                toimii = False
                                aktiivinen = False
                                text = ""
                            else:
                                toimii = False
                                aktiivinen = False
                                text = ""

                        except TypeError:
                            toimii = False
                            aktiivinen = False
                            text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            # Kun kaikki ruudut ovat täytetty Lopetus -luokan ruutu tulee näkyviin
        if summa == 0:
            loppu = Lopetus(virheet, aika)
            if loppu.lopetus:
                main()
            else:
                return


if __name__ == "__main__":
    main()
