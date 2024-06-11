from PIL import Image, ImageDraw, ImageTk
import random
from numpy import sort
from tkinter import Tk, ttk
import tkinter as tk


zoom_scale = 1.0
width = 500
height = 400
viewport_width = 400
viewport_height = 400
viewportX = width//2 - (viewport_width//2)
viewportY = height//2 -(viewport_height//2)
root = tk.Tk()
root.title("Desain IKN City _ PAA")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
map_label = ttk.Label(frame)


class MyMap:
    def __init__(self) -> None:
        self.skala = 10
        self.lebar = 150 * self.skala
        self.tinggi = 150*self.skala
        self.vertex = [(self.lebar, self.tinggi)]
        self.base_map = Image.new("RGBA" , (self.lebar, self.tinggi), "gray")
        self.editMap = ImageDraw.Draw(self.base_map)
        self.panjang_jalan = 0
        self.lebar_jalan = 20
        self.bangunanHorizontal = [
            Image.open("asset/bangunan/building-largeH.jpg").resize((100,50)),
            Image.open("asset/bangunan/building-largeH_B.jpg").resize((100,50)),
            Image.open("asset/bangunan/building-largeH_C.jpg").resize((100,50)),
            Image.open("asset/bangunan/building-largeH_D.jpg").resize((100,50)),
            Image.open("asset/bangunan/building-mediumH.jpg").resize((50,30)),
            Image.open("asset/bangunan/building-mediumH_B.jpg").resize((50,30)),
            Image.open("asset/bangunan/building-smallH.jpg").resize((20,20))
        ]

        self.bangunanVertikal = [
            Image.open("asset/bangunan/building-mediumV.jpg").resize((30, 50)),
            Image.open("asset/bangunan/building-mediumV_B.jpg").resize((30, 50))
        ]

        self.lainnya = [
            Image.open("asset/lainnya/rumput1.jpg").resize((20,20)),
            Image.open("asset/lainnya/rumput2.png").resize((20,20)),
            Image.open("asset/lainnya/rumput3.png").resize((20,20))
        ]

    def batas(self, arah, titik):
        if titik < 0:  vertex = self.lebar
        elif titik < self.lebar: vertex = titik
        else : vertex = 0
        return vertex

    def createLine(self, start, end , arah):
        while start[0] < end[0] -10 and arah == "h":
            self.editMap.line(((start[0] + 10, start[1] + 10),(start[0] + 20, start[1] + 10)),"white",2)
            start[0] += 30
        while start[1] < end[1] - 10 and arah == "v":
            self.editMap.line(((start[0] + 10, start[1] + 10),(end[0] + 10, start[1] + 20)),"white",2)
            start[1] += 30

    def createJalan(self, titikAwal, titikAkhir):
        arah = "v"
        titikSekarang = titikAwal
        while titikSekarang != titikAkhir and self.panjang_jalan < 150:
            direction = random.choice([-1, 1])
            if arah == "v":
                nextTitik = (titikSekarang[0], titikSekarang[1] + (random.choice([30, 60]) * 10 * direction))
            if arah == "h":
                nextTitik = (titikSekarang[0] + (random.choice([30, 60]) * 10 * direction), titikSekarang[1])
            if (nextTitik[0] >= self.lebar or nextTitik[0] < 0) and (nextTitik[1] < 0 or nextTitik[1] > self.tinggi) and self.panjang_jalan >= 120: break
            titikX = sort([titikSekarang[0] +(20 if titikSekarang[0] > nextTitik[0] and arah == "h" else 0), nextTitik[0]  ] )
            titikY = sort([titikSekarang[1] +(20 if titikSekarang[1] > nextTitik[1] and arah == "v" else 0), nextTitik[1]])
            if nextTitik not in self.vertex: self.vertex.append(nextTitik)
            self.editMap.rectangle((((titikX[0], titikY[0]), (titikX[1] + (self.lebar_jalan if arah == "v" else 0), titikY[1] + (self.lebar_jalan if arah == "h" else 0)))), "black")
            self.createLine([titikX[0], titikY[0]],[titikX[1], titikY[1]],arah)
            if nextTitik[0] < self.lebar and nextTitik[1] < self.tinggi: arah = "h" if arah == "v" else "v"
            titikSekarang = (self.batas("x", nextTitik[0]), self.batas("y", nextTitik[1]))
            self.panjang_jalan += 1


    points = []
    def renderArea(self, ranges):
        orderedX = sort([ranges[0][0] , ranges[1][0]]) + (30,-10)
        orderedY = sort([ranges[0][1], ranges[1][1]]) + (30,-10)
        if orderedX[1] <= orderedX[0] : return
        if orderedY[1] <= orderedY[0] : return
        self.editMap.rectangle(((orderedX[0], orderedY[0]), (orderedX[1], orderedY[1])), "gray")
        self.editMap.rectangle(((orderedX[0], orderedY[0]), (orderedX[1], orderedY[1])), "green")
        y = orderedY[0]
        while y < orderedY[1]:
            x = orderedX[0]
            while x < orderedX[1]:
                if abs(y-orderedY[0]) < 20 or abs(y-orderedY[1]) < 120 : 
                    if x + 100 > orderedX[1] :break
                    image = random.choice(self.bangunanHorizontal)
                    self.base_map.paste(image, (x,y))
                    x += image.size[0] + 20
                elif abs(x-orderedX[0]) < 20 or abs(x-orderedX[1]) < 100: 
                    if x + 70 > orderedX[1] : break
                    image =random.choice(self.bangunanVertikal)
                    if abs(x-orderedX[0]) < 20  : self.base_map.paste(image, (x,y))
                    else : self.base_map.paste(image, (orderedX[1]- image.size[0],y))
                    x += image.size[0] + 20
                else : 
                    if x + 60 > orderedX[1] : break
                    image = random.choice(self.lainnya)
                    self.base_map.paste(image ,(random.randint(x,x+30),random.randint(y, y+30)))
                    x += image.size[0] + 40
            y += 70

    def scan(self):
        for titik in self.vertex:
            x,y = 0, 0
            for near in self.vertex:
                if titik != near and near[0] < titik[0] and near[1] < titik[1]:
                    x = near[0] if near[0] < titik[0] and near[0]  >x  else x
                    y = near[1] if near[1] < titik[1] and near[1] > y else y
            if x >= 0 or y >= 0 and ( (x,y), titik) not in self.points:  
                self.points.append(( (x,y), titik))
                if (x,y) not in self.vertex : self.vertex.append((x,y))
                if (x,titik[1]) not in self.vertex :self. vertex.append((x,titik[1]))
                if (titik[0],y) not in self.vertex : self.vertex.append((titik[0],y))
                self.renderArea(( (x,y), titik)) 

Maps = None

def refresh():
    global Maps
    cropped_map = Maps.crop((viewportX * zoom_scale, viewportY * zoom_scale, viewportX* zoom_scale + viewport_width* zoom_scale, viewportY* zoom_scale + viewport_height* zoom_scale))
    resized_map = cropped_map.resize((width, height))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    

def GenerateMap():
    global Maps
    titikAwal = (0,0)
    titikAkhir = (1000, 0)
    myMap = MyMap()
    myMap.createJalan(titikAwal, titikAkhir)
    myMap.scan()
    myMap.base_map.save("map.png");
    Maps = myMap.base_map
    cropped_map = myMap.base_map.crop((viewportX, viewportY, viewportX + viewport_width, viewportY + viewport_height))
    resized_map = cropped_map.resize((width, height))
    img_tk = ImageTk.PhotoImage(resized_map)
    map_label.config(image=img_tk)
    map_label.image = img_tk
    refresh()

GenerateMap()

def scroll(event):
    global viewportX, viewportY, zoom_scale
    if event.delta > 0:
        if zoom_scale > 0.5: zoom_scale -= 0.1
    else:
        if zoom_scale < 4.0:zoom_scale += 0.1
    refresh()
            
def key_pressed(event):
    global viewportY, viewportX
    if event.keysym == 'a' and viewportX > 0: viewportX -= 20
    elif event.keysym == 's' and viewportY < (height  + viewport_height)// zoom_scale:viewportY += 20
    elif event.keysym == 'd' and viewportX < (width + viewport_width)// zoom_scale: viewportX += 20
    elif event.keysym == 'w' and  viewportY > 0:viewportY -= 20
    refresh()

root.bind("<MouseWheel>", scroll)
root.bind("<KeyPress-a>", key_pressed)
root.bind("<KeyPress-s>", key_pressed)
root.bind("<KeyPress-d>", key_pressed)
root.bind("<KeyPress-w>", key_pressed)
map_label.grid(row=0, column=0, padx=10, pady=10)

generate_button = ttk.Button(root, text="Generate Map", command=GenerateMap)
generate_button.grid(row=1, column=0, pady=10)
GenerateMap()
root.mainloop()
        
