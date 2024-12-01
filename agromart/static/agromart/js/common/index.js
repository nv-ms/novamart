window.addEventListener("scroll", ()=> {
    document.querySelector("header").classList.toggle("sticky", window.scrollY > 100);
});

function toggleNavMenu() {
    const linksItem = document.querySelector('.links-item');
    const links = document.querySelector('.links');

    linksItem.classList.toggle('menu-active');

    if (linksItem.classList.contains('menu-active')) {
        links.style.display = 'flex';
    } else {
        links.style.display = 'none';
    }
}
