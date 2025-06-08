const addressDefaultLabel = document.getElementById("address-default");
const addressNewLabel = document.getElementById("address-new");
const paymentCodLabel = document.getElementById("payment-cod");
const paymentBankLabel = document.getElementById("payment-bank");
const bankInputSection = document.getElementById("bank-input");
const bankProofInput = document.getElementById("bankingProof");
const bankProofPreview = document.getElementById("bank-proof-previewImg");
const orderNameInput = document.getElementById("name");
const orderEmailInput = document.getElementById("email");
const orderTelInput = document.getElementById("tel");
const orderAddressInput = document.getElementById("address");
const orderCityInput = document.getElementById("city");
const orderDistrictInput = document.getElementById("district");

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