/*
 * Extending Flightdeck with Browser functionality 
 * loading XPI from saved objects
 */ 

FlightDeck = Class.refactor(FlightDeck,{
	options: {
		try_in_browser_class: 'XPI_test'
	},
	initialize: function(options) {
		this.setOptions(options);
		this.previous(options);
		$$('.{try_in_browser_class} a'.substitute(this.options)).each(function(el) {
			el.addEvent('click', function(e){
				e.stop();
				if (fd.alertIfNoAddOn()) {
					if (el.getParent('li').hasClass('pressed')) {
						fd.uninstallXPI(el.get('rel'));
					} else {
						new Request.JSON({
							url: el.get('href'),
							onSuccess: fd.testXPI.bind(fd)
						}).send();
					}
				}
			});
		});
	}
});
