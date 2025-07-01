const addressDefaultLabel = document.getElementById("address-default");
const addressNewLabel = document.getElementById("address-new");
const paymentCodLabel = document.getElementById("payment-cod");
const paymentBankLabel = document.getElementById("payment-bank");
const bankInputSection = document.getElementById("bank-input");
const bankProofInput = document.getElementById("bankProof");
const bankProofPreview = document.getElementById("bank-proof-previewImg");
const orderNameInput = document.getElementById("name");
const orderEmailInput = document.getElementById("email");
const orderTelInput = document.getElementById("tel");
const orderAddressInput = document.getElementById("address");
const orderCityInput = document.getElementById("city");
const orderDistrictInput = document.getElementById("district");
const orderForm = document.getElementById("section-order-form");
const popup = document.querySelector(".order-popup");
const popupContainer = popup.querySelector(".popup-container");
const popupSpinner = popup.querySelector(".spinner");

let orderName;
let orderEmail;
let orderTel;
let orderAddress;
let orderCity;
let orderDistrict;

document.addEventListener("DOMContentLoaded", () => {
    getDefaultAddress();
    setInput();
    setAddressCardsOnHover();
    setPaymentCardsOnHover();
    setAddressCardsOnClick();
    setPaymentCardsOnClick();
    setBankProofInputOnChange();
    setFormOnSubmit();
    popupContainer.innerHTML = `Add commentMore actions
    <div class="popup-header align-center">
        Thông báo
    </div>
    <div class="popup-content">
        <div class="popup-text align-center">
            Bạn có chắc chắn muốn xóa mặt hàng này không?
        </div>
        <div class="popup-action">
            <button type="button" class="action-btn shop-btn">
                Tiếp tục mua sắm
            </button>
            <button type="button" class="action-btn order-btn">
                Xem đơn hàng
            </button>
        </div>Add commentMore actions
    </div> 
    `;
});

const setAddressCardsOnHover = () => {
    addressDefaultLabel.addEventListener("mouseover", () => {
        const parentCard = addressDefaultLabel.parentElement;
        parentCard.classList.add("card-hover");
    });

    addressDefaultLabel.addEventListener("mouseout", () => {
        const parentCard = addressDefaultLabel.parentElement;
        parentCard.classList.remove("card-hover");
    });

    addressNewLabel.addEventListener("mouseover", () => {
        const parentCard = addressNewLabel.parentElement;
        parentCard.classList.add("card-hover");
    });

    addressNewLabel.addEventListener("mouseout", () => {
        const parentCard = addressNewLabel.parentElement;
        parentCard.classList.remove("card-hover");
    });
};

const setPaymentCardsOnHover = () => {
    paymentCodLabel.addEventListener("mouseover", () => {
        const parentCard = paymentCodLabel.parentElement;
        parentCard.classList.add("card-hover");
    });

    paymentCodLabel.addEventListener("mouseout", () => {
        const parentCard = paymentCodLabel.parentElement;
        parentCard.classList.remove("card-hover");
    });

    paymentBankLabel.addEventListener("mouseover", () => {
        const parentCard = paymentBankLabel.parentElement;
        parentCard.classList.add("card-hover");
    });

    paymentBankLabel.addEventListener("mouseout", () => {
        const parentCard = paymentBankLabel.parentElement;
        parentCard.classList.remove("card-hover");
    });
};

const setAddressCardsOnClick = () => {
    addressDefaultLabel.addEventListener("click", () => {
        const parentCard = addressDefaultLabel.parentElement;
        const neighborParentCard = addressNewLabel.parentElement;
        neighborParentCard.classList.remove("card-active");
        parentCard.classList.add("card-active");
        setInput();
    });

    addressNewLabel.addEventListener("click", () => {
        const parentCard = addressNewLabel.parentElement;
        const neighborParentCard = addressDefaultLabel.parentElement;
        neighborParentCard.classList.remove("card-active");
        neighborParentCard.classList.add("card-hover");
        parentCard.classList.add("card-active");
        clearInput();
    });
};

const setPaymentCardsOnClick = () => {
    paymentCodLabel.addEventListener("click", () => {
        const parentCard = paymentCodLabel.parentElement;
        const neighborParentCard = paymentBankLabel.parentElement;
        neighborParentCard.classList.remove("card-active");
        parentCard.classList.add("card-active");
        bankInputSection.classList.add("hide");
    });

    paymentBankLabel.addEventListener("click", () => {
        const parentCard = paymentBankLabel.parentElement;
        const neighborParentCard = paymentCodLabel.parentElement;
        neighborParentCard.classList.remove("card-active");
        parentCard.classList.add("card-active");
        bankInputSection.classList.remove("hide");
    });
};

const setBankProofInputOnChange = () => {
    bankProofInput.addEventListener("change", (e) => {
        const file = e.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                bankProofPreview.src = e.target.result;
                bankProofPreview.classList.add("previewImg-active");
            };
            reader.readAsDataURL(file); // Đọc file và chuyển thành URL base64
        } else {
            bankProofPreview.src = "";
            bankProofPreview.classList.remove("previewImg-active"); // Nếu không có file, reset ảnh
        }
    })
};

const getDefaultAddress = () => {
    orderName = orderNameInput.getAttribute("value");
    orderEmail = orderEmailInput.getAttribute("value");
    orderTel = orderTelInput.getAttribute("value");
    orderAddress = orderAddressInput.getAttribute("value");
    orderCity = orderCityInput.getAttribute("value");
    orderDistrict = orderDistrictInput.getAttribute("value");
};

const setInput = () => {
    orderNameInput.setAttribute("value",orderName);
    orderEmailInput.setAttribute("value",orderEmail);
    orderTelInput.setAttribute("value",orderTel);
    orderAddressInput.setAttribute("value",orderAddress);
    orderCityInput.setAttribute("value",orderCity);
    orderDistrictInput.setAttribute("value",orderDistrict);
};

const clearInput = () => {
    orderNameInput.setAttribute("value","");
    orderEmailInput.setAttribute("value","");
    orderTelInput.setAttribute("value","");
    orderAddressInput.setAttribute("value","");
    orderCityInput.setAttribute("value","");
    orderDistrictInput.setAttribute("value","");
    bankProofInput.setAttribute("value","");
};

const setFormOnSubmit = () => {
    orderForm.addEventListener("submit", (e) => {
        e.preventDefault();
        
        showSpinner();
        togglePopup();
        const bankProofInput = document.getElementById('bankProof');

        // Lấy dữ liệu đơn hàng
        // Địa chỉ
        const orderMode = e.target.elements['orderMode'].value;
        const addressMode = e.target.elements['addressMode'].value;
        const name = e.target.elements['name'].value;
        const email = e.target.elements['email'].value;
        const tel = e.target.elements['tel'].value;
        const address = e.target.elements['address'].value;
        const city = e.target.elements['city'].value;
        const district = e.target.elements['district'].value;
        const notes = e.target.elements['notes'].value;

        // Thanh toán
        const paymentMode = e.target.elements['paymentMode'].value;
        let bankProofFile = null;
        if (bankProofInput.files){
            bankProofFile = bankProofInput.files[0]
        }

        const formData = new FormData();

        formData.append("orderMode", orderMode);
        formData.append("addressMode", addressMode);
        formData.append("name", name);
        formData.append("email", email);
        formData.append("tel", tel);
        formData.append("address", address);
        formData.append("city", city);
        formData.append("district", district);
        formData.append("notes", notes);
        formData.append("paymentMode", paymentMode);
        if (bankProofFile){
            formData.append("bankProof", bankProofFile);
        }

        fetch('/order/', {
            method: 'POST',
            body: formData,
        })
        .then(async response => {
            if (!response.ok) {
                const err = await response.json();
                throw err;
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            if (data.status)
            togglePopup();
            hideSpinner();
            popupSpinner.classList.add("hide");
            location.replace("/order/success");
        })
        .catch(error => {
            togglePopup();
            hideSpinner();
            console.log(error.message || error);
            showOrderFailure(error.message || error);
        });

        
    });
};

const showOrderFailure = (message) => {
    const popupText = popup.querySelector(".popup-text");
    const popupAction = popup.querySelector(".popup-action");
    popupText.innerHTML = message;
    popupAction.innerHTML= window.MyAppData.failureMessageHtml;
    const closeBtn = popupAction.querySelector(".close-btn");
    closeBtn.addEventListener("click", () => {
        togglePopup();
    });
    togglePopup();
    
};

const togglePopup = () => {
    popup.style.display = (popup.style.display === 'flex') ? 'none' : 'flex';   
};

const showSpinner = () => {
    popupContainer.style.display = "none";
    popupSpinner.classList.remove("hide");
};

const hideSpinner = () => {
    popupSpinner.classList.add("hide");
    popupContainer.style.display = "block";
};