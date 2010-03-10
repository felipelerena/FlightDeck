/*
 * Class representing the Capability only 
 * Prepare the editor, save, update
 */

var Capability = new Class({
	Implements: [Options, Events],
	type: 'capability',
	options: {
		version: {},
		//slug: null,
		//name: null,
		//description: null,
		//creator: null,
		//managers: [],
		//developers: [],
		//public_permission: 2,
		//group_permission: 2,
		description_el: {
			element: 'capability_description',
			type: 'text'
		},
		//switch_description_id: '',
		update_el: 'update',
		version_create_el: 'version_create',
		//edit_url: '',
		//update_url: '',
		//version_create_url: '',
		menu_el: 'UI_Editor_Menu',
		is_dependency: false // was the Capability loaded as dependency?
	},
	/*
	 * Method: initialize
	 * @attribute object options: 
	 * 	
	 * initialize Version and inside of that chosen FDEditor
	 * assign actions to the buttons
	 */
	initialize: function(options) {
		this.setOptions(options)
		this.initializeVersion();
		this.instantiateEditors();

		this.listenToEvents();
		this.initializeEditorSwitches();
		
		this.data = {};
		this.data[this.type+'_name'] = this.options.name;
		this.data[this.type+'_description'] = this.options.description;
		this.data[this.type+'_slug'] = this.options.slug;
		// #TODO: remove these - it's just to switch the buttons all the time
		// this.afterVersionChanged();
		// this.afterDataChanged();
	},
	/*
	 * Method: instantiateEditors
	 */
	instantiateEditors: function() {
		// do not create an editor for the description if loaded as dependency
		this.description_el = new FDEditor(this.options.description_el).hide();
		fd.editors.push(this.description_el);
	},
	/*
	 * Method: initializeEditorSwitches
	 */
	initializeEditorSwitches: function() {
		this.switch_description_el = $(this.options.switch_description_id);
		if (this.switch_description_el) {
			this.switch_description_el.addEvent('click', this.switchToDescription.bind(this));
		}	
	},
	/*
	 * Method: switchToDescription
	 */
	switchToDescription: function(e) {
		e.preventDefault();
		fd.hideEditors();
		this.description_el.show();
	},
	createAfterBounds: function() {
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.boundAfterVersionChanged = this.afterVersionChanged.bind(this);
	},
	/*
	 * Method: listenToEvents
	 */
	listenToEvents: function() {
		this.createAfterBounds();
		this.version.addEvent('change', this.boundAfterVersionChanged);
		this.description_el.addEvent('change', this.boundAfterDataChanged);
		var switch_version_el = $('switch_to_version');
		if (switch_version_el) {
			switch_version_el.addEvent('change', function() {
				window.location.href=this.options.edit_url + 'v_' + switch_version_el.value;
			}.bind(this));
		}
	},
	/* 
	 * Method: afterVersionChanged
	 * assign version_create with the $('version_create') click event
	 */
	afterDataChanged: function() {
		$(this.options.update_el).addEvent('click', function(e) {
			e.stop();
			this.update();
		}.bind(this));
		this.description_el.removeEvent('change', this.boundAfterDataChanged);
		if (this.switch_description_el) {
			this.switch_description_el.getParent('li').addClass('UI_File_Modified');
			fd.enableMenuButtons();
		}
	},
	/* 
	 * Method: afterVersionChanged
	 * assign version_create with the $('version_create') click event
	 */
	afterVersionChanged: function() {
		// TODO: discover if change was actually an undo and there is 
		//       no change to the original content
		$(this.options.version_create_el).addEvent('click', function(e) {
			e.stop(); 
			this.version_create();
		}.bind(this));
		this.version.removeEvent('change', this.boundAfterVersionChanged);
	},
	/*
	 * Method: initializeVersion
	 * assigns CapVersion to this.version
	 */
	initializeVersion: function() {
		this.version = new CapVersion(this.options.version);
	},
	/*
	 * Method: update
	 * Prepare data and send Request to the back-end
	 */
	update: function() {
		var data = this.prepareData();
		new Request.JSON({
			url: this.options.update_url,
			data: data,
			method: 'post',
			onSuccess: function(response) {
				// display notification from response
				fd.message.alert('Success', response.message);
			}
		}).send();
	},
	/*
	 * Method: version_create
	 * Prepare data and send Request - create a new version
	 */
	version_create: function(data) {
		var data = $pick(data, this.version.prepareData());
		new Request.JSON({
			url: this.options.version_create_url,
			data: data,
			method: 'post',
			onSuccess: this.afterVersionCreated.bind(this)
		}).send();
	},
	afterVersionCreated: function(response) {
		window.location.href = response.version_absolute_url;
	},
	/*
	 * Method: getContent
	 * Wrapper for getting content from the Editor
	 */
	getContent: function() {
		return this.version.getContent();
	},
	/*
	 * Method: getVersionName
	 * Wrapper for getting Version name from options
	 */
	getVersionName: function() {
		return this.version.getName();
	},
	/*
	 * Method: prepareData
	 * Take all jetpack available data and return
	 */
	prepareData: function() {
		this.updateFromDOM();
		return this.data;
	},
	/*
	 * Method: updateFromDOM
	 * get all jetpack editable fields from DOM and set parameters in model
	 */
	updateFromDOM: function() {
		// here update metadata from its editors
		this.data[this.type+'_description'] = this.description_el.getContent();
	},
	/*
	 * Method: getFullData
	 * get all data to save Jetpack and Version models
	 */
	getFullData: function() {
		var data = $H(this.prepareData());
		data.extend(this.version.prepareData());
		return data.getClean();
	}
	
});

/*
 * Class representing the Version only 
 * Prepare the editor, save, update
 */
var CapVersion = new Class({
	Implements: [Options, Events],
	type: 'capability',
	options: {
		//commited_by: null,
		//name: null,
		//counter: null,
		//description: null,
		//content: null,
		//status: null,
		//is_base: null,
		name_el: 'version_name',
		// TODO: move to new Editor
		description_el: {
			element: 'version_description',
			type: 'text'
		},
		content_el: {
			element: 'version_content',
			type: 'js'
		},
		update_el: 'update',
		set_as_base_el: 'set_as_base',
		add_dependency_el: 'add_dependency_action',
		add_dependency_input: 'add_dependency',
		addnew_dependency_el: 'create_and_add_dependency_acton',
		// add_dependency_url: '',
		// edit_url: '',
		// update_url: '',
		// set_as_base_url: '',
		is_dependency: false
	},
	/*
	 * Method: initialize
	 * instantiate Editor
	 */
	initialize: function(options) {
		this.capabilities = $H({});
		this.setOptions(options);
		this.switch_content_el = $(this.options.switch_content_id);
		this.switch_description_el = $(this.options.switch_description_id);
		this.instantiateEditors();
		this.listenToEvents();
		this.initializeEditorSwitches();

		// this.data is everything we send to the backend
		this.data = $H({
			version_content: this.options.content,
			version_name: this.options.name,
			version_description: this.options.description,
			version_counter: this.options.counter
		});
		// set as base functionality
		if (!this.options.is_base) {
			this.set_as_base_el = $(this.options.set_as_base_el);
			this.set_as_base_el.addEvent('click', function(e) {
				e.stop();
				this.setAsBase();
			}.bind(this));
		}
	},
	/*
	 * Method: instantiateEditors
	 */
	instantiateEditors: function() {
		this.content_el = new FDEditor(this.options.content_el);
		fd.editors.push(this.content_el);
		this.name_el = $(this.options.name_el);
		this.description_el = new FDEditor(this.options.description_el).hide();
		fd.editors.push(this.description_el);
	},
	/*
	 * Method: initializeEditorSwitches
	 */
	initializeEditorSwitches: function() {
		if (this.switch_content_el) {
			this.switch_content_el.addEvent('click', this.switchToContent.bind(this));
		}
		if (this.switch_description_el) {
			this.switch_description_el.addEvent('click', this.switchToDescription.bind(this));
		}	
	},
	/*
	 * Method: switchToContent
	 */
	switchToContent: function(e) {
		e.preventDefault();
		fd.hideEditors();
		this.content_el.show();
	},
	/*
	 * Method: switchToDescription
	 */
	switchToDescription: function(e) {
		e.preventDefault();
		fd.hideEditors();
		this.description_el.show();
	},
	/*
	 * Method: listenToCapabilityEvents
	 */
	listenToEvents: function() {		
		this.changed = false;
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.name_el.addEvent('change', this.boundAfterDataChanged);
		this.description_el.addEvent('change', this.boundAfterDataChanged);
		this.description_el.addEvent('change', function() {
			if (this.switch_description_el) {
				this.switch_description_el.getParent('li').addClass('UI_File_Modified');
			}
		}.bind(this));
		this.content_el.addEvent('change', this.boundAfterDataChanged);
		this.content_el.addEvent('change', function() {
			if (this.switch_content_el) {
				this.switch_content_el.getParent('li').addClass('UI_File_Modified');
			}
		}.bind(this));
		// adding dependencies
		var add_dependency_action = $(this.options.add_dependency_el);
		if (add_dependency_action) {
			add_dependency_action.addEvent('click', function(e) {
				e.stop();
				this.addDependencyFromInput();
			}.bind(this));
		}
		var addnew_dependency_action = $(this.options.addnew_dependency_el);
		console.log ( addnew_dependency_action, this.options.addnew_dependency_el);
		if (addnew_dependency_action) {
			addnew_dependency_action.addEvent('click', function(e) {
				e.stop();
				this.displayAddNewDependencyWindow();
			}.bind(this));
		}
	},
	displayAddNewDependencyWindow: function() {
			fd.addnewDependencyModal = fd.displayModal(this.options.addnew_dependency_template);
			$('addnew_dependency_form').addEvent('submit', function(e) { 
				e.stop();
				var data = {};
				data['capability_name'] = $('create-name').get('value');
				data['capability_description'] = $('create-description').get('value');
				new Request.JSON({
					url: this.options.addnew_dependency_url,
					data: data,
					method: 'post',
					onSuccess: function(response) {
						fd.message.alert('Success',response.message);
						this.createDependency(response.dependency, true);
						this.fireEvent('change');
						fd.addnewDependencyModal.hide();
						fd.addnewDependencyModal = null;
					}.bind(this)
				}).send();
				return false;
			}.bind(this));
	},
	/*
	 * Method: addDependencyFromInput
	 */
	addDependencyFromInput: function() {
		dependency_slug = $(this.options.add_dependency_input).get('value');
		// TODO: some validation
		if (this.capabilities[dependency_slug]) {
			fd.error.alert('Not Allowed', 'You may not add the same dependency again');
			return false;
		}
		// TODO: add not base version 
		new Request.JSON({
			url: this.options.add_dependency_url,
			method: 'post',
			data: {'dependency_slug': dependency_slug},
			onSuccess: function(response) {
				fd.message.alert('Success',response.message);
				this.createDependency(response.dependency, true);
				this.fireEvent('change');
			}.bind(this)
		}).send();
	},
	/*
	 * Method: addDependency
	 */
	addDependency: 	function(options){
		var dep = new CapDependency(options);
		this.registerDependency(dep);
	},
	registerDependency: function(dep) {
		var slug = dep.options.slug;
		dep.addEvent('remove', function() { 
			// TODO: Why this is not working?
			this.removeDependency(slug);
		}.bind(this));
		this.capabilities[slug] = dep;
	},
	/*
	 * Method: removeDependency
	 */
	removeDependency: function(slug) {
		this.capabilities.erase(slug);
	},
	/*
	 * Method: createDependency
	 * add dependency and create whole DOM structure if needed
	 */
	createDependency: function(options, create_elements) {
		if (create_elements) {
			// create whole DOM (code and triggers)
			Elements.from(options.dependency_link_html)
				.inject($('dependency_list_container'), 'bottom');
			Elements.from(options.dependency_textarea_html)
				.inject($('editor-wrapper'), 'bottom');
			$(options.version.content_el.element).hide();
		}
		this.addDependency(options);
	},
	afterDataChanged: function() {
		// TODO: discover if change was actually an undo and there is 
		//       no change to the original content
		this.changed = true;
		fd.enableMenuButtons();
		$(this.options.update_el).addEvent('click', function(e) {
			e.stop();
			this.update();
		}.bind(this));
		this.content_el.removeEvent('change', this.boundAfterDataChanged);
		this.description_el.removeEvent('change', this.boundAfterDataChanged);
		this.fireEvent('change');
	},
	/*
	 * Method: setAsBase
	 * set current version as Base
	 */
	setAsBase: function() {
		new Request.JSON({
			url: this.options.set_as_base_url,
			method: 'post',
			onSuccess: function(response) {
				fd.message.alert('Success', response.message);
				this.set_as_base_el.set('text', 'Base version')
			}.bind(this)
		}).send()
	},
	/*
	 * Method: update
	 * get current data and send Request to the backend
	 */
	update: function() {
		var data = this.prepareData();
		// prevent from updating a version with different name
		if (data.version_name && data.version_name != this.options.name) {
			return item.version_create(data);
		}
		new Request.JSON({
			url: this.options.update_url,
			data: data,
			method: 'post',
			onSuccess: function(response) {
				fd.message.alert('Success', response.message);
			}
		}).send();
	},
	/*
	 * Method: getContent
	 * Wrapper for getting content from the FDEditor
	 */
	getContent: function() {
		return this.content_el.getContent();
	},
	/*
	 * Method: getName
	 * Wrapper for getting Version name from options
	 */
	getName: function() {
		return this.options.name
	},
	/*
	 * Method: prepareData
	 * Prepare all version specific available data
	 */
	prepareData: function() {
		this.updateFromDOM();
		// prepare capability info
		var get_data = function(cap) {
			return cap.prepareData();
		}
		this.data['capabilities'] = JSON.encode($H(this.capabilities).getValues().map(get_data));
		return this.data;
	},
	/*
	 * Method: updateFromDOM
	 * get all version editable fields from DOM and set parameters in model
	 */
	updateFromDOM: function() {
		this.data.version_name = this.name_el.get('value');
		this.data.version_description = this.description_el.getContent();
		this.data.version_content = this.content_el.getContent();
	}
});

