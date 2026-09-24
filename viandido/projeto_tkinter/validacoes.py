def validar_nome(nome):
    nome = nome.strip()

    if nome == "":
        return False

    if len(nome) < 2:
        return False

    return True


def validar_resposta(resposta, quantidade_opcoes):
    try:
        resposta = int(resposta)

        return 1 <= resposta <= quantidade_opcoes

    except ValueError:
        return False
