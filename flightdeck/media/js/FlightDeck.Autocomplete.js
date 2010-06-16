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
			valueField: $(this.options.value_el),
			valueFilter: function(data) {
				return data.id_number
			},
			filter: {
				type: 'contains',
				path: 'full_name'
			}
		});
		return this.autocomplete;
	}
});
