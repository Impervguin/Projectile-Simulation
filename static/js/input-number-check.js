function check_number(input) {
    ch = input.value.replace(/[^\d.]/g, '');
    var point_cnt = ch.split('.').length - 1;
    if (point_cnt > 1) {
        pos = ch.indexOf('.');
        ch = ch.slice(0, pos) + ch.slice(pos + 1, ch.length);
    };

    if ((ch.charAt(ch.length - 1) != "0" || (point_cnt == 0)) && (ch.charAt(ch.length - 1) != ".") && (ch.length != 0)) {
        max = parseFloat(input.getAttribute('data-max'));
        min = parseFloat(input.getAttribute('data-min'));
        ch = parseFloat(ch);
        if (max < ch) {
            ch = max;
        } else if (min > ch) {
            ch = min;
        };
    };


    input.value = ch;
};
