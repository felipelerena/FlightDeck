/* 
 * File: Flightdeck.Modal.js
 */

FlightDeck = Class.refactor(FlightDeck,{
	options: {
		modalWrap: {
			start: '<div class="UI_Modal_Wrapper"><div class="UI_Modal">',
			end: '</div></div>'
		}
	},
	initialize: function(options) {
		this.modal = new ModalWindow();
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
	displayModal: function(content) {
		// modal is defined in base.html - this should probably be done elsewhere
		return this.modal.create(this.makeModal(content)[0]);
	},
	// these two are not really used atm
	hideModal: function(key) {
		this.modals[key].hide();
	},
	destroyModal: function(key) {
		this.modals[key].destroy();
	},
	showQuestion: function(data) {
		if (!data.cancel) data.cancel = 'Cancel';
		if (!data.ok) data.ok = 'OK';
		if (!data.id) data.id = '';
		var template = '<div id="display-package-info">'+
							'<h3>{title}</h3>'+
							'<div class="UI_Modal_Section">'+
								'<p>{message}</p>'+
							'</div>'+
							'<div class="UI_Modal_Actions">'+
								'<ul>'+
									'<li><input id="{id}" type="button" value="{ok}" class="submitModal"/></li>'+
									'<li><input type="reset" value="{cancel}" class="closeModal"/></li>'+
								'</ul>'+
							'</div>'+
						'</div>';
		display = this.displayModal(template.substitute(data));
		if (data.callback && data.id) {
			$(data.id).addEvent('click', data.callback);
		}
		return display;
	}
});
