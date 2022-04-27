function check_number(input) {
    ch = input.value.replace(/[^\d,]/g, '');
//    pos = ch.indexOf(',');
//    if(pos != -1){
//        if((ch.length-pos)>2){
//            ch = ch.slice(0, -1);
//        }
//    }
    input.value = ch;
};