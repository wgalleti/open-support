import factory


class AtendenteFactory(factory.django.DjangoModelFactory):
    nome = factory.Faker('first_name', locale='pt_BR')

    @factory.lazy_attribute
    def email(self):
        if self.nome is None:
            return None

        return f"{self.nome.lower()}@hifuzion.com.br"

    class Meta:
        model = 'core.Atendente'


class ClienteFactory(factory.django.DjangoModelFactory):
    codigo_cliente = factory.Faker('random_number', digits=3)
    nome = factory.Faker('company', locale='pt_BR')

    @factory.lazy_attribute
    def email(self):
        if self.nome is None:
            return None

        return f"contact@{self.nome.replace(',', '').replace('.', '').split(' ')[0].lower()}.com"

    contato = factory.Faker('first_name', locale='pt_BR')
    contato_telefone = factory.Faker('random_number', digits=14)

    class Meta:
        model = 'core.Cliente'
