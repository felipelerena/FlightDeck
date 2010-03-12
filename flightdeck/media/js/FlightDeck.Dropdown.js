/* 
 * File: Flightdeck.Dropdown.js
 */

var Dropdown = new Class({

	initialize: function(){
		this.dropdown = {
			cont: '.UI_Versions',
			trigger: '.UI_Pick_Version'
		};

		this.setDefaults();
	},

	setDefaults: function(){
		$$(this.dropdown.cont).fade('hide');
		$$(this.dropdown.cont).set('tween', {
			duration: 200
		});

		$$(this.dropdown.trigger).each(function(trigger){
			trigger.addEvents({
				click: this.toggle.bindWithEvent(trigger, this)
			});
		}, this);

		$(document.body).addEvents({
			click: function(e){
				if (!$(e.target).getParent(this.dropdown.cont)){
					this.hide();
				}
			}.bind(this)
		});
	},

	toggle: function(e, parent){
		e.stop();
		
		$$(parent.dropdown.cont).fade('out');
		$$(parent.dropdown.trigger).removeClass('active');
		
		if (this.getElement(parent.dropdown.cont).getStyles('opacity')['opacity'] === 0){
			this.getElement(parent.dropdown.cont).fade('in');
			this.addClass('active');
		}
	},

	hide: function(){
		$$(this.dropdown.cont).fade('out');
		$$(this.dropdown.trigger).removeClass('active');
	}
});

window.addEvent('domready', function(){
	new Dropdown();
});