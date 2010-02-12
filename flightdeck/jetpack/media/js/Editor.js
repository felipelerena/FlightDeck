/*
 * Class which provides basic wrapper.
 * Its functionalities should be overwritten in specific classes (Bespin.js, etc.)
 * Otherwise standard textarea will be used.
 */

var Editor = new Class({
	Implements: [Options, Events],
	options: {
		element: "version_code"
	},
	initialize: function(options) {
		this.setOptions(options);
		this.element = $(this.options.element);
	},
	toElement: function() {
		return this.element;
	},
	getCode: function() {
		return this.element.value;
	},
	setCode: function(value) {
		this.element.set('value', value);
	},
	destroy: function() {
	}
});
