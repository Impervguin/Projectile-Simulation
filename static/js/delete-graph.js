function delete_graph(id) {
  const XHR = new XMLHttpRequest(),
  XHR.open( 'POST', '/delete_graph' );
  XHR.send( id );
}
