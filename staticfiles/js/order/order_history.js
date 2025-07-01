let expandBtns;
let orderCardItemContainer;

document.addEventListener("DOMContentLoaded", () => {
    expandBtns = document.querySelectorAll(".expand-btn");
    orderCardItemContainer = document.querySelectorAll(".order-card-items");
    setExpandBtnsOnClick();
});

const setExpandBtnsOnClick = () => {
    expandBtns.forEach(btn => {
        btn.addEventListener("click",() => {
            const expandIcon = btn.querySelector(".expand-icon");
            const orderCard = btn.closest(".order-card");
            const orderCardItems = orderCard.querySelector(".order-card-items"); 
            const isExpanded = orderCardItems.style.maxHeight && orderCardItems.style.maxHeight !== '0px';

            shrinkAllExpands();
            if (!isExpanded){
                expandIcon.classList.replace("bx-chevron-down","bx-chevron-up");
                orderCardItems.style.maxHeight = orderCardItems.scrollHeight + 'px';
            }
        });
    });
};

const shrinkAllExpands = () => {
    orderCardItemContainer.forEach(container => {
        const orderCard = container.closest(".order-card");
        const expandIcon = orderCard.querySelector(".expand-icon");
        expandIcon.classList.replace("bx-chevron-up","bx-chevron-down");
        // container.classList.remove("order-items-visible");
        container.style.maxHeight = '0';
    });
};