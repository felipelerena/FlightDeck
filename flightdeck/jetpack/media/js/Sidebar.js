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
		this.showItem = [];
		this.checkTogglers();
	},
	
	checkTogglers: function(){
		this.togglers = $$(this.options.togglerTrigger);
		this.containers = $$(this.options.togglerContainer);
		this.slideFx = [];
		this.sideContStatus = JSON.decode(Cookie.read('openedSidebarItems'));
		
		this.containers.each(this.attachActions.bind(this));
	},
	
	attachActions: function(container, index){
		var self = this,
			currentToggler = this.togglers[index].getParent();
		
		this.slideFx[index] = new Fx.Slide(container);
		
		// hide side item if the class is 'closed'
		if (currentToggler.hasClass('closed')){
			this.slideFx[index].hide();
		}
		
		// show site item if it was toggled open before reloading
		if (this.sideContStatus && this.sideContStatus[index]){
			this.slideFx[index].show();
			this.containers[index].getParent().setStyle('height', 'auto');
			this.togglers[index].getParent().removeClass('closed');
		}
		
		this.togglers[index].addEvents({
			click: function(e){
				e.stop();
				
				this.getParent().toggleClass('closed');
				self.slideFx[index].toggle();
				
				self.showItem = [];
				
				self.togglers.getParent().each(function(el){
					self.showItem.push(!(el.hasClass('closed') && el.hasClass('opened')));
				});
				
				Cookie.write('openedSidebarItems', JSON.encode(self.showItem));
			}
		});
	}
});

window.addEvents({
	domready: function(){
		new Sidebar();
	}
});