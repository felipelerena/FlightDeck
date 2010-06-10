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
				// type: '', // 'a'/'l'
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
		package_info_el: 'package-info',
		test_el: 'try_in_browser'
	},
	modules: {},
	initialize: function(options) {
		this.setOptions(options);
		this.instantiate_modules();
		$('revisions_list').addEvent('click', this.show_revision_list);

		// testing
		this.boundTestAddon = this.testAddon.bind(this);
		if (this.isAddon()) {
			this.test_url = $(this.options.test_el).get('href');
			$(this.options.test_el).addEvent('click', this.boundTestAddon)
		}
	},
	testAddon: function(e){
		if (e) e.stop();
		if (fd.alertIfNoAddOn()) {
			new Request.JSON({
				url: this.test_url,
				data: this.data || {},
				onSuccess: fd.testXPI.bind(fd)
			}).send();
		}
	},
	isAddon: function() {
		return (this.options.type == 'a');
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
	},
	show_revision_list: function(e) {
		if (e) e.stop();
		new Request({
			url: settings.revisions_list_html_url,
			onSuccess: function(html) {
				fd.displayModal(html);
			}
		}).send();
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
		active: false,
		type: 'js',
		append: false
	},
	initialize: function(options) {
		this.setOptions(options);
		if (this.options.append) {
			this.append();
		}
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
				if (e) e.preventDefault();
				// placeholder for switching editors
				fd.switchBespinEditor(this.get_editor_id(), this.options.type); 
			}.bind(this));
			if (this.options.main || this.options.executable) {
				this.trigger.getParent('li').switch_mode_on();
			} 
			if (this.options.active) {
				fd.switchBespinEditor(this.get_editor_id(), this.options.type); 
				var li = this.trigger.getParent('li')
				fd.assignModeSwitch(li);
				li.switch_mode_on();
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
	},
	append: function() {
		var html = '<a title="" href="#" class="Module_file" id="{filename}_switch">'+
						'{filename}<span class="File_status"></span>'+
						'<span class="File_close"></span>'+
					'</a>';
		var li = new Element('li',{
			'class': 'UI_File_normal',
			'html': html.substitute(this.options)
		}).inject($('add_module_div').getPrevious('ul'));
		
		var textarea = new Element('textarea', {
			'id': this.options.filename + '_textarea',
			'class': 'UI_Editor_Area',
			'name': this.options.filename + '_textarea',
			'html': this.options.code
		}).inject('editor-wrapper');
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
		this.copy_el = $(this.options.copy_el)
		if (this.copy_el) {
			this.copy_el.addEvent('click', this.copyPackage.bind(this));
		}
	},
	/*
	 * Method: showInfo
	   display a window with info about current Package
	 */
	showInfo: function(e) {
		e.stop();
		fd.displayModal(this.options.package_info);
	},
	/*
	 * Method: copyPackage
	 * create a new Package with the same name for the current user
	 */
	copyPackage: function(e) {
		e.stop();
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
			assign_library_el: 'assign_library_action',
			assign_library_input: 'library_id_number',
			add_module_el: 'add_module_action',
			add_module_input: 'add_module',

		// urls
			// save_url: '',
			// delete_url: '',
			// add_module_url: '',
			// assign_library_url: '',
		package_info_form_elements: ['version_name', 'package_description', 'revision_message']
	},
	initialize: function(options) {
		this.setOptions(options);
		// this.data is a temporary holder of the data for the submit
		this.data = {};
		this.parent(options);
		$(this.options.package_info_el).addEvent('click', this.editInfo.bind(this));
		$(this.options.save_el).addEvent('click', this.save.bind(this));
		this.boundSubmitInfo = this.submitInfo.bind(this);
		this.boundAssignLibraryAction = this.assignLibraryAction.bind(this);
		this.boundAddModuleAction = this.addModuleAction.bind(this);
		$(this.options.add_module_el).addEvent('click', 
			this.boundAddModuleAction);
		$(this.options.assign_library_el).addEvent('click',
			this.boundAssignLibraryAction);
		this.autocomplete = new FlightDeck.Autocomplete({
			'url': settings.library_autocomplete_url
		});
	},
	addModuleAction: function(e) {
		e.stop();
		// get data
		var filename = $(this.options.add_module_input).value;
		if (!filename) {
			fd.error.alert('Filename can\'t be empty', 'Please provide the name of the module');
			return;
		}
		if (this.options.modules.contains(filename)) {
			fd.error.alert('Filename has to be unique', 'You already have the module with that name');
			return;
		}
		this.addModule(filename);
	},
	addModule: function(filename) {
		new Request.JSON({
			url: this.options.add_module_url,
			data: {'filename': filename},
			onSuccess: function(response) {
				// set the redirect data to edit_url of the new revision
				fd.setURIRedirect(response.edit_url);
				// set data changed by save
				this.setUrls(response);
				fd.message.alert(response.message_title, response.message);
				// initiate new Module
				var mod = new Module({
					append: true,
					active: true,
					filename: response.filename,
					author: response.author,
					code: response.code
				});
				this.modules[response.filename] = mod;
			}.bind(this)
		}).send();
	},
	assignLibraryAction: function(e) {
		// get data
		library_id = $(this.options.assign_library_input).get('value');
		// assign Library by giving filename
		this.assignLibrary(library_id);
	},
	assignLibrary: function(library_id) {
		new Request.JSON({
			url: this.options.assign_library_url,
			data: {'id_number': library_id},
			onSuccess: function(response) {
				// set the redirect data to edit_url of the new revision
				fd.setURIRedirect(response.edit_url);
				// set data changed by save
				this.setUrls(response);
				fd.message.alert('Library assigned', response.message);
				this.appendLibrary(response);
			}.bind(this)
		}).send();
	},
	appendLibrary: function(lib) {
		var html='<a title="" href="{library_url}" target="{library_name}" class="library_link">{full_name}</a>';
		new Element('li', {
			'class': 'UI_File_Normal',
			'html': html.substitute(lib)
		}).inject($('assign_library_div').getPrevious('ul'));
	},
	editInfo: function(e) {
		e.stop();
		this.savenow = false;
		fd.editPackageInfoModal = fd.displayModal(settings.edit_package_info_template.substitute(this.data || this.options));
		$('package-info_form').addEvent('submit', this.boundSubmitInfo);
		$('savenow').addEvent('click', function() {
			this.savenow = true;
		}.bind(this));
		// XXX: hack to get the right data in the form
		$each(this.data, function(value, key) {
			if ($(key)) $(key).value = value;
		})
	},
	submitInfo: function(e) {
		e.stop();
		// collect data from the Modal
		this.options.package_info_form_elements.each(function(key) {
			this.data[key] = $(key).value;
		}, this);
		// check if save should be called
		if (this.savenow) {
			return this.save();
		}
		fd.editPackageInfoModal.destroy();
	},
	collectData: function() {
		fd.saveCurrentEditor();
		$each(this.modules, function(module, filename) {
			this.data[filename] = fd.editor_contents[filename + module.options.code_editor_suffix]
		}, this);
	},
	testAddon: function(e){
		this.collectData();
		this.data.live_data_testing = true;
		this.parent(e);
	},
	save: function(e) {
		if (e) e.stop();
		this.collectData();
		new Request.JSON({
			url: this.save_url || this.options.save_url,
			data: this.data,
			onSuccess: function(response) {
				// set the redirect data to edit_url of the new revision
				fd.setURIRedirect(response.edit_url);
				// set data changed by save
				this.setUrls(response);
				fd.message.alert(response.message_title, response.message);
				// clean data leaving package_info data
				this.data = {};
				this.options.package_info_form_elements.each(function(key) {
					if ($defined(response[key])) {
						this.data[key] = response[key]
					}
				}, this);
				if (fd.editPackageInfoModal) fd.editPackageInfoModal.destroy();
			}.bind(this)
		}).send();
	},
	setUrls: function(urls) {
		this.save_url = urls.save_url;
		this.test_url = urls.test_url;
	}
});
