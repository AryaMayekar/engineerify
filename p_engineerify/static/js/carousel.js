const carousel = document.querySelector('.carousel');
const dots = document.querySelectorAll('.dot');
let currentIndex = 0; //first slide
const totalslides = 4;
const slideInterval = 5000;//5 seconds

//function to update carousel postiom and dot state
function updatecarousel() {
  const offset = -currentIndex * 100;
  carousel.style.transform= `translateX(${offset}%`;
  updatedots();
}

//function to update dots
function updatedots(){
  dots.forEach((dot, index) => {
    dot.classList.toggle('active', index === currentIndex);
  });
}

//function to handle dot click
dots.forEach(dot => {
  dot.addEventListener('click', () => {
    clearInterval(autoslide);// pause auto-slide
    currentIndex = Number(dot.dataset.index)// get the clicked dot index
    updatecarousel();
    startautoslide();//restart autoslide
  });
});

//auto slide change
let autoslide;
function startautoslide() {
  autoslide = setInterval(() => {
    currentIndex = (currentIndex + 1) % totalslides;
    updatecarousel();
  },slideInterval);
}

startautoslide();