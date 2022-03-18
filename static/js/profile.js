document.getElementsByClassName('favourite-profile')[0].classList.add('hidden');
document.getElementsByClassName('requests-profile')[0].classList.add('hidden');



function Fav() {
    document.getElementsByClassName('requests-profile')[0].classList.add('hidden');
    document.getElementsByClassName('about-me')[0].classList.add('hidden');
    document.getElementsByClassName('favourite-profile')[0].classList.remove('hidden');
}

function Req() {
    document.getElementsByClassName('favourite-profile')[0].classList.add('hidden');
    document.getElementsByClassName('about-me')[0].classList.add('hidden');
    document.getElementsByClassName('requests-profile')[0].classList.remove('hidden');
}

function About() {
    document.getElementsByClassName('requests-profile')[0].classList.add('hidden');
    document.getElementsByClassName('favourite-profile')[0].classList.add('hidden');
    document.getElementsByClassName('about-me')[0].classList.remove('hidden');
}