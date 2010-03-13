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
				new Request.JSON({
					url: el.get('href'),
					onSuccess: function(response) {
						if (response.stderr) {
							fd.error.alert('Error',response.stderr);
							return;
						}
						// now call the add-on
						this.install_xpi(response.get_xpi_url);
					}.bind(this)
				}).send();
			});
		}, this);
	},
	install_xpi: function(url) {
		window.mozFlightDeck.send({cmd: "install", path: url});
	}
});

window.addEvent('load', function() {
	window.mozFlightDeck.whenMessaged(function(data) {
		// This gets called when one of our extensions has been installed
		// successfully, or failed somehow.
		fd.message.alert('Loading extension', 'Extension {msg}'.substitute(data));
	});
});
