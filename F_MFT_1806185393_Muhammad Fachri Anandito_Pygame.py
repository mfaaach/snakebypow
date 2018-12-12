""" TP 4 | 'Snake' by Muhammad Fachri Anandito | 1806185393 | DDP1-F | Asdos : MFT """

import random
import math
import pygame
from tkinter import *
from tkinter.messagebox import showinfo

## Membuat Class Objek yang memuat perintah menggambar untuk objek pygame pada surface
class Objek:
    kolom = 25
    lebar = 500

    ## Membuat fungsi initiator untuk membuat objek
    def __init__(self,mulai,dirx=1,diry=0,warna=(111, 60, 137)):
        self.pos  = mulai
        self.dirx = 1
        self.diry = 0
        self.warna = warna

    ## Fungsi untuk membuat tiap kotak bergerak
    def gerak(self,dirx,diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    ## Fungsi untuk menggambar kotak pada surface
    def gambar_kotak(self, layar, mata = False):
        jarak = self.lebar // self.kolom
        i = self.pos[0]
        j = self.pos[1]
        
        ## Jika nilai mata = True, maka akan digambar mata
        if mata:
            tengah = jarak//2
            radius = 3
            MataKiri = (i*jarak + tengah - radius, j*jarak + 8)
            MataKanan = (i*jarak + jarak - radius*2, j*jarak + 8)
            pygame.draw.rect(layar, (167, 136, 168), (i*jarak,j*jarak,jarak,jarak))
            pygame.draw.circle(layar, (0,0,0), MataKiri, radius)
            pygame.draw.circle(layar, (0,0,0), MataKanan, radius)

        else:
            pygame.draw.rect(layar, self.warna, (i*jarak,j*jarak,jarak,jarak))


    ## Fungsi untuk menggambar makanan berupa apel pada surface
    def gambar_apel(self,layar):

        jarak = self.lebar // self.kolom
        i = self.pos[0]
        j = self.pos[1]
        rad = 10

        pygame.draw.circle(layar, self.warna,(jarak*i+10,jarak*j+10), 10)
        pygame.draw.line(layar, (0,255,0), (jarak*i+9,jarak*j-2),(jarak*i+9,jarak*j+8),2)


## Membuat class snake untuk badan dan gerakan snake
class Snake:
    ## Membuat set kosong untuk menyimpan belokan dan list kosong untuk menyimpan panjang badan
    belokan = {}
    badan = []

    ## Membuat fungsi initiator untuk menyimpan beberapa variabel penting
    def __init__(self,warna,pos):
        self.warna = warna
        self.pala = Objek(pos)
        self.badan.append(self.pala)
        self.dirx = 1
        self.diry = 0

    ## Fungsi untuk mengatur gerak snake
    def gerak(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        ## Menyimpan tombol yg dipencet di keyboard di sebuah variabel
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        ## Algoritma untuk mengatur gerakan snake sesuai pencetan tombol
        for key in keys:

            if keys[pygame.K_UP]:
                self.dirx = 0
                self.diry = -1
                self.belokan[self.pala.pos[:]] = [self.dirx,self.diry]

            if keys[pygame.K_DOWN]:
                self.dirx = 0
                self.diry = 1
                self.belokan[self.pala.pos[:]] = [self.dirx,self.diry]

            if keys[pygame.K_LEFT]:
                self.dirx = -1
                self.diry = 0
                self.belokan[self.pala.pos[:]] = [self.dirx,self.diry]

            if keys[pygame.K_RIGHT]:
                self.dirx = 1
                self.diry = 0
                self.belokan[self.pala.pos[:]] = [self.dirx,self.diry]

        ## Akgoritma untuk ketika snake belok
        for i,o in enumerate(self.badan):
            p = o.pos[:]

            if p in self.belokan:
                belok = self.belokan[p]
                o.gerak(belok[0],belok[1])

                if i == len(self.badan)-1:
                    self.belokan.pop(p)

            ## Algoritma jika snake sampai di ujung layar akan teleport ke ujung satunya
            else:
                if o.dirx == -1 and o.pos[0] <= 0:
                     o.pos = (o.kolom-1, o.pos[1])
                elif o.dirx == 1 and o.pos[0] >= o.kolom-1:
                     o.pos = (0,o.pos[1])
                elif o.diry == 1 and o.pos[1] >= o.kolom-1:
                     o.pos = (o.pos[0], 0)
                elif o.diry == -1 and o.pos[1] <= 0:
                     o.pos = (o.pos[0],o.kolom-1)
                else:
                    o.gerak(o.dirx,o.diry)

    ## Fungsi untuk mereset game snake setelah menabrak
    def reset(self,pos):
        global skor
        self.pala = Objek(pos)
        self.badan = []
        self.badan.append(self.pala)
        self.belokan = {}
        self.dirx = 1
        self.diry = 0
        skor = 0

    ## Fungsi untuk menambah panjang snake ketika memakan snack
    def updateKotak(self):
        buntut = self.badan[-1]
        dx, dy = buntut.dirx, buntut.diry

        if dx == 1 and dy == 0:
            self.badan.append(Objek((buntut.pos[0]-1,buntut.pos[1])))
        elif dx == -1 and dy == 0:
            self.badan.append(Objek((buntut.pos[0]+1,buntut.pos[1])))
        elif dx == 0 and dy == 1:
            self.badan.append(Objek((buntut.pos[0],buntut.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.badan.append(Objek((buntut.pos[0],buntut.pos[1]+1)))

        self.badan[-1].dirx = dx
        self.badan[-1].diry = dy

    def gambar(self,layar):
        for i,o in enumerate(self.badan):
            if i == 0:
                o.gambar_kotak(layar,True)
            else:
                o.gambar_kotak(layar)
        
## Fungsi untuk menghasilkan posisi random untuk makanan snake
def random_makanan(kolom,benda):
    posisi = benda.badan

    while True:

        x = random.randrange(kolom)
        y = random.randrange(kolom)

        lst = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(0,1),(0,2),(0,3),(0,4)]

        if len(list(filter(lambda e:e.pos == (x,y),posisi))) > 0:
            continue
        elif len(list(filter(lambda e:e == (x,y), lst))) > 0:
            continue
        else:
            break

    return(x,y)

## Fungsi untuk menampilkan message box ketika snake menabrak dirinya sendiri
def messageBox(judul,isi):
    root = Tk()
    root.attributes("-topmost",True)
    root.withdraw()
    showinfo(judul,isi)
    try:
        root.destroy()
    except:
        pass

## Fungsi untuk merefresh layar tiap loop
def redraw(layar):
    global lebar, kolom, snake, snack, bg, text_skor, text_hs   
    layar.blit(bg, (0, 0))
    snake.gambar(layar)
    snack.gambar_apel(layar)
    layar.blit(text_skor,(0, 20))
    layar.blit(text_hs,(0,0)) 
    pygame.display.update()


## Program Utama
def main():

    # Mengglobalkan variabel supaya bisa diakses diluar fungsi dan didalam class-class di atas
    global lebar, kolom, snake, snack, bg, text_skor, text_hs, skor, vel
    pygame.init()       # Menginisiasi modul yang ada di pygame

    # Mengatur dimensi untuk game
    lebar = 500
    kolom = 25
    surf = pygame.display.set_mode((lebar,lebar))

    # Memuat gambar background serta membuat objek snake dan makanannya
    bg = pygame.image.load("wood.png")
    snake = Snake((0,0,255),(5,5))
    snack = Objek(random_makanan(kolom,snake),warna=(255,0,0))
    skor = 0

    # Memuat font untuk ditampilkan di surface
    myfont = pygame.font.SysFont('Seoge UI', 30)

    # Membuat variabel untuk menyimpan modul time clock untuk nantinya diberi tick
    clock = pygame.time.Clock()

    # Loop utama
    while True:
        clock.tick(15)                              # Memberi 15 frame per second pada game
        pygame.time.delay(50)                       # Memberi delay pada game
        snake.gerak()

        # Mengakses file highscore untuk menampilkan skor tertinggi
        file_ = open('High Score Snake.txt')
        highscore = int(file_.readline())
        file_.close()

        # Memuat text yang akan di tampilkan nantinya di surface pygame
        text_skor = myfont.render('Skor : {}'.format(skor), True, (255, 255, 255))
        text_hs = myfont.render('Skor Tertinggi : {}'.format(highscore),True,(255,255,255))

        # Algoritma supaya nantinya ketika snake memakan snack akan mengakibatkan skor bertambah dan badan tambah panjang
        if snake.badan[0].pos == snack.pos:
            snake.updateKotak()
            snack = Objek(random_makanan(kolom,snake),warna=(255,0,0))
            skor += 1
            
            # if len(snake.badan) >= 10 and (len(snake.badan) % 10) == 0:
            #     vel += 5

        # Memeriksa jika snake memakan dirinya sendiri atau tidak
        for i in range(len(snake.badan)):
            if snake.badan[i].pos in list(map(lambda e:e.pos, snake.badan[i+1:])):
                messageBox('Ouch!!', '''Anda memakan diri anda sendiri
         Skor Anda adalah {}
                
                main lagi...'''.format(len(snake.badan)-1))

                # Meng-override high score jika skor ternyata lebih tinggi
                if skor > highscore:
                    file_ = open('High Score Snake.txt','w')
                    print(str(skor),file=file_)
                    file_.close()
                    snake.reset((5,5))

                else:
                    snake.reset((5,5))

                break

        # Menggambar ulang surface
        redraw(surf)

# Menjalankan Program Utama
if __name__ == '__main__':
    main()