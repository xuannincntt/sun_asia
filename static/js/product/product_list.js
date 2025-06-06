const catCards = document.getElementsByClassName('category-card');
const subCatContainer = document.getElementsByClassName('category-main-subcat')[0];
const subCatItems = document.getElementsByClassName('subcat-item');
const catMain = document.getElementsByClassName('category-main-name');
const subCatBtn = document.getElementsByClassName('subcat-icon')[0];
const cartBtns = document.querySelectorAll('.cart-btn');
const buyBtns = document.querySelectorAll('.buy-btn');
const filterForm = document.getElementById("filter-form");


document.addEventListener('DOMContentLoaded', () => {
    setSubcatMenu();
    setHoveredCategories();
    setCartBtnsOnClick();
    setBuyBtnsOnClick();
});

const setHoveredCategories = () => {
    menuItems.forEach(item => {
        item.addEventListener('mouseover', () => {
            if (!item.classList.contains('category-card-active')){
                item.classList.add('category-card-hover');
            }
            
        });
    });

    menuItems.forEach(item => {
        item.addEventListener('mouseout', () => {
            item.classList.remove('category-card-hover');
        });
    });
};

const setSubcatMenu = () => {
    subCatBtn.addEventListener('click', () => {
        if (isSubCatOpen){
            subCatContainer.classList.add('hide');
            subCatBtn.classList.replace('bx-chevron-down','bx-chevron-up');
            isSubCatOpen = false;
        }
        else {
            subCatContainer.classList.remove('hide');
            subCatBtn.classList.replace('bx-chevron-up','bx-chevron-down');
            isSubCatOpen = true;
        }

    });
};

const setCartBtnsOnClick = () => {
    cartBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            
        });
    });
};

const setBuyBtnsOnClick = () => {
    buyBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            
        });
    });
};


