import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# =========================
# CAMINHO DO ARQUIVO
# =========================

BASE_DIR = Path(__file__).absolute().parent

FILE_PATH = BASE_DIR / "Preços semestrais - AUTOMOTIVOS_2026.01.csv"


# =========================
# LENDO O CSV
# =========================

df_precos_1_semestre = pd.read_csv(
    FILE_PATH,
    sep=";",
    encoding="UTF-8",
    low_memory=True
)


# =========================
# PEGANDO OS ESTADOS
# =========================

df_pegando_estados = sorted(
    df_precos_1_semestre["Estado - Sigla"]
    .dropna()
    .unique()
)

print("\nEstados Disponíveis:")

# Mostra 5 estados por linha
for i in range(0, len(df_pegando_estados), 5):
    print(", ".join(df_pegando_estados[i:i + 5]))


# =========================
# INPUT DO ESTADO
# =========================

estado_escolhido = input(
    "\nEscolha um estado: "
).strip().upper()


# Verifica se o estado existe
if estado_escolhido not in df_pegando_estados:

    print("\nEstado inválido.")

else:

    # =========================
    # FILTRO DO ESTADO
    # =========================

    df_estado = (
        df_precos_1_semestre["Estado - Sigla"]
        == estado_escolhido
    )


    # =========================
    # FILTRO DA GASOLINA
    # =========================

    lista_de_combustiveis = ['GASOLINA', 'DIESEL', 'DIESEL S10', 'GASOLINA ADITIVADA', 'ETANOL', 'GNV']
    # =========================
    # FILTRO DA etanol
    # =========================
    df_combustiveis = (
        df_precos_1_semestre["Produto"].isin(lista_de_combustiveis)
    )
    # =========================
    # TRANSFORMANDO A DATA
    # =========================

    df_data = pd.to_datetime(
        df_precos_1_semestre["Data da Coleta"],
        dayfirst=True
    )


    # =========================
    # FILTRO DA DATA
    # 30/06/2026
    # =========================

    df_dia30_mes6_ano2026 = (

        (df_data.dt.day == 30)
        &
        (df_data.dt.month == 6)
        &
        (df_data.dt.year == 2026)

    )


    # =========================
    # JUNTANDO TODOS OS FILTROS
    # =========================

    filtro = (
        df_estado
        &
        df_combustiveis
        &
        df_dia30_mes6_ano2026

    )


    # =========================
    # APLICANDO O FILTRO
    # =========================

    df_filtrado = df_precos_1_semestre[
        filtro
    ].copy()


    # =========================
    # VERIFICANDO SE EXISTEM DADOS
    # =========================

    if df_filtrado.empty:

        print(
            "\nNenhum dado encontrado para:"
        )

        print(f"Estado: {estado_escolhido}")
        print("Produto: GASOLINA")
        print("Data: 30/06/2026")


    else:

        # =========================
        # TRANSFORMANDO O PREÇO
        # =========================

        df_filtrado["Valor de Venda"] = (
            df_filtrado["Valor de Venda"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )


        # =========================
        # GROUPBY
        # =========================

        df_resultado_total = (

            df_filtrado
            .groupby(
                ["Estado - Sigla", "Municipio", "Produto"],
                as_index=False
            )
            .agg(

                media_preco=(
                    "Valor de Venda",
                    "mean"
                ),

                maior_preco=(
                    "Valor de Venda",
                    "max"
                ),

                menor_preco=(
                    "Valor de Venda",
                    "min"
                )

            )

        )


        # =========================
        # MAIOR PREÇO
        # =========================

        df_maiores_precos = (

            df_resultado_total
            .sort_values(
                by="maior_preco",
                ascending=False
            )
            .reset_index(drop=True)

        )


        # =========================
        # MAIOR MÉDIA
        # =========================

        df_media_precos = (

            df_resultado_total
            .sort_values(
                by="media_preco",
                ascending=False
            ).reset_index(drop=True)
        )

        df_media_precos["media_preco"] = (df_media_precos["media_preco"].map("R${:.2f}".format))


        # =========================
        # MENOR PREÇO
        # =========================

        df_menores_precos = (

            df_resultado_total
            .sort_values(
                by="menor_preco",
                ascending=True
            )
            .reset_index(drop=True)

        )


        # =========================
        # PEGANDO O PRIMEIRO DE CADA COMBUSTÍVEL
        # =========================

        df_primeiro_maiores_preco = (
            df_resultado_total.sort_values(by="maior_preco", ascending=False).groupby("Produto", as_index=False).head(1))

        
        df_primeiro_media_preco = (
            df_resultado_total.sort_values(by="media_preco", ascending=False).groupby("Produto", as_index=False).head(1))

        
        df_primeiro_menores_preco = (
            df_resultado_total.sort_values(by="menor_preco", ascending=True).groupby("Produto", as_index=False).head(1))



        # =========================
        # EXIBINDO RESULTADOS
        # =========================

        print("\n--- MAIOR PREÇO ---")

        df_primeiro_maiores_preco["maior_preco"] = df_primeiro_maiores_preco["maior_preco"].map("R${:.2f}".format)

        
        print(
            df_primeiro_maiores_preco[
                [
                    "Estado - Sigla",
                    "Municipio",
                    "Produto",
                    "maior_preco"
                ]
            ]
        )


        print("\n--- MAIOR MÉDIA DE PREÇO ---")

        # formatando o valo de media preco
        df_primeiro_media_preco["media_preco"] = df_primeiro_media_preco["media_preco"].map("R${:.2f}".format)

        print(
            df_primeiro_media_preco[
                [
                    "Estado - Sigla",
                    "Municipio",
                    "Produto",
                    "media_preco"
                ]
            ]
        )

        df_primeiro_media_precos = df_primeiro_media_preco.reset_index(drop=True)
        
        print(df_media_precos)

        print("\n--- MENOR PREÇO ---")

        df_primeiro_menores_preco["menor_preco"] = df_primeiro_menores_preco["menor_preco"].map("R${:.2f}".format)

        df_primeiro_menores_preco[
                [
                    "Estado - Sigla",
                    "Municipio",
                    "Produto",
                    "menor_preco"
                ]
            ]

        df_menores_precos = df_menores_precos.reset_index(drop=True)

        print(df_menores_precos)
