/*
 * Bespin wrapper
 */

/*
 * Class: CodeMirror.js
 * Extension for Editor to use CodeMirror
 */

Class.refactor(FDEditor, {
	options: {
		type: null,
		version: '0.6.2'
	},
	initialize: function(options) {
		this.previous(options);
	},
	initEditor: function() {
		$log('FD: instantiating ',this.options.element)
		this.element = $(this.options.element);
		this.editor = new Element('div',{
			'text': this.element.get('text'),
			'id': this.element.get('id') + '_bespin',
			'class': 'UI_Editor_Area'
		}).inject(this.element, 'before');
		$log('FD: div element created ', this.editor, 'with content ', this.editor.get('text'));

		if (this.element.isHidden()) {
			this.editor.hide();
			this.hidden = true;
			$log('div hidden');
		}
		this.element.hide();
		$log('FD: textarea hidden');
		(function() {
			this.bespin = tiki
				.require("Embedded")
				.useBespin(this.editor, {syntax: this.options.type});
			$log('FD: bespin instantiated');

			var boundOnBespinChange = this.onBespinChange.bind(this);
			this.bespin._editorView.getPath('layoutManager.textStorage')
				.addDelegate(SC.Object.create({
					textStorageEdited: boundOnBespinChange
				}));
			$log('FD: bespin onChange hooked');
		}.bind(this)).delay(10);
	},
	onBespinChange: function() {
		this.fireEvent('change');
		this.changed = true;
	},
	getContent: function() {
		// this.textarea.set('text', this.bespin.value);
		return this.bespin.value;
	},
	setContent: function(value) {
		this.previous(value);	
		// TODO: set in Bespin
	},
	
	hide: function() {
		this.editor.hide();
		return this;
	},
	destroy: function() {
		this.editor.destroy();
	},
	show: function() {
		this.editor.show();
		this.editor.getChildren().each(function(content) {
			$log('show', content);
			content.show();
		});
		return this;
	},
	cleanUp: $empty
});
