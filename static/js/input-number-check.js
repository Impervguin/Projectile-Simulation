function check_number(input) {
    ch = input.value.replace(/[^\d.]/g, '');
    var point_cnt = ch.split('.').length - 1;
    if (point_cnt > 1) {
        pos = ch.indexOf('.');
        ch = ch.slice(0, pos) + ch.slice(pos + 1, ch.length);
    }
    input.value = ch;
};