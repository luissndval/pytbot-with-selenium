from behave import *

from features.page.init_browser import Browser
from features.page.login_code import Login


@given(u'que el usuario está en la página web de la aplicación Ambiente: "{ambiente}" Link: "{link}"')
def step_impl(context, ambiente, link):
    try:
        Browser.start_browser(context, ambiente, link)
    except:
        print(f"Error al dirigirse a la pagina web")
        context.driver.close()
        assert False,  "Error al dirigirse a la pagina web"


@when(u'el usuario hace clic en "Iniciar Sesión" e ingresa email: "{email}" y password: "{password}"')
def step_impl(context, email, password):
    try:
        Login.loginuser(context, email, password)
    except:
        print(f"Error al inicar sesion")
        context.driver.close()
        assert False, "Error al inicar sesion"


@then(u'Cierra el navegador.')
def step_impl(context):
    try:
        context.driver.close()
    except:
        print(f"Error al cerrar navegador)")
        context.driver.close()
        assert False,"Error al cerrar navegador" # Lanza la excepción nuevamente para que Behave la registre

