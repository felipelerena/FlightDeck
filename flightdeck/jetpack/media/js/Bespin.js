/*
 * Bespin wrapper
 */

Class.refactor(FDEditor, {
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
			'class': 'UI_Editor_Area'
		}).inject(this.textarea, 'before');
		console.log('FD: div element created ', this.element, 'with content ', this.element.get('text'));

		if (this.textarea.isHidden()) {
			this.element.hide();
			this.hidden = true;
			console.log('div hidden');
		}
		this.textarea.hide();
		console.log('FD: textarea hidden');
		(function() {
			this.bespin = tiki
				.require("Embedded")
				.useBespin(this.element, {syntax: "js"});
			console.log('FD: bespin instantiated');

			var boundOnBespinChange = this.onBespinChange.bind(this);
			this.bespin._editorView.getPath('layoutManager.textStorage')
				.addDelegate(SC.Object.create({
					textStorageEdited: boundOnBespinChange
				}));
			console.log('FD: bespin onChange hooked');
		}.bind(this)).delay(10);
	},
	onBespinChange: function() {
		this.fireEvent('change');
		this.changed = true;
	},
	getContent: function() {
		this.textarea.set('text', this.bespin.value);
		return this.bespin.value;
	},
	hide: function() {
		this.element.hide();
		return this;
	},
	show: function() {
		this.element.show();
		this.element.getChildren().each(function(content) {
			console.log('show', content);
			content.show();
		});
		return this;
	}
});
