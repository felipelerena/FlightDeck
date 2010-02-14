/*
 * Class representing the Jetpack only 
 * Prepare the editor, save, update
 */
var Jetpack = new Class({
	Extends: Capability,
	Implements: [Options, Events],
	/*
	 * Method: initialize
	 * @attribute object options: 
	 * 	
	 * initialize Version and inside of that chosen Editor
	 * assign actions to the buttons
	 */
	initialize: function(options) {
		this.parent(options);
	},
	/*
	 * Method: initializeVersion
	 * assigns JetVersion to this.version
	 */
	initializeVersion: function() {
		this.version = new CapVersion(this.options.version);
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
	options: {
		editor: {},
		//commited_by: null,
		//name: null,
		//manifest: null,
		//content: null,
		//description: null,
		//status: null,
		//published: null,
		//is_base: null,
		update_el: 'update'
	},
	/*
	 * Method: initialize
	 * instantiate Editor
	 */
	initialize: function(options) {
		this.parent(options);
		this.data.manifest = this.options.manifest;
		this.published = this.options.published;
	},
	/*
	 * Method: updateFromDOM
	 * get all version editable fields from DOM and set parameters in model
	 */
	updateFromDOM: function() {
		this.data.content = this.editor.getContent();
		// #TODO: add more fields here
	},
});
