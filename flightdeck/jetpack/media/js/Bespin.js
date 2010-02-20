/*
 * Inspired from http://github.com/jeresig/sizzle/commit/7631f9c3f85e5fa72ac51532399cb593c2cdc71f
 * and this http://github.com/jeresig/sizzle/commit/5716360040a440041da19823964f96d025ca734b
 * and then http://dev.jquery.com/ticket/4512
 */

Element.implement({

	isHidden: function(){
		var w = this.offsetWidth, h = this.offsetHeight,
		force = (this.tagName.toLowerCase() === 'tr');
		return (w===0 && h===0 && !force) ? true : (w!==0 && h!==0 && !force) ? false : this.getStyle('display') === 'none';
	},

	isVisible: function(){
		return !this.isHidden();
	}

});


/*
 * Bespin wrapper
 */

Class.refactor(Editor, {
	options: {
		version: 0.6
	},
	initialize: function(options) {
		this.previous(options);
		if (this.options.version < 0.6) {
			this.embed = tiki.require("bespin:embed");
		} else {
			this.embed = tiki.require("Embedded");
		}	
		this.textarea = this.element;
		this.element = new Element('div',{
			'text': this.element.get('text'),
			'id': this.element.get('id'),
			'class': 'bespin' 
		});
		this.textarea.set('id',this.textarea.get('id')+'_textarea')
		this.element.inject(this.textarea, 'after');
		if (this.textarea.isHidden()) {
			this.element.hide();
		}
		this.textarea.hide();

		this.embed.useBespin(this.element);
		this.element.addClass("bespin");
	},
	getContent: function() {
		this.textarea.set('text', this.element.value);
		return this.element.value;
	}
});
