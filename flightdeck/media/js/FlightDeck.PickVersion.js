/* 
 * File: Flightdeck.PickVersion.js
 * TODO: 
 * - caching
 */

var PickVersion = new Class({

	initialize: function(){
		this.version = {
			cont: '.UI_Versions',
			trigger: '.UI_Pick_Version'
		};

		this.setDefaults();
	},

	setDefaults: function(){
		var self = this;
		
		$$(this.version.trigger).each(function(trigger, index){
			trigger.getElement('a').addEvents({
				click: function(e){
					e.preventDefault();
					
					// fetch the versions
					new Request.JSON({
						url: this.get('href'),
						onComplete: function(response){
							this.attachInfo.call(this, response, index);
						}.bind(self)
					}).send();
				}
			});
		}, this);
		
		$$(this.version.cont).addEvents({
			'click:relay(a)': self.updateActions
		});
	},
	
	attachInfo: function(response, index){
		
		// get the versions container
		var verCont = $$(this.version.cont)[index];
		
		// remove previous versions
		verCont.set('html', '');
		
		// add new versions
		response.each(function(item){
			var li = new Element('li').inject(verCont);
			
			var a = new Element('a', {
				text: item.version,
				href: '#'
			}).store('version:info', item).inject(li);
		});
		
		// remove the spinner class
		verCont.removeClass('loading');
		
		// TODO: this needs some adjusting - like an arrow at the very bottom of the scrolling area
		//
		// if (response.length > 10){
		// 	verCont.setStyles({
		// 		'height': 200,
		// 		'overflow': 'hidden'
		// 	});
		// 	
		// 	new Scroller(verCont).start();
		// }
	},

	updateActions: function(e){
		e.preventDefault();
		
		// retrieve info
		var info = this.retrieve('version:info');
		var actions = this.getParent('.UI_Actions');
		
		// update the install url
		actions.getElement('.UI_Try_in_Browser a').set('href', info.install_url);
		
		// update the edit url
		actions.getElement('.UI_Edit_Version a').set('href', info.edit_url);
		
		// update version name
		actions.getElement('.UI_Pick_Version strong').set('text', info.version);
	}
});

window.addEvent('domready', function(){
	new PickVersion();
});