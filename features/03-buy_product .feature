Feature: Compras en una tienda en línea

  Scenario Outline: Finalizar Compra
    Given que el usuario está en la página web de la aplicación Ambiente: "<ambiente>" Link: "<link>"
    When el usuario hace clic en "Iniciar Sesión" e ingresa email: "<email>" y password: "<password>"
    When el usuario agrega productos al carrito
    Then el usuario concreta la compra y obtiene el numero de orden.
    Examples:
      | email                           | password      | ambiente | link                               |
      | automationtestingqa@yopmail.com | Test123456789 | QA       | https://ecommerce.tealiumdemo.com/ |
#      | cristian.depicciotto.qa.ar@balloon-group.com | Test123456 | PE           | Ensure | MercadoPago |

