function Search(i) {
    window.location.assign('http://127.0.0.1:5000/search/q=' + document.getElementsByClassName('search-prod')[i].value);
}