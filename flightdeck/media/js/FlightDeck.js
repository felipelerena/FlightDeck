/*
 * File: media/js/FlightDeck.js
 */

if (!console) { 
	var console = {
		log: $empty,
		dir: $empty,
		info: $empty,
		error: function(value) { alert(value); }
	};
}

Element.implement({
	getSiblings: function(match,nocache) {
		return this.getParent().getChildren(match,nocache).erase(this);
	}
});

/*
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
		this.editors = [];
	},
	/*
	 * Method: hideEditors
	 */
	hideEditors: function() {
		this.editors.each(function(ed){ ed.hide(); });
	},
	
});
