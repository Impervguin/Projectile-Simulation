const promo1 = document.getElementById('promo1');
const promo2 = document.getElementById('promo2');
const sys_form = document.getElementById('sys-form');


function resize_promo(){
    const height = getComputedStyle(sys_form).getPropertyValue('height');
    console.log(height);
    promo1.style.height = height;
    promo2.style.height = height;
    console.log("script done");
}

resize_promo();