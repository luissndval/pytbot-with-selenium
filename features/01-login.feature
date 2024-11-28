Feature: Automatización de acciones en la aplicación

  Scenario Outline: Iniciar Sesión
    Given que el usuario está en la página web de la aplicación Ambiente: "<ambiente>" Link: "<link>"
    When el usuario hace clic en "Iniciar Sesión" e ingresa email: "<email>" y password: "<password>"
    Then Cierra el navegador.


    Examples:
      | email                           | password      | ambiente | link                               |
      | automationtestingqa@yopmail.com | Test123456789 | QA       | https://ecommerce.tealiumdemo.com/ |
