/*
 * Bespin wrapper
 */

Class.refactor(Editor, {
	options: {
		version: 0.5
	},
	initialize: function(options) {
		this.previous(options);
		if (this.options.version < 0.6) {
			this.embed = tiki.require("bespin:embed");
		} else {
			this.embed = tiki.require("Embedded");
		}	
		this.embed.useBespin(this.element);
		this.element.addClass("bespin");
	},
});
