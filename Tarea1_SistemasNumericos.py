import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction

DIGITOS = "0123456789ABCDEF"
PRECISION_SALIDA = 16


# Revisa que el número escrito sí corresponda a la base seleccionada
def validar_numero(numero, base):
    numero = numero.strip().upper()

    if numero.startswith("-"):
        numero = numero[1:]

    if numero == "" or numero.count(".") > 1:
        return False

    if numero.endswith("."):
        return False

    partes = numero.split(".")

    if all(parte == "" for parte in partes):
        return False

    for parte in partes:
        for caracter in parte:
            if caracter not in DIGITOS:
                return False
            if DIGITOS.index(caracter) >= base:
                return False

    return True


# Convierte el número de entrada a un valor exacto usando notación posicional
def a_fraccion(numero, base):
    numero = numero.strip().upper()

    negativo = numero.startswith("-")
    if negativo:
        numero = numero[1:]

    if "." in numero:
        parte_entera, parte_decimal = numero.split(".")
    else:
        parte_entera = numero
        parte_decimal = ""

    if parte_entera == "":
        parte_entera = "0"

    entero = 0
    for caracter in parte_entera:
        entero = entero * base + DIGITOS.index(caracter)

    fraccion = Fraction(0, 1)
    divisor = base

    for caracter in parte_decimal:
        fraccion += Fraction(DIGITOS.index(caracter), divisor)
        divisor *= base

    resultado = Fraction(entero, 1) + fraccion

    if negativo:
        resultado = -resultado

    return resultado


# Convierte el valor a la base destino con el método de la cuenta larga
def fraccion_a_base(valor, base, precision=PRECISION_SALIDA):
    if valor == 0:
        return "0"

    negativo = valor < 0
    if negativo:
        valor = -valor

    entero = valor.numerator // valor.denominator
    resto = valor - entero

    if entero == 0:
        parte_entera = "0"
    else:
        parte_entera = ""
        while entero > 0:
            residuo = entero % base
            parte_entera = DIGITOS[residuo] + parte_entera
            entero //= base

    parte_decimal = ""

    for _ in range(precision):
        if resto == 0:
            break

        resto *= base
        digito = resto.numerator // resto.denominator
        parte_decimal += DIGITOS[digito]
        resto -= digito

    resultado = parte_entera

    if parte_decimal:
        resultado += "." + parte_decimal

    if negativo:
        resultado = "-" + resultado

    return resultado


# Une las dos etapas: interpretar la base origen y generar la base destino
def convertir(numero, base_origen, base_destino):
    return fraccion_a_base(a_fraccion(numero, base_origen), base_destino)


# Sumador de una sola columna
def sumar_un_bit(bit_a, bit_b, acarreo_in):
    suma_total = bit_a + bit_b + acarreo_in
    suma = suma_total % 2
    acarreo_out = 1 if suma_total >= 2 else 0
    return suma, acarreo_out


# Obtiene la magnitud positiva en exactamente 5 bits
def decimal_a_binario_5_bits(numero):
    if numero < 0 or numero > 31:
        return None

    resultado = ""
    for _ in range(5):
        resultado = str(numero % 2) + resultado
        numero //= 2
    return resultado


# Suma 1 a una cadena de 5 bits usando el mismo sumador de 1 bit
def sumar_uno_5_bits(bits):
    resultado = ""
    acarreo = 1

    for i in range(4, -1, -1):
        suma, acarreo = sumar_un_bit(int(bits[i]), 0, acarreo)
        resultado = str(suma) + resultado

    return resultado


# Genera la representación con signo de 6 bits
# Si el número es negativo, se invierten los 5 bits de magnitud y se suma 1
def decimal_a_complemento_2_6_bits(numero):
    if numero < -32 or numero > 31:
        return None

    if numero >= 0:
        magnitud = decimal_a_binario_5_bits(numero)
        return {
            "bits": "0" + magnitud,
            "magnitud": magnitud,
            "invertido": "",
            "despues_mas_uno": "",
            "negativo": False,
            "caso_limite": False
        }

    # -32 es el caso límite en complemento a 2 de 6 bits
    if numero == -32:
        return {
            "bits": "100000",
            "magnitud": "100000",
            "invertido": "011111",
            "despues_mas_uno": "100000",
            "negativo": True,
            "caso_limite": True
        }

    magnitud = decimal_a_binario_5_bits(abs(numero))
    invertido = ""
    for bit in magnitud:
        invertido += "1" if bit == "0" else "0"

    complemento_magnitud = sumar_uno_5_bits(invertido)
    return {
        "bits": "1" + complemento_magnitud,
        "magnitud": magnitud,
        "invertido": invertido,
        "despues_mas_uno": complemento_magnitud,
        "negativo": True,
        "caso_limite": False
    }


# Realiza la suma completa, las 5 columnas de magnitud y una sexta para el signo
def sumar_6_bits(a, b):
    datos_a = decimal_a_complemento_2_6_bits(a)
    datos_b = decimal_a_complemento_2_6_bits(b)

    bits_a = datos_a["bits"]
    bits_b = datos_b["bits"]

    resultado_magnitud = ""
    # El primer acarreo comienza en cero y se va propagando entre columnas
    acarreo = 0
    detalle_ciclos = []

    for i in range(5, 0, -1):
        acarreo_in = acarreo
        suma, acarreo = sumar_un_bit(int(bits_a[i]), int(bits_b[i]), acarreo)
        resultado_magnitud = str(suma) + resultado_magnitud
        detalle_ciclos.append((6 - i, bits_a[i], bits_b[i], acarreo_in, suma, acarreo))

    acarreo_entrada_signo = acarreo

    # Sexta suma:bits de signo
    suma_signo, acarreo_salida_signo = sumar_un_bit(
        int(bits_a[0]), int(bits_b[0]), acarreo_entrada_signo
    )

    resultado_bits = str(suma_signo) + resultado_magnitud
    # Hay overflow cuando el acarreo que entra al signo no coincide con el que sale
    overflow = acarreo_entrada_signo != acarreo_salida_signo

    # Convertimos el resultado solo para mostrar también su valor decimal
    valor = 0
    for bit in resultado_bits:
        valor = valor * 2 + int(bit)
    if resultado_bits[0] == "1":
        valor -= 64

    return {
        "a": datos_a,
        "b": datos_b,
        "resultado_bits": resultado_bits,
        "resultado_decimal": valor,
        "overflow": overflow,
        "acarreo_entrada_signo": acarreo_entrada_signo,
        "acarreo_salida_signo": acarreo_salida_signo,
        "detalle_ciclos": detalle_ciclos,
        "signo": (bits_a[0], bits_b[0], acarreo_entrada_signo,
                  suma_signo, acarreo_salida_signo)
    }

def mostrar_error(texto):
    messagebox.showerror("Error", texto)


def escribir_resultado(texto):
    caja_resultado.config(state="normal")
    caja_resultado.delete("1.0", tk.END)
    caja_resultado.insert(tk.END, texto)
    caja_resultado.config(state="disabled")


# Validación usada por la interfaz antes de intentar una conversión
def comprobar_numero(numero, base, nombre):
    if numero.strip() == "":
        mostrar_error("Escribe el " + nombre + ".")
        return False

    if not validar_numero(numero, base):
        mostrar_error(
            "El " + nombre + " no es válido para base " + str(base) +
            ".\n\nDígitos permitidos: " + DIGITOS[:base] +
            "\nSe permite un signo negativo al inicio y un solo punto decimal."
        )
        return False

    return True


# Lee los datos de la pestaña de conversión y muestra el resultado
def realizar_conversion():
    base_origen = int(combo_origen.get())
    base_destino = int(combo_destino.get())
    numero = entrada_conversion.get().strip().upper()

    if not comprobar_numero(numero, base_origen, "número"):
        return

    resultado = convertir(numero, base_origen, base_destino)

    escribir_resultado(
        "Conversión de bases\n\n"
        "Número: " + numero + "\n"
        "Base de origen: " + str(base_origen) + "\n"
        "Base de destino: " + str(base_destino) + "\n\n"
        "Resultado: " + resultado + "  (base " + str(base_destino) + ")"
    )


# Prepara el procedimiento que se muestra
def texto_complemento(nombre, numero, datos):
    if not datos["negativo"]:
        return (
            nombre + " = " + str(numero) + "\n"
            "Magnitud de 5 bits:          " + datos["magnitud"] + "\n"
            "Bit de signo:                0\n"
            "Representación de 6 bits:    " + datos["bits"] + "\n\n"
        )

    if datos["caso_limite"]:
        return (
            nombre + " = -32\n"
            "Caso límite de 6 bits:       100000\n"
            "(-32 es el menor valor representable en complemento a 2 de 6 bits.)\n\n"
        )

    return (
        nombre + " = " + str(numero) + "\n"
        "Magnitud de 5 bits:          " + datos["magnitud"] + "\n"
        "Bits de magnitud invertidos: " + datos["invertido"] + "\n"
        "Invertidos + 1:              " + datos["despues_mas_uno"] + "\n"
        "Bit de signo:                1\n"
        "Complemento a 2 de 6 bits:  " + datos["bits"] + "\n\n"
    )


# Lee los dos enteros, valida el rango y ejecuta el sumador de 6 bits
def realizar_operacion():
    texto_a = entrada_numero1.get().strip()
    texto_b = entrada_numero2.get().strip()

    if texto_a == "" or texto_b == "":
        mostrar_error("Escribe los dos números decimales enteros.")
        return

    try:
        a = int(texto_a)
        b = int(texto_b)
    except ValueError:
        mostrar_error("El sumador solo acepta números decimales enteros, por ejemplo: -12, 0 o 25.")
        return

    if not (-32 <= a <= 31) or not (-32 <= b <= 31):
        mostrar_error("Cada número debe estar en el rango de -32 a 31.")
        return

    datos = sumar_6_bits(a, b)

    procedimiento = "EMULADOR DE SUMADOR BINARIO DE 6 BITS\n\n"
    procedimiento += texto_complemento("A", a, datos["a"])
    procedimiento += texto_complemento("B", b, datos["b"])

    procedimiento += "SUMA SECUENCIAL DE COLUMNAS\n"
    procedimiento += "Ciclo | A | B | Cin | Suma | Cout\n"
    procedimiento += "----------------------------------\n"

    for ciclo, bit_a, bit_b, cin, suma, cout in datos["detalle_ciclos"]:
        procedimiento += (
            str(ciclo).rjust(5) + " | " + bit_a + " | " + bit_b + " |  " +
            str(cin) + "  |   " + str(suma) + "  |   " + str(cout) + "\n"
        )

    sa, sb, cin_s, suma_s, cout_s = datos["signo"]
    procedimiento += (
        "    6 | " + sa + " | " + sb + " |  " + str(cin_s) +
        "  |   " + str(suma_s) + "  |   " + str(cout_s) + "   <- bit de signo\n\n"
    )

    procedimiento += (
        "Suma binaria:\n"
        "   " + datos["a"]["bits"] + "\n"
        "+  " + datos["b"]["bits"] + "\n"
        "--------\n"
        "   " + datos["resultado_bits"] + "\n\n"
        "Resultado binario final: " + datos["resultado_bits"] + "\n"
        "Interpretación decimal:  " + str(datos["resultado_decimal"]) + "\n\n"
        "Acarreo que entra al signo: " + str(datos["acarreo_entrada_signo"]) + "\n"
        "Acarreo que sale del signo:  " + str(datos["acarreo_salida_signo"]) + "\n"
    )

    if datos["overflow"]:
        procedimiento += (
            "Overflow: SÍ\n"
            "Los acarreos son diferentes, por lo tanto ocurrió desbordamiento.\n"
            "El patrón de 6 bits se muestra, pero su interpretación decimal no "
            "representa la suma matemática fuera del rango -32 a 31."
        )
    else:
        procedimiento += "Overflow: NO\nLos acarreos de entrada y salida del signo son iguales."

    escribir_resultado(procedimiento)

def limpiar():
    entrada_conversion.delete(0, tk.END)
    entrada_numero1.delete(0, tk.END)
    entrada_numero2.delete(0, tk.END)
    combo_origen.set("10")
    combo_destino.set("2")
    escribir_resultado("")


ventana = tk.Tk()
ventana.title("Conversor y calculadora de bases")
ventana.geometry("860x760")
ventana.resizable(False, False)
ventana.configure(bg="#EEF7EE")


COLOR_FONDO = "#EEF7EE"
COLOR_TARJETA = "#F8FCF7"
COLOR_ACENTO = "#B7D7B0"
COLOR_ACENTO_2 = "#D5E8D0"
COLOR_BOTON = "#AFCFA8"
COLOR_BOTON_SEC = "#DCEBD8"
COLOR_TEXTO = "#344438"
COLOR_BORDE = "#C7DCC3"
COLOR_RESULTADO = "#F1F8EF"

estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure(
    "TNotebook",
    background=COLOR_FONDO,
    borderwidth=0
)

estilo.configure(
    "TNotebook.Tab",
    background="#DCEBD8",
    foreground=COLOR_TEXTO,
    padding=(18, 9),
    font=("Segoe UI", 10, "bold")
)

estilo.map(
    "TNotebook.Tab",
    background=[("selected", COLOR_ACENTO)],
    foreground=[("selected", "#29402D")]
)

estilo.configure(
    "TFrame",
    background=COLOR_TARJETA
)

estilo.configure(
    "TLabelFrame",
    background=COLOR_TARJETA,
    foreground=COLOR_TEXTO,
    bordercolor=COLOR_BORDE,
    relief="solid"
)

estilo.configure(
    "TLabelFrame.Label",
    background=COLOR_TARJETA,
    foreground=COLOR_TEXTO,
    font=("Segoe UI", 10, "bold")
)

estilo.configure(
    "TEntry",
    fieldbackground="#FFFFFF",
    foreground=COLOR_TEXTO,
    padding=6
)

estilo.configure(
    "TCombobox",
    fieldbackground="#FFFFFF",
    background="#FFFFFF",
    foreground=COLOR_TEXTO,
    padding=5
)

estilo.configure(
    "Principal.TButton",
    background=COLOR_BOTON,
    foreground="#29402D",
    padding=(16, 8),
    font=("Segoe UI", 10, "bold"),
    borderwidth=0
)

estilo.map(
    "Principal.TButton",
    background=[("active", "#9FC398")],
    foreground=[("active", "#203824")]
)

estilo.configure(
    "Secundario.TButton",
    background=COLOR_BOTON_SEC,
    foreground=COLOR_TEXTO,
    padding=(14, 7),
    font=("Segoe UI", 9, "bold"),
    borderwidth=0
)

estilo.map(
    "Secundario.TButton",
    background=[("active", "#C7DEC2")]
)

# ----Interfaz gráfica 
# Encabezado
encabezado = tk.Frame(ventana, bg=COLOR_FONDO)
encabezado.pack(fill="x", padx=30, pady=(22, 10))

tk.Label(
    encabezado,
    text="Conversor y calculadora de bases",
    font=("Segoe UI", 20, "bold"),
    bg=COLOR_FONDO,
    fg="#304534"
).pack()

tk.Label(
    encabezado,
    text="Conversiones de bases y sumador binario de 6 bits en complemento a 2",
    font=("Segoe UI", 10),
    bg=COLOR_FONDO,
    fg="#667A69"
).pack(pady=(4, 0))

pestanas = ttk.Notebook(ventana)
pestanas.pack(fill="x", padx=30, pady=(6, 0))

bases = [str(i) for i in range(2, 17)]

# Pestaña de conversión de bases.
pestana_conversion = ttk.Frame(pestanas, padding=22)
pestanas.add(pestana_conversion, text="Conversión")

for columna in range(2):
    pestana_conversion.columnconfigure(columna, weight=1)

tk.Label(
    pestana_conversion,
    text="Conversión entre bases",
    font=("Segoe UI", 13, "bold"),
    bg=COLOR_TARJETA,
    fg=COLOR_TEXTO
).grid(row=0, column=0, columnspan=2, pady=(2, 16))

tk.Label(
    pestana_conversion, text="Número:",
    font=("Segoe UI", 10), bg=COLOR_TARJETA, fg=COLOR_TEXTO
).grid(row=1, column=0, padx=12, pady=8, sticky="e")
entrada_conversion = ttk.Entry(pestana_conversion, width=31, font=("Segoe UI", 10))
entrada_conversion.grid(row=1, column=1, padx=12, pady=8, sticky="w")

tk.Label(
    pestana_conversion, text="Base de origen:",
    font=("Segoe UI", 10), bg=COLOR_TARJETA, fg=COLOR_TEXTO
).grid(row=2, column=0, padx=12, pady=8, sticky="e")
combo_origen = ttk.Combobox(
    pestana_conversion, values=bases, state="readonly", width=28, font=("Segoe UI", 10)
)
combo_origen.set("10")
combo_origen.grid(row=2, column=1, padx=12, pady=8, sticky="w")

tk.Label(
    pestana_conversion, text="Base de destino:",
    font=("Segoe UI", 10), bg=COLOR_TARJETA, fg=COLOR_TEXTO
).grid(row=3, column=0, padx=12, pady=8, sticky="e")
combo_destino = ttk.Combobox(
    pestana_conversion, values=bases, state="readonly", width=28, font=("Segoe UI", 10)
)
combo_destino.set("2")
combo_destino.grid(row=3, column=1, padx=12, pady=8, sticky="w")

ttk.Button(
    pestana_conversion, text="Convertir", command=realizar_conversion, style="Principal.TButton"
).grid(row=4, column=0, columnspan=2, pady=(15, 4))

# Pestaña de sumador binario con signo.
pestana_operaciones = ttk.Frame(pestanas, padding=22)
pestanas.add(pestana_operaciones, text="Sumador")

for columna in range(2):
    pestana_operaciones.columnconfigure(columna, weight=1)

tk.Label(
    pestana_operaciones,
    text="Sumador binario con signo de 6 bits",
    font=("Segoe UI", 13, "bold"),
    bg=COLOR_TARJETA,
    fg=COLOR_TEXTO
).grid(row=0, column=0, columnspan=2, pady=(2, 16))

tk.Label(
    pestana_operaciones, text="Primer decimal (-32 a 31):",
    font=("Segoe UI", 10), bg=COLOR_TARJETA, fg=COLOR_TEXTO
).grid(row=1, column=0, padx=12, pady=8, sticky="e")
entrada_numero1 = ttk.Entry(pestana_operaciones, width=31, font=("Segoe UI", 10))
entrada_numero1.grid(row=1, column=1, padx=12, pady=8, sticky="w")

tk.Label(
    pestana_operaciones, text="Segundo decimal (-32 a 31):",
    font=("Segoe UI", 10), bg=COLOR_TARJETA, fg=COLOR_TEXTO
).grid(row=2, column=0, padx=12, pady=8, sticky="e")
entrada_numero2 = ttk.Entry(pestana_operaciones, width=31, font=("Segoe UI", 10))
entrada_numero2.grid(row=2, column=1, padx=12, pady=8, sticky="w")

ttk.Button(
    pestana_operaciones, text="Calcular", command=realizar_operacion, style="Principal.TButton"
).grid(row=3, column=0, columnspan=2, pady=(15, 4))

# Área donde se muestra el procedimiento y el resultado
marco_resultado = ttk.LabelFrame(
    ventana, text="Resultado y procedimiento", padding=10
)
marco_resultado.pack(fill="both", expand=True, padx=30, pady=18)

caja_resultado = tk.Text(
    marco_resultado,
    height=16,
    width=90,
    font=("Cascadia Mono", 10),
    wrap="none",
    bg=COLOR_RESULTADO,
    fg="#344A38",
    insertbackground="#344A38",
    relief="flat",
    padx=12,
    pady=12
)
caja_resultado.pack(fill="both", expand=True)
caja_resultado.config(state="disabled")

# Botones generales de ventana
marco_botones = tk.Frame(ventana, bg=COLOR_FONDO)
marco_botones.pack(pady=(0, 20))

ttk.Button(
    marco_botones, text="Limpiar", command=limpiar, style="Secundario.TButton"
).pack(side="left", padx=6)

ttk.Button(
    marco_botones, text="Salir", command=ventana.destroy, style="Secundario.TButton"
).pack(side="left", padx=6)

ventana.mainloop()
