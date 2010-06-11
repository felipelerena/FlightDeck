// Extend FlightDeck with Bespin features

var FDBespin = new Class({
	Implements: [Options, Events],
	options: {
		validSyntaxes: ['js', 'html', 'plain']
	},
	initialize: function(element, options) {
		var self = this;
		this.setOptions(options);
		var embedded = tiki.require('Embedded');
		this.element = embedded.useBespin($(element), {syntax: 'plain'});
		$log('FD: bespin instantiated');
		// hook onChange event
		this.element._editorView.getPath('layoutManager.textStorage')
			.addDelegate(SC.Object.create({
				textStorageEdited: function() {
					self.fireEvent('change');
				}
			}));
		$log('FD: bespin onChange hooked');
		window.addEvent('resize', function() {
			self.element.dimensionsChanged();
		});
	},
	setContent: function(value) {
		this.element.set('value', value);
		return this;
	},
	getContent: function() {
		return this.element.get('value');
	},
	setSyntax: function(syntax) {
		if (!this.options.validSyntaxes.contains(syntax)) {
			if (syntax == 'css') {
				syntax = 'html'
			} else {
				if (syntax == 'json') {
					syntax = 'js'
				
				} else {
					syntax = 'plain'
				}
			}
		}
		// thanks to jviereck#bespin@irc.mozilla.org
		this.element.setPath('_editorView.layoutManager.syntaxManager.initialContext', syntax);
		return this;
	}
});

Class.refactor(FlightDeck, {
	initialize: function(options) {
		this.previous(options);
		this.editor_contents = {};
		this.current_editor = false;
		this.bespin_editor = new Element('div',{
			'text': '',
			'id': 'bespin_editor',
			'class': 'UI_Editor_Area'
		}).inject($('editor-wrapper'), 'top');
		var self = this;
		(function() {
			self.bespin = new FDBespin(self.bespin_editor);
			self.bespin.addEvent('change', function() {
				self.fireEvent('bespinChange');
			});
			self.fireEvent('bespinLoad')
		}).delay(10);
	},
	saveCurrentEditor: function() {
		if (this.current_editor) {
			this.editor_contents[this.current_editor] = this.bespin.getContent();
		}
	},
	switchBespinEditor: function(editor_id, syntax) {
		$log('FD: switching Bespin to {e} with syntax {s}'.substitute({e:editor_id, s:syntax}));
		this.saveCurrentEditor();
		this.current_editor = editor_id;
		this.bespin.setContent(this.editor_contents[editor_id]);
		this.bespin.setSyntax(syntax);
	},
	cleanBespin: function() {
		this.bespin.setContent('');
	}
});

