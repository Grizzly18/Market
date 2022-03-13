if (!(window.matchMedia('(min-device-aspect-ratio: 16/9)').matches || window.matchMedia('(min-device-aspect-ratio: 16/10)').matches)) {
    let b = document.getElementsByClassName('card-row')[0];
    let article = b.getElementsByClassName('shadow-sm')[0];
    article.style.display = 'none';
    let b2 = document.getElementsByClassName('card-row')[1];
    let article2 = b2.getElementsByClassName('shadow-sm')[0];
    article2.style.display = 'none';
} 