/*
 * File: jetpack/Sidebar.js
 */


var Sidebar = new Class({
	Implements: [Options, Events],
	options: {
		togglerTrigger: '.UI_Sidebar_Toggler a',
		togglerContainer: '.UI_Sidebar_ItemCont'
	},
	
	initialize: function(options) {
		this.setOptions(options);
		this.checkTogglers();
	},
	
	checkTogglers: function() {
		this.togglers = $$(this.options.togglerTrigger);
		this.containers = $$(this.options.togglerContainer);
		this.slideFx = [];
		var self = this;
		
		this.containers.each(function(container, index){
			this.slideFx[index] = new Fx.Slide(container).hide();
			this.togglers[index].getParent().addClass('closed');
			this.togglers[index].addEvents({
				click: function(e){
					e.stop();
					this.getParent().toggleClass('closed');
					self.slideFx[index].toggle();
				}
			});
		}, this);
	}
});

window.addEvents({
	domready: function(){
		new Sidebar();
	}
});