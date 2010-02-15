/*
 * Class representing the Capability only 
 * Prepare the editor, save, update
 */

var Capability = new Class({
	Implements: [Options, Events],
	type: 'capability',
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
		description_el: 'capability_description',
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
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.boundAfterVersionChanged = this.afterVersionChanged.bind(this);
		// TODO: add more hooks for changing the Jetpack itself
		this.description_el = $(this.options.description_el);
		// #TODO: using change is wrong here 
		this.description_el.addEvent('change', this.boundAfterDataChanged);
		this.version.addEvent('change', this.boundAfterVersionChanged);
		// one may try even not edited data
		$(this.options.try_in_browser_el).addEvent('click', function(e) {
			e.stop();
			this.try_in_browser();
		}.bind(this));
		
		this.data = {};
		this.data[this.type+'_slug'] = this.options.slug;
		this.data[this.type+'_name'] = this.options.name;
		this.data[this.type+'_description'] = this.options.description;
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
		var data = this.version.prepareData();
		new Request.JSON({
			url: this.options.version_create_url,
			data: data,
			method: 'post',
			onSuccess: function(response) {
				//window.location.href = response.version_absolute_url;
			}
		}).send();
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
		var data = $H(this.prepareData());
		data.extend(this.version.prepareData());
		return data.getClean();
	}
	
});

/*
 * Class representing the Version only 
 * Prepare the editor, save, update
 */
var CapVersion = new Class({
	Implements: [Options, Events],
	type: 'capability',
	options: {
		editor: {},
		//commited_by: null,
		//name: null,
		//description: null,
		//content: null,
		//status: null,
		//is_base: null,
		description_el: 'version_description',
		content_el: 'version_content',
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
		// listen to change events
		this.boundAfterDataChanged = this.afterDataChanged.bind(this);
		this.description_el = $(this.options.description_el);
		this.description_el.addEvent('change', this.boundAfterDataChanged);
		this.editor.addEvent('change', this.boundAfterDataChanged);
		// this.data is everything we send to the backend
		this.data = {
			version_name: this.options.name,
			version_description: this.options.description,
			version_content: this.options.content,
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
		console.log('version.update', this.options.update_url, data);
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
		this.data.version_content = this.editor.getContent();
		this.data.version_description = this.description_el.get('value');
	}
});

