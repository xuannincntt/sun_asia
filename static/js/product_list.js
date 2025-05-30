const catCards = document.getElementsByClassName('category-card');
const subCatContainer = document.getElementsByClassName('category-main-subcat')[0];
const subCatItems = document.getElementsByClassName('subcat-item');
const catMain = document.getElementsByClassName('category-main-name');
const subCatBtn = document.getElementsByClassName('subcat-icon')[0];
const slides = document.querySelector('.slides');
const cards = document.querySelectorAll('.recommend-card');
const nextBtn = document.getElementById('next');
const prevBtn = document.getElementById('prev');
const menuItems = [...catCards, ...subCatItems, ...catMain];
let isSubCatOpen = true;
const cardsToShow = 5;
const cardWidth = cards[0].offsetWidth + 20; // include gap
let currentIndex = cardsToShow; // Start after prepended clones


document.addEventListener('DOMContentLoaded', () => {
    const firstClones = Array.from(cards).slice(0, cardsToShow).map(card => card.cloneNode(true));
    const lastClones = Array.from(cards).slice(-cardsToShow).map(card => card.cloneNode(true));

    firstClones.forEach(clone => slides.appendChild(clone));
    lastClones.forEach(clone => slides.insertBefore(clone, slides.firstChild));

    // Update total cards after cloning
    const totalCards = slides.querySelectorAll('.recommend-card').length;

    // Set initial position to the "first real slide"
    slides.style.transform = `translateX(-${cardWidth * currentIndex}px)`;

    // Add transition for smooth slide
    slides.style.transition = "transform 0.5s ease-in-out";

    setSubcatMenu();
    setHoveredCategories();
    
    nextBtn.addEventListener('click', () => {
        currentIndex++;
        slides.style.transform = `translateX(-${cardWidth * currentIndex}px)`;
        slides.style.transition = "transform 0.5s ease-in-out";

        // Loop logic
        if (currentIndex === totalCards - cardsToShow) {
            setTimeout(() => {
            slides.style.transition = "none";
            currentIndex = cardsToShow;
            slides.style.transform = `translateX(-${cardWidth * currentIndex}px)`;
            }, 500); // match transition duration
        }
    });

    prevBtn.addEventListener('click', () => {
        currentIndex--;
        slides.style.transform = `translateX(-${cardWidth * currentIndex}px)`;
        slides.style.transition = "transform 0.5s ease-in-out";

        // Loop logic
        if (currentIndex === 0) {
            setTimeout(() => {
            slides.style.transition = "none";
            currentIndex = totalCards - 2 * cardsToShow;
            slides.style.transform = `translateX(-${cardWidth * currentIndex}px)`;
            }, 500);
        }
    });
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
