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
	},
	initEditor: function() {
		console.log('FD: instantiating ',this.options.element)
		this.textarea = $(this.options.element);
		var editor_id = this.textarea.get('id');
		console.log('FD: changing ', this.textarea);
		this.textarea.set('id',editor_id+'_textarea')
		console.log('FD: textarea id changed ', this.textarea.get('id'));
		this.element = new Element('div',{
			'text': this.textarea.get('text'),
			'id': editor_id,
		}).inject(this.textarea, 'before');
		console.log('FD: div element created ', this.element, 'with content ', this.element.get('text'));

		if (this.textarea.isHidden()) {
			this.element.hide();
			console.log('div hidden');
		}
		this.textarea.hide();
		console.log('FD: textarea hidden');
		this.bespin = tiki
			.require("Embedded")
			.useBespin(this.element,{syntax: "js"});
		console.log('FD: bespin instantiated');

		var boundOnBespinChange = this.onBespinChange.bind(this);
		this.bespin._editorView.getPath('layoutManager.textStorage')
			.addDelegate(SC.Object.create({
				textStorageEdited: boundOnBespinChange
			}));
		console.log('FD: bespin onChange hooked');
	},
	onBespinChange: function() {
		this.fireEvent('change');
		this.changed = true;
	},
	getContent: function() {
		this.textarea.set('text', this.bespin.value);
		return this.bespin.value;
	}
});
