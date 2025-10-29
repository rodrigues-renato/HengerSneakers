import os
import sys
from pathlib import Path

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'henger.settings'
settings.USE_TZ = False

django.setup()

if __name__ == '__main__':
    import faker

    from clientes.models import CustomUser
    from pedidos.models import Carrinho

    fake = faker.Faker('pt_BR')

    usuarios = []
    carrinho = []
    for _ in range(NUMBER_OF_OBJECTS):
        profile = fake.profile()
        email = profile['mail']
        first_name, last_name = profile['name'].split(' ', 1)
        telefone = fake.phone_number()
        cpf = fake.cpf()

        usuarios.append(
            CustomUser(
                username=email,
                first_name=first_name,
                last_name=last_name,
                telefone=telefone,
                email=email,
                cpf=cpf,
            )
        )
        carrinho.append(Carrinho(cliente=usuarios[-1]))

    if len(usuarios) > 0:
        CustomUser.objects.bulk_create(usuarios)
        Carrinho.objects.bulk_create(carrinho)
