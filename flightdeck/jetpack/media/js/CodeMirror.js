/*
 * File: jetpack/CodeMirror.js
 */

/*
 * Class: CodeMirror.js
 * Extension for Editor to use CodeMirror
 */

Class.refactor(Editor, {
	options: {
		type: null,
		codeMirror: {
			lineNumbers: false,
			autoMatchParens: true,
			indentUnit: 4,
			tabMode: 'shift',
			height: '',
			path: '/media/codemirror/js/',
			stylesheet: []
		}
	},
	initialize: function(options) {
		this.previous(options);
	},
	initEditor: function() {
		if (this.options.type == 'js' || this.options.type == 'json') {
			this.options.codeMirror.parserfile = [
				"tokenizejavascript.js", 
				"parsejavascript.js"
			];
			this.options.codeMirror.stylesheet = '/media/jetpack/css/codemirror/jscolors.css';
		} else if (this.options.type == 'css') {
			this.options.codeMirror.parserfile = ["parsecss.js"];
			this.options.codeMirror.stylesheet = '/media/jetpack/css/codemirror/csscolors.css';
		} else { // text
			this.options.codeMirror.parserfile = ["parsedummy.js"];
			this.options.codeMirror.stylesheet = '/media/jetpack/css/codemirror/textcolors.css';
		}

		this.element = $(this.options.element);
		$log(this.options.element);
		if (this.element.isHidden()) {
			this.hidden = true;
		}
		// hook to the onChange event
		// this has some delay
		if (!this.options.codeMirror.onChange) {
			this.options.codeMirror.onChange = this.onCodeMirrorChange.bind(this);
		}
		// instantiate editor
		this.editor = CodeMirror.fromTextArea(this.element, this.options.codeMirror);
		// fix codemirror focus
		if (! this.editor.editor) this.editor.editor = {};
		// hide if textarea was hidden
		if (this.hidden) {
			this.hide();
		} else {
			this.editor.focus();
		}
	},
	onCodeMirrorChange: function() {
		this.changed = true;
		this.fireEvent('change');
	},
	getContent: function() {
		return this.editor.getCode();
	},
	hide: function() {
		this.editor.wrapping.hide();
		return this;
	},
	show: function() {
		this.editor.wrapping.show();
		return this;
	},
	getWindow: function() {
		// return CodeMirror window
		if (!this._window) {
			this._window = this.element.getParent('.window');
		}
		return this._window || this.element;
	}
});
