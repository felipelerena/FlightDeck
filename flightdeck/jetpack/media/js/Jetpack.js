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
		console.log('saving in the same version', this.getCode());
	},
	/*
	 * Method: newversion
	 * Prepare data and send Request - create a new version
	 */
	newversion: function() {
		console.log('saving new version', this.getCode());
	},
	/*
	 * Method: try
	 * Prepare Jetpack using saved code and install temporary in the browser
	 */
	try: function() {
		console.log('try in browser');
	},
	/*
	 * Method: prepareData
	 * Take all available data and return jetpack and version
	 */
	prepareData: function() {
		var data = {
			jetpack: {
				slug: this.options.slug,
				name: this.options.name,
				description: this.options.description
				// author will be saved on the backend
			},
			version: this.version.prepareData()
		};
		return data;	
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
	 * Prepare all version specifi available data
	 */
	prepareData: function() {
		var data = {
			// commited_by will be added in the backend
			name: this.options.name,
			description: this.options.description,
			code: this.options.code,
			is_base: this.options.is_base
		};
		return data
	}
});
