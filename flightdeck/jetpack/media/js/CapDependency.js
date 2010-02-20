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
		item = jetpack || capability;
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
	instantiateEditors: $empty,
	initializeEditorSwitches: $empty,
	switchToDescription: $empty,
	try_in_browser: $empty,
	getContent: $empty,
	prepareData: $empty
}); 

var CapVersionDependency = new Class({
	Extends: CapVersion, 
	options: {
		is_dependency: true
	},
	initialize: function(options) {
		this.setOptions(options);
		this.instantiateEditors();
		this.listenToEvents();
		this.initializeEditorSwitches();
		this.data = $H({
			version_name: this.options.name,
			versin_description: this.options.description,
			version_content: this.options.content,
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
		this.fireEvent('change');
	},
	instantiateEditors: function() {
		this.content_el = new Editor(this.options.content_el).hide();
		fd.editors.push(this.content_el);
	},
	initializeEditorSwitches: function() {
		this.switch_content_el = $(this.options.switch_content_id);
		if (this.switch_content_el) {
			this.switch_content_el.addEvent('click', this.switchToContent.bind(this));
		}
	},
	updateFromDOM: function() {
		this.data.version_content = this.content_el.getContent();
	},
	setAsBase: $empty,
	switchToDescription: $empty,
	getName: $empty,
	
});
