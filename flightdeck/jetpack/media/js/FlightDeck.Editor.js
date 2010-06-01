/*
 * Extending Flightdeck with Editor functionality 
 */

FlightDeck = Class.refactor(FlightDeck,{
	initialize: function(options) {
		this.setOptions(options);
		this.previous(options);
		this.enableMenuButtons();
	},
	/*
	 * Method: getItem
	 */
	getItem: function() {
		// item is currently a global 
		return this.item;
	},
	/*
	 * Method: enableMenuButtons
	 * Switch on menu buttons, check if possible
	 */
	enableMenuButtons: function() {
		$$('.' + this.options.menu_el + ' li.disabled').each(function(menuItem){
			var switch_on = true;
			if (switch_on) {
				menuItem.removeClass('disabled');
			}
		}, this);
	}
	
});
