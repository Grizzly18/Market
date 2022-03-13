function myFunction() {
    if (!(window.matchMedia('(min-device-aspect-ratio: 16/9)').matches || window.matchMedia('(min-device-aspect-ratio: 16/10)').matches)) {
      window.location.href = 'catalog';
    } else {
      document.getElementById("myDropdown").classList.toggle("show");
    }
}