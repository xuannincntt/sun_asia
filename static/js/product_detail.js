const detailImages = document.querySelectorAll('.detail-image-sub');
const slide = document.querySelector('.detail-images-slides');
const images = document.querySelectorAll('.carousel-image');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const tabs = document.querySelectorAll('.detail-tab');
const contents = document.querySelectorAll('.tab-content');
const slides = document.querySelector('.slides');
const cards = document.querySelectorAll('.recommend-card');
const nextRecBtn = document.getElementById('next');
const prevRecBtn = document.getElementById('prev');

let currentIndex = 0;
const cardsToShow = 5;
const cardWidth = cards[0].offsetWidth + 20; // include gap
let currentRecIndex = cardsToShow; // Start after prepended clones

document.addEventListener("DOMContentLoaded", () => {
    const firstClones = Array.from(cards).slice(0, cardsToShow).map(card => card.cloneNode(true));
    const lastClones = Array.from(cards).slice(-cardsToShow).map(card => card.cloneNode(true));

    firstClones.forEach(clone => slides.appendChild(clone));
    lastClones.forEach(clone => slides.insertBefore(clone, slides.firstChild));

    // Update total cards after cloning
    const totalCards = slides.querySelectorAll('.recommend-card').length;

    // Set initial position to the "first real slide"
    slides.style.transform = `translateX(-${cardWidth * currentRecIndex}px)`;

    // Add transition for smooth slide
    slides.style.transition = "transform 0.5s ease-in-out";

    updateSlide(0);
    console.log(detailImages);
    setCarouselBtns();
    setImagesOnClick();
    setTabsOnClick();

    nextRecBtn.addEventListener('click', () => {
        currentRecIndex++;
        slides.style.transform = `translateX(-${cardWidth * currentRecIndex}px)`;
        slides.style.transition = "transform 0.5s ease-in-out";

        // Loop logic
        if (currentRecIndex === totalCards - cardsToShow) {
            setTimeout(() => {
            slides.style.transition = "none";
            currentRecIndex = cardsToShow;
            slides.style.transform = `translateX(-${cardWidth * currentRecIndex}px)`;
            }, 500); // match transition duration
        }
    });

    prevRecBtn.addEventListener('click', () => {
        currentRecIndex--;
        slides.style.transform = `translateX(-${cardWidth * currentRecIndex}px)`;
        slides.style.transition = "transform 0.5s ease-in-out";

        // Loop logic
        if (currentRecIndex === 0) {
            setTimeout(() => {
            slides.style.transition = "none";
            currentRecIndex = totalCards - 2 * cardsToShow;
            slides.style.transform = `translateX(-${cardWidth * currentRecIndex}px)`;
            }, 500);
        }
    });
});

const updateSlide = (index) => {
    if (index < 0) index = 0;
    if (index >= images.length) index = images.length - 1;

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







