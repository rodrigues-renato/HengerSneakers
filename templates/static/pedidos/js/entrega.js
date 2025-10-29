document.addEventListener("DOMContentLoaded", function () {
  const radioEntrega = document.getElementById("entrega");
  const formEndereco = document.getElementById("form-endereco");

  if (radioEntrega && formEndereco) {
    radioEntrega.addEventListener("change", function () {
      formEndereco.style.display = this.checked ? "block" : "none";
    });

    document.getElementById("retirada").addEventListener("change", function () {
      formEndereco.style.display = "none";
    });
  }

  const formPagamento = document.getElementById("metodo_pagamento");
  const formCartao = document.getElementById("cartao");
  const formDinheiro = document.getElementById("dinheiro");

  formPagamento.addEventListener("change", function () {
    if (this.value === "debito" || this.value === "credito") {
      formCartao.style.display = "block";
    } else {
      formCartao.style.display = "none";
    }

    if (this.value === "dinheiro") {
      formDinheiro.style.display = "block";
    } else {
      formDinheiro.style.display = "none";
    }
  });
});
