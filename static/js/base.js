if (window.matchMedia('(min-device-aspect-ratio: 16/9)').matches || window.matchMedia('(min-device-aspect-ratio: 16/10)').matches) {
  document.getElementsByClassName('login')[0].classList.toggle("computer-login");
  document.getElementById('login-logo').classList.toggle("computer-login-logo");
}


function myFunction() {
    if (!(window.matchMedia('(min-device-aspect-ratio: 16/9)').matches || window.matchMedia('(min-device-aspect-ratio: 16/10)').matches)) {
      window.location.href = 'catalog';
    } else {
      document.getElementById("myDropdown").classList.toggle("show");
    }
}


function SettingsProfile() {
  if (!(window.matchMedia('(min-device-aspect-ratio: 16/9)').matches || window.matchMedia('(min-device-aspect-ratio: 16/10)').matches)) {
    window.location.href = 'profile';
  } else {
    document.getElementById("myDropdown2").classList.toggle("show");
  }
}