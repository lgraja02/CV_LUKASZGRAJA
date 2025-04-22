// Inicjalizacja AOS
AOS.init({
    duration: 1000, // Czas trwania animacji (w ms)
    easing: 'ease-in-out', // Typ przejścia
    once: false // Animacja wykonana tylko raz
  });


document.addEventListener('scroll', function() {
    var intro = document.querySelector('.intro');
    var scrollTop = window.scrollY || window.pageYOffset;
    var introHeight = intro.offsetHeight;

    // Kiedy przewijanie jest większe niż wysokość sekcji .intro, ukryj obraz tła
    if (scrollTop > introHeight) {
        intro.classList.add('fade-background');
    } else {
        intro.classList.remove('fade-background');
    }
});


const zoomContainers = document.querySelectorAll('.zoom-container');

zoomContainers.forEach(container => {
    const zoomImg = container.querySelector('.zoom-img');
    
    container.addEventListener('mousemove', function(e) {
        const rect = container.getBoundingClientRect(); // Pobranie pozycji kontenera
        const x = e.clientX - rect.left; // Pozycja kursora względem kontenera (oś X)
        const y = e.clientY - rect.top;  // Pozycja kursora względem kontenera (oś Y)
        
        const xPercent = (x / rect.width) * 100; // Przeliczenie na procenty dla transform-origin
        const yPercent = (y / rect.height) * 100; // Przeliczenie na procenty dla transform-origin
        
        // Ustawienie punktu przybliżenia w miejscu kursora
        zoomImg.style.transformOrigin = `${xPercent}% ${yPercent}%`;
        zoomImg.style.transform = 'scale(2)'; // Powiększenie obrazu 2x
    });

    container.addEventListener('mouseleave', function() {
        // Przywrócenie obrazu do normalnych rozmiarów, gdy mysz opuści obraz
        zoomImg.style.transform = 'scale(1)';
        zoomImg.style.transformOrigin = 'center center'; // Resetowanie punktu powiększenia
    });
});

document.getElementById("myShopLink").addEventListener("click", function(event){
    alert("WORK IN PROGRESS");
});