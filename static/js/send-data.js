const btn = document.querySelector('#addbtn');

function sendData( data ) {
  const XHR = new XMLHttpRequest(),
        FD  = new FormData();

  for( name in data ) {
    FD.append( name, data[ name ] );
  }
  XHR.addEventListener("load", req_load());
  XHR.addEventListener(' error', function( event ) {
    alert( 'Oops! Something went wrong.' );
  } );
  XHR.open( 'POST', '/postdata' );
  XHR.send( FD );
}

btn.addEventListener( 'click', function()
  { data = get_input_values();
  if (data != 0) {
    sendData(data);
  };
} )

function req_load() {
    window.location.replace("/wait");
}