import addProductToCart from "../utils/addProductToCart.js";

let catCards;
let cartBtns;
let buyBtns;
let filterForm;

const popup = document.getElementsByClassName("section-popup")[0];
const popupHeader = document.getElementsByClassName("popup-header")[0];
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
            addProductToCart(productSlug, productId)
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
        });
    });
};

const showBuyNowPopup = (productImage, productName, productOrgPrice, productSalePrice) => {

};


const showAddCartResponse = (message) => {
    const continueBtn = document.querySelector(".continue-btn");
    const cartNavBtn = document.querySelector("cartNav-btn");
    popupText.textContent = message;
    togglePopup();
    continueBtn.addEventListener('click', () => {
        togglePopup();
    });

};

const togglePopup = () => {
    popup.style.display = (popup.style.display === 'flex') ? 'none' : 'flex';   
}




