class Board:
    def __init__(self, szerokosc, wysokosc):
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.pozioma = [[False for x in range(self.szerokosc)] for y in range(self.wysokosc + 1)]
        self.pionowa = [[False for x in range(self.szerokosc + 1)] for y in range(self.wysokosc)]