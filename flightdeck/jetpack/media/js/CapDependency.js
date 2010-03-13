/*
 * File: jetpack/CapDependency.js
 */


/*
 * Class: CapDependency
 * Refactored Capability class. Changes the behaviour to make it work as dependency
 */ 

var CapDependency = new Class({
	Extends: Capability, 
	options: {
		is_dependency: true // this will probably be redundant
	},
	initialize: function(options) {
		this.setOptions(options);
		this.initializeVersion();
		this.listenToEvents();
	},
	initializeVersion: function() {
		this.version = new CapVersionDependency(this.options.version);
	},
	createAfterBounds: function() {
		this.boundAfterVersionChanged = this.afterVersionChanged.bind(this);
	},
	listenToEvents: function() {
		this.createAfterBounds();
		this.version.addEvent('change', this.boundAfterVersionChanged);
	},
	afterVersionChanged: function() {
		$(item.options.version_create_el).addEvent('click', function(e) {
			e.stop();
			this.version_create();
		}.bind(this));
		this.version.removeEvent('click', this.boundAfterVersionChanged);
	},
	afterVersionCreated: function(response) {
		fd.message.alert(response.message);
		// change id's on the elements
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
	instantiateEditors: $empty,
	initializeEditorSwitches: $empty,
	switchToDescription: $empty,
	try_in_browser: $empty,
	getContent: $empty
}); 

var CapVersionDependency = new Class({
	Extends: CapVersion, 
	options: {
		is_dependency: true
	},
	initialize: function(options) {
		this.setOptions(options);
		this.switch_content_el = $(this.options.switch_content_id);
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
	listenToEvents: function() {
		this.changed = false;
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.content_el.addEvent('change', this.boundAfterDataChanged);
	},
	afterDataChanged: function() {
		this.changed = true;
		$(this.options.update_el).addEvent('click', function(e) {
			e.stop();
			this.update();			
		}.bind(this));
		this.content_el.removeEvent('change', this.boundAfterDataChanged);
		if (this.switch_content_el) {
			this.switch_content_el.getParent('li').addClass('UI_File_Modified');
		}
		this.fireEvent('change');
	},
	instantiateEditors: function() {
		this.content_el = new FDEditor(this.options.content_el).hide();
		fd.editors.push(this.content_el);
	},
	initializeEditorSwitches: function() {
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
				// TODO: REFACTOR - this should work from the event
				fd.getItem().version.capabilities.erase(this.options.slug);
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
