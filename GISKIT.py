import tkinter as tk
# from tkinter import *
from tkinter import Tk, Frame, Label, Button, ttk, Checkbutton
from tkinter import BOTH, X, Y, LEFT, RIGHT, TOP, BOTTOM, END
from tkinter import Menu, Canvas, PhotoImage, Scrollbar
from tkinter import IntVar, BooleanVar, messagebox, filedialog, Entry
from PIL import Image, ImageTk
import geopandas as gp
import matplotlib.pyplot as plt
import rasterio
import os
import matplotlib
import fiona
import numpy as np
from osgeo import gdal, ogr, osr, gdalconst, gdalnumeric
import libpysal
import mapclassify
import rasterio.features
from shapely import geometry
from shapely.geometry import shape, mapping
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry import MultiLineString, LineString, Point, MultiPoint, Polygon

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import random
from os.path import exists

plt.interactive(True)
import rasterio.mask
from rasterio.plot import show
from rasterio.warp import calculate_default_transform, reproject, Resampling

listOfDirec = ['', '']  # lista direktorijuma za odredjene metode
listaKoordinata = ['']  # lista koordinata za odredjene metode
fajlZaCRS = ['', '']  # lista fajlova za odredjene metode
listaVekRas = []  # lista ucitanih vektora i rastera
fig = Figure()  # formiranje figure za prikaz fajlova


class VekRas:  # konstruktor za kreiranje objekta tipa Vektor ili Raster
    def __init__(self, directory, tip, listOfAttributes):
        self.directory = directory  # atribut koji pokazuje putanju do fajla
        self.name = os.path.basename(directory)  # atribut koji pokazuje naziv fajla
        self.type = tip  # atribut koji pokazuje tip fajla (vektor ili raster)
        self.listOfAttributes = listOfAttributes  # atribut koji pokazuje listu atributa tog fajla
        lista.insert(END, self.name)  # dodavanje fajla na listu interfejsa
        lista.itemconfig(END, {'bg': 'white'})  # podesavanje pozadine


fileOpcijeV = dict(defaultextension='.shp',  #
                   filetypes=[('ESRI Shapefile', '*.shp'), ('AutoCad DWG', '*.dwg'), ('AutoCad DXF', '*.dxf'),
                              ('All files', '*.*')])

fileOpcijeR = dict(defaultextension='.img',  #
                   filetypes=[('DISC Image File', '*.img'), ('TIFF', '*.tiff'), ('PNG', '*png'), ('JPEG', '*.jpeg'),
                              ('All files', '*.*')])


def changingColors(indeks):  # metoda koja sluzi da promjeni boju pozadine fajla koji je prikazan,
    for x in range(
            len(listaVekRas)):  # prima promjenljivu 'indeks' koja pokazuje koji fajl u listi treba da se promjeni
        lista.itemconfig(x, {'bg': 'white'})
    lista.itemconfig(indeks, {'bg': color})


def closeprogram():  # metoda koja sluzi za gasenje aplikacije
    poruka = tk.messagebox.askquestion("Close", "Are you sure you want to exit the program?")
    if poruka == 'yes':
        prozor.destroy()
    elif poruka == 'no':
        return


def preview():  # metoda koja sluzi za prikaz fajla
    try:
        nekiNiz = lista.curselection()  # preuzimanje indeksa odabranog clana iz liste
        indeks = nekiNiz[0]
        if listaVekRas[indeks].type == 'raster':  # provjera da li je fajl tipa raster ili vektor
            fig.clf()
            fajl = listaVekRas[indeks].directory
            raster = rasterio.open(fajl)
            src = raster.read(1)
            ax = fig.gca()
            ax.set_anchor('SW')
            ax.set_axis_off()
            ax.format_coord = lambda x, y: " ".format(x, y)
            ax.imshow(src)
            ram.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
            canvas.draw()
        elif listaVekRas[indeks].type == 'vektor':
            fig.clf()
            fajl1 = listaVekRas[indeks].directory
            shp = gp.read_file(fajl1, encoding='utf-8')
            ax = fig.gca()
            ax.set_anchor('SW')
            ax.set_axis_off()
            ax.format_coord = lambda x, y: " ".format(x, y)
            shp.plot(ax=ax, cmap='inferno')
            ram.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
            canvas.draw()
            plt.close()
        changingColors(indeks)
    except IndexError:  # ako korisnik ne izabere fajl iz liste a pozove funkciju, ispisuje se poruka
        messagebox.showerror(title='Error', message='Choose a file first.', parent=prozor)


def openVector():  # metoda koja sluzi za ucitavanje vektora
    try:
        file1 = filedialog.askopenfilename(**fileOpcijeV)  # otvaranje prozora za biranje fajla
        shp = gp.read_file(file1, encoding='utf-8')  # citanje fajla
        listaAtributa = []
        for x in shp.columns:  # dodavanje atributa listi koja ce biti prosljedjena kreiranju objekta
            listaAtributa.append(x)
        listaVekRas.append(VekRas(file1, 'vektor', listaAtributa))  # formiranje i ubacivanje fajla u listu
    except fiona.errors.DriverError:  # ako korisnik ne izabere nijedan fajl a zatvori prozor, ispisuje se poruka
        print('No file was picked.')


def openRaster():  # metoda koja sluzi za uticavanje rastera
    file = filedialog.askopenfilename(**fileOpcijeR)
    if file == '':  # ako korisnik ne izabere nijedan fajl a zatvori prozor, ispisuje se poruka
        print('No file was chosen.')
    else:
        src = rasterio.open(file)  # citanje fajla
        listaVekRas.append(VekRas(file, 'raster', ''))


def iskacuciProzorZaDelete():  # metoda koja pravi prozor da provjeri s korisnikom da li je siguran da zeli da obrise fajl
    if len(listaVekRas) == 0:  # ako je lista fajlova prazna, ispisuje se poruka
        messagebox.showerror(title='Error', message='There are no opened files.', parent=prozor)
    else:
        try:
            def brisanje():  # metoda koja sluzi za brisanje fajlova
                fig.clf()
                ram.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
                canvas.draw()
                nekiNiz = lista.curselection()
                indeks = nekiNiz[0]
                listaVekRas.pop(indeks)
                lista.delete(indeks)
                window.destroy()

            window = tk.Toplevel()
            nekiNiz = lista.curselection()
            indeks = nekiNiz[0]
            imeFajla = listaVekRas[indeks].name
            tekst = "Are you sure you want to delete file: " + imeFajla
            label = tk.Label(window, text=tekst)
            label.grid(row=0, column=0, padx=50, pady=5)
            button_close = tk.Button(window, text="Cancel", command=lambda: window.destroy())
            button_close.grid(row=1, column=0)
            button_delete = tk.Button(window, text="Delete", command=brisanje)
            button_delete.grid(row=2, column=0)
        except IndexError:  # ako lista fajlova sadrzi fajlove a nijedan nije izabran, ispisuje se poruka
            messagebox.showerror(title='Error', message='Choose a file first.', parent=prozor)


def presek():  # metoda koja otvara prozor za biranje fajlova za presjek
    listOfDirec[0] = ''
    presekProzor = tk.Toplevel(prozor)
    presekProzor.title("Intersection")
    presekProzor.geometry("300x200+50+50")
    presekProzor.grid()
    inputlayer = Label(presekProzor, text='Input layer:')
    inputlayer.grid(column=0, row=0)
    stringVar1 = tk.StringVar()
    ilejeri = ttk.Combobox(presekProzor, width=12, textvariable=stringVar1)
    ilejeri.grid(column=0, row=1)
    stringVar2 = tk.StringVar()
    overlaylayer = Label(presekProzor, text='Overlay layer:')
    overlaylayer.grid(column=0, row=2)
    olejeri = ttk.Combobox(presekProzor, width=20, textvariable=stringVar2)
    olejeri.grid(column=0, row=3)
    fileLocation = Label(presekProzor, text='Choose name and path for the new file:')
    fileLocation.grid(column=0, row=4)
    stringVar3 = tk.StringVar()
    outputLayer = Entry(presekProzor, textvariable=stringVar3)
    outputLayer.grid(column=0, row=5)

    def pathLocation():  # metoda koja sluzi za odabiranje lokacije novonastalog fajla
        listOfDirec[0] = filedialog.askdirectory(parent=presekProzor)

    outputButton = Button(presekProzor, command=pathLocation, image=imgDirectory)
    outputButton.image = imgDirectory
    outputButton.grid(column=1, row=5)
    for x in range(len(listaVekRas)):  # popunjavanje combobox-a fajlovima
        if listaVekRas[x].type == "vektor":
            ilejeri['values'] = (*ilejeri['values'], listaVekRas[x].name)
            olejeri['values'] = (ilejeri['values'])

    def presekRezultat():  # metoda koja vrsi uniju odabranih fajlova, uz obezbjedjivanje pravilnog koriscenja podataka
        vektor1 = ilejeri.get()
        vektor2 = olejeri.get()
        directory1 = ''
        directory2 = ''
        name1 = ''
        name2 = ''
        for x in range(len(listaVekRas)):
            if vektor1 == listaVekRas[x].name:
                directory1 = listaVekRas[x].directory
                name1 = listaVekRas[x].name
                break
        for x in range(len(listaVekRas)):
            if vektor2 == listaVekRas[x].name:
                directory2 = listaVekRas[x].directory
                name2 = listaVekRas[x].name
                break
        if directory1 == '' or directory2 == '':
            messagebox.showerror(title='Error', message='Fill in empty spots.', parent=presekProzor)
        elif directory1 == directory2:
            messagebox.showerror(title='Error', message='Both files are the same.', parent=presekProzor)
        elif outputLayer.get() == '':
            messagebox.showerror(title='Error', message='Input a name for the output file.', parent=presekProzor)
        elif listOfDirec[0] == '':
            messagebox.showerror(title='Error', message='Choose a location for the output file.', parent=presekProzor)
        else:
            file1 = gp.read_file(directory1, encoding='utf-8')
            file2 = gp.read_file(directory2, encoding='utf-8')
            if str(file1.crs) != str(file2.crs):
                messagebox.showerror(title='Error', message='Files don\'t have the same CRS.', parent=presekProzor)
            else:
                title = outputLayer.get() + '.shp'
                direc = os.path.join(listOfDirec[0], title)
                if exists(direc) == False:
                    p = gp.overlay(file1, file2, how="intersection", keep_geom_type=True)
                    if p.empty:
                        messagebox.showerror(title='Error', message='There\'s no intersection between these two files.',
                                             parent=presekProzor)
                    else:
                        p.to_file(direc, driver='ESRI Shapefile')
                        fig, ax = plt.subplots(figsize=(10, 10))
                        p.plot(ax=ax, cmap='Blues')
                        fig.align_labels()
                        ax.set_anchor('SW')
                        plt.close()
                        ram.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
                        canvas.draw()
                        listaAt = []
                        shp = gp.read_file(direc, encoding='utf-8')
                        for x in shp.columns:
                            listaAt.append(x)
                        listaVekRas.append(VekRas(direc, 'vektor', listaAt))
                else:
                    messagebox.showerror(title='Error', message='There\'s already an existing file with this name.',
                                         parent=presekProzor)

    run = Button(presekProzor, command=presekRezultat, text='Run')
    run.grid(column=0, row=6)


def statistika():  # metoda koja otvara prozor za biranje fajla za prikaz statistickih parametara
    statProzor = tk.Toplevel(prozor, bg='#e4edf5')
    statProzor.title('Read band statistics')
    statProzor.option_add('*font', ('Times', 12))
    statProzor.geometry('350x150+300+50')
    raster = Label(statProzor, text='Choose raster')
    raster.grid(row=0, column=0, pady=3)
    stringVar = tk.StringVar()
    rasteri = ttk.Combobox(statProzor, width=20, textvariable=stringVar)
    rasteri.grid(row=1, column=0, pady=10)
    for x in range(len(listaVekRas)):
        if listaVekRas[x].type == "raster":
            rasteri['values'] = (*rasteri['values'], listaVekRas[x].name)

    def citanjestat():  # metoda koja vrsi citanje i prikaz statistickih parametara fajla
        newWindow = tk.Toplevel(prozor, bg='#e4edf5')
        newWindow.title('Band statistics')
        newWindow.geometry('350x150+300+50')
        newWindow.option_add('*font', ('Times', 12))
        r = rasteri.get()
        directory = 'nesto'
        for x in range(len(listaVekRas)):
            if r == listaVekRas[x].name:
                directory1 = listaVekRas[x].directory
                ds = gdal.Open(directory1)
                count = ds.RasterCount
                response = {}
                for counter in range(1, count + 1):
                    stats = ds.GetRasterBand(counter).GetStatistics(0, 1)
                    response["band_{}".format(counter)] = "Minimum=%.3f, Maximum=%.3f, Mean=%.3f, StdDev=%.3f" % (
                    stats[0], stats[1], stats[2], stats[3])
                minm = stats[0]
                maxm = stats[1]
                mean = stats[2]
                stdev = stats[3]
        minimum = Label(newWindow, text='Minimum:', bg='#e4edf5')
        minimum.grid(row=0, column=0, padx=5)
        stat1 = Label(newWindow, text=minm, bg='#e4edf5')
        stat1.grid(row=0, column=1)
        maximum = Label(newWindow, text='Maximum:', bg='#e4edf5')
        maximum.grid(row=1, column=0, padx=5)
        stat2 = Label(newWindow, text=maxm, bg='#e4edf5')
        stat2.grid(row=1, column=1)
        meanLabel = Label(newWindow, text='Mean:', bg='#e4edf5')
        meanLabel.grid(row=2, column=0, padx=5)
        stat3 = Label(newWindow, text=mean, bg='#e4edf5')
        stat3.grid(row=2, column=1)
        stdevLabel = Label(newWindow, text='Standard deviation:', bg='#e4edf5')
        stdevLabel.grid(row=3, column=0, padx=5)
        stat4 = Label(newWindow, text=stdev, bg='#e4edf5')
        stat4.grid(row=3, column=1)

    read = Button(statProzor, text='Read', command=citanjestat)
    read.grid(row=2, column=0, padx=3)

    def close_window():
        statProzor.destroy()

    ok = Button(statProzor, text='OK', command=close_window)
    ok.grid(row=2, column=1)


def openAT():  # metoda koja prikazuje atribute odabranog fajla
    newWindow = tk.Toplevel(prozor)
    newWindow.title("Open attribute table")
    newWindow.geometry('350x200+300+50')
    newWindow.option_add('*font', ('Times', 12))
    vector = Label(newWindow, text='Choose vector')
    vector.grid(row=0, column=0, pady=3)
    stringVar = tk.StringVar()
    vektori = ttk.Combobox(newWindow, width=20, textvariable=stringVar)
    vektori.grid(row=1, column=0, pady=8)
    for x in range(len(listaVekRas)):  # dodavanje vektora u combobox
        if listaVekRas[x].type == "vektor":
            vektori['values'] = (*vektori['values'], listaVekRas[x].name)

    def attributeTable():  # metoda za prikaz atributa odabranog fajla
        if vektori.get() == '':
            messagebox.showerror(title='Error', message='Choose a file.', parent=newWindow)
        else:
            attable = tk.Toplevel(prozor)
            attable.title("Attribute table")
            attable.geometry("900x500+50+50")
            attable.option_add('*font', ('Times', 10))
            v = vektori.get()
            directory1 = ''
            for x in range(len(listaVekRas)):  # preuzimanje putanje odabranog fajla
                if v == listaVekRas[x].name:
                    directory1 = listaVekRas[x].directory
                    break
            fajl = gp.read_file(directory1, encoding='utf-8')
            tree = ttk.Treeview(attable)
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Treeview")
            scrollbar_horizontal = ttk.Scrollbar(attable, orient='horizontal', command=tree.xview)
            scrollbar_vertical = ttk.Scrollbar(attable, orient='vertical', command=tree.yview)
            scrollbar_horizontal.pack(side='bottom', fill=X)
            scrollbar_vertical.pack(side='right', fill=Y)
            tree.configure(xscrollcommand=scrollbar_horizontal.set, yscrollcommand=scrollbar_vertical.set)
            tree.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
            tree["columns"] = fajl.columns
            tree['show'] = 'headings'
            listaindexa = fajl.index.values
            i = 0
            for x in fajl.columns:  # preuzimanje naziva kolona
                tree.heading(i, text=x)
                tree.column(i, width=150, anchor=tk.CENTER)
                i += 1
            for y in listaindexa:  # ubacivanje vrijednosti u kolone
                tree.insert("", tk.END, values=fajl.loc[y].values.tolist())

    show = Button(newWindow, text='Show', command=attributeTable)
    show.grid(row=2, column=0)


def klasifikacija():  # metoda koja otvara prozor za biranje fajla za klasifikaciju
    klasProzor = tk.Toplevel(prozor)
    klasProzor.title('Classification')
    klasProzor.option_add('*font', ('Times', 12))
    klasProzor.geometry('300x300+300+50')
    vektor = Label(klasProzor, text='Choose vector')
    vektor.grid(row=0, column=0, pady=5)
    stringVar1 = tk.StringVar()
    vektori = ttk.Combobox(klasProzor, width=20, textvariable=stringVar1)
    vektori.grid(row=1, column=0, pady=5)
    for x in range(len(listaVekRas)):
        if listaVekRas[x].type == "vektor":
            vektori['values'] = (*vektori['values'], listaVekRas[x].name)
    stringVar = tk.StringVar()
    kategorija = ttk.Combobox(klasProzor, width=20, textvariable=stringVar)
    kategorija.grid(row=2, column=0, pady=5)
    kategorija['values'] = ['Categorized', 'Graduated']
    value = Label(klasProzor, text='Attribute value')
    value.grid(row=3, column=0, pady=3)
    stringVar2 = tk.StringVar()
    atributi = ttk.Combobox(klasProzor, width=20, textvariable=stringVar2)
    atributi.grid(row=4, column=0, pady=5)
    directoryList = ['']

    def biranjeVektora(self):  # metoda koja se poziva za izabrani vektor, resetuje sve widget-e
        vrste.config(state='normal')
        spin.config(state='normal')
        kategorija.set('')
        atributi.set('')
        atributi['values'] = ('')
        vrste.set('')

    def attribute(self):  # metoda koja se poziva za izabrani tip klasifikacija, postavlja odredjene atribute u combobox
        atributi.set('')
        v = vektori.get()
        listaAtributa = []
        if kategorija.get() == 'Categorized':  # postavlja sve atribute u combobox
            vrste.config(state='disabled')
            spin.config(state='disabled')
            for x in range(len(listaVekRas)):
                if v == listaVekRas[x].name:
                    directory = listaVekRas[x].directory
                    file2 = gp.read_file(directory, encoding='utf-8')
                    directoryList[0] = directory
                    for x in file2.columns:
                        if x != 'geometry':
                            listaAtributa.append(x)
        elif kategorija.get() == 'Graduated':  # postavlja numericke atribute u combobox
            vrste.config(state='normal')
            spin.config(state='normal')
            for x in range(len(listaVekRas)):
                if v == listaVekRas[x].name:
                    directory = listaVekRas[x].directory
                    file2 = gp.read_file(directory, encoding='utf-8')
                    directoryList[0] = directory
                    listaNaziva = []
                    a = []
                    for x in file2.columns:
                        listaNaziva.append(x)
                        a.append(str(file2.from_features(file2, columns=[x])).split())
                    for x in range(len(listaNaziva)):
                        l = True
                        i = 0
                        if len(a[0]) > 12:
                            end = 12
                        else:
                            end = len(a[0])
                        for y in range(2, end - 1, 2):  # listanje preuzetih vrijednosti kolona
                            if a[x][y].lower() != 'none':  # provjera da li postoji Null vrijednost
                                try:  # provjera da li je vrijednost tip String
                                    temp = float(a[x][y])
                                    i += 1
                                except ValueError:
                                    l = False
                                    i += 1
                        if l == True and i > 0 and (listaNaziva[x] not in listaAtributa):
                            listaAtributa.append(listaNaziva[x])
        else:
            messagebox.showerror(title='Error', message='Choose a category', parent=klasProzor)
        atributi['values'] = (listaAtributa)

    kategorija.bind('<<ComboboxSelected>>', attribute)
    vektori.bind('<<ComboboxSelected>>', biranjeVektora)
    klasif = Label(klasProzor, text='Classify')
    klasif.grid(row=5, column=0, pady=3)
    stringVar2 = tk.StringVar()
    vrste = ttk.Combobox(klasProzor, width=20, textvariable=stringVar2,
                         values=['Equal interval', 'Equal count', 'Fisher jenks'])
    vrste.grid(row=6, column=0, padx=8)
    klase = Label(klasProzor, text='Classes')
    klase.grid(row=5, column=1, padx=2)
    textVar = tk.IntVar()
    spin = tk.Spinbox(klasProzor, width=5, from_=1, to=10, increment=1, textvariable=textVar)
    spin.grid(row=6, column=1, pady=8)

    def apply():  # metoda koja vrsi klasifikaciju za odabrani fajl
        p = gp.read_file(directoryList[0], encoding='utf-8')
        kat = kategorija.get()
        vektor = vektori.get()
        val = atributi.get()
        tip = vrste.get()
        broj = spin.get()
        listaAtributa = []
        niz = str(p.from_features(p, columns=[val])).split()
        listaProvera = []
        listaProvera.append(niz[0])
        t = 0
        for x in range(2, len(niz), 2):  # provjera koliko postoji razlicitih vrijednosti u koloni
            k = True
            for y in range(len(listaProvera)):
                if listaProvera[y] == niz[x]:
                    k = False
                    break
            if k == True:
                listaProvera.append(niz[x])
                t += 1
        if int(broj) > t and kat != 'Categorized':  # provjera da li je broj razlicitih vrijednosti u kolini veci od broja klasa
            messagebox.showerror(title='Error', message='Fewer unique values than specified classes.',
                                 parent=klasProzor)
        else:
            for x in range(len(listaVekRas)):
                if vektor == listaVekRas[x].name:
                    directory = listaVekRas[x].directory
                    file5 = gp.read_file(directory, encoding='utf-8')
                    for x in file5.columns:
                        listaAtributa.append(x)
                    if kat == 'Categorized':
                        classified = file5.plot(column=str(val), k=int(broj), figsize=(10, 10), legend=True)
                    elif tip == 'Equal interval':
                        classified1 = file5.plot(column=str(val), scheme='equalinterval', k=int(broj), figsize=(10, 10),
                                                 legend=True)
                    elif tip == 'Equal count':
                        classified2 = file5.plot(column=str(val), scheme='quantiles', k=int(broj), figsize=(10, 10),
                                                 legend=True)
                    elif tip == 'Fisher jenks':
                        classified3 = file5.plot(column=str(val), scheme='fisherjenks', k=int(broj), figsize=(10, 10),
                                                 legend=True)
                    break

    apply = Button(klasProzor, text='Apply', command=apply)
    apply.grid(row=7, column=1)


def vektorizacija():  # metoda koja otvara prozor za biranje fajla za vektorizaciju
    vektorizProzor = tk.Toplevel(prozor)
    vektorizProzor.title('Polygonize')
    vektorizProzor.option_add('*font', ('Times', 12))
    vektorizProzor.geometry('450x400+300+50')
    raster = Label(vektorizProzor, text='Choose raster')
    raster.grid(row=0, column=0, pady=3)
    stringVar1 = tk.StringVar()
    rasteri = ttk.Combobox(vektorizProzor, width=20, textvariable=stringVar1)
    rasteri.grid(row=1, column=0, pady=5)
    output = Label(vektorizProzor, text='Choose file name and location')
    output.grid(row=2, column=0, pady=3)
    stringVar2 = tk.StringVar()
    outputLayer = Entry(vektorizProzor, textvariable=stringVar2)
    outputLayer.grid(row=3, column=0, pady=8, padx=3)
    listOfDirec[0] = ''

    def pathLocation1():
        listOfDirec[0] = filedialog.askdirectory(parent=vektorizProzor)

    outputButton = Button(vektorizProzor, image=imgDirectory, command=pathLocation1)
    outputButton.image = imgDirectory
    outputButton.grid(row=3, column=1, pady=8)
    for x in range(len(listaVekRas)):
        if listaVekRas[x].type == "raster":
            rasteri['values'] = (*rasteri['values'], listaVekRas[x].name)

    def funkcija():  # metoda za vrsenje vektorizacije fajla
        if rasteri.get() == '':
            messagebox.showerror(title='Error', message='Fill in empty spots.', parent=vektorizProzor)
        elif outputLayer.get() == '':
            messagebox.showerror(title='Error', message='Input a name for the output file.', parent=vektorizProzor)
        elif listOfDirec[0] == '':
            messagebox.showerror(title='Error', message='Choose a location for the output file.', parent=vektorizProzor)
        else:
            r = rasteri.get()
            directory = ''
            title = outputLayer.get() + '.shp'
            direc = os.path.join(listOfDirec[0], title)
            if exists(direc) == False:
                for x in range(len(listaVekRas)):
                    if r == listaVekRas[x].name:
                        directory = listaVekRas[x].directory
                        name = ''
                    mask = None
                    with rasterio.Env():
                        with rasterio.open(directory) as src:
                            image = src.read(1)
                            results = (
                                {'properties': {'raster_val': v}, 'geometry': s}
                                for i, (s, v)
                                in enumerate(
                                rasterio.features.shapes(image, mask=mask, transform=src.transform)))
                    geoms = list(results)  # features u geojson obliku
                    polygonized_raster = gp.GeoDataFrame.from_features(geoms)  # kreira gpd na osnovu features-a
                    polygonized_raster.to_file(direc, driver='ESRI Shapefile')
                    listaAt = []
                    shp = gp.read_file(direc, encoding='utf-8')
                    print(shp.crs)
                    for x in shp.columns:
                        listaAt.append(x)
                    listaVekRas.append(VekRas(direc, 'vektor', listaAt))
                    layer['values'] = (*layer['values'], listaVekRas[-1].name)
                    break
            else:
                messagebox.showerror(title='Error', message='This file already exists.', parent=vektorizProzor)

    run = Button(vektorizProzor, text='Run', command=funkcija)
    run.grid(row=4, column=0, pady=5)
    inputlayer = Label(vektorizProzor, text='Input layer')
    inputlayer.grid(row=5, column=0)
    stringVar3 = tk.StringVar()
    layer = ttk.Combobox(vektorizProzor, width=20, textvariable=stringVar3)
    layer.grid(row=6, column=0)
    reproj = Label(vektorizProzor, text='Reproject layer')
    reproj.grid(row=7, column=0, pady=3)
    stringVar4 = tk.StringVar()
    koordsistemi = ttk.Combobox(vektorizProzor, width=20, textvariable=stringVar4,
                                values=['EPSG:4326 - WGS 84', 'EPSG:32634 - WGS 84/UTM ZONE 34N',
                                        'EPSG:31276 - MGI/Balkans zone 6', 'EPSG:31277 - MGI/Balkans zone 7'])
    koordsistemi.grid(row=8, column=0, padx=3)
    namelabel = Label(vektorizProzor, text='Reprojected')
    namelabel.grid(row=9, column=0)
    stringVar5 = tk.StringVar()
    outputLayer2 = Entry(vektorizProzor, textvariable=stringVar5)
    outputLayer2.grid(row=10, column=0)
    listOfDirec[1] = ''

    def pathLocation2():
        listOfDirec[1] = filedialog.askdirectory(parent=vektorizProzor)

    outputButton2 = Button(vektorizProzor, image=imgDirectory, command=pathLocation2)
    outputButton2.image = imgDirectory
    outputButton2.grid(row=10, column=1, pady=3)

    def reprojectLayer():  # metoda koja sluzi za mjenjanje koordinatnog sistema fajla
        if layer.get() == '':
            messagebox.showerror(title='Error', message='Choose one file.', parent=vektorizProzor)
        elif koordsistemi.get() == '':
            messagebox.showerror(title='Error', message='Choose one coordinate system.', parent=vektorizProzor)
        elif outputLayer2.get() == '':
            messagebox.showerror(title='Error', message='Choose a name for the output file.', parent=vektorizProzor)
        elif listOfDirec[1] == '':
            messagebox.showerror(title='Error', message='Choose a location for the output file.', parent=vektorizProzor)
        else:
            ks = koordsistemi.get()
            lay = layer.get()
            title2 = outputLayer2.get() + '.shp'
            direc = os.path.join(listOfDirec[1], title2)
            if exists(direc) == False:
                listaAt = []
                directory1 = 'nesto'
                if ks == 'EPSG:4326 - WGS 84':
                    for x in range(len(listaVekRas)):
                        if lay == listaVekRas[x].name:
                            directory1 = listaVekRas[x].directory
                            lejer = gp.read_file(directory1, encoding='utf-8')
                            kopija = lejer.copy()
                            kopija.crs = {'init': 'epsg:32634'}
                            print(kopija.crs)
                            kopija = kopija.to_crs({'init': 'epsg:4326'})
                            print(kopija.crs)
                            kopija.to_file(direc, driver='ESRI Shapefile')
                            f = gp.read_file(direc, encoding='utf-8')
                            for x in f.columns:
                                listaAt.append(x)
                            listaVekRas.append(VekRas(direc, 'vektor', listaAt))
                elif ks == 'EPSG:32634 - WGS 84/UTM ZONE 34N':
                    for x in range(len(listaVekRas)):
                        if lay == listaVekRas[x].name:
                            directory1 = listaVekRas[x].directory
                            lejer = gp.read_file(directory1, encoding='utf-8')
                            kopija = lejer.copy()
                            kopija.crs = {'init': 'epsg:4326'}
                            kopija = kopija.to_crs({'init': 'epsg:32634'})
                            kopija.to_file(direc, driver='ESRI Shapefile')
                            f = gp.read_file(direc, encoding='utf-8')
                            for x in f.columns:
                                listaAt.append(x)
                            listaVekRas.append(VekRas(direc, 'vektor', listaAt))
                elif ks == 'EPSG:31276 - MGI/Balkans zone 6':
                    for x in range(len(listaVekRas)):
                        if lay == listaVekRas[x].name:
                            directory1 = listaVekRas[x].directory
                            lejer = gp.read_file(directory1, encoding='utf-8')  # NAS FAJL KOJI SACUVAMO
                            kopija = lejer.copy()
                            kopija.crs = {'init': 'epsg:32634'}
                            kopija = kopija.to_crs({'init': 'epsg:31276'})
                            kopija.to_file(direc, driver='ESRI Shapefile')
                            f = gp.read_file(direc, encoding='utf-8')
                            for x in f.columns:
                                listaAt.append(x)
                            listaVekRas.append(VekRas(direc, 'vektor', listaAt))
                elif ks == 'EPSG:31277 - MGI/Balkans zone 7':
                    for x in range(len(listaVekRas)):
                        if lay == listaVekRas[x].name:
                            directory1 = listaVekRas[x].directory
                            lejer = gp.read_file(directory1, encoding='utf-8')  # NAS FAJL KOJI SACUVAMO
                            kopija = lejer.copy()
                            kopija.crs = {'init': 'epsg:32634'}  # epsg=32634
                            kopija = kopija.to_crs({'init': 'epsg:31277'})  # epsg=31277
                            kopija.to_file(direc, driver='ESRI Shapefile')
                            f = gp.read_file(direc, encoding='utf-8')
                            for x in f.columns:
                                listaAt.append(x)
                            listaVekRas.append(VekRas(direc, 'vektor', listaAt))
            else:
                messagebox.showerror(title='Error', message='This file already exists.', parent=vektorizProzor)

    reprojectButton = Button(vektorizProzor, text='Run', command=reprojectLayer)
    reprojectButton.grid(row=11, column=0)


def isecanjeRastera():  # metoda koja otvara prozor za biranje fajla za isjecanje
    fajlZaCRS[0] = ''
    fajlZaCRS[1] = ''
    listOfDirec.clear()
    listOfDirec.append('')
    listOfDirec.append('')
    listOfDirec.append('')
    nizEntrija = []
    isecanjeProzor = tk.Toplevel(prozor)
    isecanjeProzor.title('Clip raster by mask layer')
    isecanjeProzor.option_add('*font', ('Times', 12))
    isecanjeProzor.geometry('400x500+300+50')
    choose = Label(isecanjeProzor, text='Choose raster')
    choose.grid(row=0, column=0, pady=3)
    stringVar1 = tk.StringVar()
    rasteri = ttk.Combobox(isecanjeProzor, width=20, textvariable=stringVar1)
    rasteri.grid(row=1, column=0, pady=5)
    textVar = tk.IntVar()

    def ogranicavanjeUnosa():  # metoda koja na osnovu izbora broja tacaka gasi odredjeni broj polja za unos koordinata
        for x in range(len(nizEntrija)):
            nizEntrija[x].config(state='normal')
        for x in range(int(spin.get()) * 2, len(nizEntrija)):
            nizEntrija[x].config(state='disabled')

    spin = tk.Spinbox(isecanjeProzor, width=5, from_=3, to=10, increment=1, textvariable=textVar,
                      command=ogranicavanjeUnosa)
    spin.grid(row=2, column=1, pady=5)
    for x in range(len(listaVekRas)):
        if listaVekRas[x].type == "raster":
            rasteri['values'] = (*rasteri['values'], listaVekRas[x].name)

    def start():  # metoda provjera CRS fajla i otvara fajl
        if rasteri.get() == '':
            messagebox.showerror(title='Error', message='Choose one file.', parent=isecanjeProzor)
        else:
            for x in range(len(listaVekRas)):
                if listaVekRas[x].name == rasteri.get():
                    listOfDirec[0] = listaVekRas[x].directory
                    break

            def otvori():
                imagery = rasterio.open(listOfDirec[2])
                show(imagery.read(), transform=imagery.transform)
                fajlZaCRS[1] = imagery.crs

            if str(rasterio.open(listOfDirec[0]).crs) == '' or str(rasterio.open(listOfDirec[0]).crs) == 'None':
                listOfDirec[1] = ''
                listOfDirec[2] = ''
                noviFajlProzor = tk.Toplevel(isecanjeProzor)
                noviFajlProzor.title('New file')
                noviFajlProzor.option_add('*font', ('Times', 12))
                noviFajlProzor.geometry('400x200+300+50')
                info = Label(noviFajlProzor,
                             text='Your file doesn\'t have a defined CRS. \nReprojecting your file with a new CRS. \nChoose CRS, name and location:')
                info.grid(row=0, column=0, pady=3)
                stringVar1 = tk.StringVar()
                crss = ttk.Combobox(noviFajlProzor, width=20, textvariable=stringVar1,
                                    values=['EPSG:4326 - WGS 84', 'EPSG:32634 - WGS 84/UTM ZONE 34N',
                                            'EPSG:31276 - MGI/Balkans zone 6', 'EPSG:31277 - MGI/Balkans zone 7'])
                crss.grid(row=1, column=0, padx=3)
                stringVar2 = tk.StringVar()
                newDestination = Entry(noviFajlProzor, textvariable=stringVar2)
                newDestination.grid(row=2, column=0)

                def pathLocation():
                    listOfDirec[1] = filedialog.askdirectory(parent=noviFajlProzor)

                pickNewDestination = Button(noviFajlProzor, command=pathLocation, image=imgDirectory)
                pickNewDestination.image = imgDirectory
                pickNewDestination.grid(row=2, column=1)

                def closingThis():
                    if crss.get() == '':
                        messagebox.showerror(title='Error', message='Choose a new CRS.', parent=noviFajlProzor)
                    elif newDestination.get() == '':
                        messagebox.showerror(title='Error', message='Choose a name for the output file.',
                                             parent=noviFajlProzor)
                    elif listOfDirec[1] == '':
                        messagebox.showerror(title='Error', message='Choose a location for the output file.',
                                             parent=noviFajlProzor)
                    else:
                        title = newDestination.get() + '.img'
                        listOfDirec[2] = os.path.join(listOfDirec[1], title)
                        if exists(listOfDirec[2]) == True:
                            messagebox.showerror(title='Error', message='File under this name already exists.',
                                                 parent=noviFajlProzor)
                        else:
                            crs = ''
                            if crss.get() == 'EPSG:4326 - WGS 84':
                                crs = "EPSG:4326"
                            elif crss.get() == 'EPSG:32634 - WGS 84/UTM ZONE 34N':
                                crs = "EPSG:32634"
                            elif crss.get() == 'EPSG:31276 - MGI/Balkans zone 6':
                                crs = "EPSG:31276"
                            elif crss.get() == 'EPSG:31277 - MGI/Balkans zone 7':
                                crs = "EPSG:31277"
                            with rasterio.open(listOfDirec[0]) as src:
                                transform, width, height = calculate_default_transform(
                                    src.crs, crs, src.width, src.height, *src.bounds)
                                kwargs = src.meta.copy()
                                kwargs.update({
                                    'crs': crs,
                                    'transform': transform,
                                    'width': width,
                                    'height': height
                                })
                                with rasterio.open(listOfDirec[2], 'w', **kwargs) as dst:
                                    for i in range(1, src.count + 1):
                                        reproject(
                                            source=rasterio.band(src, i),
                                            destination=rasterio.band(dst, i),
                                            src_transform=src.transform,
                                            src_crs=src.crs,
                                            dst_transform=transform,
                                            dst_crs=crs,
                                            resampling=Resampling.nearest)
                            listaVekRas.append(VekRas(listOfDirec[2], 'raster', ''))
                            for x in range(len(listaVekRas)):
                                if listaVekRas[x].directory == listOfDirec[2]:
                                    rasteri['values'] = (*rasteri['values'], listaVekRas[x].name)
                                    rasteri.set(listaVekRas[x].name)
                                    break
                            otvori()
                            noviFajlProzor.destroy()

                ok = Button(noviFajlProzor, text="OK", command=closingThis)
                ok.grid(row=3, column=0)
            else:
                listOfDirec[2] = listOfDirec[0]
                otvori()

    def createBB():  # metoda koja vrsi presjecanje fajlova
        listOfDirec[0] = ''
        for x in range(len(listaVekRas)):
            if listaVekRas[x].name == rasteri.get():
                listOfDirec[0] = listaVekRas[x].directory
                break
        if rasteri.get() == '':
            messagebox.showerror(title='Error', message='Choose one file.', parent=isecanjeProzor)
        elif str(rasterio.open(listOfDirec[0]).crs) == '' or str(rasterio.open(listOfDirec[0]).crs) == 'None':
            messagebox.showerror(title='Error',
                                 message='This file doesn\'t have CRS.\nClick \"Open raster\" to set a new CRS.',
                                 parent=isecanjeProzor)
        elif outputLayer.get() == '':
            messagebox.showerror(title='Error', message='Choose a name for the output file.', parent=isecanjeProzor)
        elif fajlZaCRS[0] == '':
            messagebox.showerror(title='Error', message='Choose a location for the output file.', parent=isecanjeProzor)
        else:
            listaKoordinata.clear()
            i = int(spin.get())  # broj tacaka
            try:
                nizKoordinata = [coords1.get(), coords2.get(), coords3.get(), coords4.get(), coords5.get(),
                                 coords6.get(), coords7.get(), coords8.get(), coords9.get(), coords10.get(),
                                 coords11.get(), coords12.get(), coords13.get(), coords14.get(), coords15.get(),
                                 coords16.get(), coords17.get(), coords18.get, coords19.get(), coords20.get()]
                for x in range(2 * i):
                    listaKoordinata.append(float(nizKoordinata[x]))
                pointList = []
                for x in range(i):
                    pointList.append(geometry.Point(listaKoordinata[2 * x], listaKoordinata[2 * x + 1]))
                poly = geometry.Polygon([[p.x, p.y] for p in pointList])
                s2 = gp.GeoSeries([Polygon(poly)])
                gpd = gp.GeoDataFrame(geometry=s2, crs=fajlZaCRS[1])
                t = 1  # pomocna promjenljiva za pravljenje nove maske
                title = 'maska' + str(t) + '.shp'
                direcTemp1 = os.path.join(fajlZaCRS[0], title)
                while (exists(direcTemp1)):
                    t += 1
                    title = 'maska' + str(t) + '.shp'
                    direcTemp1 = os.path.join(fajlZaCRS[0], title)
                gpd.to_file(direcTemp1)
                with fiona.open(direcTemp1, "r") as shapefile:
                    shapes = [feature["geometry"] for feature in shapefile]
                with rasterio.open(listOfDirec[2]) as src:
                    out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
                    out_meta = src.meta
                out_meta.update({"driver": "GTiff",
                                 "height": out_image.shape[1],
                                 "width": out_image.shape[2],
                                 "transform": out_transform})
                title = outputLayer.get() + '.img'
                direct = os.path.join(fajlZaCRS[0], title)
                with rasterio.open(direct, "w", **out_meta) as dest:
                    dest.write(out_image)
                j = rasterio.open(direct)
                show(j.read(), transform=j.transform)
                listaVekRas.append(VekRas(direct, 'raster', ''))
            except ValueError:
                messagebox.showerror(title='Error', message='Use \'.\' instead of \',\'.', parent=isecanjeProzor)

    start = Button(isecanjeProzor, text='Open raster', command=start)
    start.grid(row=2, column=0)

    def location():
        fajlZaCRS[0] = filedialog.askdirectory(parent=isecanjeProzor)

    stringVar4 = tk.StringVar()
    outputLayer = Entry(isecanjeProzor, textvariable=stringVar4)
    outputLayer.grid(row=3, column=0)
    btn2 = Button(isecanjeProzor, command=location, image=imgDirectory)
    btn2.image = imgDirectory
    btn2.grid(row=3, column=1)
    labela1 = Label(isecanjeProzor, text='X')
    labela1.grid(row=4, column=0, pady=3)
    labela2 = Label(isecanjeProzor, text='Y')
    labela2.grid(row=4, column=1, pady=3)
    stringVar5 = tk.StringVar()
    coords1 = Entry(isecanjeProzor, textvariable=stringVar5)
    coords1.grid(row=5, column=0)
    nizEntrija.append(coords1)
    stringVar6 = tk.StringVar()
    coords2 = Entry(isecanjeProzor, textvariable=stringVar6)
    coords2.grid(row=5, column=1)
    nizEntrija.append(coords2)
    stringVar7 = tk.StringVar()
    coords3 = Entry(isecanjeProzor, textvariable=stringVar7)
    coords3.grid(row=6, column=0)
    nizEntrija.append(coords3)
    stringVar8 = tk.StringVar()
    coords4 = Entry(isecanjeProzor, textvariable=stringVar8)
    coords4.grid(row=6, column=1)
    nizEntrija.append(coords4)
    stringVar9 = tk.StringVar()
    coords5 = Entry(isecanjeProzor, textvariable=stringVar9)
    coords5.grid(row=7, column=0)
    nizEntrija.append(coords5)
    stringVar10 = tk.StringVar()
    coords6 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords6.grid(row=7, column=1)
    nizEntrija.append(coords6)
    stringVar10 = tk.StringVar()
    coords7 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords7.grid(row=8, column=0)
    nizEntrija.append(coords7)
    stringVar10 = tk.StringVar()
    coords8 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords8.grid(row=8, column=1)
    nizEntrija.append(coords8)
    stringVar10 = tk.StringVar()
    coords9 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords9.grid(row=9, column=0)
    nizEntrija.append(coords9)
    stringVar10 = tk.StringVar()
    coords10 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords10.grid(row=9, column=1)
    nizEntrija.append(coords10)
    stringVar10 = tk.StringVar()
    coords11 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords11.grid(row=10, column=0)
    nizEntrija.append(coords11)
    stringVar10 = tk.StringVar()
    coords12 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords12.grid(row=10, column=1)
    nizEntrija.append(coords12)
    stringVar10 = tk.StringVar()
    coords13 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords13.grid(row=11, column=0)
    nizEntrija.append(coords13)
    stringVar10 = tk.StringVar()
    coords14 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords14.grid(row=11, column=1)
    nizEntrija.append(coords14)
    stringVar10 = tk.StringVar()
    coords15 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords15.grid(row=12, column=0)
    nizEntrija.append(coords15)
    stringVar10 = tk.StringVar()
    coords16 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords16.grid(row=12, column=1)
    nizEntrija.append(coords16)
    stringVar10 = tk.StringVar()
    coords17 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords17.grid(row=13, column=0)
    nizEntrija.append(coords17)
    stringVar10 = tk.StringVar()
    coords18 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords18.grid(row=13, column=1)
    nizEntrija.append(coords18)
    stringVar10 = tk.StringVar()
    coords19 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords19.grid(row=14, column=0)
    nizEntrija.append(coords19)
    stringVar10 = tk.StringVar()
    coords20 = Entry(isecanjeProzor, textvariable=stringVar10)
    coords20.grid(row=14, column=1)
    nizEntrija.append(coords20)
    for x in range(6, len(nizEntrija)):
        nizEntrija[x].config(state='disabled')
    clip = Button(isecanjeProzor, text='Clip', command=createBB)
    clip.grid(row=15, column=0)


def unija():  # metoda koja otvara prozor za biranje fajlova za uniju
    unijaProzor = tk.Toplevel(prozor)
    unijaProzor.title("Union")
    unijaProzor.geometry("300x250+50+50")
    unijaProzor.option_add('*font', ('Times', 11))
    unijaProzor.grid()
    inputlayer = Label(unijaProzor, text='Input layer')
    inputlayer.grid(row=0, column=0, pady=3)
    stringVar1 = tk.StringVar()
    ilejeri = ttk.Combobox(unijaProzor, width=20, textvariable=stringVar1)
    ilejeri.grid(row=1, column=0, pady=5)
    stringVar2 = tk.StringVar()
    overlaylayer = Label(unijaProzor, text='Overlay layer')
    overlaylayer.grid(row=2, column=0, pady=3)
    olejeri = ttk.Combobox(unijaProzor, width=20, textvariable=stringVar2)
    olejeri.grid(row=3, column=0, pady=8)
    fileLocation = Label(unijaProzor, text='Choose name and path for the new file:')
    fileLocation.grid(row=4, column=0)
    stringVar3 = tk.StringVar()
    outputLayer = Entry(unijaProzor, textvariable=stringVar3)
    outputLayer.grid(row=5, column=0)
    listOfDirec[0] = ''

    def pathLocation():
        listOfDirec[0] = filedialog.askdirectory(parent=unijaProzor)

    outputButton = Button(unijaProzor, compound=TOP, command=pathLocation, image=imgDirectory)
    outputButton.image = imgDirectory
    outputButton.grid(row=5, column=1)
    for x in range(len(listaVekRas)):
        if listaVekRas[x].type == "vektor":
            ilejeri['values'] = (*ilejeri['values'], listaVekRas[x].name)
            olejeri['values'] = (ilejeri['values'])

    def unijaRezultat():  # metoda koja vrsi uniju odabranih fajlova, uz obezbjedjivanje pravilnog koriscenja podataka
        vektor1 = ilejeri.get()
        vektor2 = olejeri.get()
        directory1 = ''
        directory2 = ''
        name1 = ''
        name2 = ''
        for x in range(len(listaVekRas)):
            if vektor1 == listaVekRas[x].name:
                directory1 = listaVekRas[x].directory
                name1 = listaVekRas[x].name
                break
        for x in range(len(listaVekRas)):
            if vektor2 == listaVekRas[x].name:
                directory2 = listaVekRas[x].directory
                name2 = listaVekRas[x].name
                break
        if vektor1 == '' or vektor2 == '':
            messagebox.showerror(title='Error', message='Fill in empty spots.', parent=unijaProzor)
        elif directory1 == directory2:
            messagebox.showerror(title='Error', message='Both files are the same.', parent=unijaProzor)
        elif outputLayer.get() == '':
            messagebox.showerror(title='Error', message='Input a name for the output file.', parent=unijaProzor)
        elif listOfDirec[0] == '':
            messagebox.showerror(title='Error', message='Choose a location for the output file.', parent=unijaProzor)
        else:
            file1 = gp.read_file(directory1, encoding='utf-8')
            file2 = gp.read_file(directory2, encoding='utf-8')
            if str(file1.crs) != str(file2.crs):
                messagebox.showerror(title='Error', message='Files don\'t have the same CRS.', parent=unijaProzor)
            else:
                title = outputLayer.get() + '.shp'
                direc = os.path.join(listOfDirec[0], title)
                if exists(direc) == True:
                    messagebox.showerror(title='Error', message='This file already exists.', parent=unijaProzor)
                else:
                    p = gp.overlay(file1, file2, how="union", keep_geom_type=True)
                    if p.empty:
                        messagebox.showerror(title='Error', message='There\'s no union between these two files.',
                                             parent=unijaProzor)
                    else:
                        title = outputLayer.get() + '.shp'
                        direc = os.path.join(listOfDirec[0], title)
                        p.to_file(direc, driver='ESRI Shapefile')
                        fig, ax = plt.subplots(figsize=(10, 10))
                        p.plot(ax=ax, cmap='Blues')
                        fig.align_labels()
                        ax.set_anchor('SW')
                        plt.close()
                        ram.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
                        canvas.draw()
                        listaAt = []
                        shp = gp.read_file(direc, encoding='utf-8')
                        for x in shp.columns:
                            listaAt.append(x)
                        listaVekRas.append(VekRas(direc, 'vektor', listaAt))

    run = Button(unijaProzor, text='Run', command=unijaRezultat)
    run.grid(row=6, column=0)


def razlika():  # metoda koja otvara prozor za biranje fajlova za razliku
    razlikaProzor = tk.Toplevel(prozor)
    razlikaProzor.title("Difference")
    razlikaProzor.geometry("325x250+50+50")
    razlikaProzor.option_add('*font', ('Times', 11))
    razlikaProzor.grid()
    inputlayer = Label(razlikaProzor, text='Choose vector')
    inputlayer.grid(row=0, column=0, pady=3)
    stringVar1 = tk.StringVar()
    ilejeri = ttk.Combobox(razlikaProzor, width=20, textvariable=stringVar1)
    ilejeri.grid(row=1, column=0, pady=5, padx=5)
    stringVar2 = tk.StringVar()
    overlaylayer = Label(razlikaProzor, text='Choose vector')
    overlaylayer.grid(row=2, column=0, pady=3)
    olejeri = ttk.Combobox(razlikaProzor, width=20, textvariable=stringVar2)
    olejeri.grid(row=3, column=0, pady=8, padx=5)
    fileLocation = Label(razlikaProzor, text='Choose name and path for the new file:')
    fileLocation.grid(row=4, column=0)
    stringVar3 = tk.StringVar()
    outputLayer = Entry(razlikaProzor, textvariable=stringVar3)
    outputLayer.grid(row=5, column=0)
    listOfDirec[0] = ''

    def pathLocation():
        listOfDirec[0] = filedialog.askdirectory(parent=src.crsrazlikaProzor)

    outputButton = Button(razlikaProzor, compound=TOP, command=pathLocation, image=imgDirectory)
    outputButton.image = imgDirectory
    outputButton.grid(row=5, column=1)
    for x in range(len(listaVekRas)):
        if listaVekRas[x].type == "vektor":
            ilejeri['values'] = (*ilejeri['values'], listaVekRas[x].name)
            olejeri['values'] = (ilejeri['values'])

    def razlikaRezultat():  # metoda koja vrsi razlikupre odabranih fajlova, uz obezbjedjivanje pravilnog koriscenja podataka
        vektor1 = ilejeri.get()
        vektor2 = olejeri.get()
        directory1 = ''
        directory2 = ''
        name1 = ''
        name2 = ''
        for x in range(len(listaVekRas)):
            if vektor1 == listaVekRas[x].name:
                directory1 = listaVekRas[x].directory
                break
        for x in range(len(listaVekRas)):
            if vektor2 == listaVekRas[x].name:
                directory2 = listaVekRas[x].directory
                break
        if vektor1 == '' or vektor2 == '':
            messagebox.showerror(title='Error', message='Fill in empty spots.', parent=razlikaProzor)
        elif directory1 == directory2:
            messagebox.showerror(title='Error', message='Both files are the same.', parent=razlikaProzor)
        elif outputLayer.get() == '':
            messagebox.showerror(title='Error', message='Input a name for the output file.', parent=razlikaProzor)
        elif listOfDirec[0] == '':
            messagebox.showerror(title='Error', message='Choose a location for the output file.', parent=razlikaProzor)
        else:
            file1 = gp.read_file(directory1, encoding='utf-8')
            file2 = gp.read_file(directory2, encoding='utf-8')
            if str(file1.crs) != str(file2.crs):
                messagebox.showerror(title='Error', message='Files don\'t have the same CRS.', parent=razlikaProzor)
            else:
                title = outputLayer.get() + '.shp'
                direc = os.path.join(listOfDirec[0], title)
                if exists(direc) == True:
                    messagebox.showerror(title='Error', message='This file already exists.', parent=razlikaProzor)
                else:
                    p = gp.overlay(file1, file2, how="difference", keep_geom_type=True)
                    if p.empty:
                        messagebox.showerror(title='Error', message='There\'s no difference between these two files.',
                                             parent=razlikaProzor)
                    else:
                        title = outputLayer.get() + '.shp'
                        direc = os.path.join(listOfDirec[0], title)
                        p.to_file(direc, driver='ESRI Shapefile')
                        fig, ax = plt.subplots(figsize=(10, 10))
                        p.plot(ax=ax, cmap='Blues')
                        fig.align_labels()
                        ax.set_anchor('SW')
                        plt.close()
                        ram.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
                        canvas.draw()
                        listaAt = []
                        shp = gp.read_file(direc, encoding='utf-8')
                        for x in shp.columns:
                            listaAt.append(x)
                        listaVekRas.append(VekRas(direc, 'vektor', listaAt))

    run = Button(razlikaProzor, text='Run', command=razlikaRezultat)
    run.grid(row=6, column=0)


def reprojekcija():  # metoda koja otvara prozor za biranje fajla za reprojekciju
    listOfDirec[0] = ''
    reprojProzor = tk.Toplevel(prozor)
    reprojProzor.title('Reprojection')
    reprojProzor.option_add('*font', ('Times', 12))
    reprojProzor.geometry('300x300+400+50')
    file = Label(reprojProzor, text='Choose file')
    file.grid(row=0, column=0, pady=3)
    stringVar1 = tk.StringVar()
    listaFajlova = ttk.Combobox(reprojProzor, width=20, textvariable=stringVar1)
    listaFajlova.grid(row=1, column=0, pady=5)
    for x in range(len(listaVekRas)):
        listaFajlova['values'] = (*listaFajlova['values'], listaVekRas[x].name)
    coordsistem = Label(reprojProzor, text='Coordinate System')
    coordsistem.grid(row=2, column=0, pady=3)
    stringVar2 = tk.StringVar()
    crs = ttk.Combobox(reprojProzor, width=20, textvariable=stringVar2,
                       values=['EPSG:4326 - WGS 84', 'EPSG:32634 - WGS 84/UTM ZONE 34N',
                               'EPSG:31276 - MGI/Balkans zone 6', 'EPSG:31277 - MGI/Balkans zone 7'])
    crs.grid(row=3, column=0, pady=5)
    output = Label(reprojProzor, text='Choose file name and location')
    output.grid(row=4, column=0, pady=3)
    stringVar3 = tk.StringVar()
    outputLayer = Entry(reprojProzor, textvariable=stringVar3)
    outputLayer.grid(row=5, column=0, padx=3, pady=5)
    listOfDirec[0] = ''

    def pathLocation():
        listOfDirec[0] = filedialog.askdirectory(parent=reprojProzor)

    outputButton = Button(reprojProzor, image=imgDirectory, command=pathLocation)
    outputButton.image = imgDirectory
    outputButton.grid(row=5, column=1)

    def reprojectFile():  # metoda koja vrsi reprojekciju fajla
        if outputLayer.get() == '':
            messagebox.showerror(title='Error', message='Input a name for the output file.', parent=reprojProzor)
        elif listOfDirec[0] == '':
            messagebox.showerror(title='Error', message='Choose a location for the output file.', parent=reprojProzor)
        else:
            f = listaFajlova.get()
            ks = crs.get()
            title = outputLayer.get() + '.shp'
            direc = os.path.join(listOfDirec[0], title)
            if exists(direc) == False:
                listaAt = []
                directory = ''
                for x in range(len(listaVekRas)):
                    if f == listaVekRas[x].name:
                        if listaVekRas[x].type == 'vektor':
                            directory = listaVekRas[x].directory
                            crss = ''
                            if ks == 'EPSG:4326 - WGS 84':
                                crss = 'EPSG:4326'
                            elif ks == 'EPSG:32634 - WGS 84/UTM ZONE 34N':
                                crss = 'EPSG:32634'
                            elif ks == 'EPSG:31276 - MGI/Balkans zone 6':
                                crss = 'EPSG:31276'
                            else:
                                crss = 'EPSG:31277'
                            lejer = gp.read_file(directory, encoding='utf-8')
                            print(lejer.crs)
                            lejer = lejer.to_crs(crss)
                            print(lejer.crs)
                            lejer.to_file(direc, driver='ESRI Shapefile')
                            g = gp.read_file(direc, encoding='utf-8')
                            for x in g.columns:
                                listaAt.append(x)
                            listaVekRas.append(VekRas(direc, 'vektor', listaAt))
                            break
                        else:
                            directory = listaVekRas[x].directory
                            crss = ''
                            if ks == 'EPSG:4326 - WGS 84':
                                crss = 'EPSG:4326'
                            elif ks == 'EPSG:32634 - WGS 84/UTM ZONE 34N':
                                crss = 'EPSG:32634'
                            elif ks == 'EPSG:31276 - MGI/Balkans zone 6':
                                crss = 'EPSG:31276'
                            else:
                                crss = 'EPSG:31277'
                            with rasterio.open(directory) as src:
                                print(src.crs)
                                transform, width, height = calculate_default_transform(
                                    src.crs, crss, src.width, src.height, *src.bounds)
                                kwargs = src.meta.copy()
                                kwargs.update({
                                    'crs': crss,
                                    'transform': transform,
                                    'width': width,
                                    'height': height
                                })
                                with rasterio.open(direc, 'w', **kwargs) as dst:
                                    for i in range(1, src.count + 1):
                                        reproject(
                                            source=rasterio.band(src, i),
                                            destination=rasterio.band(dst, i),
                                            src_transform=src.transform,
                                            src_crs=src.crs,
                                            dst_transform=transform,
                                            dst_crs=crss,
                                            resampling=Resampling.nearest)
                                    listaVekRas.append(VekRas(direc, 'raster', ''))
                                    print(dst.crs)
                        break
            else:
                messagebox.showerror(title='Error', message='File with this name already exists.', parent=reprojProzor)

    run = Button(reprojProzor, text='Run', command=reprojectFile)
    run.grid(row=6, column=0)


def findDirectory():  # metoda koja otvara prozor za izbor fajlova
    find = tk.Toplevel(prozor)
    find.title("Find directory:")
    find.geometry('700x250+400+200')
    find.option_add('*font', ('Times', 12))
    label1 = Label(find, text='Choose a file:')
    label1.pack(side=TOP, fill=X, expand=True, padx=5, pady=10)
    stringVar = tk.StringVar()
    files = ttk.Combobox(find, width=20, textvariable=stringVar)
    files.pack(side=TOP, fill=X, expand=True, padx=5, pady=10)
    label2 = Label(find)
    label2.pack(side=BOTTOM, fill=X, expand=True, padx=5, pady=10)
    for x in range(len(listaVekRas)):
        files['values'] = (*files['values'], listaVekRas[x].name)

    def action(self):  # metoda koja ispisuje direktorijum fajla
        for x in range(len(listaVekRas)):
            if listaVekRas[x].name == files.get():
                label2.config(text=listaVekRas[x].directory)
                break

    files.bind('<<ComboboxSelected>>', action)

    def copy():  # metoda koja kopira direktorijuma u clipboard
        if label2.cget("text") == '':
            messagebox.showerror(title='Error', message='Choose a file.', parent=find)
        else:
            prozor.clipboard_clear()
            prozor.clipboard_append(label2.cget("text"))
            prozor.update()
            messagebox.showinfo("Information", "Directory has been copied to the clipboard", parent=find)

    button = Button(find, text='Copy', command=copy)
    button.pack(side=BOTTOM, fill=X, expand=True, padx=5, pady=10)


# GUI
prozor = Tk()
prozor.option_add('*font', ('Times', 10))
prozor.title("Gis-kit")
prozor.geometry("1600x800+0+0")
color = '#badcf7'
prozor.configure(bg=color)
photo = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/icon.png"))
prozor.iconphoto(False, photo)

# ucitavanje svih slika potrebnih za gui
imgVector = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/vector.png"))
imgRaster = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/raster.png"))
imgSave = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/save.png"))
imgSaveAs = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/saveas.png"))
imgDelete = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/delete.png"))
imgUnion = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/union.png"))
imgIntersect = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/intersect.png"))
imgDifference = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/difference.png"))
imgClassification = ImageTk.PhotoImage(
    Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/classification.png"))
imgVectorize = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/polygonize.png"))
imgClipRaster = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/clipraster.png"))
imgStatistics = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/statistics.jpg"))
imgAttable = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/attable.png"))
imgPreview = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/preview.png"))
imgDirectory = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/directory.png"))
imgZoomIn = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/zoomin.png"))
imgZoomOut = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/zoomout.png"))
imgZoomExtent = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/zoomfull.png"))
imgPan = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/pan.png"))
imgClose = ImageTk.PhotoImage(Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/close.png"))
imgReprojection = ImageTk.PhotoImage(
    Image.open("C:/Users/korisnik/Desktop/GIS/Projekat/slikeProjekat/reprojection.png"))

# pravljenje menubar-a sa osnovnim funkcijama i zadacima
menubar = Menu(prozor, background='#e4edf5')
prozor.config(menu=menubar)

filemenu = Menu(menubar, tearoff=0, background='#e4edf5')
menubar.add_cascade(label="File", menu=filemenu)
openmenu = Menu(filemenu, background='#e4edf5', tearoff=0)
openmenu.add_command(label="Vector", image=imgVector, compound='left', command=openVector)
openmenu.add_command(label="Raster", image=imgRaster, compound='left', command=openRaster)
filemenu.add_cascade(label="Open", menu=openmenu)
filemenu.add_command(label="Find directory", image=imgDirectory, compound='left', command=findDirectory)
filemenu.add_command(label="Close", image=imgClose, compound='left', command=closeprogram)

editmenu = Menu(menubar, tearoff=0, background='#e4edf5')
menubar.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Delete', image=imgDelete, compound='left', command=iskacuciProzorZaDelete)
editmenu.add_command(label='Reprojection', image=imgReprojection, compound='left', command=reprojekcija)

vectormenu = Menu(menubar, tearoff=0, background='#e4edf5')
menubar.add_cascade(label="Vector", menu=vectormenu)
overlaymenu = Menu(vectormenu, background='#e4edf5', tearoff=0)
overlaymenu.add_command(label="Union", background='#e4edf5', image=imgUnion, compound='left', command=unija)
overlaymenu.add_command(label="Intersection", background='#e4edf5', image=imgIntersect, compound='left', command=presek)
overlaymenu.add_command(label="Difference", background='#e4edf5', image=imgDifference, compound='left', command=razlika)
vectormenu.add_cascade(label="Overlay", menu=overlaymenu)
vectormenu.add_command(label="Classification", background='#e4edf5', image=imgClassification, compound='left',
                       command=klasifikacija)

rastermenu = Menu(menubar, tearoff=0, background='#e4edf5')
menubar.add_cascade(label="Raster", menu=rastermenu)
rastermenu.add_command(label="Polygonize", background='#e4edf5', image=imgVectorize, compound='left',
                       command=vektorizacija)
rastermenu.add_command(label="Clip raster by mask layer", background='#e4edf5', image=imgClipRaster, compound='left',
                       command=isecanjeRastera)
rastermenu.add_command(label="Statistics", background='#e4edf5', image=imgStatistics, compound='left',
                       command=statistika)

# leftframe za toolbar, alate i ucitane lejere, a rightframe za prikaz
leftframe = Frame(prozor, width=300, height=700, bg='#e4edf5')
rightframe = Frame(prozor, width=1050, height=700, bg='#e4edf5')
leftframe.pack(side=LEFT, fill=Y, expand=False, padx=5)
rightframe.pack(side=RIGHT, fill=BOTH, expand=True, pady=50, padx=5)

# panel2 su lejeri
panel1 = Frame(leftframe, width=300, height=300, bg='#e4edf5')
panel1.grid(row=0, column=0, padx=10, pady=5)
panel2 = Frame(leftframe, width=300, height=450, bg='#e4edf5')
panel2.grid(row=1, column=0, padx=10, pady=5)

# panel1a je toolbar, panel1b su alati
panel1a = Frame(panel1, width=50, height=300, bg='#e4edf5')
panel1a.grid(row=0, column=0)
panel1b = Frame(panel1, width=250, height=300, bg='#e4edf5')
panel1b.grid(row=0, column=1, pady=5)

# toolbar
attable = Button(panel1a, image=imgAttable, command=openAT)
attable.grid(row=0, column=0, pady=5)

# dugmad za ucitavanje vektora i rastera i njihov prikaz
vector = Button(panel1a, image=imgVector, compound=TOP, command=openVector)
vector.grid(row=1, column=0, pady=5)

raster = Button(panel1a, image=imgRaster, compound=TOP, command=openRaster)
raster.grid(row=2, column=0, pady=5)

button_preview = tk.Button(panel1a, image=imgPreview, compound=TOP, command=preview)
button_preview.grid(row=3, column=0)

# alati
intersection = Button(panel1b, image=imgIntersect, compound=TOP, command=presek)
intersection.grid(row=0, column=0, padx=5, pady=5)

union = Button(panel1b, image=imgUnion, compound=TOP, command=unija)
union.grid(row=0, column=1, padx=5)

difference = Button(panel1b, image=imgDifference, compound=TOP, command=razlika)
difference.grid(row=0, column=2, padx=5)

classButton = Button(panel1b, image=imgClassification, compound=TOP, command=klasifikacija)
classButton.grid(row=0, column=3, padx=5)

clipraster = Button(panel1b, image=imgClipRaster, compound=TOP, command=isecanjeRastera)
clipraster.grid(row=1, column=0, padx=5)

polygonize = Button(panel1b, image=imgVectorize, compound=TOP, command=vektorizacija)
polygonize.grid(row=1, column=1, padx=5)

statButton = Button(panel1b, image=imgStatistics, compound=TOP, command=statistika)
statButton.grid(row=1, column=2, padx=5)

reprojButton = Button(panel1b, image=imgReprojection, compound=TOP, command=reprojekcija)
reprojButton.grid(row=1, column=3, padx=5)


# tooltip
class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500  # miliseconds
        self.wraplength = 180  # pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)  # uzima samo label a brise prozor
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


attable_tp = CreateToolTip(attable, 'Open Attribute Table')
vector_tp = CreateToolTip(vector, 'Add vector')
raster_tp = CreateToolTip(raster, 'Add raster')
preview_tp = CreateToolTip(button_preview, 'Show selected file')
intersect_tp = CreateToolTip(intersection, 'Intersection')
union_tp = CreateToolTip(union, 'Union')
difference_tp = CreateToolTip(difference, 'Difference')
classif_tp = CreateToolTip(classButton, 'Classification')
clip_tp = CreateToolTip(clipraster, 'Clip raster by mask layer')
poly_tp = CreateToolTip(polygonize, 'Polygonize')
stat_tp = CreateToolTip(statButton, 'Raster statistics')
reproj_tp = CreateToolTip(reprojButton, 'Reprojection')

podpanel = Frame(panel2, width=300, height=440)
podpanel.grid(row=1, column=0)
lista = tk.Listbox(podpanel, selectmode='single')
lista.grid(row=0, column=0)
scrollbar = Scrollbar(podpanel)
scrollbar.grid(row=0, column=1)
lista.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=lista.yview)

ram = Frame(rightframe)
ram.pack(side=RIGHT, fill=BOTH, expand=True, padx=5)
canvas = FigureCanvasTkAgg(fig, ram)
canvas.draw()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(canvas, ram)
toolbar.update()

prozor.mainloop()