def calcula_valor_total_carrinho(carrinho):
    """
    Calcula o valor total de um carrinho.
    
    Aceita tanto um QuerySet de ItemCarrinho quanto um ID de Carrinho.
    Compatível com a estrutura normalizada (DetalheProduto).
    
    Exemplos:
        # Passando QuerySet de itens
        item_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho_obj)
        total = calcula_valor_total_carrinho(item_carrinho)
        
        # Passando ID do carrinho
        total = calcula_valor_total_carrinho(carrinho_id)
    """
    from pedidos.models import ItemCarrinho, Carrinho
    
    subtotal = 0
    
    # Se receber um ID (int), busca os itens do carrinho
    if isinstance(carrinho, int):
        try:
            carrinho_obj = Carrinho.objects.get(id=carrinho)
            itens = ItemCarrinho.objects.filter(carrinho=carrinho_obj)
        except Carrinho.DoesNotExist:
            return 0
    else:
        # Se receber um QuerySet ou lista de ItemCarrinho
        itens = carrinho
    
    # Calcula o subtotal usando o método get_total() de cada item
    # que agora usa detalhe_produto.preco
    if itens:
        for item in itens:
            subtotal += item.get_total()
    
    return subtotal


import re

# Fonte: https://github.com/luizomf/django-simple-ecommerce/blob/master/utils/validacpf.py
def valida_cpf(cpf):
    cpf = str(cpf)
    cpf = re.sub(r'[^0-9]', '', cpf)

    if not cpf or len(cpf) != 11:
        return False

    novo_cpf = cpf[:-2]  # Elimina os dois últimos digitos do CPF
    reverso = 10  # Contador reverso
    total = 0

    # Loop do CPF
    for index in range(19):
        if index > 8:  # Primeiro índice vai de 0 a 9,
            index -= 9  # São os 9 primeiros digitos do CPF

        total += int(novo_cpf[index]) * reverso  # Valor total da multiplicação

        reverso -= 1  # Decrementa o contador reverso
        if reverso < 2:
            reverso = 11
            d = 11 - (total % 11)

            if d > 9:  # Se o digito for > que 9 o valor é 0
                d = 0
            total = 0  # Zera o total
            novo_cpf += str(d)  # Concatena o digito gerado no novo cpf

    # Evita sequencias. Ex.: 11111111111, 00000000000...
    sequencia = novo_cpf == str(novo_cpf[0]) * len(cpf)

    # Descobri que sequências avaliavam como verdadeiro, então também
    # adicionei essa checagem aqui
    if cpf == novo_cpf and not sequencia:
        return True
    else:
        return False
