import addProductToCart from "../utils/addProductToCart.js";

const detailImages = document.querySelectorAll('.detail-image-sub');
const slide = document.querySelector('.detail-images-slides');
const images = document.querySelectorAll('.carousel-image');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const tabs = document.querySelectorAll('.detail-tab');
const contents = document.querySelectorAll('.tab-content');

const popup = document.getElementsByClassName("detail-popup")[0];
const popupContainer = document.getElementsByClassName("popup-container")[0];
const popupHeader = document.getElementsByClassName("popup-header")[0];
const popupContent = document.getElementsByClassName("popup-content")[0];
const popupText = document.getElementsByClassName("popup-text")[0];
let cartBtn;
let buyBtn;

let currentIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    cartBtn = document.querySelector('.cart-btn');
    buyBtn = document.querySelector('.buy-btn');
    // Update total cards after cloning
    console.log(images);

    updateSlide(0);
    console.log(detailImages);
    setCarouselBtns();
    setImagesOnClick();
    setTabsOnClick();

    setCartBtnOnClick();
    // setBuyBtnOnClick();

});

const updateSlide = (index) => {
    if (index < 0) index = images.length - 1;
    if (index >= images.length) index = 0;
    console.log(index)

    currentIndex = index;
    slide.style.transform = `translateX(-${currentIndex * 100}%)`;
}

const setCarouselBtns = () => {
    nextBtn.addEventListener('click', () => {
        updateSlide(currentIndex + 1);
    });

    prevBtn.addEventListener('click', () => {
        updateSlide(currentIndex - 1);
    });
};

const setImagesOnClick = () => {
    detailImages.forEach((image, index) => {
        image.addEventListener('click', () => {
            console.log(index);
            updateSlide(index);
        });
    })
};

const setTabsOnClick = () => {
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Bỏ class active khỏi tất cả tabs và content
            tabs.forEach(t => t.classList.remove('tab-active'));
            contents.forEach(c => c.classList.remove('tab-content-active'));

            // Thêm active cho tab đang chọn và nội dung tương ứng
            tab.classList.add('tab-active');
            const contentId = tab.getAttribute('data-tab');
            document.getElementById(contentId).classList.add('tab-content-active');
        });
    });
};

const setCartBtnOnClick = () => {
    cartBtn.addEventListener("click", (e) => {
        const productCard = cartBtn.closest(".detail-product-action");
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

};

// const setBuyBtnOnClick = () => {
//     buyBtn.addEventListener("click", (e) => {
//         const productCard = btn.closest(".detail-product-action");
//         const productInfo = productCard.getAttribute("data-index").split("_");
//         const [productSlug, productId] = productInfo;
//         // buyProduct(productSlug, productId)
//         const productImageTag = productCard.querySelector(".product-card-image");
//         const productNameTag = productCard.querySelector(".product-card-name");
//         const orgPriceTag = productCard.querySelector(".product-card-orgPrice");
//         const orgPrice = orgPriceTag? orgPriceTag.textContent: "0đ";
//         const salePriceTag = productCard.querySelector(".product-card-salePrice");
//         console.log(salePriceTag.textContent);
//         showBuyNowPopup(productId, productImageTag.src, productNameTag.textContent, orgPrice, salePriceTag.textContent);
//     });
// };

const showAddCartResponse = (message) => {
    const notifyContent = `
        <div class="popup-header align-center">
                Thông báo
            </div>
        <div class="popup-content">
            <div class="popup-text align-center">
                Thêm vào giỏ hàng thành công
            </div>
            <div class="popup-action">
                <button type="button" class="action-btn continue-btn align-center">
                    Tiếp tục mua sắm
                </button>
                <a href="/cart" class="action-btn cartNav-btn align-center">
                    Xem giỏ hàng
                </button>
            </div>
        </div>`;
    popupContainer.innerHTML = notifyContent;
    // popupContainer.style.width = "35%";
    const continueBtn = popupContainer.querySelector(".continue-btn");
    popupText.textContent = message;
    togglePopup();
    continueBtn.addEventListener('click', () => {
        togglePopup();
    });

};

const togglePopup = () => {
    popup.style.display = (popup.style.display === 'flex') ? 'none' : 'flex';   
};







