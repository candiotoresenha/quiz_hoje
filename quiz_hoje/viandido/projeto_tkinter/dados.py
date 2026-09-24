import json
import os


PASTA_DADOS = "dados"

ARQUIVO_PERGUNTAS = os.path.join(
    PASTA_DADOS,
    "perguntas.json"
)

ARQUIVO_RESULTADOS = os.path.join(
    PASTA_DADOS,
    "resultados.json"
)


def carregar_perguntas():
    try:
        with open(
            ARQUIVO_PERGUNTAS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def carregar_resultados():
    try:
        with open(
            ARQUIVO_RESULTADOS,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        return []


def salvar_resultado(resultado):
    resultados = carregar_resultados()

    resultados.append(resultado)

    with open(
        ARQUIVO_RESULTADOS,
        "w",
        encoding="utf-8"
    ) as arquivo:
        json.dump(
            resultados,
            arquivo,
            ensure_ascii=False,
            indent=4
        )
