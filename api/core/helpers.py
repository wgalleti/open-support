def choice_para_lista(choice):
    """
    Precessa uma tupla do tipo choice e devolve uma lista de dicionario como se fosse uma tabela do banco
    :param choice:
    :return:
    """
    return [dict(id=s[0], descricao=s[1].title()) for s in choice]
