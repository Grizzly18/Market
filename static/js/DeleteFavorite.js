let btns = document.getElementsByClassName('send-card');

function sendData( data ) {
    const XHR = new XMLHttpRequest();
    XHR.open( 'POST', 'http://127.0.0.1:5000/delete-favorite' );
    XHR.send( data );
}

for (let i = 0; i < btns.length; i++) {
    btns[i].addEventListener( 'click', function() {
        sendData(  btns[i].getAttribute('value') );
    } )
}