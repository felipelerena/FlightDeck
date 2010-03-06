/*
 * Extending Flightdeck with Modal 
 */

FlightDeck = Class.refactor(FlightDeck,{
	options: {
		modalWrap: {
			start: '<div class="UI_Modal_Wrapper"><div class="UI_Modal">',
			end: '</div></div>'
		}
	},
	initialize: function(options) {
		this.setOptions(options);
		this.previous(options);
		this.modals = {};
	},
	/*
	 * Method: displayModal
	 * Pretty dummy function which just wraps the content with divs and shows on the screen
	 */
	makeModal: function(content) {
		// copy options
		var data = $H(this.options.modalWrap).getClean();
		data['content'] = content;
		var modal_el = Elements.from('{start}{content}{end}'.substitute(data));
		var key = new Date().getTime();
		modal_el.store('modalKey', key);
		this.modals[key] = modal_el;
		return modal_el;
	},
	/*
	 * Method: displayModal
	 * Pretty dummy function which just wraps the content with divs and shows on the screen
	 */
	displayModal: function(content, inside_el) {
		// stickywin goes here
		
		return this.makeModal(content).inject(inside_el, 'top');
	},
	// these two are not really used atm
	hideModal: function(key) {
		this.modals[key].hide();
	},
	destroyModal: function(key) {
		this.modals[key].destroy();
	}
});
