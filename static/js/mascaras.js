(function ($) {
  "use strict";

  function aplicarMascaraTelefone(field) {
    var mascaraTelefone = function (valor) {
      return valor.replace(/\D/g, "").length === 11
        ? "(00) 00000-0000"
        : "(00) 0000-00009";
    };

    field.mask(mascaraTelefone, {
      onKeyPress: function (valor, evento, elemento, opcoes) {
        elemento.mask(mascaraTelefone(valor), opcoes);
      },
    });
  }

  $(function () {
    $("input[name]").each(function () {
      var field = $(this);
      var identificador = (field.attr("name") + " " + (field.attr("id") || ""))
        .toLowerCase();

      if (identificador.indexOf("cpf") !== -1) {
        field.mask("000.000.000-00");
      } else if (identificador.indexOf("cnpj") !== -1) {
        field.mask("00.000.000/0000-00");
      } else if (
        identificador.indexOf("cep") !== -1 ||
        identificador.indexOf("postal") !== -1
      ) {
        field.mask("00000-000");
      } else if (
        identificador.indexOf("telefone") !== -1 ||
        identificador.indexOf("celular") !== -1 ||
        identificador.indexOf("whatsapp") !== -1 ||
        identificador.indexOf("phone") !== -1
      ) {
        aplicarMascaraTelefone(field);
      }
    });
  });
})(jQuery);
