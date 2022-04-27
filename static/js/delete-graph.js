function delete_graph(id) {
  const XHR = new XMLHttpRequest();
  XHR.addEventListener("load", req_load());
  XHR.open( 'POST', '/delete_graph' );
  XHR.send( id );
}

function req_load() {
    window.location.replace("/wait");
}