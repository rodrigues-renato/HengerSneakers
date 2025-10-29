document.addEventListener("DOMContentLoaded", function () {
  document
    .getElementById("btn-add-address")
    .addEventListener("click", function (event) {
      event.preventDefault(); // Impede o recarregamento da página

      let form = event.target.closest("form");
      if (!form) {
        console.error("Formulário não encontrado!");
        return;
      }
      let formData = new FormData(form);
      
      // Captura a URL no atributo data-url do botão
      const url = document.getElementById("btn-add-address").getAttribute("data-url");
      console.log(url);
      fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            alert(data.error);
          } else {
            // Cria um novo elemento <option> para a picklist de endereços
            let novoEndereco = document.createElement("option");
            novoEndereco.value = `${data.rua}, ${data.numero}, ${data.bairro}`;
            novoEndereco.textContent = `${data.rua}, ${data.numero}, ${data.bairro}`;

            // Adiciona o Option ao Select
            document.getElementById("endereco").appendChild(novoEndereco);

            // Deixa o novo endereço selecionado
            document.getElementById("endereco").value = novoEndereco.value;

            // Fecha o modal
            let modal = bootstrap.Modal.getInstance(
              document.getElementById("adicionar_endereco")
            );
            modal.hide();

            // Reseta o form do modal
            form.reset();
          }
        })
        .catch((error) => console.error("Erro ao salvar endereço:", error));
    });
});
