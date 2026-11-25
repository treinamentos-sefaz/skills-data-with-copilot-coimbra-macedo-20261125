"""Módulo 2 — Manipulação de DataFrames com pandas.

Complete cada função com o apoio do GitHub Copilot. Prefira operações
vetorizadas e evite alterar o DataFrame original (use ``.copy()``).

Valide com:  ``python lab/check.py --module pandas``
"""
from __future__ import annotations

import pandas as pd


def load_wines(path: str) -> pd.DataFrame:
    """Carrega os dados de vinhos de um arquivo CSV.

    Args:
        path: Caminho do arquivo CSV.

    Returns:
        DataFrame com os dados carregados.

    Exibe as informações estruturais do DataFrame carregado.
    """
    df = pd.read_csv(path)
    df.info()
    return df


def clean_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Converte ``rating`` para número e remove avaliações nulas.

    Args:
        df: DataFrame com a coluna ``rating``.

    Returns:
        Cópia do DataFrame com ``rating`` numérico e sem valores nulos.

    Exibe as informações estruturais do DataFrame de entrada e do resultado.
    """
    df.info()
    df_clean = df.copy()
    df_clean["rating"] = pd.to_numeric(df_clean["rating"], errors="coerce")
    df_clean = df_clean.dropna(subset=["rating"])

    df_clean.info()
    return df_clean

def top_varieties_by_avg_rating(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Retorna as variedades com maiores médias de avaliação.

    Args:
        df: DataFrame com as colunas ``variety`` e ``rating``.
        n: Número máximo de variedades no resultado.

    Returns:
        DataFrame agregado com ``variety`` e ``avg_rating``, em ordem
        decrescente de média.

    Exibe as informações estruturais do DataFrame de entrada e do resultado.
    """
    df.info()
    df_copy = df.copy()
    result = (
        df_copy.groupby("variety", as_index=False)["rating"]
        .mean()
        .rename(columns={"rating": "avg_rating"})
        .sort_values("avg_rating", ascending=False)
        .head(n)
        .reset_index(drop=True)
    )
    result.info()
    return result


def add_rating_category(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona uma categoria para cada avaliação.

    Args:
        df: DataFrame com a coluna ``rating``.

    Returns:
        Cópia do DataFrame com a coluna ``rating_category`` nas faixas
        ``Baixa``, ``Média`` e ``Alta``.

    Exibe as informações estruturais do DataFrame de entrada e do resultado.
    """
    df.info()
    df_copy = df.copy()
    df_copy["rating_category"] = pd.cut(
        df_copy["rating"],
        bins=[-float("inf"), 85, 90, float("inf")],
        labels=["Baixa", "Média", "Alta"],
        right=False,
    )
    df_copy.loc[df_copy["rating"] == 90, "rating_category"] = "Média"
    df_copy.loc[df_copy["rating"] > 90, "rating_category"] = "Alta"
    df_copy.info()
    return df_copy


def enrich_with_country(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona uma coluna de país extraída da região.

    Args:
        df: DataFrame com a coluna textual ``region``.

    Returns:
        Cópia do DataFrame com a coluna ``country`` extraída de ``region``.

    Exibe as informações estruturais do DataFrame de entrada e do resultado.
    """
    df.info()
    df_copy = df.copy()
    df_copy["country"] = df_copy["region"].str.rsplit(",", n=1).str[-1].str.strip()
    df_copy.info()
    return df_copy
