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
		this.uri = new URI();
		if (this.uri.getData('redirect','fragment')) {
			window.location.href = this.uri.getData('redirect', 'fragment');
		}
		this.warning = this.error = this.message = {
			'alert': function(title, message) {
				alert(title+"\n"+message);
			}
		};
		this.editors = [];
		this.parseTooltips();
		this.createActionSections();
		this.parseTestButtons.bind(this).delay(10);
		this.addEvent('xpi_installed', this.whenXpiInstalled);
		this.addEvent('xpi_uninstalled', this.whenXpiUninstalled);
	},

	parseTooltips: function() {
		this.tips = new Tips({
			fixed: false,
			className: 'UI_tooltip',
			offset: {
				x: 0,
				y: 16
			}
		});
		
		$$('div.UI_tooltip_source').each(function(tipSource){
			tipSource.hide();
			var target = $(tipSource.get('data-tooltip-for'));
			target.set('title', '');
			target.store('tip:title', tipSource.get('data-tooltip-title'));
			target.store('tip:text', tipSource.get('html'));
			this.tips.attach(target);
		}, this);
	},

	setURIRedirect: function(url) {
		// change the URL add #/path/to/saved/revision
		if (this.uri.get('directory') != url) {
			this.uri.setData({'redirect': url}, false, 'fragment');
			this.uri.go();
		}
	},

	whenXpiInstalled: function() {
		this.parseTestButtons();
		this.message.alert('Add-ons Builder', 'Add-on installed');
		// remove SDK from disk
		if (this.rm_xpi_url) {
			new Request.JSON({
				url: this.rm_xpi_url,
				onSuccess: function() {
					this.fireEvent('sdk_removed');
				}.bind(this)
			}).send();
			this.rm_xpi_url = undefined;
		}
	},

	whenXpiUninstalled: function() {
		this.parseTestButtons();
		this.message.alert('Add-ons Builder', 'Add-on uninstalled');
	},

	parseTestButtons: function() {
		var installed = (this.isAddonInstalled()) ? this.isXpiInstalled() : false;
		if (installed) {
			$$('.{try_in_browser_class} a'.substitute(this.options)).each(function(test_button){
				if (installed && installed.installedID == test_button.get('rel')) {
					test_button.getParent('li').addClass('pressed');
				} else {
					test_button.getParent('li').removeClass('pressed');
				}
			}, this);
		}
	},

	/*
	 * Method: testXPI
	 */
	testXPI: function(response) {
		if (response.stderr) {
			fd.error.alert('Error in building Add-on XPI', response.stderr);
			return;
		}
		this.rm_xpi_url = response.rm_xpi_url;
		this.installXPI(response.test_xpi_url);
	},

	isXpiInstalled: function() {
		return window.mozFlightDeck.send({cmd:'isInstalled'});
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
			new Request({
				url: url,
				headers: {'Content-Type': 'text/plain; charset=x-user-defined'},
				onSuccess: function(responseText) {
					$log('FD: installing ' + url);
					var result = window.mozFlightDeck.send({cmd: "install", contents: responseText});
					if (result && result.success) {
						this.fireEvent('xpi_installed');
					} else {
						this.warning.alert(
							'Add-ons Builder', 
							'Wrong response from Add-ons Helper. Please <a href="https://bugzilla.mozilla.org/show_bug.cgi?id=573778">let us know</a>'
						);
					}
				}.bind(this)
			}).send();
		}
	},
	uninstallXPI: function(jid) {
		$log('FD: uninstalling ' + jid);
		var result = window.mozFlightDeck.send({cmd:'uninstall'});
		if (result.success) this.fireEvent('xpi_uninstalled');
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

	isAddonInstalled: function() {
		return (window.mozFlightDeck) ? true : false;
	},

	/*
	 * Method: alertIfNoAddOn
	 */
	alertIfNoAddOn: function(text, title) {
		if (this.isAddonInstalled()) return true;
		text = $pick(text, "To test this add-on, please install the <a href='{addons_helper}'>Add-ons Builder Helper add-on</a>".substitute(settings));
		title = $pick(title, "Install Add-ons Builder Helper");
		fd.warning.alert(title, text);
		return false;
	},
	/*
	 * Method: createActionSections
	 */	
	createActionSections: function(){
		$$('.UI_Editor_Menu_Separator').each(function(separator){
			separator.getPrevious('li').addClass('UI_Section_Close');
			separator.getNext('li').addClass('UI_Section_Open');
		});
		
		var UI_Editor_Menu_Button = $$('.UI_Editor_Menu_Button');

		if (UI_Editor_Menu_Button.length === 1){
			UI_Editor_Menu_Button[0].addClass('UI_Single');
		}
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
	This wasn't working
window.addEvent('load', function() {
	if (window.mozFlightDeck) {
		window.mozFlightDeck.whenMessaged(function(data) {
			// This gets called when one of our extensions has been installed
			// successfully, or failed somehow.
			fd.message.alert('Add-ons Builder', 'Add-on {msg}'.substitute(data));
			// log to console result of isInstalled command
			$log('sending isInstalled to window.mozFlightDeck');
			$log(fd.isXpiInstalled());
		});
	}
});
 */
