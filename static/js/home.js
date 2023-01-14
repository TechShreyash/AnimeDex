let slideIndex = 0;
let clickes = 0;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
    clickes = 1;
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
    clickes = 1;
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex - 1].style.display = "flex";

}

showSlides2();

async function showSlides2() {
    if (clickes == 1) {
        await sleep(10000)
        clickes = 0
    }
    let i;
    let slides = document.getElementsByClassName("mySlides");
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) { slideIndex = 1 }
    slides[slideIndex - 1].style.display = "flex";
    setTimeout(showSlides2, 5000); // Change image every 2 seconds
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Infinite Scroll


const container = document.querySelector('.recento');
let page = 2
let isLoading = 0
let errCount = 0

function loadAnimes() {
    try {
        if (isLoading == 0) {
            isLoading = 1
            const x = Array.from(
                document.querySelectorAll('.poster')
            ).pop()
            fetch('/api/latest/' + page.toString())
                .then(response => {
                    return response.json();
                })
                .then(data => {
                    container.innerHTML += data['html']
                    x.scrollIntoView()
                    page += 1;
                    isLoading = 0
                })
            errCount = 0
        }
    } catch (error) {
        isLoading = 0
        errCount += 1
        if (errCount < 5) {
            setTimeout(loadAnimes(), 2000)
        }

    }
}

window.addEventListener('scroll', () => {
    if (window.scrollY + window.innerHeight >=
        document.documentElement.scrollHeight) {
        loadAnimes();
    }
})
