NUMERO_INVALIDO = "Numero de tweet invalido."
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS = "Tweets eliminados:"
ATRAS = "**"


def mostrar_menu():
    print("1. Crear Tweet")
    print("2. Buscar Tweet")
    print("3. Eliminar Tweet")
    print("4. Salir")

def normalizar(texto):
    texto = texto.lower()
    palabra = ''
    palabras = []

    for l in texto:
        if l.isalnum():
            palabra += l
        elif palabra:
            palabras.append(palabra)
            palabra = ''

    if palabra:
        palabras.append(palabra)

    return palabras




def main():
    opcion = 0
    while opcion != 4:
        mostrar_menu()
        try:
            opcion = int(input("ingrese una opcion: "))
        except ValueError:
            print("Opcion invalida.")
            continue

        if opcion == 1:
            crear_tweet()
            pass
        elif opcion == 2:
            buscar_tweet()
            pass
        elif opcion == 3:
            eliminar_tweet()
            pass
        elif opcion == 4:
            print("Finalizando programa...")
        else:
            print("Opcion invalida.")


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final, asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.
if __name__ == "__main__":
    main()