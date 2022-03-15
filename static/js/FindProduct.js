function FindProduct() {
    let res = [];
    res.push( window.location.pathname.split("&")[0].split('=')[1]);
    if (document.getElementsByClassName('brand-for-product')[0].value.length > 0){
        res.push(  "brand=" + document.getElementsByClassName('brand-for-product')[0].value )
    }
    let radio_sort_btns = document.getElementsByClassName('radio-sort-product');
    for (let i = 0; i < radio_sort_btns.length; i++){
        if (radio_sort_btns[i].checked){
            res.push( "sort=" + radio_sort_btns[i].value );
            break;
        }
    }
    let radio_size_btns = document.getElementsByClassName('radio-for-product');
    for (let i = 0; i < radio_size_btns.length; i++){
        if (radio_size_btns[i].checked){
            res.push( "size=" + radio_size_btns[i].value );
            break;
        }
    }
    let from_prc = document.getElementsByClassName('price-from-prod')[0].value;
    let to_prc = document.getElementsByClassName('price-to-prod')[0].value;
    if (from_prc.length > 0 && to_prc.length > 0){
        res.push( "price=" + from_prc + "," + to_prc );
    }
    window.location.replace('q=' + res.join('&'));
}