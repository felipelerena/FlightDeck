/*
 * Extending Flightdeck with Roar messages
 */

FlightDeck = Class.refactor(FlightDeck,{
	initialize: function(options) {
		this.setOptions(options);
		this.previous(options);
		
		this.warning = new Roar({
			className: 'roar warning'
		});
		this.error = new Roar({
			className: 'roar error',
			duration: 50000
		});
		this.message = new Roar({
			className: 'roar warning'
		});
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
