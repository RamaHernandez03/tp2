""" Palabras claves """
NUMERO_INVALIDO = "Numero de tweet invalido."
NO_ENCONTRADOS = "No se encontraron tweets."
INPUT_INVALIDO = "Input invalido."
FIN = "Finalizando..."
RESULTADOS_BUSQUEDA = "Resultados de la busqueda:"
TWEETS_ELIMINADOS = "Tweets eliminados:"

# -------------------------------------------------
# Funciones Auxiliares:

def mostrar_menu():
    """ Muestra el menu de opciones al usuario. """
    print("1. Crear Tweet")
    print("2. Buscar Tweet")
    print("3. Eliminar Tweet")
    print("4. Salir")

def normalizar(texto):
    """ Convierte el texto a minsculas y divide en palabras alfaNum. """
    texto = texto.lower()
    palabra = ""
    palabras = []

    for letra in texto:
        if letra.isalnum():
            palabra += letra
        elif palabra:
            palabras.append(palabra)
            palabra = ""

    if palabra:
        palabras.append(palabra)
    return palabras

def tokenizar_segmentos(palabra):
    """ Te arma los segmentos de Longitud N >= 3 """
    n = 3
    segmentos = set()
    for i in range(len(palabra)):
        for j in range(i + n, len(palabra) + 1):
            segmentos.add(palabra[i:j])
    return segmentos

def busqueda_binaria(lista, clave):
    """ busca una clave en una lista de tuplas ordenadas usando la busqueda binaria. """
    izquierda = 0
    derecha = len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        actual = lista[medio][0]

        if actual == clave:
            return medio
        elif actual < clave:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return -1

def insertar_en_orden(indice, clave, tweet_id):
    """ inserta una clave y su id en orden alfabetico en el indice.
     Si la clave ya existe, agrega el id. """
    izquierda = 0
    derecha = len(indice)
    while izquierda < derecha:
        medio = (izquierda + derecha) // 2
        if indice[medio][0] < clave:
            izquierda = medio + 1
        else:
            derecha = medio

    if izquierda < len(indice) and indice[izquierda][0] == clave:
        indice[izquierda][1].add(tweet_id)
    else:
        indice.insert(izquierda, (clave, {tweet_id}))

# -------------------------------------------------
# Funciones para el uso del menu:

def crear_tweet(tweets, indice_palabras, indice_segmentos, siguiente_id):
    """ te crea un "tweet", actualiza indices y devuelve el siguiente id. """
    while True:
        print("Ingrese su tweet: ")
        tweet = input(" ").strip()
        palabras_normalizadas = normalizar(tweet)

        if not palabras_normalizadas:
            print(INPUT_INVALIDO)
            continue

        tweets[siguiente_id] = tweet
        for palabra in palabras_normalizadas:
            insertar_en_orden(indice_palabras, palabra, siguiente_id)
            for segmento in tokenizar_segmentos(palabra):
                insertar_en_orden(indice_segmentos, segmento, siguiente_id)

        print(f"Listo! {siguiente_id}")
        return siguiente_id + 1

def buscar_tweet(tweets, indice_palabras, indice_segmentos):
    """ busca "tweets", Con palabras claves o segmentos de palabras claves. """
    print("Ingrese el tweet que quiere buscar: ")
    tweet = input(" ").strip()
    tokens_busqueda = normalizar(tweet)

    if not tokens_busqueda:
        print(NO_ENCONTRADOS)
        return

    resultados = None
    for token in tokens_busqueda:
        id_encontrados = set()

        pos_palabra = busqueda_binaria(indice_palabras, token)
        if pos_palabra != -1:
            id_encontrados.update(indice_palabras[pos_palabra][1])

        pos_segmento = busqueda_binaria(indice_segmentos, token)
        if pos_segmento != -1:
            id_encontrados.update(indice_segmentos[pos_segmento][1])

        if not id_encontrados:
            resultados = set()
            break

        if resultados is None:
            resultados = id_encontrados
        else:
            resultados = resultados & id_encontrados

    if not resultados:
        print(NO_ENCONTRADOS)
        return

    print(RESULTADOS_BUSQUEDA)
    for tweet_id in sorted(resultados):
        print(f"{tweet_id}. {tweets[tweet_id]}")

def eliminar_tweet(tweets, indice_palabras, indice_segmentos):
    """ Elimina si se quiere 1 o mas "tweets", y ademas actualiza los indices. """
    while True:
        print("Ingrese el tweet a eliminar:")
        tweet = input(" ").strip()
        tokens = normalizar(tweet)

        if not tokens:
            print(NO_ENCONTRADOS)
            continue

        token = tokens[0]
        id_encontrados = set()
        pos_palabra = busqueda_binaria(indice_palabras, token)
        if pos_palabra != -1:
            id_encontrados.update(indice_palabras[pos_palabra][1])

        pos_segmento = busqueda_binaria(indice_segmentos, token)
        if pos_segmento != -1:
            id_encontrados.update(indice_segmentos[pos_segmento][1])

        if not id_encontrados:
            print(NO_ENCONTRADOS)
            continue

        print(RESULTADOS_BUSQUEDA)
        for tweet_id in sorted(id_encontrados):
            print(f"{tweet_id}. {tweets[tweet_id]}")
        print("Ingrese los numeros de tweets a eliminar (ej: 0,2-4):")
        entrada = input(" ").replace(" ", "")
        if not entrada:
            print(INPUT_INVALIDO)
            continue
        try:
            seleccionados = set()
            partes = entrada.split(",")
            for parte in partes:
                if "-" in parte:
                    inicio_fin = parte.split("-")
                    if len(inicio_fin) != 2:
                        print(INPUT_INVALIDO)
                        break
                    inicio, fin = map(int, inicio_fin)
                    if inicio > fin:
                        print(INPUT_INVALIDO)
                        break
                    seleccionados.update(range(inicio, fin + 1))
                else:
                    seleccionados.add(int(parte))

            if not seleccionados.issubset(id_encontrados):
                print(NUMERO_INVALIDO)
                continue
            print(TWEETS_ELIMINADOS)
            for id_eliminar in sorted(seleccionados):
                print(f"{id_eliminar}. {tweets[id_eliminar]}")
                palabras = normalizar(tweets[id_eliminar])
                for palabra in palabras:
                    pos_palabra = busqueda_binaria(indice_palabras, palabra)
                    if pos_palabra != -1:
                        indice_palabras[pos_palabra][1].discard(id_eliminar)
                        if not indice_palabras[pos_palabra][1]:
                            indice_palabras.pop(pos_palabra)
                    for segmento in tokenizar_segmentos(palabra):
                        pos_segmento = busqueda_binaria(indice_segmentos, segmento)
                        if pos_segmento != -1:
                            indice_segmentos[pos_segmento][1].discard(id_eliminar)
                            if not indice_segmentos[pos_segmento][1]:
                                indice_segmentos.pop(pos_segmento)
                tweets.pop(id_eliminar)

            return
        except ValueError:
            print(INPUT_INVALIDO)

def main():
    """ Funcion principal, que renderiza el programa. """
    opcion = 0
    tweets = {}
    indice_palabras = []
    indice_segmentos = []
    siguiente_id = 0

    while opcion != 4:
        mostrar_menu()
        try:
            opcion = int(input("ingrese una opcion: "))
        except ValueError:
            print(INPUT_INVALIDO)
            continue

        if opcion == 1:
            siguiente_id = crear_tweet(tweets, indice_palabras, indice_segmentos, siguiente_id)
        elif opcion == 2:
            buscar_tweet(tweets, indice_palabras, indice_segmentos)
        elif opcion == 3:
            eliminar_tweet(tweets, indice_palabras, indice_segmentos)
        elif opcion == 4:
            print(FIN)
        else:
            print(INPUT_INVALIDO)

# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final, asegurando que se ejecute el programa
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.


if __name__ == "__main__":
    main()
