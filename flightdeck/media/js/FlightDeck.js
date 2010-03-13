/*
 * Class: FlightDeck
 * Initializes all needed functionality
 */

var FlightDeck = new Class({
	Implements: [Options],
	options: {
		menu_el: 'UI_Editor_Menu'
	},
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
	/*
	 * Method: enableMenuButtons
	 */
	enableMenuButtons: function() {
		$$('.' + this.options.menu_el + ' li').each(function(menuItem){
			if (menuItem.hasClass('disabled')){
				menuItem.removeClass('disabled');
			}
		});
	},
});


/*
 * Default onFailure in all Requests
 */

Request = Class.refactor(Request, {
	options: {
		onFailure: function(xhr) {
			fd.error.alert('Error {status}'.substitute(xhr), xhr.statusText);
		}
	}
});


/*
 * Inspired by
 * http://github.com/jeresig/sizzle/commit/7631f9c3f85e5fa72ac51532399cb593c2cdc71f
 * and this http://github.com/jeresig/sizzle/commit/5716360040a440041da19823964f96d025ca734b
 * and then http://dev.jquery.com/ticket/4512
 */

Element.implement({

	isHidden: function(){
		var w = this.offsetWidth, h = this.offsetHeight,
		force = (this.tagName.toLowerCase() === 'tr');
		return (w===0 && h===0 && !force) 
			? true 
			: (w!==0 && h!==0 && !force) ? false : this.getStyle('display') === 'none';
	},
	isVisible: function(){
		return !this.isHidden();
	},
	getSiblings: function(match,nocache) {
		return this.getParent().getChildren(match,nocache).erase(this);
	}

});


Class.Mutators.$name = function(name){ this.implement('$family', {name: name}); };
/*
 * File: media/js/FlightDeck.js

if (!console) { 
	var console = {
		log: $empty,
		dir: $empty,
		info: $empty,
		error: function(value) { alert(value); }
	};
}
 */


window.addEvent('load', function() {
	window.mozFlightDeck.whenMessaged(function(data) {
		// This gets called when one of our extensions has been installed
		// successfully, or failed somehow.
		fd.message.alert(JSON.stringify(data));
	});
});
