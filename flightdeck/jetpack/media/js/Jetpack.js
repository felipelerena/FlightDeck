/*
 * Class representing the Jetpack only 
 * Prepare the editor, save, update
 */

var Jetpack = new Class({
	Implements: [Options, Events],
	options: {
		editor: {
		},
		version: {
		},
		slug: '',
		name: '',
		description: '',
		author: '',
		//managers: [],
		//developers: [],
		//public_permission: 2,
		//group_permission: 2,
		save_el: 'save',
		newversion_el: 'newversion',
		try_el: 'try'
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
		this.version = new Version(this.options.version);
		
		this.data = {
			slug: this.options.slug,
			name: this.options.name,
			description: this.options.description
		};
		// initiate actions
		var save_el = $(this.options.save_el);
		if (save_el) save_el.addEvent('click', function(e) {
			e.stop();
			this.update_version();
		}.bind(this));
		var newversion_el = $(this.options.newversion_el);
		if (newversion_el) newversion_el.addEvent('click', function(e) {
			e.stop();
			this.save_new_version();
		}.bind(this));
		var try_el = $(this.options.try_el);
		if (try_el) try_el.addEvent('click', function(e) {
			e.stop();
			this.try_in_browser();
		}.bind(this));
	},
	/*
	 * Method: update_version
	 * Prepare data and send Request to the back-end
	 */
	update_version: function() {
		var data = { version: this.version.prepareData() };
		console.log('update_version', settings.jp_jetpack_update_version_url, data);
	},
	/*
	 * Method: newversion
	 * Prepare data and send Request - create a new version
	 */
	save_new_version: function() {
		var data = { version: this.version.prepareData() };
		console.log('save_new_version', settings.jp_jetpack_save_new_version_url, data);
	},
	/*
	 * Method: try
	 * Prepare Jetpack using saved content and install temporary in the browser
	 */
	try_in_browser: function() {
		var data = this.getFullData();
		console.log('trying in browser', data);
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
		return this.version.getName()
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
		// here update name/description whatever
	},
	/*
	 * Method: getFullData
	 * get all data to save Jetpack and Version models
	 */
	getFullData: function() {
		return {
			jetpack: this.prepareData(),
			version: this.version.prepareData()
		}
	}
	
});

/*
 * Class representing the Version only 
 * Prepare the editor, save, update
 */
var Version = new Class({
	Implements: [Options],
	options: {
		editor: {
		},
		commited_by: '',
		name: '',
		manifest: '',
		content: '',
		description: '',
		status: '',
		published: false,
		is_base: false
	},
	/*
	 * Method: initialize
	 * instantiate Editor
	 */
	initialize: function(options) {
		this.setOptions(options);
		this.editor = new Editor(this.options.editor);
		// this.data is everything which may be set in the frontend
		this.data = {
			name: this.options.name,
			description: this.options.description,
			content: this.options.content,
			manifest: this.options.manifest,
			is_base: this.options.is_base
		};
	},
	/*
	 * Method: getContent
	 * Wrapper for getting content from the Editor
	 */
	getContent: function() {
		return this.editor.getContent();
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
		return this.data;
	},
	/*
	 * Method: updateFromDOM
	 * get all version editable fields from DOM and set parameters in model
	 */
	updateFromDOM: function() {
		this.data.content = this.editor.getContent();
		// add more fields here
	}
});
