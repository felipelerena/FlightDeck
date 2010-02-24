/*
 * Class representing the Jetpack only 
 * Prepare the editor, save, update
 */
var Jetpack = new Class({
	Extends: Capability,
	type: 'jetpack',
	options: {
		description_el: {element: 'jetpack_description'},
		try_in_browser_el: 'try_in_browser'
	},
	/*
	 * Method: initialize
	 * @attribute object options: 
	 * 	
	 * initialize Version and inside of that chosen Editor
	 * assign actions to the buttons
	 */
	initialize: function(options) {
		this.setOptions(options);
		this.parent(this.options);
	},
	/*
	 * Method: initializeVersion
	 * assigns JetVersion to this.version
	 */
	initializeVersion: function() {
		this.version = new JetVersion(this.options.version);
	},
	/*
	 * Method: updateFromDOM
	 * get all jetpack editable fields from DOM and set parameters in model
	 */
	updateFromDOM: function() {
		this.parent();
	}
});

/*
 * Class representing the Version only 
 * Prepare the editor, save, update
 */
var JetVersion = new Class({
	Extends: CapVersion, 
	type: 'jetpack',
	options: {
		//manifest: null,
		//published: null,
		manifest_el: {
			element: 'version_manifest',
			type: 'json'
		}
		//switch_manifest_id: ''
	},
	/*
	 * Method: initialize
	 * instantiate Editor
	 */
	initialize: function(options) {
		this.setOptions(options);
		this.parent(options);
		this.data.version_manifest = this.options.manifest;
	},
	/*
	 * Method: instantiateEditors
	 */
	instantiateEditors: function() {
		this.parent();
		this.manifest_el = new Editor(this.options.manifest_el).hide();
		fd.editors.push(this.manifest_el);
	},
	/*	
	 * Method: listenToJetpackEvents
	 */
	listenToEvents: function() {
		this.parent();
	},
	/*
	 * Method: initializeEditorSwitches
	 */
	initializeEditorSwitches: function() {
		this.parent();
		this.switch_manifest_el = $(this.options.switch_manifest_id);
		if (this.switch_manifest_el) {
			this.switch_manifest_el.addEvent('click', this.switchToManifest.bind(this));
		}
	},
	/*
	 * Method: switchToManifest
	 */
	switchToManifest: function(e) {
		e.stop();
		fd.hideEditors();
		this.manifest_el.show();
	},
	/*
	 * Method: updateFromDOM
	 * get all version editable fields from DOM and set parameters in model
	 */
	updateFromDOM: function() {
		this.parent();
		this.data.version_manifest = this.manifest_el.getContent();
	}
});
