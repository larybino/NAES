from django.urls import path
from .views import AboutView, IndexView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
    path("login/", LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
            extra_context = {
                'titulo': 'Autenticação de Usuário',
                'botao': 'Entrar'
            }
        ), name="login"),

    # a URL de logout não precisa de template
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "alterar-senha/",
        PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            success_url=reverse_lazy("alterar-senha-concluida"),
        ),
        name="alterar-senha",
    ),
    path(
        "alterar-senha/concluida/",
        PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"),
        name="alterar-senha-concluida",
    ),
    
]