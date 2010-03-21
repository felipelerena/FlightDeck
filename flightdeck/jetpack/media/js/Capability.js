/*
 * File: jetpack/Capability.js
 */

/*
 * 	Update algorithm
	c = new Capability(...)
	c.update()
		get data from the form
		update MetaData from c.data
			onSuccess 
				mark updated
				fire 'update' event
		call c.version.update()
			c.addEvent('update', c.boundAfterUpdate)
			this.addEvent('update', c.boundAfterUpdate)
			update c.version.data
				onSuccess 
					mark updated
					fire 'update' event
		foreach dep from c.changed_dependencies
			if dep.method is 'update'
				dep.addEvent('update', c.boundUpdateAfterDepSave)
				dep.update
					onSuccess
						fire 'update' event
			elif dep.method is 'new_version'
				dep.addEvent('new_version', c.boundUpdateAfterDepSave)
				dep.save_new_version('update')
					onSuccess
						fire 'new_version' event
						dep.reload

	c.updateAfterDepSave
		stop listening to event
		remove from c.changed_dependencies
		if empty c.changed_dependencies
			call c.afterUpdate

	c.afterUpdate
		if c.updated and c.version.updated and no changed_dependencies
			stop listening to events
			message 'updated'
 */

/*
 *	Save New Version algorithm
	c = new Capability(...)
	c.save_new_version()
		get data from the form
		update MetaData from c.data
			onSuccess
				mark updated
				fire 'update' event
		call c.new_version
			c.addEvent('update' c.boundAfterSaveNewVersion)
			c.addEvent('new_version', c.boundAfterSaveNewVersion)
			get version data
			save new version
				onSuccess
					save new url
					if not c.changed_dependencies
						fire 'new_version' event
					foreach dep from c.changed_dependencies
						if dep.method is 'update'
							dep.addEvent('update', c.boundNewVersionAfterDepSave)
							dep.update
								onSuccess
									fire 'update' event
						elif dep.method is 'new_version'
							dep.addEvent('new_version', c.boundNewVersionAfterDepSave)
							dep.save_new_version('update')
								onSuccess
									fire 'new_version' event
							
	c.newVersionAfterDepSave
		stop listening to event
		remove from c.changed_dependencies
		if empty c.changed_dependencies
			call c.afterNewVersion
	
	c.afterNewVersion
		if c.updated
			reload the page to the saved new url
 */
		
				

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
		// add_dependency_url: '',
		add_dependency_el: 'add_dependency_action',
		add_dependency_input: 'add_dependency',
		// addnew_dependency_template: '',
		addnew_dependency_el: 'create_and_add_dependency_action'
	},
	/*
	 * Method: initialize
	 * @attribute object options: 
	 * 	
	 * initialize Version and inside of that chosen FDEditor
	 * assign actions to the buttons
	 */
	initialize: function(options) {
		this.dependencies = $H({});
		this.changed_dependencies = $H({});

		this.setOptions(options);
		this.initializeVersion();
		this.instantiateEditors();

		this.createBounds();
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
	 * Method: initializeVersion
	 * assigns CapVersion to this.version
	 */
	initializeVersion: function() {
		var self = this;
		this.version = new CapVersion(this.options.version);
		this.version.get_item = function() {return self;};
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
	 * save Bound functions
	 */
	createBounds: function() {
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.boundAfterVersionChanged = this.afterVersionChanged.bind(this);
		// update bounds
		this.boundAfterUpdate = this.afterUpdate.bind(this);
		this.boundUpdateAfterDepSave = this.updateAfterDepSave.bind(this);
		// new version bounds
		this.boundAfterNewVersion = this.afterNewVersion.bind(this);
		this.boundNewVersionAfterDepSave = this.newVersionAfterDepSave.bind(this);
	},
	/*
	 * Method: listenToEvents
	 */
	listenToEvents: function() {
		// change events
		var self = this;
		this.version.addEvent('change', this.boundAfterVersionChanged);
		this.description_el.addEvent('change', this.boundAfterDataChanged);
		// switch to version is a select box
		var switch_version_el = $('switch_to_version');
		if (switch_version_el) {
			switch_version_el.addEvent('change', function() {
				// TODO: change value of option in _edit_item_info.html to get_absolute_url
				//		 then use the url here directly
				window.location.href = self.options.edit_url + 'v_' + switch_version_el.value;
			});
		}
		// editor menu actions
		$(this.options.update_el).addEvent('click', function(e) {
			e.stop();
			self.update();
		});
		$(this.options.version_create_el).addEvent('click', function(e) {
			e.stop(); 
			self.new_version();
		});
		// adding dependencies
		var add_dependency_action = $(this.options.add_dependency_el);
		if (add_dependency_action) {
			add_dependency_action.addEvent('click', function(e) {
				e.stop();
				self.addDependencyFromInput();
			});
		}
		// TODO: change this to handle radio button
		var addnew_dependency_action = $(this.options.addnew_dependency_el);
		if (addnew_dependency_action) {
			addnew_dependency_action.addEvent('click', function(e) {
				e.stop();
				self.displayAddNewDependencyWindow();
			});
		}
	},
	markChanged: function() {
		this.changed = true;
		this.fireEvent('change');
	},
	/* 
	 * Method: afterDataChanged
	 */
	afterDataChanged: function() {
		this.markChanged();
		this.description_el.removeEvent('change', this.boundAfterDataChanged);
		// Mark description as changed (this is the only editable field of the Capability)
		if (this.switch_description_el) {
			this.switch_description_el.getParent('li').addClass('UI_File_Modified');
		}
	},
	/* 
	 * Method: afterVersionChanged
	 */
	afterVersionChanged: function() {
		this.markChanged();
		this.version.removeEvent('change', this.boundAfterVersionChanged);
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
	saveDependencies: function(callback, version_identification) {
		this.changed_dependencies.each(function(dep) {
			// dep.method may be 'update' or 'new_version'
			// setting it to anything else will prevent from saving
			if (['update', 'new_version'].contains(dep.method)) {
				dep.obj.addEvent(dep.method, callback);
				dep.obj[dep.method](version_identification);
			}
		});
	},
	/*
	 * Method: update
	 * Prepare data and send Request to the back-end
	 */
	update: function() {
		this.updated = false;
		if (this.options.creator == fd.options.user) {
			this.addEvent('part_update', this.boundAfterUpdate);
			new Request.JSON({
				url: this.options.update_url,
				data: this.prepareData(),
				method: 'post',
				onSuccess: function(response) {
					//fd.message.alert('DEBUG:', response.message);
					// save the message
					this.update_message = response.message;
					this.updated = true;
					this.fireEvent('part_update');
				}.bind(this)
			}).send();
		} else {
			// can't be updated
			// TODO: fix in next iteration
			this.updated = true;
		}
		if (this.version.author == fd.options.user) {
			this.version.addEvent('update', this.boundAfterUpdate);
			this.version.update();
		} else {
			// can't be updated
			// TODO: fix in next iteration
			this.updated = true;
			if (this.version.changed) {
				fd.warning.alert(
					'{type} couldn\'t be updated'.substitute(this.options),
					'Not enough priviliges. Try Save New Version'
				);
			}
		}
		this.saveDependencies(this.boundUpdateAfterDepSave, this.version.getIdentification());
	},
	afterUpdate: function() {
		if (this.updated 
		&& this.version.updated 
		&& this.changed_dependencies.getLength() == 0) {
			fd.message.alert('Success', this.update_message);
			// clean up
			this.updated = null;
			this.version.updated = null;
			this.removeEvent('part_update', this.boundAfterUpdate);
			this.version.removeEvent('update', this.boundAfterUpdate);
			// fire event
			this.fireEvent('update');
		}
	},
	updateAfterDepSave: function(dep) {
		var method = this.changed_dependencies[dep.options.slug].method;
		dep.removeEvent(method, this.boundUpdateAfterDepSave);
		if (method == 'new_version') {
			fd.warning.alert('NOT YET IMPLEMENTED','reload version, please reload page');
		}
		this.changed_dependencies.erase(dep.options.slug);
		if (this.changed_dependencies.getLength() == 0) {
			this.afterUpdate();
		}
	},
	/*
	 * Method: new_version
	 * Prepare data and send Request - create a new version
	 */
	new_version: function(data) {
		this.updated = false;
		if (this.options.creator == fd.options.user) {
			this.addEvent('part_update', this.boundAfterNewVersion);
			// updating Meta
			new Request.JSON({
				url: this.options.update_url,
				data: this.prepareData(),
				method: 'post',
				onSuccess: function(response) {
					//fd.message.alert('DEBUG:', response.message);
					// save the message
					this.updated = true;
					this.fireEvent('part_update');
				}.bind(this)
			}).send();
		} else {
			// can't be updated
			// TODO: fix in next iteration
			this.updated = true;
		}
		// creating new version
		data = $pick(data, this.getFullData());
		this.version.created = false;
		new Request.JSON({
			url: this.options.version_create_url,
			data: data,
			method: 'post',
			onSuccess: function(response) {
				this.version.created = true;
				//fd.message.alert('DEBUG: Success', response.message);
				// save the message
				this.update_message = response.message;
				this.saved_new_version_url = response.version_absolute_url;
				if (this.changed_dependencies.getLength() == 0) {
					return this.afterNewVersion();
				}
				this.saveDependencies(
					this.boundNewVersionAfterDepSave, 
					response.version_identification
				);
			}.bind(this)
		}).send();
	},
	afterNewVersion: function() {
		if (this.updated 
		&& this.version.created
		&& this.changed_dependencies.getLength() == 0) {
			this.fireEvent('new_version');
			window.location.href = this.saved_new_version_url
		}
	},
	newVersionAfterDepSave: function(dep) {
		var method = this.changed_dependencies[dep.options.slug].method;
		dep.removeEvent(method, this.boundUpdateAfterDepSave);
		this.changed_dependencies.erase(dep.slug);
		if (this.changed_dependencies.getLength() == 0) {
			this.afterNewVersion();
		}
	},
	/*
	afterVersionCreated: function(response) {
		// update or create new versions of all dependencies and assign them
		this.version.updateDependenciesAndReload(
			response.version_update_dependency_url,
			response.version_absolute_url
		);
		// deprecayed: reload the page to the new version
		// window.location.href = response.version_absolute_url;
	},
	*/
	/*
	 * Method: addDependencyFromInput
	 */
	addDependencyFromInput: function() {
		dependency_slug = $(this.options.add_dependency_input).get('value');
		// TODO: some validation
		if (this.dependencies[dependency_slug]) {
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
				// create DOM elements 
				this.createDependency(response.dependency, true);
				// version is changed
				this.fireEvent('change');
			}.bind(this)
		}).send();
	},
	// TODO: remove this and make it work on the overall New Extension/Library
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
	/*
	 * Method: addDependency
	 */
	addDependency: 	function(options){
		var dep = new CapDependency(options);
		this.registerDependency(dep);
	},
	registerDependency: function(dep) {
		var slug = dep.options.slug;
		var self = this;
		dep.addEvents({
			'change': function() {
				self.registerDependencyChange(this);
			},
			'remove': function() { 
				self.removeDependency(this);
			}
		});
		this.dependencies[slug] = dep;
	},
	/*
	 * Method: removeDependency
	 * Remove dependency from all collectors
	 */
	removeDependency: function(dep) {
		var slug = dep.options.slug;
		this.dependencies.erase(slug);
		if (this.changed_dependencies.has(slug)) {
			this.changed_dependencies.erase(slug);
		}
	},
	/*
	 * Method: registerDependencyChange
	 */
	registerDependencyChange: function(dep, method) {
		if (!method) method = 'update';
		// force new_version if update not possible
		if (method == 'update' && dep.version.options.author != fd.options.user) {
			method = 'new_version';
		}
		this.changed_dependencies[dep.options.slug] = {
			// TODO: add ability to change method
			//		 should be chosen in a special modalWindow
			method: method,
			obj: dep
		}
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
		// prepare capability info
		var get_data = function(cap) {
			return cap.prepareData();
		};
		this.data['capabilities'] = JSON.encode(this.dependencies.getValues().map(get_data));
		return this.data;
	},
	/*
	 * Method: updateFromDOM
	 * get all jetpack editable fields from DOM and set parameters in model
	 */
	updateFromDOM: function() {
		// here update metadata from its editors
		this.data[this.type+'_description'] = this.description_el.getContent();
		return this.data;
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
})

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
		this.setOptions(options);
		this.instantiateEditors();
		this.createBounds();
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
		// instantiate content editor
		this.content_el = new FDEditor(this.options.content_el);
		fd.editors.push(this.content_el);
		// instantiate description editor
		this.description_el = new FDEditor(this.options.description_el).hide();
		fd.editors.push(this.description_el);
		// save the hook to edit name
		this.name_el = $(this.options.name_el);
	},
	/*
	 * Method: createAfterBounds
	 */
	createBounds: function() {
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.boundAfterDescriptionChanged = function() {
			this.changed = true;
			if (this.switch_description_el) {
				this.switch_description_el.getParent('li').addClass('UI_File_Modified');
			}
			this.description_el.removeEvent('change',this.boundAfterDescriptionChanged);
		}.bind(this);
		this.boundAfterContentChanged = function() {
			this.changed = true;
			if (this.switch_content_el) {
				this.switch_content_el.getParent('li').addClass('UI_File_Modified');
			}
			this.content_el.removeEvent('change',this.boundAfterContentChanged);			
		}.bind(this);
		this.boundSwitchToContent = this.switchToContent.bind(this);
		this.boundSwitchToDescription = this.switchToDescription.bind(this);
	},
	/*
	 * Method: listenToCapabilityEvents
	 */
	listenToEvents: function() {		
		this.changed = false;
		// listen to data change events
		this.name_el.addEvent('change', this.boundAfterDataChanged);
		this.description_el.addEvent('change', this.boundAfterDataChanged);
		this.content_el.addEvent('change', this.boundAfterDataChanged);
		// mark switches with content
		this.switch_content_el = $(this.options.switch_content_id);
		this.content_el.addEvent('change', this.boundAfterContentChanged);
		this.switch_description_el = $(this.options.switch_description_id);
		this.description_el.addEvent('change', this.boundAfterDescriptionChanged);
	},
	/*
	 * Method: initializeEditorSwitches
	 */
	initializeEditorSwitches: function() {
		if (this.switch_content_el) {
			this.switch_content_el.addEvent('click', this.boundSwitchToContent);
		}
		if (this.switch_description_el) {
			this.switch_description_el.addEvent('click', this.boundSwitchToDescription);
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
	updateDependenciesAndReload: function(version_update_dependency_url, version_reload_url){
		var callback = function() {
			window.location.href = version_reload_url;
		}
		this.updateDependencies(callback); 
	},
	/*
	 * Method: update
	 * get current data and send Request to the backend
	 */
	update: function() {
		this.updated = false;
		var self = this;
		var data = this.prepareData();
		// prevent from updating a version with different name
		if (data.version_name && data.version_name != this.options.name) {
			return item.new_version(data);
		}
		new Request.JSON({
			url: this.options.update_url,
			data: data,
			method: 'post',
			onSuccess: function(response) {
				self.updated = true;
				//fd.message.alert('DEBUG',response.message);
				// remove modification indicator from the file listing
				$$('.UI_File_Listing li').removeClass('UI_File_Modified');
				self.fireEvent('update');
			}
		}).send();
	},
	updateFinished: function() {
		fd.message.alert('Success', this.update_message);
		this.fireEvent('update');
		// change all "changed" marks
	},
	afterDataChanged: function() {
		// TODO: discover if change was actually an undo and there is 
		//       no change to the original content
		this.changed = true;
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
				this.set_as_base_el.set('text', 'Base version');
				// TODO: consider reloading to the base url
			}.bind(this)
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
		return this.options.name;
	},
	/*
	 * Method: prepareData
	 * Prepare all version specific available data
	 */
	prepareData: function() {
		this.updateFromDOM();
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
	},
	getIdentification: function() {
		return {
			version_name: this.data.version_name,
			version_counter: this.options.counter,
			slug: this.get_item().options.slug,
			type: this.get_item().options.type
		}
	}
});
