/*
 * File: jetpack/Sidebar.js
 */


var Sidebar = new Class({
	
	Implements: [Options, Events],
	
	options: {
		togglerTrigger: '.UI_Sidebar_Toggler a',
		togglerContainer: '.UI_Sidebar_ItemCont'
	},
	
	initialize: function(options){
		this.setOptions(options);
		this.checkTogglers();
	},
	
	checkTogglers: function(){
		this.togglers = $$(this.options.togglerTrigger);
		this.containers = $$(this.options.togglerContainer);
		this.slideFx = [];
		
		this.containers.each(this.attachActions.bind(this));
	},
	
	attachActions: function(container, index){
		var self = this,
			currentToggler = this.togglers[index].getParent();
		
		this.slideFx[index] = new Fx.Slide(container);
		
		if (currentToggler.hasClass('closed')){
			this.slideFx[index].hide();
		}
		
		this.togglers[index].addEvents({
			click: function(e){
				e.stop();
				this.getParent().toggleClass('closed');
				self.slideFx[index].toggle();
			}
		});
	}
});

window.addEvents({
	domready: function(){
		new Sidebar();
	}
});