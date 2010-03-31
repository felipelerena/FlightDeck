/* 
 * File: FlightDeck.Autocomplete.js
 */

FlightDeck.Autocomplete = new Class({
	initialize: function() {
		this.create();
		this.autocomplete;
	},

	create: function(content) {
		
		this.autocomplete = new Meio.Autocomplete.Select('add_dependency', '/autocomplete/', {
			filter: {
				type: 'contains',
				path: 'name'
			},
			onSelect: function(elements, library){
				console.log(library);
				$('dependency_slug').set('value', library.slug);
			}
		});
		
		return this.autocomplete;
	}
});

window.addEvent('domready', function(){
	new FlightDeck.Autocomplete();
});