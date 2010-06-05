/* 
 * File: FlightDeck.Autocomplete.js
 */

FlightDeck.Autocomplete = new Class({
	Implements: [Options],
	options: {
		value_el: 'library_id_number',
		display_el: 'assign_library',
		value_field: 'id_number',
		url: '/autocomplete/library/'
	},
	initialize: function(options) {
		this.setOptions(options);
		this.create();
		this.autocomplete;
	},

	create: function(content) {
		this.autocomplete = new Meio.Autocomplete.Select(
			this.options.display_el, 
			this.options.url, {
			filter: {
				type: 'contains',
				path: 'full_name'
			},
			onSelect: function(elements, item){
				$(this.options.value_el).set('value', 
											item[this.options.value_field]);
			}.bind(this)
		});
		return this.autocomplete;
	}
});
