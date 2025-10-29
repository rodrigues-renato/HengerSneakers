const URL_FINALIZAR_PEDIDO = "/pedido/finalizar_pedido/";

function createMenuItem(productId, data) {
  return `
    <div id="menu-item-${productId}-carrinho" class="menu-item d-flex justify-content-between align-items-center py-2 border-bottom">
        <div class="menu-details d-flex align-items-center flex-grow-1">
            <div class="quantity-controls d-flex align-items-center me-3">
                <a href="/remover_do_carrinho/${productId}/" class="btn btn-danger btn-sm btn-ajax">
                    <i class="fas fa-minus"></i>
                </a>
                <span id="quantidade-${productId}-carrinho" class="quantity mx-2">${
    data.quantidade
  }</span>
                <a href="/adicionar_ao_carrinho/${productId}/" class="btn btn-success btn-sm btn-ajax">
                    <i class="fas fa-plus"></i>
                </a>
            </div>
            <span class="product-name flex-grow-1">${data.produto_nome}</span>
            <span id="total-${productId}-carrinho" class="product-total me-3">R$ ${parseFloat(
    data.total
  ).toFixed(2)}</span>
        </div>
        <div class="remove-action">
            <a href="/excluir_do_carrinho/${productId}/" class="btn btn-outline-danger btn-ajax">
                <i class="fas fa-trash"></i>
            </a>
        </div>
    </div>
  `;
}

document.addEventListener("DOMContentLoaded", function () {
  function updateCartUI(data) {
    const productId = data.produto_id;
    const quantityCartElement = document.querySelector(
      `#quantidade-${productId}-carrinho`
    );
    const quantityOrderElement = document.querySelector(
      `#quantidade-${productId}-pedido`
    );
    const totalCartElement = document.querySelector(
      `#total-${productId}-carrinho`
    );
    const totalOrderElement = document.querySelector(
      `#total-${productId}-pedido`
    );
    let menuCartItem = document.querySelector(
      `#menu-item-${productId}-carrinho`
    );
    const menuOrderItem = document.querySelector(
      `#menu-item-${productId}-pedido`
    );
    let totalPrice = document.querySelector(`#valor-total`);
    let totalOrderPrice = document.querySelector(`#valor-total-pedido`);
    let finalizeOrder = document.querySelector(`#finalizar-pedido`);
    let cartItens = document.querySelector(`#item-carrinho`);
    let cartOrderItens = document.querySelector(`#item-carrinho-pedido`);
    let finalizeOrderTotal = document.querySelector(`#finalizar-pedido-total`);
    const cartAmount = document.querySelector(`#qtd-item-carrinho`);
    cartAmount.textContent = data.qtd_item_carrinho;

    if (!cartItens) {
      // Se a div que exibe os itens na offcanvas não existir, no caso do carrinho
      // estiver vazio esse bloco a cria, e cria a div que exibe o valor total e o link
      // para finalizar o pedido
      cartItens = document.createElement("div");
      cartItens.id = "item-carrinho";
      cartItens.className = "menu";
      document.querySelector(".offcanvas-body").appendChild(cartItens);
      cartItens.innerHTML = createMenuItem(productId, data);
      menuCartItem = document.querySelector(`#menu-item-${productId}-carrinho`);
      // Apaga a div da parte inferior, que neste momento está dizendo que o Carrinho está vazio!
      // e a cria novamente, pronta para exibir o valor total e o link para finalizar o pedido
      finalizeOrder.remove();
      finalizeOrder = document.createElement("div");
      finalizeOrder.id = "finalizar-pedido";
      finalizeOrder.className =
        "d-flex justify-content-between align-items-center mt-4 p-3 border rounded bg-light";
      document.querySelector(".offcanvas-body").appendChild(finalizeOrder);
    }

    if (data.quantidade == 1 && !menuCartItem) {
      // Cria no carrinho a div dos itens que foram adicionados pela primeira vez
      cartItens.innerHTML += createMenuItem(productId, data);
    }

    if (cartItens && !totalPrice) {
      // Se um item foi adicionado no carrinho, após ele estar vazio
      // a div inferior é criada aqui
      finalizeOrder.innerHTML = `
          <span id="valor-total" class="fs-4 fw-bold">Total: R$ ${parseFloat(
            data.total_price
          ).toFixed(2)}</span>
          <a href="/pedido/finalizar_pedido/" class="btn btn-lg btn-danger ms-3">
            Finalizar pedido
            <i class="fas fa-shopping-cart ms-2"></i>
          </a>
      `;
      totalPrice = document.querySelector(`#valor-total`);
    }

    if (quantityCartElement) {
      if (data.quantidade > 0) {
        quantityCartElement.textContent = data.quantidade;
        if (quantityOrderElement) {
          quantityOrderElement.textContent = data.quantidade;
        }
        totalCartElement.textContent = `R$ ${parseFloat(data.total).toFixed(
          2
        )}`;
        if (totalOrderElement) {
          totalOrderElement.textContent = `R$ ${parseFloat(data.total).toFixed(
            2
          )}`;
        }
      } else {
        menuCartItem.remove();
        if (menuOrderItem) {
          menuOrderItem.remove();
        }
      }
    }

    if (!data.total_price || data.qtd_item_carrinho === 0) {
      cartItens.remove();
      finalizeOrder.innerHTML = `<span class="fs-4 fw-bold">O carrinho está vazio!</span>`;
      finalizeOrder.className =
        "d-flex justify-content-between align-items-center mt-4 p-3 border rounded bg-light";
      if (window.location.pathname === URL_FINALIZAR_PEDIDO) {
        finalizeOrderTotal.remove();
        setTimeout(() => {
          window.location.href = "/menu/";
        }, 0); // Redireciona após 0 ms
      }
    } else {
      totalPrice.textContent = `Total: R$ ${parseFloat(
        data.total_price
      ).toLocaleString("pt-BR", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}`;

      if (window.location.pathname === URL_FINALIZAR_PEDIDO) {
        totalOrderPrice.textContent = `Total: R$ ${parseFloat(
          data.total_price
        ).toLocaleString("pt-BR", {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        })}`;
      }
      finalizeOrder.remove();
      finalizeOrder = document.createElement("div");
      finalizeOrder.id = "finalizar-pedido";
      finalizeOrder.className =
        "d-flex justify-content-between align-items-center mt-4 p-3 border rounded bg-light";
      document.querySelector(".offcanvas-body").appendChild(finalizeOrder);

      finalizeOrder.innerHTML = `
      <span id="valor-total" class="fs-4 fw-bold">Total: R$ ${parseFloat(
        data.total_price
      ).toFixed(2)}</span>
      <a href="/pedido/finalizar_pedido/" class="btn btn-lg btn-danger ms-3">
        Finalizar pedido
        <i class="fas fa-shopping-cart ms-2"></i>
      </a>
  `;
    }
  }
  function handleAjaxButtonClick(event) {
    const target = event.target.closest(".btn-ajax");
    if (target) {
      event.preventDefault();
      const url = target.getAttribute("href");
      sendAjaxRequest(url, "GET");
    }
  }
  document.addEventListener("click", handleAjaxButtonClick);

  function sendAjaxRequest(url, method) {
    fetch(url, {
      method: method,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": getCSRFToken(),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          updateCartUI(data);
        } else {
          alert(data.message);
        }
      })
      .catch((error) => console.error("Erro:", error));
  }

  function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
  }
});
