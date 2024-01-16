from django.contrib.auth import get_user_model

from core.models import User, Customer, Attendant


class UsuarioService:
    def __init__(self):
        self.data = None
        self.origin = None
        self.created = False
        self.user = None
        self.new_password = None
        self.nivel = User.LEVEL1

    def add(self):
        self.user, self.created = get_user_model().objects.update_or_create(**self.data)

        if self.created:
            self.new_password = get_user_model().objects.make_random_password()
            self.user.set_password(self.new_password)
            self.user.save()

    def _normalize(self):
        def _extract_dict(data):
            id = data.get('id', None)
            if id is None:
                return dict(
                    email=data.get('email'),
                    defaults=data
                )
            return dict(
                id=id,
                defaults=data
            )

        def _extract_model(data):
            pk = data.usuario_acesso_id if data.usuario_acesso is not None else None
            email = data.email
            is_active = True
            nivel = data.level

            separate = data.name.split(' ')

            if len(separate) == 1:
                first_name = separate[0].title()
                last_name = ''
                username = separate[0].lower()
            else:
                first_name = separate[0].title()
                last_name = separate[-1].title()
                username = f'{first_name.lower()}.{last_name.lower()}'

            if pk is not None:
                return dict(
                    id=pk,
                    defaults=dict(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        is_active=is_active,
                        nivel=nivel
                    )
                )

            return dict(
                email=email,
                defaults=dict(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    is_active=is_active,
                    nivel=nivel
                )
            )

        if isinstance(self.origin, dict):
            self.data = _extract_dict(self.origin.copy())
            return True

        if type(self.origin) in [Customer, Attendant]:
            self.data = _extract_model(self.origin)
            self.data['is_attendant'] = type(self.origin) == Attendant
            self.data['is_customer'] = type(self.origin) == Customer

            return True

        raise Exception('Unable to normalize data to user')

    def link_user(self, data):
        self.origin = data
        self._normalize()
        return self.add()
