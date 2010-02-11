/*
 * Class which provides basic wrapper.
 * It's functionalities should be overwritten in specific classes (Bespin.js, etc.)
 * Otherwise standard textarea will be used.
 */

var Editor = new Class({
	Implements: [Options, Events, Class.Occlude],
	options: {
		element_id: "version_code"
	},
	property: "editor",
	initialize: function(options) {
		this.setOptions(options);
		this.element = $(this.options.element_id);
		if (this.occlude()) return this.occluded;
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
