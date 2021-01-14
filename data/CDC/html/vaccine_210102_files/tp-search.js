$( document ).ready( function() {

	$( 'header' ).on( 'click', '.search-submit', function( e ) {
		e.preventDefault();
		$( this ).parents( 'form' ).first().submit();
	} );

});