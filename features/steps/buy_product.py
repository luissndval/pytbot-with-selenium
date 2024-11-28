from behave import *

from features.page.payment_options import buy


@then(u'el usuario concreta la compra y obtiene el numero de orden.')
def step_impl(context):
    try:
        buy.Shipping(context)
        buy.Select_Shipping_Price(context)
        buy.Payment(context)
        buy.OrderReview(context)
    except:
        print(f"Error al dirigirse a la pagina web:")
        context.driver.close()
        assert False, "Error al dirigirse a la pagina web"  # Lanza la excepción nuevamente para que Behave la registre

