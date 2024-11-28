Feature: Compras en una tienda en línea

  Scenario Outline: Agregar productos al carrito
    Given que el usuario está en la página web de la aplicación Ambiente: "<ambiente>" Link: "<link>"
    When el usuario hace clic en "Iniciar Sesión" e ingresa email: "<email>" y password: "<password>"
    When el usuario agrega productos al carrito
    Then Cierra el navegador.
    Examples:
      | email                           | password      | ambiente | link                               |
      | automationtestingqa@yopmail.com | Test123456789 | QA       | https://ecommerce.tealiumdemo.com/ |
#      | test123456@yopmail.com | Test123456789 | AR           | store_2 |
#      | test123456@yopmail.com | Test123456789 | AR           | store_3 |
