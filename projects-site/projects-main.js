import { projects } from "./projects-list.js";

// Inicjalizacja AOS
AOS.init({
    duration: 1000, // Czas trwania animacji (w ms)
    easing: 'ease-in-out', // Typ przejścia
    once: false // Animacja wykonana tylko raz
  });


document.getElementById("myShopLink").addEventListener("click", function(event){
    alert("WORK IN PROGRESS");
});

function projectDisplay() {
    let projectsHTML = ''; // Deklaracja zmiennej
    projects.forEach(elem => {
        projectsHTML += 
        `<div class="project-id ${elem.projectID}" data-aos="fade-up">
                <div class="project-info">
                    <div class="project-name">
                        <a>${elem.projectName}</a>
                    </div>
                    <div class="project-description">
                        <h2>${elem.description}</h2>
                    </div>
                    <div class="project-buttons-section">
                        <div class="read-more-section read-${elem.projectID}">
                            <a target="_blank" href="${elem.readMoreLink}">Read More &rarr;</a>
                        </div>
                        <div class="download-section download-${elem.projectID}">
                            <a>Download:</a>
                            <a href="${elem.downloadFile}">file.zip</a>
                        </div>
                    </div>
                </div>
                <div class="project-photo-section">
                    <img class="project-photo" src="${elem.thumbnailPath}">
                    <img class="project-mobile-photo" src="${elem.thumbnailMobilePath}">
                    <a class="technologies">Technologies: ${elem.technologies}</a>
                </div>
            </div>`;
    });

    // Przypisanie całości do .project-container dopiero po zakończeniu iteracji
    document.querySelector(".project-container").innerHTML = projectsHTML;

    // Teraz sprawdzamy, czy link "Read More" jest dostępny, i ukrywamy go, jeśli nie jest podany
    projects.forEach(elem => {
        if (elem.readMoreLink === "#") {
            let element = document.querySelector(`.read-${elem.projectID}`);
            if (element) {
                element.style.display = "none"; // Ukryj link "Read More" jeśli URL to "#"
            }
        }
        if (elem.downloadFile === "#") {
            let element = document.querySelector(`.download-${elem.projectID}`);
            if (element) {
                element.style.display = "none"; // Ukryj link "Read More" jeśli URL to "#"
            }
        }
    });
}

projectDisplay();