/*
 * File: jetpack/CapDependency.js
 */


/*
 * Class: CapDependency
 * Refactored Capability class. Changes the behaviour to make it work as dependency
 */ 

var CapDependency = new Class({
	Extends: Capability, 
	//options: {
	//	is_dependency: true // this will probably be redundant
	//},
	initialize: function(options) {
		this.setOptions(options);
		this.initializeVersion();
		this.createBounds();
		this.listenToEvents();
	},
	initializeVersion: function() {
		var self = this;
		this.version = new CapVersionDependency(this.options.version);
		this.version.get_item = function() {return self;};
		// pass version events
		this.version.addEvents({
			'change': function() { self.fireEvent('change'); },
			'remove': function() { self.fireEvent('remove'); },
			'update': function() { self.fireEvent('update', self); }
		});
	},
	createBounds: function() {
		this.boundAfterVersionChanged = this.afterVersionChanged.bind(this);
	},
	listenToEvents: function() {
		this.version.addEvent('change', this.boundAfterVersionChanged);
	},
	afterVersionChanged: function() {
		this.version.removeEvent('click', this.boundAfterVersionChanged);
		this.fireEvent('change');
	},
	afterNewVersion: function(response) {
		//fd.message.alert('DEBUG: Success', response.message);
		this.fireEvent('new_version', this);
		// reload version
		//this.version = new CapVersionDependency(response.version)
	},
	update: function(version_identification) {
		this.version.update();
	},
	/*
	 * Method: new_version
	 * Prepare data and send Request - create a new version
	 */
	new_version: function(version_identification) {
		var data = this.version.prepareData();
		data['assign_to'] = JSON.encode(version_identification);
		if (this.version.options.name) {
			data['copy_capabilities_from'] = JSON.encode(this.version.getIdentification());
		}
		new Request.JSON({
			url: this.options.version_create_url,
			data: data,
			method: 'post',
			onSuccess: function(response) {
				//fd.message.alert('DEBUG: cap', response.message);
				this.fireEvent('new_version', this);
			}.bind(this)
		}).send();
	},
	prepareData: function() {
		var data = $H({
			name: this.options.name,
			slug: this.options.slug,
			creator: this.options.creator
		});
		data.extend(this.version.prepareData());
		return data.getClean();
	},
	// switch off some Capability methods
	instantiateEditors: $empty,
	initializeEditorSwitches: $empty,
	switchToDescription: $empty,
	try_in_browser: $empty,
	getContent: $empty
}); 

var CapVersionDependency = new Class({
	Extends: CapVersion, 
	//options: {
	//	is_dependency: true
	//},
	initialize: function(options) {
		this.setOptions(options);
		this.instantiateEditors();
		this.listenToEvents();
		this.initializeEditorSwitches();
		this.data = $H({
			version_name: this.options.name,
			version_counter: this.options.counter,
			version_description: this.options.description,
			version_content: this.options.content
		});
	},
	instantiateEditors: function() {
		this.content_el = new FDEditor(this.options.content_el).hide();
		fd.editors.push(this.content_el);
	},
	listenToEvents: function() {
		this.changed = false;
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.content_el.addEvent('change', this.boundAfterDataChanged);
	},
	afterDataChanged: function() {
		/*
		$(this.options.update_el).addEvent('click', function(e) {
			e.stop();
			this.update();			
		}.bind(this));
		this.content_el.removeEvent('change', this.boundAfterDataChanged);
		if (this.switch_content_el) {
			this.switch_content_el.getParent('li').addClass('UI_File_Modified');
		}
		*/
		this.changed = true;
		this.content_el.removeEvent('change', this.boundAfterDataChanged);
		if (this.switch_content_el) {
			this.switch_content_el.getParent('li').addClass('UI_File_Modified');
		}
		this.fireEvent('change');
	},
	/*
	 * Method: update
	 * get current data and send Request to the backend
	 */
	update: function(version_identification) {
		var data = this.prepareData();
		data['assign_to'] = JSON.encode(version_identification);
		var self = this;
		new Request.JSON({
			url: this.options.update_url,
			data: data,
			method: 'post',
			onSuccess: function(response) {
				//fd.message.alert('DEBUG: cap updated', response.message);
				// TODO: remove modification indicator from the file listing
				self.fireEvent('update');
			}
		}).send();
	},
	initializeEditorSwitches: function() {
		this.switch_content_el = $(this.options.switch_content_id);
		if (this.switch_content_el) {
			this.switch_content_el.addEvent('click', this.switchToContent.bind(this));
			this.switch_content_el.getChildren('.File_close').addEvent('click', function(e) {
				e.stop();
				this.unassign();
			}.bind(this));
		}
	},
	unassign: function() {
		new Request.JSON({
			url: this.options.remove_url,
			data: {},
			onSuccess: function(response) {
				fd.message.alert('Success',response.message);
				if (!this.content_el.hidden) {
					// this is actually wrong
					// fd.getItem().version.switch_content_el.fireEvent('click', e);
				}
				this.content_el.destroy();
				this.switch_content_el.destroy();
				this.fireEvent('remove');
			}.bind(this)
		}).send();
	},
	updateFromDOM: function() {
		this.data.version_content = this.content_el.getContent();
	},
	prepareData: function() {
		this.updateFromDOM();
		return this.data;
	},
	setAsBase: $empty,
	switchToDescription: $empty,
	getName: $empty
});
