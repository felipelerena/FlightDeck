/*
 * File: jetpack/Editor.js
 * Provides functionality for the Jetpack/Capability Editor
 */
/*
 * Class which provides basic wrapper.
 * Its functionalities should be overwritten in specific classes (Bespin.js, etc.)
 * Otherwise standard textarea will be used.
 */

var FDEditor = new Class({
	Implements: [Options, Events],
	$name: 'FlightDeckEditor',
	options: {
		// element: "main_textarea",
		activate: false,
		readonly: false
	},
	initialize: function(options) {
		this.setOptions(options);
		this.changed = false;
		this.initEditor();
	},
	initEditor: function() {
		this.element = $(this.options.element);
		var boundOnChange = this.onChange.bind(this);
		this.element.addEvents({
			'change': boundOnChange 
		});
	},
	onChange: function () {
		this.fireEvent('change');
		this.changed = true;
	},
	toElement: function() {
		return this.element;
	},
	getContent: function() {
		return this.element.value;
	},
	setContent: function(value) {
		this.element.set('value', value);
		return this;
	},
	destroy: function() {
		this.hide();
		this.element.destroy();
		this.fireEvent('destroy');
	},
	hide: function() {
		this.hidden = true;
		this.element.hide();
		this.fireEvent('hide');
		return this;
	},
	show: function() {
		this.hidden = false;
		this.element.show();
		this.fireEvent('show');
		return this;
	},
	cleanUp: $empty
});
