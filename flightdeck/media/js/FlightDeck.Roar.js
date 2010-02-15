/*
 * Extending Flightdeck with Roar messages
 */

FlightDeck = Class.refactor(FlightDeck,{
	initialize: function(options) {
		this.setOptions(options);
		this.previous(options);
		
		this.warning = new Roar();
		this.error = new Roar();
		this.message = new Roar();
		this.parseMessages();
	},
	/*
	 * Method: parseMessages
	 * Parses DOM to find elements with fd_{type_of_message} 
	 * displays messages and removes elements from DOM
	 */
	parseMessages: function() {
		['message', 'warning', 'error'].each(function(t) {
			$$('.fd_'+t).each(function(el) {
				this[t].alert(el.get('title') || t, el.get('text'));
				el.destroy();
			}, this);
		}, this);
	}

});
