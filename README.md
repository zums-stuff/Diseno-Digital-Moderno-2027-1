# Diseño Digital Moderno — 2027-1

Repositorio del equipo para la materia **Diseño Digital Moderno** (Grupo 5),
Facultad de Ingeniería, UNAM. Semestre 2027-1.

## Integrantes

- Duarte Puertas Manuel
- Hernandez Rosas Jafet Daniel
- Reyes Garcia Miguel Angel
- Torres Rodriguez Lizeth Danae

## Tarea 1 — Sistemas numéricos y sumador binario

Programa en Python (Tkinter) que convierte números entre bases 2, 8, 10 y 16
(enteros, fraccionarios y negativos en complemento a 2 de 6 bits) y realiza la
suma binaria de dos números de 6 bits, mostrando los acarreos y el caso límite
de desbordamiento. El reporte en PDF y el código fuente están en este
repositorio.

**Video explicativo:** https://youtu.be/Xfu8AbT2y00


## Proyecto 1 - Elementos principales en la construcción de un sistema alambrado

Construcción de un sistema digital alambrado básico únicamente con el uso de compuertas básicas, el cual
debe contar con dos entradas, y solo cuando ambas entradas sean iguales se deberá encender
una luz.

**Video explicativo:** https://youtu.be/R66zv_TvAZE

## Proyecto 2 - Tablas de verdad

**Video explicativo:** https://youtu.be/KSkfQ0wjZ-U

Entregable en video: `P02/Video_Proyecto2.mp4`

## Proyecto 3 - Sistema de supervisión con circuitos MSI

Sistema de seguridad con 9 puntos de supervisión, implementado con circuitos de
mediana escala de integración: un codificador con prioridad 74147, una etapa de
inversión de sus salidas y un decodificador BCD a 7 segmentos (7447/7448) que
muestra en el display el número del punto que detecta una intrusión.

Las entradas se implementaron con módulos de pares infrarrojos, cuya respuesta
resultó poco sensible frente a la distancia y a la iluminación del entorno. Por
eso la verificación de la lógica combinacional se hizo excitando las entradas del
codificador con un dipswitch, lo que permitió comprobar de forma aislada la cadena
completa: codificación con prioridad, inversión y decodificado. El reporte
documenta cinco combinaciones del dipswitch y el dígito resultante en el display.

Reporte en PDF: `P03/Reporte_Proyecto3.pdf`

## Estructura

```
.
├── .gitignore                               # Excluye artefactos de compilación
├── T01/                                     # Tarea 1 — Sistemas numéricos
│   ├── Tarea1_SistemasNumericos.py          # Copia del programa (idéntica a tarea1.py)
│   ├── Tarea1_SistemasNumericos_Reporte.pdf # Reporte en PDF
│   ├── Tarea 1 Video.mp4                    # Video explicativo
│   └── Tarea1_LaTeX/                        # Fuentes LaTeX del reporte
│       ├── main.tex
│       ├── config.tex
│       ├── tarea1.py                        # Programa principal (el que cita el reporte)
│       └── img/
│           └── ejecucion/                   # Capturas de las 12 pruebas del programa
├── P02/                                     # Proyecto 2 — Tablas de verdad
│   └── Video_Proyecto2.mp4                  # Entregable en video
└── P03/                                     # Proyecto 3
    ├── main.tex                             # Fuentes LaTeX del reporte
    ├── Reporte_Proyecto3.pdf                # Reporte en PDF (entregable)
    ├── config/
    │   ├── config.tex                       # Preámbulo compartido
    │   └── references.bib                   # Fuentes bibliográficas
    ├── images/                              # Logos y figuras del reporte
    └── build/                               # Artefactos de compilación, no se versionan
```
