/* 
 * File: Flightdeck.PickVersion.js
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
		var parent = this;
		
		$$(this.version.trigger).each(function(trigger, index){
			trigger.getElement('a').addEvents({
				click: function(e){
					e.preventDefault();
					
					new Request.JSON({
						url: this.get('href'),
						onComplete: function(response){
							
							// get the versions container
							var verCont = $$(parent.version.cont)[index];
							
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
						}.bind(this)
					}).send();
				}
			});
		}, this);
		
		$$(this.version.cont).addEvents({
			'click:relay(a)': parent.updateActions
		});
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