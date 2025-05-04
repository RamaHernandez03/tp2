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
    """ busca una clave en una lista de tuplas ordenadas usando la busqueda
    binaria. """
    izquierda = 0
    derecha = len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        actual = lista[medio][0]
        if actual == clave:
            return medio
        if actual < clave:
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


def mostrar_tweets_a_eliminar(tweets, ids):
    """ MUestra los resultados que concuerdan. """
    print(RESULTADOS_BUSQUEDA)
    for tweet_id in sorted(ids):
        print(f"{tweet_id}. {tweets[tweet_id]}")


def eliminar_de_indices(tweet_id, texto, indice_palabras, indice_segmentos):
    """ elimina las referencias a un tweet especifico dentro indice_p e
    indice_s. """
    palabras = normalizar(texto)
    for palabra in palabras:
        pos_palabra = busqueda_binaria(indice_palabras, palabra)
        if pos_palabra != -1:
            indice_palabras[pos_palabra][1].discard(tweet_id)
            if not indice_palabras[pos_palabra][1]:
                indice_palabras.pop(pos_palabra)
        for segmento in tokenizar_segmentos(palabra):
            pos_segmento = busqueda_binaria(indice_segmentos, segmento)
            if pos_segmento != -1:
                indice_segmentos[pos_segmento][1].discard(tweet_id)
                if not indice_segmentos[pos_segmento][1]:
                    indice_segmentos.pop(pos_segmento)


def obtener_ids_por_token(token, indice_palabras, indice_segmentos):
    """ te retorna los conjuntos de IDs que estan contenidos por el token. """
    ids = set()
    pos_palabra = busqueda_binaria(indice_palabras, token)
    if pos_palabra != -1:
        ids.update(indice_palabras[pos_palabra][1])
    pos_segmento = busqueda_binaria(indice_segmentos, token)
    if pos_segmento != -1:
        ids.update(indice_segmentos[pos_segmento][1])
    return ids


def parsear_rangos(entrada):
    """ Te parsea la cantidad de "tweets" id, segun el id o rango dado. """
    seleccionados = set()
    for parte in entrada.split(","):
        if "-" in parte:
            inicio, fin = map(int, parte.split("-"))
            if inicio > fin:
                raise ValueError
            seleccionados.update(range(inicio, fin + 1))
        else:
            seleccionados.add(int(parte))
    return seleccionados


def eliminar_tweets_por_ids(ids, tweets, indice_palabras, indice_segmentos):
    """ recibe los id y elimina los respectivos "tweets" actualizando
    sus indices para reflejar cambios."""
    print(TWEETS_ELIMINADOS)
    for tweet_id in sorted(ids):
        print(f"{tweet_id}. {tweets[tweet_id]}")
        eliminar_de_indices(tweet_id,
                            tweets[tweet_id],
                            indice_palabras,
                            indice_segmentos)
        tweets.pop(tweet_id)

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
        id_encontrados = obtener_ids_por_token(token,
                                               indice_palabras,
                                               indice_segmentos)
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
    """ Elimina uno o varios "tweets" y actualiza los indice. """
    while True:
        print("Ingrese el tweet a eliminar:")
        tweet = input(" ").strip()
        tokens = normalizar(tweet)
        if not tokens:
            print(NO_ENCONTRADOS)
            continue
        ids_encontrados = obtener_ids_por_token(tokens[0],
                                                indice_palabras,
                                                indice_segmentos)
        if not ids_encontrados:
            print(NO_ENCONTRADOS)
            continue

        mostrar_tweets_a_eliminar(tweets, ids_encontrados)
        print("Ingrese los numeros de tweets a eliminar (ej: 0,2-4):")
        indices = input(" ").replace(" ", "")
        if not indices:
            print(INPUT_INVALIDO)
            continue
        try:
            seleccionados = parsear_rangos(indices)
            if not seleccionados.issubset(ids_encontrados):
                print(NUMERO_INVALIDO)
                continue
            eliminar_tweets_por_ids(seleccionados,
                                    tweets,
                                    indice_palabras,
                                    indice_segmentos)
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
            siguiente_id = crear_tweet(tweets,
                                       indice_palabras,
                                       indice_segmentos,
                                       siguiente_id)
        if opcion == 2:
            buscar_tweet(tweets, indice_palabras, indice_segmentos)
        if opcion == 3:
            eliminar_tweet(tweets, indice_palabras, indice_segmentos)
        if opcion == 4:
            print(FIN)
        else:
            print(INPUT_INVALIDO)


# -----------------------------------------------------------------------------

# Esta parte del código se ejecuta al final, asegurando que se ejecute el ->
# -> programa.
# mediante la terminal correctamente y permitiendo que se puedan realizar
# los tests de forma automática y aislada.


if __name__ == "__main__":
    main()
