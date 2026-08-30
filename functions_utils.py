from pathlib import Path

import pandas as pd


# =========================
# CAMINHO DO CSV
# =========================

BASE_DIR = Path(__file__).absolute().parent

FILE_PATH = (
    BASE_DIR /
    "Preços semestrais - AUTOMOTIVOS_2026.01.csv"
)


# =========================
# COMBUSTÍVEIS
# =========================

COMBUSTIVEIS = [
    "GASOLINA",
    "DIESEL",
    "DIESEL S10",
    "GASOLINA ADITIVADA",
    "ETANOL",
    "GNV"
]


# =========================
# CARREGAR DADOS
# =========================

def carregar_dados():

    df = pd.read_csv(
        FILE_PATH,
        sep=";",
        encoding="UTF-8",
        low_memory=True
    )

    return df


# =========================
# RETORNAR ESTADOS
# =========================

def retornar_estados():

    estados = (
        carregar_dados()["Estado - Sigla"]
        .dropna()
        .unique()
    )

    return sorted(estados)


# =========================
# FILTRAR DADOS
# =========================

def filtrar_dados(
    estado_escolhido="SP",
    combustiveis_selecionados=None
):

    df = carregar_dados()

    # Converte a coluna de data
    df_data = pd.to_datetime(
        df["Data da Coleta"],
        dayfirst=True
    )

    # =========================
    # FILTRO DE DATA
    # =========================

    filtro_data = (
        (df_data.dt.day == 30)
        &
        (df_data.dt.month == 6)
        &
        (df_data.dt.year == 2026)
    )

    # Se nenhum combustível foi selecionado,
    # utiliza todos
    if not combustiveis_selecionados:

        combustiveis_selecionados = COMBUSTIVEIS

    # =========================
    # FILTROS
    # =========================

    filtro = (
        (df["Estado - Sigla"] == estado_escolhido)
        &
        filtro_data
        &
        (
            df["Produto"].isin(
                combustiveis_selecionados
            )
        )
    )

    # Cria DataFrame filtrado
    df_filtrado = df[filtro].copy()

    # =========================
    # CONVERTER PREÇO
    # =========================

    df_filtrado["Valor de Venda"] = (
        df_filtrado["Valor de Venda"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    return df_filtrado


# =========================
# RESULTADO TOTAL
# =========================

def resultado_total(
    estado_escolhido,
    combustiveis_selecionados
):

    # Recebe os dados filtrados
    df = filtrar_dados(
        estado_escolhido,
        combustiveis_selecionados
    )

    # Agrupa os dados
    df_resultado_total = (
        df
        .groupby(
            [
                "Estado - Sigla",
                "Municipio",
                "Produto"
            ],
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

    return df_resultado_total