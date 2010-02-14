/*
 * Class representing the Capability only 
 * Prepare the editor, save, update
 */

var Capability = new Class({
	Implements: [Options, Events],
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
		this.initializeVersion();
		// TODO: add hooks for changing the Jetpack itself
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.boundAfterVersionChanged = this.afterVersionChanged.bind(this);
		this.version.addEvents({
			// #TODO: using change is wrong here 
			'change': this.boundAfterVersionChanged
		});
		// one may try even not edited data
		$(this.options.try_in_browser_el).addEvent('click', function(e) {
			e.stop();
			this.try_in_browser();
		}.bind(this));
		
		this.data = {
			slug: this.options.slug,
			name: this.options.name,
			description: this.options.description
		};
		// #TODO: remove these - it's just to switch the buttons all the time
		this.afterVersionChanged();
		this.afterDataChanged();
	},
	/* 
	 * Method: afterVersionChanged
	 * assign version_create with the $('version_create') click event
	 */
	afterDataChanged: function() {
		$(this.options.update_el).addEvent('click', function(e) {
			e.stop();
			this.update();
		}.bind(this));
		// TODO: stop listening the data changing event
	},
	/* 
	 * Method: afterVersionChanged
	 * assign version_create with the $('version_create') click event
	 */
	afterVersionChanged: function() {
		// TODO: discover if change was actually an undo and there is 
		//       no change to the original content
		$(this.options.version_create_el).addEvent('click', function(e) {
			e.stop(); 
			this.version_create();
		}.bind(this));
		this.version.removeEvent('change', this.boundAfterVersionChanged);
	},
	/*
	 * Method: initializeVersion
	 * assigns CapVersion to this.version
	 */
	initializeVersion: function() {
		this.version = new CapVersion(this.options.version);
	},
	/*
	 * Method: update
	 * Prepare data and send Request to the back-end
	 */
	update: function() {
		var data = { version: this.version.prepareData() };
		console.log('update', this.options.update_url, data);
	},
	/*
	 * Method: version_create
	 * Prepare data and send Request - create a new version
	 */
	version_create: function() {
		var data = { version: this.version.prepareData() };
		console.log('version_create', this.options.version_create_url, data);
	},
	/*
	 * Method: try_in_browser
	 * Prepare Capability using saved content and install temporary in the browser
	 */
	try_in_browser: function() {
		var data = this.getFullData();
		console.log('try_in_browser', data);
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
		// here update metadata from its editors
	},
	/*
	 * Method: getFullData
	 * get all data to save Jetpack and Version models
	 */
	getFullData: function() {
		return {
			capability: this.prepareData(),
			version: this.version.prepareData()
		}
	}
	
});

/*
 * Class representing the Version only 
 * Prepare the editor, save, update
 */
var CapVersion = new Class({
	Implements: [Options, Events],
	options: {
		editor: {},
		//commited_by: null,
		//name: null,
		//description: null,
		//content: null,
		//status: null,
		//is_base: null,
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
		this.setOptions(options);
		this.editor = new Editor(this.options.editor);
		this.changed = false;
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.editor.addEvents({
			'change': this.boundAfterDataChanged
		});
		// this.data is everything we send to the backend
		this.data = {
			name: this.options.name,
			description: this.options.description,
			content: this.options.content,
			is_base: this.options.is_base
		};
		// #TODO: remove these - it's just to switch the buttons all the time
		this.afterDataChanged();
	},
	afterDataChanged: function() {
		this.fireEvent('change');
		// TODO: discover if change was actually an undo and there is 
		//       no change to the original content
		this.changed = true;
		$(this.options.update_el).addEvent('click', function(e) {
			e.stop();
			this.update();
		}.bind(this));
		this.editor.removeEvent('change', this.boundAfterDataChanged);
	},
	/*
	 * Method: update
	 * get current data and send Request to the backend
	 */
	update: function() {
		data = this.prepareData();
		console.log('version.update', data);
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
		// #TODO: add more fields here
	}
});

