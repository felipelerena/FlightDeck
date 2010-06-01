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
		file_selected_class: 'UI_File_Selected',
		file_normal_class: 'UI_File_Normal',
		file_listing_class: 'UI_File_Listing'
	},
	modules: {},
	initialize: function(options) {
		this.setOptions(options);
		var file_selected_class = this.options.file_selected_class;
		var file_normal_class = this.options.file_normal_class;
		var switch_mode_on  = function() {
			$$('.' + file_selected_class).each(function(el) {
				el.switch_mode_off();
			});
			this.removeClass(file_normal_class)
				.addClass(file_selected_class);
		};
		var switch_mode_off = function() {
			this.removeClass(file_selected_class)
				.addClass(file_normal_class);
		};
		$$('.'+this.options.file_listing_class + ' li').each(function(file_el) {
			file_el.switch_mode_on = switch_mode_on;
			file_el.switch_mode_off = switch_mode_off;
		});
		$$('.'+this.options.file_listing_class).each(function(container) { 
			container.addEvent('click:relay(li a)', function(e, el) {
				var li = $(el).getParent('li');
				if (!li.switch_mode_on) li.switch_mode_on = switch_mode_on;
				if (!li.switch_mode_off) li.switch_mode_off = switch_mode_off;
				li.switch_mode_on();
			});
		});
		this.instantiate_modules();
	},
	instantiate_modules: function() {
		// iterate by modules and instantiate Module
		var main_module;
		this.options.modules.each(function(module) {
			module.readonly = this.options.readonly;
			if (!main_module) {
				module.main = true;
				main_module = module;
			}
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
		readonly: false,
		main: false,
		executable: false,
		type: 'js'
	},
	initialize: function(options) {
		this.setOptions(options);
		// connect trigger with editor
		if ($(this.get_trigger_id()) && $(this.get_editor_id())) {
			this.textarea = $(this.get_editor_id());
			this.trigger = $(this.get_trigger_id());
			this.editor = new FDEditor({
				element: this.get_editor_id(),
				activate: this.options.main || this.options.executable,
				type: this.options.type,
				readonly: this.options.readonly
			});
			// connect trigger
			this.trigger.addEvent('click', function(e) {
				e.stop();
				// placeholder for switching editors
				fd.switchBespinEditor(this.get_editor_id(), this.options.type); 
			}.bind(this));
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
