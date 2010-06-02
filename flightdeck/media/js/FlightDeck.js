/*
 * Class: FlightDeck
 * Initializes all needed functionality
 */

var FlightDeck = new Class({
	Implements: [Options, Events],
	options: {
		menu_el: 'UI_Editor_Menu',
		try_in_browser_class: 'XPI_test'
		//user: ''
	},
	initialize: function() {
		this.warning = this.error = this.message = {
			'alert': function(title, message) {
				alert(title+"\n"+message);
			}
		};
		this.editors = [];
		// loading XPI from saved objects
		$$('.{try_in_browser_class} a'.substitute(this.options)).each(function(el) {
			el.addEvent('click', function(e) {
				e.stop();
				if (fd.alertIfNoAddOn()) {
					new Request.JSON({
						url: this.get('href'),
						onSuccess: fd.testXPI.bind(fd)
					}).send();
				}
			});
		});
		this.tips = new Tips({
			fixed: true,
			className: 'tooltip'
		});
		$$('label.tip').each(function(tip){
			tip.hide();
			var target = $(tip.get('for'));
			target.store('tip:title', tip.get('title'));
			target.store('tip:text', tip.get('html'));
			this.tips.attach(target);
		}, this);
	},
	/*
	 * Method: testXPI
	 */
	testXPI: function(response) {
		if (response.stderr) {
			fd.alert('Error in building Add-on XPI', response.stderr);
			return;
		}
		this.rm_xpi_url = response.rm_xpi_url;
		this.installXPI(response.test_xpi_url);
	},
	/*
	 * Method: hideEditors
	 */
	hideEditors: function() {
		this.editors.each(function(ed){ ed.hide(); });
	},
	/*
	 * Method: installXPI
	 */
	installXPI: function(url) {
		if (fd.alertIfNoAddOn()) {
			window.mozFlightDeck.send({cmd: "install", path: url});
		}
	},
	/*
	 * Method: enableMenuButtons
	 */
	enableMenuButtons: function() {
		$$('.' + this.options.menu_el + ' li').each(function(menuItem){
			if (menuItem.hasClass('disabled')){
				menuItem.removeClass('disabled');
			}
		});
	},
	/*
	 * Method: alertIfNoAddOn
	 */
	alertIfNoAddOn: function(text, title) {
		if (window.mozFlightDeck) return true;
		text = $pick(text, "Please install <a href='https://secure.toolness.com/xpi/flightdeck.xpi'>FlightDeck Add On</a>");
		title = $pick(title, "Add on not installed");
		fd.warning.alert(title, text);
		return false;
	}
});


/*
 * Default onFailure in all Requests
 */

Request = Class.refactor(Request, {
	options: {
		onFailure: function(xhr) {
			fd.error.alert(
				'Error {status}'.substitute(xhr), 
				'{statusText}<br/>{responseText}'.substitute(xhr)
				);
		}
	}
});


/*
 * Inspired by
 * http://github.com/jeresig/sizzle/commit/7631f9c3f85e5fa72ac51532399cb593c2cdc71f
 * and this http://github.com/jeresig/sizzle/commit/5716360040a440041da19823964f96d025ca734b
 * and then http://dev.jquery.com/ticket/4512
 */

Element.implement({

	isHidden: function(){
		var w = this.offsetWidth, h = this.offsetHeight,
		force = (this.tagName.toLowerCase() === 'tr');
		return (w===0 && h===0 && !force) 
			? true 
			: (w!==0 && h!==0 && !force) ? false : this.getStyle('display') === 'none';
	},
	isVisible: function(){
		return !this.isHidden();
	},
	getSiblings: function(match,nocache) {
		return this.getParent().getChildren(match,nocache).erase(this);
	}

});

/*
	Add $name mutator - specifies the type of the created Class
	Usage:
		var C = new Class({$name = 'sometype', inititate: function() {}});
		var c = new C();
		alert($type(c)); // 'sometype'
 */
Class.Mutators.$name = function(name){ this.implement('$family', {name: name}); };


/*
	Listen to an event fired when Extension is installed
 */
window.addEvent('load', function() {
	if (fd.alertIfNoAddOn()) {
		window.mozFlightDeck.whenMessaged(function(data) {
			// This gets called when one of our extensions has been installed
			// successfully, or failed somehow.
			fd.message.alert('Addon-builder', 'Add-on {msg}'.substitute(data));
		});
	}
});
