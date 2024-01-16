from django.template.loader import render_to_string


class UsuarioReport:
    def __init__(self, usuario, pwd=None):
        self.usuario = usuario
        self.senha = pwd

    def get_dict(self):
        return dict(email=self.usuario.email, senha=self.senha)

    def get_html(self, template):
        context = dict(data=self.get_dict())
        return render_to_string(template, context)
