from behave import *
from features.page.add_product_page import addProduct


@when(u'el usuario agrega productos al carrito')
def step_impl(context):
    try:
        addProduct.addProduct(context)
    except:
        print(f"Error al dirigirse a la pagina web")
        context.driver.close()
        assert False,"Error al dirigirse a la pagina web"  # Lanza la excepción nuevamente para que Behave la registre



