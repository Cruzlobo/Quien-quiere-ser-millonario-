import pygame
import json
import time
import math
import random
from pygame.locals import *
from Funciones import *

niveles = [1000, 500, 300, 200, 100]
nombres_amigos = ["Juan", "María", "Pedro", "Ana", "Luis"]
nivel_actual = 100
tiempo_limite = 30
tiempo_inicio = None
flag = True
indice_pregunta = 0  
pregunta_actual = None
modo_visualizacion_cuatro_opciones = True
monto_total = 0
niveles_acertados= 0
preguntas_realizadas = 0

try:
    fondo = pygame.image.load('imagenes/fondo.jpg')
except FileNotFoundError:
    print("Error: Archivo no encontrado")
rectangulos_opciones = []

ancho = 800
alto = 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("¿Quién quiere ser millonario?")
preguntas= cargar_preguntas()

publico_image = pygame.image.load('imagenes\publico.png')
boton_x = 50
boton_y = 50
radio_boton = 15
ancho_publico = radio_boton * 2  
alto_publico = radio_boton * 2
publico_image = pygame.transform.scale(publico_image, (ancho_publico, alto_publico))
publico_x = boton_x - radio_boton
publico_y = boton_y - radio_boton

telefono_image = pygame.image.load('imagenes\\telefono.png')
boton_telefono_x = 80
boton_telefono_y = 35
ancho_telefono = radio_boton *2
alto_telefono = radio_boton *2
telefono_image = pygame.transform.scale(telefono_image, (ancho_telefono, alto_telefono))
telefono_x = boton_telefono_x + radio_boton  
telefono_y = boton_telefono_y + radio_boton

boton_50_50_image = pygame.image.load('imagenes\\boton_50_50.png')  
boton_50_50_x = 130  
boton_50_50_y = 34
ancho_boton_50_50 = radio_boton *2  
alto_boton_50_50 = radio_boton *2 
boton_50_50_image = pygame.transform.scale(boton_50_50_image,\
                     (ancho_boton_50_50, alto_boton_50_50))
mitad_50_50_x = boton_50_50_x + radio_boton
mitad_50_50_Y = boton_50_50_y + radio_boton




if __name__ == "__main__":
    pygame.init()


while flag:
    
    for evento in pygame.event.get():
        if evento.type == QUIT:
            flag = False
        if evento.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i, opcion_rectangulo in enumerate(rectangulos_opciones):
                if opcion_rectangulo.collidepoint(x, y):
                    if 0 <= i < len(opciones):
                        if opciones[i][0].lower() == pregunta_actual["respuesta_correcta"].lower():
                            
                            preguntas_realizadas += 1
                            if preguntas_realizadas == 22:
                               
                                mostrar_mensaje_ganador(ventana)
                                time.sleep(3)
                                flag = False
                            else:
                                indice_pregunta, nivel_actual = mostrar_siguiente_pregunta\
                                    (indice_pregunta, nivel_actual, preguntas)
                                tiempo_inicio = reiniciar_temporizador()
                                puntaje_obtenido = nivel_actual
                                niveles_acertados += 2  
                                if niveles_acertados == 5:
                                    monto_total += 1000
                                elif niveles_acertados == 10:
                                    monto_total += 32000
                                guardar_progreso(niveles_acertados, monto_total)
                            
                        else:
                            mostrar_game_over(ventana)
                            time.sleep(3)
                            flag = False
            if (x - boton_x) ** 2 + (y - boton_y) ** 2 <= radio_boton ** 2:
                    opcion_mas_probable = calcular_opcion_mas_probable_comodin_publico(pregunta_actual)
                    mensaje = opcion_mas_probable
                    mostrar_ventana_emergente_publico(mensaje,ventana) 
                    comodin_publico_usada_en_pregunta = True      
            if (telefono_x - radio_boton <= x <= telefono_x + radio_boton * 2) and\
                  (telefono_y - radio_boton <= y <= telefono_y + radio_boton * 2):
                if llamada_amigo_usada != True:
                    amigo = random.choice(nombres_amigos)
                    respuesta_amigo = (f"{amigo} la respuesta es {pregunta_actual['respuesta_correcta']}",ventana) 
                    mostrar_llamada_amigo(respuesta_amigo, opciones , ventana)
                    llamada_amigo_usada = True 
                else:
                    mensaje="Comodin no disponible"
                    mostrar_ventana_emergente_publico(mensaje, ventana)     
            if (mitad_50_50_x - radio_boton <= x <= mitad_50_50_x + radio_boton * 2) and\
                  (mitad_50_50_Y - radio_boton <= y <= mitad_50_50_Y + radio_boton * 2):
                if dos_opciones_usadas != True:
                    ventana.fill((0,0,0))
                    modo_visualizacion_cuatro_opciones = False
                    dos_opciones_usadas = True
                    pygame.display.update()
                else:
                    mensaje="Comodin no disponible"
                    mostrar_ventana_emergente_publico(mensaje, ventana)
            else:
                modo_visualizacion_cuatro_opciones = True  
      
   
    if tiempo_inicio is None:
        tiempo_inicio = reiniciar_temporizador()
    
    
    tiempo_actual = time.time()
    tiempo_transcurrido = tiempo_actual - tiempo_inicio
    tiempo_restante = max(tiempo_limite - tiempo_transcurrido, 0)
    if tiempo_restante == 0:
        mostrar_game_over(ventana)
        time.sleep(3)
        flag = False
    ventana.fill((0, 0, 0), (100, 10, 250, 36))  
    try:
        pregunta_actual = preguntas[indice_pregunta]
    except IndexError:
        print("Se han agotado todas las preguntas")
        mostrar_mensaje_ganador(ventana)
        time.sleep(3)
        flag = False
    opciones = pregunta_actual["opciones"]
    ventana.fill((0, 0, 0))
    ventana.blit(fondo,(0, 0))
    dibujar_monto_ganado(monto_total, ventana)
    dibujar_pregunta(pregunta_actual["pregunta"],ventana,ancho)
    
    if modo_visualizacion_cuatro_opciones:
        dibujar_cuatro_opciones(opciones, ventana, rectangulos_opciones)
    else:
        dibujar_dos_opciones(opciones, ventana, rectangulos_opciones)
    dibujar_temporizador(tiempo_restante, ventana, ancho)
    pygame.draw.circle(ventana, (255, 255, 255), (boton_x, boton_y), radio_boton)
    pygame.draw.circle(ventana, (255, 255, 255), (telefono_x, telefono_y), radio_boton)
    pygame.draw.circle(ventana, (255, 255, 255), (mitad_50_50_x, mitad_50_50_Y), radio_boton)
    
    ventana.blit(publico_image, (publico_x, publico_y))
    ventana.blit(telefono_image, (telefono_x - radio_boton, telefono_y - radio_boton)) 
    ventana.blit(boton_50_50_image, (mitad_50_50_x - radio_boton, mitad_50_50_Y - radio_boton))
    
    
    dibujar_niveles(niveles, nivel_actual, ventana)
    
    
    pygame.display.update()

pygame.quit()
