import addProductToCart from "../utils/addProductToCart.js";

let catCards;
let cartBtns;
let buyBtns;
let filterForm;

const popup = document.getElementsByClassName("section-popup")[0];
const popupContainer = document.getElementsByClassName("popup-container")[0];
const popupHeader = document.getElementsByClassName("popup-header")[0];
const popupContent = document.getElementsByClassName("popup-content")[0];
const popupText = document.getElementsByClassName("popup-text")[0];


document.addEventListener('DOMContentLoaded', () => {
    catCards = document.querySelectorAll('.category-card');
    cartBtns = document.querySelectorAll('.cart-btn');
    buyBtns = document.querySelectorAll('.buy-btn');
    filterForm = document.getElementById("filter-form");

    setHoveredCategories();
    console.log(cartBtns);
    setCartBtnsOnClick();
    setBuyBtnsOnClick();
});

const setHoveredCategories = () => {
    catCards.forEach(item => {
        item.addEventListener('mouseover', () => {
            if (!item.classList.contains('category-card-active')){
                item.classList.add('category-card-hover');
            }
            
        });
    });

    catCards.forEach(item => {
        item.addEventListener('mouseout', () => {
            item.classList.remove('category-card-hover');
        });
    });
};


const setCartBtnsOnClick = () => {
    cartBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            const productCard = btn.closest(".product-card");
            const productInfo = productCard.getAttribute("data-index").split("_");
            const [productSlug, productId] = productInfo;
            console.log(productSlug, productId);
            addProductToCart(productSlug, productId, 1)
            .then(response => {
                console.log(response);
                showAddCartResponse(response);
            })  
            .catch(error => {
                console.log(error);
                showAddCartResponse(error);
            });
        });
    });
};

const setBuyBtnsOnClick = () => {
    buyBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.preventDefault();
            e.stopPropagation();
            const productCard = btn.closest(".product-card");
            const productInfo = productCard.getAttribute("data-index").split("_");
            const [productSlug, productId] = productInfo;
            // buyProduct(productSlug, productId)
            const productImageTag = productCard.querySelector(".product-card-image");
            const productNameTag = productCard.querySelector(".product-card-name");
            const orgPriceTag = productCard.querySelector(".product-card-orgPrice");
            const orgPrice = orgPriceTag? orgPriceTag.textContent: "0đ";
            const salePriceTag = productCard.querySelector(".product-card-salePrice");
            console.log(salePriceTag.textContent);
            showBuyNowPopup(productId, productImageTag.src, productNameTag.textContent, orgPrice, salePriceTag.textContent);
        });
    });
};

const showBuyNowPopup = (productId, productImage, productName, productOrgPrice, productSalePrice) => {
    const buyNowContent = `
        <div class="popup-close align-right">
            <i class='bx bx-x close-icon'></i> 
        </div>
        <div class="popup-product">
            <div class="popup-section-image align-center" >
                <img class="popup-image" src=${productImage} alt="" />
            </div>
            <form class="popup-section-form" action="/checkout/" method="POST">
                <label for="productId" style="display: none;">
                    <input type="text" id="productId" name="productId" value=${productId} />
                </label>
                <div class="popup-name">${productName}</div>
                <div class="popup-price">
                    ${productOrgPrice == productSalePrice?
                        `
                        <div class="popup-salePrice align-left">${productSalePrice}</div>`:
                        `
                        <div class="popup-orgPrice align-left">${productOrgPrice}</div>
                        <div class="popup-salePrice align-left">${productSalePrice}</div>
                        `
                    }
                <label class="popup-quantity" for="productQuantity">
                    <span class="popup-quantity-name">Số lượng</span>
                    <div class="popup-quantity-controller">
                        <div class="popup-minus-btn align-center">
                            <i class='bx bx-minus minus-icon'></i> 
                        </div>
                        <div class="popup-quantity-input align-center">
                            <input
                                type="number"
                                id="productQuantity"
                                name="productQuantity"
                                placeholder="0"
                                value="1"
                                class="quantity-input"
                            />
                        </div>
                        <div class="popup-add-btn align-center">
                            <i class='bx bx-plus plus-icon'></i> 
                        </div>
                    </div>
                </label>
                <div class="popup-submit">  
                    <button type="submit" class="action-btn proceed-btn align-center">
                        {% trans "Mua ngay" %}
                    </button>
                </div>
                
            </form>
        </div>`;
    popupContainer.innerHTML = buyNowContent;
    // popupContainer.style.width = "40%";
    const closeBtn = popupContainer.querySelector(".close-icon");
    const increaseBtn = popupContainer.querySelector(".plus-icon");
    const decreaseBtn = popupContainer.querySelector(".minus-icon");
    const quantityInput = popupContainer.querySelector("#productQuantity");
    togglePopup();
    closeBtn.addEventListener("click", () => {
        togglePopup();
    });
    
    increaseBtn.addEventListener("click", () => {
        const currentQuantity = parseInt(quantityInput.getAttribute("value")) || 1;
        quantityInput.setAttribute("value", currentQuantity + 1);

    });

    decreaseBtn.addEventListener("click", () => {
        const currentQuantity = parseInt(quantityInput.getAttribute("value")) || 1;
        if (currentQuantity <= 1){
            return;
        }
        quantityInput.setAttribute("value", currentQuantity - 1);
    });
    
};


const showAddCartResponse = (message) => {
    const notifyContent = `
        <div class="popup-header align-center">
                {% trans "Thông báo" %}
            </div>
        <div class="popup-content">
            <div class="popup-text align-center">
                {% trans "Thêm vào giỏ hàng thành công!" %}
            </div>
            <div class="popup-action">
                <button type="button" class="action-btn continue-btn align-center">
                    {% trans "Tiếp tục mua sắm" %}
                </button>
                <a href="/cart" class="action-btn cartNav-btn align-center">
                    {% trans "Xem giỏ hàng" %}
                </button>
            </div>
        </div>`;
    popupContainer.innerHTML = notifyContent;
    // popupContainer.style.width = "35%";
    const continueBtn = popupContainer.querySelector(".continue-btn");
    const cartNavBtn = popupContainer.querySelector("cartNav-btn");
    popupText.textContent = message;
    togglePopup();
    continueBtn.addEventListener('click', () => {
        togglePopup();
    });

};

const togglePopup = () => {
    popup.style.display = (popup.style.display === 'flex') ? 'none' : 'flex';   
};






