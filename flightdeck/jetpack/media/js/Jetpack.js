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
		//group_permission: 2
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
		$('save').addEvent('click', function(e) {
			e.stop();
			this.save();
		}.bind(this));
		$('newversion').addEvent('click', function(e) {
			e.stop();
			this.newversion();
		}.bind(this));
		$('try').addEvent('click', function(e) {
			e.stop();
			this.try();
		}.bind(this));
	},
	/*
	 * Method: save
	 * Prepare data and send Request to the back-end
	 */
	save: function() {
		var data = { version: this.version.prepareData() };
		console.log('saving in the same version', data);
	},
	/*
	 * Method: newversion
	 * Prepare data and send Request - create a new version
	 */
	newversion: function() {
		var data = { version: this.version.prepareData() };
		console.log('saving new version', data);
	},
	/*
	 * Method: try
	 * Prepare Jetpack using saved code and install temporary in the browser
	 */
	try: function() {
		var data = this.getFullData();
		console.log('trying in browser', data);
	},
	/*
	 * Method: getCode
	 * Wrapper for getting code from the Editor
	 */
	getCode: function() {
		return this.version.getCode();
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
		description: '',
		code: '',
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
			code: this.options.code,
			is_base: this.options.is_base
		};
	},
	/*
	 * Method: getCode
	 * Wrapper for getting code from the Editor
	 */
	getCode: function() {
		return this.editor.getCode();
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
		this.data.code = this.editor.getCode();
	}
});
