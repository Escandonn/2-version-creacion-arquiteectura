def seleccionar_perfiles(datos):

    activos = {}

    print("\n=========== NAVEGADORES ===========")

    for navegador, perfiles in datos.items():

        print(f"\n{navegador.upper()}")
        print(f"Cantidad perfiles: {len(perfiles)}")

        for i, perfil in enumerate(perfiles):

            print(f"{i} -> {perfil}")

        seleccion = input(
            "\nSelecciona perfiles separados por coma: "
        )

        indices = seleccion.split(",")

        activos[navegador] = []

        for indice in indices:

            indice = indice.strip()

            if indice.isdigit():

                indice = int(indice)

                if indice < len(perfiles):

                    activos[navegador].append(
                        perfiles[indice]
                    )

    return activos