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
			onSelect: function(elements, resp){
				// $('value-field').set('value', resp);
			}
		});
		
		return this.autocomplete;
	}
});

window.addEvent('domready', function(){
	new FlightDeck.Autocomplete();
});