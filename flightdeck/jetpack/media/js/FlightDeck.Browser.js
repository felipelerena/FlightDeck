/*
 * Extending Flightdeck with Browser functionality 
 */

FlightDeck = Class.refactor(FlightDeck,{
	options: {
		try_in_browser_class: 'UI_Try_in_Browser'
	},
	initialize: function(options) {
		this.setOptions(options);
		this.previous(options);
		$$('.{try_in_browser_class} a'.substitute(this.options)).each(function(el) {
			el.addEvent('click', function(e){
				e.stop();
				if (fd.alertIfNoAddOn()) {
					new Request.JSON({
						url: el.get('href'),
						onSuccess: function(response) {
							if (response.stderr) {
								fd.error.alert('Error',response.stderr);
								return;
							}
							// now call the add-on
							fd.install_xpi(response.get_xpi_url);
						}
					}).send();
				}
			});
		});
	},
	install_xpi: function(url) {
		if (fd.alertIfNoAddOn()) {
			window.mozFlightDeck.send({cmd: "install", path: url});
		}
	}
});
