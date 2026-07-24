#!/bin/python3

# Script creado por Nita, colaboradora de LyndsOS

import tkinter as tk
from tkinter import ttk
from random import randint
import json
import os

ARCHIVO_SCORE = "score-gatas.json"

# ----------------------------
# Skins y Fondos
# ----------------------------
SKINS = {
    "normal": "🐱",
    "pirata": "🐱‍☠️",
    "espacial": "🐱🚀",
    "fiesta": "😺🎉",
    "ninja": "🐱🥷",
    "robot": "🤖🐱",
    "oro": "🐱✨",
    "samurai": "🐱🗡️",
    "vampiro": "🐱🧛",
    "magico": "🐱✨🪄",
    "hada": "🐱🧚",
    "payaso": "🐱🤡",
    "fantasma": "🐱👻",
    "zombie": "🐱🧟",
    "principe": "🐱🤴",
    "princesa": "🐱👸",
    "rockero": "🐱🎸",
    "deportista": "🐱🏀",
    "chef": "🐱👨‍🍳",
    "detective": "🐱🕵️",
    "explorador": "🐱🧭",
    "cientifico": "🐱🔬"
}

PRECIOS_SKINS = {skin: i*10 for i, skin in enumerate(list(SKINS.keys())[1:], 1)}

FONDOS = {
    "rosa": "#ffeef2", "azul": "#d6f0ff", "verde": "#dcffe0", "morado": "#f0ddff",
    "negro": "#1e1e1e", "naranja": "#ffd8b0", "rojo": "#ffb0b0", "amarillo": "#ffffb0",
    "celeste": "#b0ffff", "lila": "#e0b0ff", "turquesa": "#b0fff0", "gris": "#c0c0c0",
    "marron": "#d2b48c", "blanco": "#ffffff", "dorado": "#fff5b0"
}

PRECIOS_FONDOS = {fondo: i*10 for i, fondo in enumerate(list(FONDOS.keys())[1:], 1)}

# ----------------------------
# Cargar y guardar datos
# ----------------------------
def cargar_datos():
    if os.path.exists(ARCHIVO_SCORE):
        try:
            with open(ARCHIVO_SCORE, "r", encoding="utf-8") as f:
                d = json.load(f)
                return (
                    d.get("puntos", 0),
                    d.get("skin", "normal"),
                    d.get("desbloqueadas_skins", ["normal"]),
                    d.get("fondo", "rosa"),
                    d.get("desbloqueados_fondos", ["rosa"])
                )
        except:
            pass
    return 0, "normal", ["normal"], "rosa", ["rosa"]

def guardar():
    datos = {
        "puntos": puntos,
        "skin": skin_actual,
        "desbloqueadas_skins": skins_desbloqueadas,
        "fondo": fondo_actual,
        "desbloqueados_fondos": fondos_desbloqueados
    }
    with open(ARCHIVO_SCORE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)

# ----------------------------
# Ventana principal
# ----------------------------
ventana = tk.Tk()
ventana.title("Gati Clicker 🐱")
ventana.geometry("1000x1000")

puntos, skin_actual, skins_desbloqueadas, fondo_actual, fondos_desbloqueados = cargar_datos()

pantalla_completa = False
def toggle_fullscreen(event=None):
    global pantalla_completa
    pantalla_completa = not pantalla_completa
    ventana.attributes("-fullscreen", pantalla_completa)
def salir_fullscreen(event=None):
    global pantalla_completa
    pantalla_completa = False
    ventana.attributes("-fullscreen", False)

ventana.bind("<F11>", toggle_fullscreen)
ventana.bind("<Escape>", salir_fullscreen)
ventana.config(bg=FONDOS[fondo_actual])

# ----------------------------
# Variables globales
# ----------------------------
gato = None
label_puntos = None

# ----------------------------
# Funciones juego
# ----------------------------
def actualizar_puntos():
    if label_puntos is not None:
        label_puntos.config(text=f"Puntos: {puntos}")

def mover_gato():
    if gato is not None:
        x = randint(50, ventana.winfo_width() - 100)
        y = randint(120, ventana.winfo_height() - 100)
        gato.place(x=x, y=y)
        gato.lift()

def click():
    global puntos
    puntos += 1
    actualizar_puntos()
    mover_gato()
    guardar()

def cambiar_skin(skin):
    global skin_actual, puntos
    if skin in skins_desbloqueadas:
        skin_actual = skin
        gato.config(text=SKINS[skin])
        guardar()
        return
    costo = PRECIOS_SKINS.get(skin, 999)
    if puntos >= costo:
        puntos -= costo
        skins_desbloqueadas.append(skin)
        skin_actual = skin
        gato.config(text=SKINS[skin])
        actualizar_puntos()
        guardar()

def cambiar_fondo(color):
    global fondo_actual, puntos
    if color in fondos_desbloqueados:
        fondo_actual = color
        ventana.config(bg=FONDOS[color])
        guardar()
        return
    costo = PRECIOS_FONDOS.get(color, 999)
    if puntos >= costo:
        puntos -= costo
        fondos_desbloqueados.append(color)
        fondo_actual = color
        ventana.config(bg=FONDOS[color])
        actualizar_puntos()
        guardar()

# ----------------------------
# Tienda con Tabs y Scroll visible pegado a botones
# ----------------------------
tienda = None
def abrir_tienda():
    global tienda
    if tienda is not None and tk.Toplevel.winfo_exists(tienda):
        tienda.lift()
        return

    tienda = tk.Toplevel(ventana)
    tienda.title("Tienda 🛒")
    tienda.geometry("450x500")

    notebook = ttk.Notebook(tienda)
    notebook.pack(fill="both", expand=True)

    def _on_mousewheel(event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/40)), "units")

    def crear_tab(frame_tab, items, desbloqueados, actual, cambiar_func, precios, icon=""):
        # Contenedor general
        frame_main = tk.Frame(frame_tab)
        frame_main.pack(fill="both", expand=True, padx=5, pady=5)

        # Canvas y Scrollbar pegada
        canvas = tk.Canvas(frame_main)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame_main, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno donde se colocan los botones
        scroll_frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: _on_mousewheel(e, canvas))

        def cargar_items():
            for w in scroll_frame.winfo_children():
                w.destroy()
            for i in items:
                def usar(it=i):
                    cambiar_func(it)
                    cargar_items()
                if i in desbloqueados:
                    color = "green" if i == actual else "black"
                    texto = f"{icon}{i}" if icon else f"{items[i]} {i}"
                else:
                    color = "gray"
                    texto = f"❓ ??? ({precios.get(i,0)})"
                tk.Button(scroll_frame, text=texto, fg=color, width=25, command=usar).pack(pady=2)
        cargar_items()

    tab_skins = tk.Frame(notebook)
    notebook.add(tab_skins, text="Skins")
    crear_tab(tab_skins, SKINS, skins_desbloqueadas, skin_actual, cambiar_skin, PRECIOS_SKINS)

    tab_fondos = tk.Frame(notebook)
    notebook.add(tab_fondos, text="Fondos")
    crear_tab(tab_fondos, FONDOS, fondos_desbloqueados, fondo_actual, cambiar_fondo, PRECIOS_FONDOS, icon="🎨 ")

# ----------------------------
# Interfaz principal
# ----------------------------
label_titulo = tk.Label(ventana, text="🐱 GATI CLICKER 🐱", font=("Arial",20,"bold"), bg=FONDOS[fondo_actual])
label_titulo.pack(pady=10)

label_puntos = tk.Label(ventana, text=f"Puntos: {puntos}", font=("Arial",16), bg=FONDOS[fondo_actual])
label_puntos.pack(pady=10)

gato = tk.Button(ventana, text=SKINS[skin_actual], font=("Arial",40), command=click)
gato.place(x=200, y=200)

btn_tienda = tk.Button(ventana, text="🛒 Tienda", command=abrir_tienda)
btn_tienda.pack(pady=10)

ventana.mainloop()
