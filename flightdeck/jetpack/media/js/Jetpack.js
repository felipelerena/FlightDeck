/*
 * Class representing the Jetpack only 
 * Prepare the editor, save, update
 */
var Jetpack = new Class({
	Extends: Capability,
	Implements: [Options, Events],
	type: 'jetpack',
	options: {
		description_el: 'jetpack_description',
		try_in_browser_el: 'try_in_browser',
	},
	/*
	 * Method: initialize
	 * @attribute object options: 
	 * 	
	 * initialize Version and inside of that chosen Editor
	 * assign actions to the buttons
	 */
	initialize: function(options) {
		this.setOptions(options)
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
		// here update name/description whatever
	},
});

/*
 * Class representing the Version only 
 * Prepare the editor, save, update
 */
var JetVersion = new Class({
	Extends: CapVersion,
	Implements: [Options],
	type: 'jetpack',
	options: {
		//manifest: null,
		//published: null,
		manifest_el: 'version_manifest'
	},
	/*
	 * Method: initialize
	 * instantiate Editor
	 */
	initialize: function(options) {
		this.parent(options);
		this.data.version_manifest = this.options.manifest;
		this.manifest_el = $(this.options.manifest_el);
	},
	/*
	 * Method: updateFromDOM
	 * get all version editable fields from DOM and set parameters in model
	 */
	updateFromDOM: function() {
		this.data.version_name = this.name_el.get('value');
		this.data.version_content = this.editor.getContent();
		this.data.version_description = this.description_el.get('value');
		this.data.version_manifest = this.manifest_el.get('value');
	},
});
