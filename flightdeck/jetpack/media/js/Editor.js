/*
 * File: jetpack/Editor.js
 * Provides functionality for the Jetpack/Capability Editor
 */
/*
 * Class which provides basic wrapper.
 * Its functionalities should be overwritten in specific classes (Bespin.js, etc.)
 * Otherwise standard textarea will be used.
 */

var Editor = new Class({
	Implements: [Options, Events],
	options: {
		element: "version_content"
	},
	initialize: function(options) {
		this.setOptions(options);
		this.element = $(this.options.element);
		this.changed = false;
		this.element.addEvents({
			'change': function() {
				this.fireEvent('change');
				this.changed = true;
			}.bind(this)
		});
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
	},
	hide: function() {
		this.element.hide();
		return this;
	},
	show: function() {
		this.element.show();
		return this;
	}
});
