/*
 * Class representing the Jetpack only 
 * Prepare the editor, save, update
 */
var Jetpack = new Class({
	Extends: Capability,
	Implements: [Options, Events],
	type: 'jetpack',
	options: {
		editor: {},
		version: {},
		//slug: null,
		//name: null,
		//description: null,
		//author: null,
		//managers: [],
		//developers: [],
		//public_permission: 2,
		//group_permission: 2,
		description_el: 'jetpack_description',
		update_el: 'update',
		version_create_el: 'version_create',
		try_in_browser_el: 'try_in_browser',
		edit_url: '',
		update_url: '',
		version_create_url: ''
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
		editor: {},
		//commited_by: null,
		//name: null,
		//manifest: null,
		//content: null,
		//description: null,
		//status: null,
		//published: null,
		//is_base: null,
		description_el: 'version_description',
		content_el: 'version_content',
		manifest_el: 'version_manifest',
		update_el: 'update',
		edit_url: '',
		update_url: '',
		set_as_base_url: ''
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
		this.data.version_content = this.editor.getContent();
		this.data.version_description = this.description_el.get('value');
		this.data.version_manifest = this.manifest_el.get('value');
	},
});
