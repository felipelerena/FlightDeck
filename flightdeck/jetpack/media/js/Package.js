/*
 * File: jetpack.Package.js
 */

/*
 * Javascript Package/PackageRevision representation
 */

var Package = new Class({
	// this Class should be always extended
	Implements: [Options],
	options: {
		// data
			// package specific
				// id_number: '',
				// full_name: '',
				// name: '',
				// description: '',
				// type: ''
				// package_author: '',
				// url: '',
				// license: '',
				// package_version_name: '',
				// version_url: '', // link to the current version revision
				// latest_utl: '', // link to the latest revision
			// revision specific data
				// revision_verion_name: '',
				// revision_number: '',
				// message: '', // commit message
				// dependecies: [], // list of names and urls
				// origin_url: '', // link to a revision used to created this one
				// revision_author: '',
			// modules: [] // a list of module filename, author pairs
	},
	modules: {},
	initialize: function(options) {
		this.setOptions(options);
		this.instantiate_modules();
	},
	instantiate_modules: function() {
		// iterate by modules and instantiate Module
		this.options.modules.each(function(module) {
			module.readonly = this.options.readonly;
			this.modules[module.filename] = new Module(module);
		}, this);
	}
});


var Module = new Class({
	Implements: [Options, Events],
	options: {
		// data
			// filename: '',
			// code: '',
			// author: '',
		// DOM
			code_trigger_suffix: '_switch', // id of an element which is used to switch editors
			code_editor_suffix: '_textarea', // id of the textarea
		readonly: false
	},
	initialize: function(options) {
		this.setOptions(options);
		// connect trigger with editor
		if ($(this.get_trigger_id()) && $(this.get_editor_id())) {
			this.code_id = $(this.get_editor_id());
			// connect trigger
			$(this.get_trigger_id()).addEvent('click', function(e) {
				e.stop();
				$log('switch editor');
			});
			if (!this.options.readonly) {
				// here special functionality for edit page
			}
		}
	},
	get_editor_id: function() {
		if (!this._editor_id) 
			this._editor_id = this.options.filename + this.options.code_editor_suffix;
		return this._editor_id;
	},
	get_trigger_id: function() {
		if (!this._trigger_id) 
			this._trigger_id = this.options.filename + this.options.code_trigger_suffix;
		return this._trigger_id;
	}
})


Package.View = new Class({
	Extends: Package,
	Implements: [Options, Events],
	options: {
		readonly: true
	},
	initialize: function(options) {
		this.setOptions(options);
		this.parent(options);
	}
});
/*
Package.Edit = new Class({
	Extends: Package,
	Implements: [Options, Events],
	options: {
		// DOM elements
			save_el: 'package-save',
			copy_el: 'package-copy',
			menu_el: 'UI_Editor_Menu',
			add_dependency_el: 'add_dependency_action',
			add_dependency_input: 'add_dependency_input',

		// Actions
			// save_url: '',
			// copy_url: '',
			// 
	},
});
*/
