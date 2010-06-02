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
			// modules: [], // a list of module filename, author pairs
		readonly: false,
		package_info_el: 'package-info'
	},
	modules: {},
	initialize: function(options) {
		this.setOptions(options);
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
				e.preventDefault();
				// placeholder for switching editors
				fd.switchBespinEditor(this.get_editor_id(), this.options.type); 
			}.bind(this));
			if (this.options.main || this.options.executable) {
				this.trigger.getParent('li').switch_mode_on();
			}
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
		readonly: true,
		copy_el: 'package-copy',
		// copy_url: '',
	},
	initialize: function(options) {
		this.setOptions(options);
		this.parent(options);
		$(this.options.package_info_el).addEvent('click', this.showInfo.bind(this));
		$(this.options.copy_el).addEvent('click', this.copyPackage.bind(this));
	},
	/*
	 * Method: showInfo
	   display a window with info about current Package
	 */
	showInfo: function() {
		$log(this.options.package_info);
		fd.displayModal(this.options.package_info);
	},
	/*
	 * Method: copyPackage
	 * create a new Package with the same name for the current user
	 */
	copyPackage: function() {
		if (!settings.user) {
			fd.alertNotAuthenticated();
			return;
		}
		new Request.JSON({
			url: this.options.copy_url,
			onSuccess: function(response) {
				window.location.href = response.edit_url;
			}
		}).send();
	}
});


Package.Edit = new Class({
	Extends: Package,
	Implements: [Options, Events],
	options: {
		// DOM elements
			save_el: 'package-save',
			menu_el: 'UI_Editor_Menu',
			add_dependency_el: 'add_dependency_action',
			add_dependency_input: 'add_dependency_input',

		// Actions
			// save_url: '',
			// 
	},
});
