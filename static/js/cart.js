const decreaseContainers = document.querySelectorAll('.item-minus-btn');
const increaseContainers = document.querySelectorAll('.item-add-btn');
const removeItemContainers = document.querySelectorAll('.remove-item-container');
const deleteCfText = document.querySelector('.delete-confirm-text');
const cancelRemoveBtn = document.getElementsByClassName('cancel-btn')[0];
const confirmRemoveBtn = document.getElementsByClassName('confirm-btn')[0];
const deleteCartBtn = document.querySelector('.clear-btn');
const popup = document.getElementsByClassName('delete-popup')[0];

let cartItems;

let currentDeleteMode = "item";
let selectedContainer;

let totalQuantity = 9;
let totalTemp = 3870000;
let totalVat = 0;
let totalDiscount = 0;

document.addEventListener("DOMContentLoaded", () => {
    cartItems = document.querySelectorAll(".cart-table-data");
    console.log(increaseContainers);
    setQuantityBtnOnClick();
    setRemoveBtnsOnClick();
    setDeleteCartBtnOnClick();

    // updateCartTotal();

    cancelRemoveBtn.addEventListener("click", () => {
        togglePopup();
    });

    confirmRemoveBtn.addEventListener("click", () => {
        if (currentDeleteMode == "item"){
            const selectedItem = selectedContainer.closest('.cart-table-data');
            selectedItem.remove();
            cartItems = document.querySelectorAll(".cart-table-data");
            updateCart();
        }
        else if (currentDeleteMode == "cart"){
            cartItems.forEach(item => item.remove());
            totalQuantity = 0;
            totalTemp = 0;
            totalVat = 0;
            totalDiscount = 0;
            cartItems = document.querySelectorAll(".cart-table-data");
            updateCart();
        }
        
        togglePopup();
    });
});

const setQuantityBtnOnClick = () => {
    increaseContainers.forEach((btnContainer) => {
        // console.log(btnContainer);
        const btn = btnContainer.firstElementChild;
        // console.log(btn);
        btn.addEventListener("click", () => {
            const quantityInputContainer = btnContainer.previousElementSibling;
            console.log(quantityInputContainer);
            const quantityInput = quantityInputContainer.firstElementChild;
            const currentValue = parseInt(quantityInput.getAttribute("value")) || 1;
            console.log("currentValue: ", currentValue);
            const increasedValue = currentValue + 1;
            console.log("increasedValue: ", increasedValue);
            quantityInput.setAttribute("value",increasedValue.toString());
            updateCart();
        });
        
    });

    decreaseContainers.forEach((btnContainer, index) => {
        const btn = btnContainer.firstElementChild;
        btn.addEventListener("click", () => {
            const quantityInputContainer = btnContainer.nextElementSibling;
            const quantityInput = quantityInputContainer.firstElementChild;
            const currentValue = parseInt(quantityInput.getAttribute("value")) || 1;
            console.log("currentValue: ", currentValue);
            const decreasedValue = currentValue - 1;
            console.log("decreasedValue: ", decreasedValue);
            quantityInput.setAttribute("value",decreasedValue.toString());
            updateCart();
        });
        
    });
};

const setRemoveBtnsOnClick = () => {
    removeItemContainers.forEach(container => {
        const btn = container.firstElementChild;
        btn.addEventListener("click", () => {
            currentDeleteMode = "item";
            selectedContainer = container;
            togglePopup();
        });
    });
};

const setDeleteCartBtnOnClick = () => {
    deleteCartBtn.addEventListener("click",() => {
        deleteCfText.textContent = "Bạn có chắc chắn muốn xóa toàn bộ giỏ hàng này không?";
        currentDeleteMode = "cart";
        togglePopup();
    });
};

const togglePopup = () => {
    popup.style.display = (popup.style.display === 'flex') ? 'none' : 'flex';   
};

const updateCart = () => {
    totalQuantity = 0;
    totalTemp = 0;
    cartItems.forEach(row => {
        const result = updateCartItemSubtotal(row);
        totalQuantity += result.itemQuantity;
        totalTemp += result.itemSubtotal
    });
    updateCartTotal();
    saveCart();
};

const updateCartItemSubtotal = (itemRow) => {
    const itemPriceText = itemRow.querySelector('.cart-item-price').textContent;
    const itemPrice = parseInt(itemPriceText.replace("đ","").replace(/,/g, ''));
    const itemQuantity = parseInt(itemRow.querySelector('.quantity-input').getAttribute("value"));
    console.log(itemPrice, itemQuantity);
    const itemSubtotal = itemPrice*itemQuantity;
    const itemSubtotalText = itemRow.querySelector('.cart-item-subtotal');
    itemSubtotalText.innerHTML = itemSubtotal.toLocaleString() + "<span>đ</span>";
    console.log(itemSubtotal);
    return {
        itemQuantity: itemQuantity,
        itemPrice: itemPrice,
        itemSubtotal: itemPrice*itemQuantity
    }   
};

const updateCartTotal = () => {
    const totalQuantityContainer = document.getElementById('total-quantity');
    const totalTempContainer = document.getElementById('total-temp'); 
    const totalVatContainer = document.getElementById('total-vat');
    const totalDiscountContainer = document.getElementById('total-discount');
    const totalFinalContainer = document.getElementById('total-final');

    totalQuantityContainer.innerHTML = totalQuantity;
    totalTempContainer.innerHTML = totalTemp.toLocaleString() + "<span>đ</span>";
    totalVatContainer.innerHTML = totalVat.toLocaleString() + "<span>đ</span>";
    totalDiscountContainer.innerHTML = totalDiscount.toLocaleString() + "<span>đ</span>";
    const totalFinal = totalTemp + totalVat - totalDiscount;
    totalFinalContainer.innerHTML = totalFinal.toLocaleString() + "<span>đ</span>";
};

const saveCart = () => {

    // Lấy giỏ hàng

    const cartData = [];
    cartItems.forEach((item, index) => {
        const productId = item.getAttribute("data-index");
        const productQuantityInput = item.querySelector(".quantity-input");
        const productQuantity = parseInt(productQuantityInput.getAttribute("value")) || 1;
        const cartItem = {
            "productId": productId,
            "productQuantity": productQuantity
        };
        cartData.push(cartItem);
    });

    // Cập nhật phía backend
    fetch("/update-cart/", {
        method: "POST",
        body: JSON.stringify({
            cart: cartData
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error(error.message);
    });
};