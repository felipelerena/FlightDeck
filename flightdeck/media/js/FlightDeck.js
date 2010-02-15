/*
 * File: media/js/FlightDeck.js
 * Class: FlightDeck
 * Initializes all needed functionality
 */

var FlightDeck = new Class({
	Implements: [Options],
	initialize: function() {
		this.warning = this.error = this.message = {
			'alert': function(title, message) {
				alert(title+"\n"+message);
			}
		};
	}
});
