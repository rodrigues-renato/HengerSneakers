import os
import sys
from datetime import datetime
from pathlib import Path
from random import uniform, sample, randint, choice

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_PRODUCTS = 15  # Number of unique products
VARIANTS_PER_PRODUCT = 3  # Average variants per product

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'henger.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    
    from menu.models import Produto, DetalheProduto, Marca, Cor

    # Clear existing data
    print("Limpando dados existentes...")
    DetalheProduto.objects.all().delete()
    Produto.objects.all().delete()
    Marca.objects.all().delete()
    Cor.objects.all().delete()
    
    # Create Marcas
    print("Criando marcas...")
    marcas_nomes = ["Nike", "Adidas", "Puma", "Reebok", "New Balance", "Vans", "Converse", "Asics"]
    marcas = []
    for nome in marcas_nomes:
        marca = Marca.objects.create(nome=nome)
        marcas.append(marca)
    print(f"✓ {len(marcas)} marcas criadas")
    
    # Create Cores
    print("Criando cores...")
    cores_nomes = [
        "Preto", "Branco", "Vermelho", "Azul", "Verde", "Amarelo", 
        "Cinza", "Rosa", "Roxo", "Laranja", "Bege", "Marrom", 
        "Azul Marinho", "Verde Militar", "Bordô"
    ]
    cores = []
    for nome in cores_nomes:
        cor = Cor.objects.create(nome=nome)
        cores.append(cor)
    print(f"✓ {len(cores)} cores criadas")
    
    # Product models and descriptions
    modelos = [
        ("Air Max 90", "Tênis clássico com design icônico e amortecimento Air Max visível. Perfeito para o dia a dia."),
        ("Air Force 1", "O lendário tênis de basquete que virou streetwear. Estilo atemporal e conforto incomparável."),
        ("Dunk Low", "Design retrô inspirado no basquete universitário. Visual clean e versátil."),
        ("Jordan 1", "O tênis que revolucionou o basquete e a cultura urbana. Estilo premium."),
        ("Superstar", "Tênis icônico com as três listras e biqueira de borracha. Clássico do streetwear."),
        ("Stan Smith", "Minimalista e elegante, o tênis de tênis mais famoso do mundo."),
        ("Ultraboost", "Tecnologia Boost para máximo conforto e retorno de energia. Performance e estilo."),
        ("Yeezy Boost 350", "Design futurista e minimalista. O tênis mais desejado da atualidade."),
        ("Suede Classic", "Clássico em camurça com design simples e elegante."),
        ("RS-X", "Design chunky e futurista com cores vibrantes. Estilo retrô moderno."),
        ("574", "O clássico New Balance com conforto e estilo para o dia a dia."),
        ("990", "Premium craftsmanship com tecnologia de amortecimento. Made in USA."),
        ("Old Skool", "O skate shoe clássico com a icônica lateral Wave. Streetwear essencial."),
        ("Authentic", "Design simples e atemporal. O original Vans desde 1966."),
        ("Chuck Taylor All Star", "O tênis de lona mais icônico de todos os tempos."),
        ("Gel-Lyte III", "Silhueta japonesa com tecnologia Gel. Design único e confortável."),
    ]
    
    tamanhos = ["36", "37", "38", "39", "40", "41", "42", "43", "44"]
    generos = ["M", "F", "U"]
    
    print(f"\nCriando {NUMBER_OF_PRODUCTS} produtos com variantes...")
    produtos_criados = 0
    variantes_criadas = 0
    
    for i in range(NUMBER_OF_PRODUCTS):
        # Select random model and brand
        modelo_nome, descricao = choice(modelos)
        marca = choice(marcas)
        
        # Create Product
        produto = Produto.objects.create(
            nome=modelo_nome,
            marca=marca,
            descricao=descricao
        )
        produtos_criados += 1
        
        # Create variants for this product
        num_variants = randint(2, 6)  # 2 to 6 variants per product
        
        for _ in range(num_variants):
            try:
                cor = choice(cores)
                tamanho = choice(tamanhos)
                genero = choice(generos)
                preco = round(uniform(199.90, 899.90), 2)
                estoque = randint(0, 30)
                
                # Generate SKU
                sku = f"{marca.nome[:3].upper()}{modelo_nome[:3].upper()}{tamanho}{cor.nome[:2].upper()}"
                
                # Create variant
                DetalheProduto.objects.create(
                    produto=produto,
                    cor=cor,
                    tamanho=tamanho,
                    genero=genero,
                    preco=preco,
                    estoque=estoque,
                    sku=sku
                )
                variantes_criadas += 1
                
            except Exception as e:
                # Skip if duplicate (unique_together constraint)
                continue
        
        if (i + 1) % 5 == 0:
            print(f"  {i + 1}/{NUMBER_OF_PRODUCTS} produtos criados...")
    
    print(f"\n{'='*50}")
    print(f"✓ Criação concluída com sucesso!")
    print(f"{'='*50}")
    print(f"Marcas criadas: {len(marcas)}")
    print(f"Cores criadas: {len(cores)}")
    print(f"Produtos criados: {produtos_criados}")
    print(f"Variantes criadas: {variantes_criadas}")
    print(f"Média de variantes por produto: {variantes_criadas/produtos_criados:.1f}")
    print(f"{'='*50}\n")

