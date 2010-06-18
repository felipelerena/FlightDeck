/*
 * File: jetpack.Package.js
 */

/*
 * Javascript Package/PackageRevision representation
 */

var Package = new Class({
	// this Class should be always extended
	Implements: [Options],
	options: {
		// data
			// package specific
				// id_number: '',
				// full_name: '',
				// name: '',
				// description: '',
				// type: '', // 'a'/'l'
				// package_author: '',
				// url: '',
				// license: '',
				// package_version_name: '',
				// version_url: '', // link to the current version revision
				// latest_utl: '', // link to the latest revision
			// revision specific data
				// revision_verion_name: '',
				// revision_number: '',
				// message: '', // commit message
				// dependecies: [], // list of names and urls
				// origin_url: '', // link to a revision used to created this one
				// revision_author: '',
				// modules: [], // a list of module filename, author pairs
		readonly: false,
		package_info_el: 'package-info',
		test_el: 'try_in_browser'
	},
	modules: {},
	initialize: function(options) {
		this.setOptions(options);
		this.instantiate_modules();
		$('revisions_list').addEvent('click', this.show_revision_list);

		// testing
		this.boundTestAddon = this.testAddon.bind(this);
		if (this.isAddon()) {
			this.test_url = $(this.options.test_el).get('href');
			$(this.options.test_el).addEvent('click', this.boundTestAddon)
		}
		if ($('attachments')) $('attachments').addEvent(
			'click:relay(.UI_File_Listing a)',
			function(e, target) {
				e.stop();
				var url = target.get('href');
				var ext = target.get('rel');
				var filename = target.get('text');
				var template_start = '<div id="attachment_view"><h3>'+filename+'</h3><div class="UI_Modal_Section">';
				var template_end = '</div><div class="UI_Modal_Actions"><ul><li><input type="reset" value="Close" class="closeModal"/></li></ul></div></div>';
				var template_middle = 'Download <a href="'+url+'">'+filename+'</a>';
				if (['jpg', 'gif', 'png'].contains(ext)) template_middle = '<img src="'+url+'"/>'; 
				if (['css', 'js', 'css'].contains(ext)) {
					new Request({
						url: url,
						onSuccess: function(response) {
							template_middle = '<pre>'+response+'</pre>';
							this.attachmentWindow = fd.displayModal(template_start+template_middle+template_end);
						}
					}).send();
				} else {
					this.attachmentWindow = fd.displayModal(template_start+template_middle+template_end);
				}
			}.bind(this)
		)
	},
	testAddon: function(e){
		if (e) e.stop();
		if (fd.alertIfNoAddOn()) {
			var el = e.target;
			if (el.getParent('li').hasClass('pressed')) {
				fd.uninstallXPI(el.get('rel'));
			} else {
				new Request.JSON({
					url: this.test_url,
					data: this.data || {},
					onSuccess: fd.testXPI.bind(fd)
				}).send();
			}
		}
	},
	isAddon: function() {
		return (this.options.type == 'a');
	},
	instantiate_modules: function() {
		// iterate by modules and instantiate Module
		var main_module;
		this.options.modules.each(function(module) {
			module.readonly = this.options.readonly;
			if (!main_module) {
				module.main = true;
				main_module = module;
			}
			this.modules[module.filename] = new Module(this,module);
		}, this);
	},
	show_revision_list: function(e) {
		if (e) e.stop();
		new Request({
			url: settings.revisions_list_html_url,
			onSuccess: function(html) {
				fd.displayModal(html);
			}
		}).send();
	}
});


var Module = new Class({
	Implements: [Options, Events],
	options: {
		// data
			// filename: '',
			// code: '',
			// author: '',
		// DOM
			code_trigger_suffix: '_switch', // id of an element which is used to switch editors
			code_editor_suffix: '_textarea', // id of the textarea
		readonly: false,
		main: false,
		executable: false,
		active: false,
		type: 'js',
		append: false
	},
	initialize: function(pack, options) {
		this.setOptions(options);
		this.pack = pack;
		if (this.options.append) {
			this.append();
		}
		// connect trigger with editor
		if ($(this.get_trigger_id()) && $(this.get_editor_id())) {
			this.textarea = $(this.get_editor_id());
			this.trigger = $(this.get_trigger_id());
			this.trigger.store('Module', this);
			this.editor = new FDEditor({
				element: this.get_editor_id(),
				activate: this.options.main || this.options.executable,
				type: this.options.type,
				readonly: this.options.readonly
			});
			// connect trigger
			this.trigger.addEvent('click', function(e) {
				if (e) e.preventDefault();
				this.switchBespin();
			}.bind(this));
			if (this.options.main || this.options.executable) {
				this.trigger.getParent('li').switch_mode_on();
			} 
			if (this.options.active) {
				this.switchBespin();
				var li = this.trigger.getParent('li')
				fd.assignModeSwitch(li);
				li.switch_mode_on();
			}
			if (!this.options.readonly) {
				// here special functionality for edit page
				var rm_mod_trigger = this.trigger.getElement('span.File_close');
				if (rm_mod_trigger) {
					rm_mod_trigger.addEvent('click', function(e) {
						this.pack.removeModuleAction(e);
					}.bind(this));
				}
			}
		}
	},
	switchBespin: function() {
		fd.switchBespinEditor(this.get_editor_id(), this.options.type); 
		if (fd.getItem()) {
			$each(fd.getItem().modules, function(mod) {
				mod.active = false;
			});
		}
		this.active = true;
	},
	destroy: function() {
		this.textarea.destroy();
		this.trigger.getParent('li').destroy();
		$('modules-counter').set('text', '('+ $('modules').getElements('.UI_File_Listing li').length +')')
		delete fd.getItem().modules[this.options.filename];
		delete fd.editor_contents[this.get_editor_id()];
		if (this.active) {
			// switch editor!
			mod = null;
			// try to switch to first element
			first = false;
			$each(fd.getItem().modules, function(mod) {
				if (!first) {
					first = true;
					mod.switchBespin();
					mod.trigger.getParent('li').switch_mode_on();
				}
			});
			if (!first) {
				fd.cleanBespin();
			}
		}
	},
	get_editor_id: function() {
		if (!this._editor_id) 
			this._editor_id = this.options.filename + this.options.code_editor_suffix;
		return this._editor_id;
	},
	get_trigger_id: function() {
		if (!this._trigger_id) 
			this._trigger_id = this.options.filename + this.options.code_trigger_suffix;
		return this._trigger_id;
	},
	append: function() {
		var html = '<a title="" href="#" class="Module_file" id="{filename}_switch">'+
						'{filename}<span class="File_status"></span>'+
						'<span class="File_close"></span>'+
					'</a>';
		var li = new Element('li',{
			'class': 'UI_File_normal',
			'html': html.substitute(this.options)
		}).inject($('add_module_div').getPrevious('ul'));
		$('modules-counter').set('text', '('+ $('modules').getElements('.UI_File_Listing li').length +')')
		
		var textarea = new Element('textarea', {
			'id': this.options.filename + '_textarea',
			'class': 'UI_Editor_Area',
			'name': this.options.filename + '_textarea',
			'html': this.options.code
		}).inject('editor-wrapper');
	}
})


Package.View = new Class({
	Extends: Package,
	Implements: [Options, Events],
	options: {
		readonly: true,
		copy_el: 'package-copy',
		// copy_url: '',
	},
	initialize: function(options) {
		this.setOptions(options);
		this.parent(options);
		$(this.options.package_info_el).addEvent('click', this.showInfo.bind(this));
		this.copy_el = $(this.options.copy_el)
		if (this.copy_el) {
			this.copy_el.addEvent('click', this.copyPackage.bind(this));
		}
	},
	/*
	 * Method: showInfo
	   display a window with info about current Package
	 */
	showInfo: function(e) {
		e.stop();
		fd.displayModal(this.options.package_info);
	},
	/*
	 * Method: copyPackage
	 * create a new Package with the same name for the current user
	 */
	copyPackage: function(e) {
		e.stop();
		if (!settings.user) {
			fd.alertNotAuthenticated();
			return;
		}
		new Request.JSON({
			url: this.options.copy_url,
			onSuccess: function(response) {
				window.location.href = response.edit_url;
			}
		}).send();
	}
});


Package.Edit = new Class({
	Extends: Package,
	Implements: [Options, Events],
	options: {
		// DOM elements
			save_el: 'package-save',
			menu_el: 'UI_Editor_Menu',
			assign_library_el: 'assign_library_action',
			assign_library_input: 'library_id_number',
			add_module_el: 'add_module_action',
			add_module_input: 'add_module',

		// urls
			// save_url: '',
			// delete_url: '',
			// add_module_url: '',
			// assign_library_url: '',
		package_info_form_elements: [
			'full_name', 'version_name', 'package_description', 'revision_message'
			]
	},
	initialize: function(options) {
		this.setOptions(options);
		// this.data is a temporary holder of the data for the submit
		this.data = {};
		this.parent(options);

		this.assignActions();

		// autocomplete
		this.autocomplete = new FlightDeck.Autocomplete({
			'url': settings.library_autocomplete_url
		});
	},
	assignActions: function() {
		// assign menu items
		$(this.options.package_info_el).addEvent('click', this.editInfo.bind(this));
		
		// save
		this.boundSaveAction = this.saveAction.bind(this);
		$(this.options.save_el).addEvent('click', this.boundSaveAction);
		
		// submit Info
		this.boundSubmitInfo = this.submitInfo.bind(this);
		
		// add/remove module
		this.boundAddModuleAction = this.addModuleAction.bind(this);
		this.boundRemoveModuleAction = this.removeModuleAction.bind(this);
		$(this.options.add_module_el).addEvent('click', 
			this.boundAddModuleAction);
		
		// assign/remove library
		this.boundAssignLibraryAction = this.assignLibraryAction.bind(this);
		this.boundRemoveLibraryAction = this.removeLibraryAction.bind(this);
		$(this.options.assign_library_el).addEvent('click',
			this.boundAssignLibraryAction);
		$$('#libraries .UI_File_Listing .File_close').each(function(close) { 
			close.addEvent('click', this.boundRemoveLibraryAction);
		},this);
		
		// add attachments
		this.add_attachment_el = $('add_attachment');
		this.attachment_template = '<a title="" rel="{ext}" href="{display_url}" class="Module_file" id="{filename}{ext}_display">'+
						'{basename}<span class="File_close"></span>'+
					'</a>';
		this.add_attachment_el.addEvent('change', this.sendMultipleFiles.bind(this));
		this.boundRemoveAttachmentAction = this.removeAttachmentAction.bind(this);
		$$('#attachments .UI_File_Listing .File_close').each(function(close) { 
			close.addEvent('click', this.boundRemoveAttachmentAction);
		},this);
		this.attachments_counter = $('attachments-counter');
		
		var fakeFileInput = $('add_attachment_fake'), fakeFileSubmit = $('add_attachment_action_fake');
		this.add_attachment_el.addEvents({
			change: function(){
				fakeFileInput.set('value', this.get('value'));
			},
			
			mouseover: function(){
				fakeFileSubmit.addClass('hover');
			},
			
			mouseout: function(){
				fakeFileSubmit.removeClass('hover');
			}
		});
	},

	get_add_attachment_url: function() {
		return this.add_attachment_url || this.options.add_attachment_url;
	},

	sendMultipleFiles: function() {
		self = this;
		sendMultipleFiles({
			url: this.get_add_attachment_url.bind(this),
			
			// list of files to upload
			files: this.add_attachment_el.files,
			
			// clear the container
			//onloadstart:function(){
			//	$log('loadstart')
			//},
			
			// do something during upload ...
			//onprogress:function(rpe){
			//	$log('progress');
			//},

			onpartialload: function(rpe, xhr) {
				$log('FD: file uploaded');
				// here parse xhr.responseText and append a DOM Element
				response = JSON.parse(xhr.responseText);
				new Element('li',{
					'class': 'UI_File_Normal',
					'html': self.attachment_template.substitute(response)
				}).inject($('attachments_ul'));
				$(response.filename+response.ext+'_display').getElement('.File_close').addEvent('click', self.boundRemoveAttachmentAction);
				fd.setURIRedirect(response.edit_url);
				self.setUrls(response);
				
				self.attachments_counter.set('text', '('+ $('attachments').getElements('.UI_File_Listing li').length +')')
			},
			
			// fired when last file has been uploaded
			onload:function(rpe, xhr){
				$log('FD: all files uploaded');
				$(self.add_attachment_el).set('value','');
				$('add_attachment_fake').set('value','')
			},
			
			// if something is wrong ... (from native instance or because of size)
			onerror:function(){
				fd.error.alert(
					'Error {status}'.substitute(xhr), 
					'{statusText}<br/>{responseText}'.substitute(xhr)
					);
			}
		});
	},
	removeAttachmentAction: function(e) {
		e.stop();
		var trigger = e.target.getParent('a');
		var filename = trigger.get('text');
		this.question = fd.showQuestion({
			title: 'Are you sure you want to remove "'+filename+'"?',
			message: '',
			ok: 'Remove',
			id: 'remove_attachment_button',
			callback: function() {
				this.removeAttachment(filename);
				this.question.destroy();
			}.bind(this)
		});
	},
	removeAttachment: function(filename) {
		var self = this;
		new Request.JSON({
			url: self.remove_attachment_url || self.options.remove_attachment_url,
			data: {filename: filename},
			onSuccess: function(response) {
				fd.setURIRedirect(response.edit_url);
				self.setUrls(response);
				$(response.filename+response.ext+'_display').getParent('li').destroy();
				self.attachments_counter.set('text', '('+ $('attachments').getElements('.UI_File_Listing li').length +')')
			}
		}).send();
	},

	addModuleAction: function(e) {
		e.stop();
		// get data
		var filename = $(this.options.add_module_input).value;
		if (!filename) {
			fd.error.alert('Filename can\'t be empty', 'Please provide the name of the module');
			return;
		}
		if (this.options.modules.contains(filename)) {
			fd.error.alert('Filename has to be unique', 'You already have the module with that name');
			return;
		}
		this.addModule(filename);
	},
	addModule: function(filename) {
		new Request.JSON({
			url: this.add_module_url || this.options.add_module_url,
			data: {'filename': filename},
			onSuccess: function(response) {
				// set the redirect data to edit_url of the new revision
				fd.setURIRedirect(response.edit_url);
				// set data changed by save
				this.setUrls(response);
				fd.message.alert(response.message_title, response.message);
				// initiate new Module
				var mod = new Module(this,{
					append: true,
					active: true,
					filename: response.filename,
					author: response.author,
					code: response.code
				});
				this.modules[response.filename] = mod;
			}.bind(this)
		}).send();
	},
	removeModuleAction: function(e) {
		e.stop();
		var trigger = e.target.getParent('a');
		var module = trigger.retrieve('Module');
		if (!module) {
			fd.error.alert('Application error', 'Can not associate module to the trigger');
			return;
		}
		this.question = fd.showQuestion({
			title: 'Are you sure you want to remove {filename}.js?'.substitute(module),
			message: 'You may always copy it from this revision',
			ok: 'Remove',
			id: 'remove_module_button',
			callback: function() {
				this.removeModule(module);
				this.question.destroy();
			}.bind(this)
		});
	},
	removeModule: function(module) {
		new Request.JSON({
			url: this.remove_module_url || this.options.remove_module_url,
			data: module.options,
			onSuccess: function(response) {
				fd.setURIRedirect(response.edit_url);
				this.setUrls(response);
				var mod = this.modules[response.filename];
				mod.destroy();
			}.bind(this)
		}).send();
	},
	assignLibraryAction: function(e) {
		// get data
		library_id = $(this.options.assign_library_input).get('value');
		// assign Library by giving filename
		this.assignLibrary(library_id);
	},
	assignLibrary: function(library_id) {
		new Request.JSON({
			url: this.assign_library_url || this.options.assign_library_url,
			data: {'id_number': library_id},
			onSuccess: function(response) {
				// set the redirect data to edit_url of the new revision
				fd.setURIRedirect(response.edit_url);
				// set data changed by save
				this.setUrls(response);
				//fd.message.alert('Library assigned', response.message);
				this.appendLibrary(response);
			}.bind(this)
		}).send();
	},
	appendLibrary: function(lib) {
		var html='<a title="" id="library_{library_name}" href="{library_url}" target="{id_number}" class="library_link">'+
					'{full_name}'+
					'<span class="File_close"></span>'+
				'</a>';
		new Element('li', {
			'class': 'UI_File_Normal',
			'html': html.substitute(lib)
		}).inject($('assign_library_div').getPrevious('ul'));
		$$('#library_{library_name} .File_close'.substitute(lib)).each(function(close) { 
			close.addEvent('click', this.boundRemoveLibraryAction);
		},this);
		$('libraries-counter').set('text', '('+ $('libraries').getElements('.UI_File_Listing li').length +')')
	},
	removeLibraryAction: function(e) {
		if (e) e.stop();
		var id_number = e.target.getParent('a').get('target');
		var name = e.target.getParent('a').get('text');

		this.question = fd.showQuestion({
			title: 'Are you sure you want to remove "'+name+'"?',
			message: '',
			ok: 'Remove',
			id: 'remove_library_button',
			callback: function() {
				this.removeLibrary(id_number);
				this.question.destroy();
			}.bind(this)
		});
	},
	removeLibrary: function(id_number) {
		new Request.JSON({
			url: this.remove_library_url || this.options.remove_library_url,
			data: {'id_number': id_number},
			onSuccess: function(response) {
				fd.setURIRedirect(response.edit_url);
				this.setUrls(response);
				$('library_{name}'.substitute(response)).getParent('li').destroy();
				$('libraries-counter').set('text', '('+ $('libraries').getElements('.UI_File_Listing li').length +')')
			}.bind(this)
		}).send();
	},
	/*
	 * Method: editInfo
	 * display the EditInfoModalWindow
	 */
	editInfo: function(e) {
		e.stop();
		this.savenow = false;
		fd.editPackageInfoModal = fd.displayModal(settings.edit_package_info_template.substitute(this.data || this.options));
		$('package-info_form').addEvent('submit', this.boundSubmitInfo);
		if ($('savenow')) {
			$('savenow').addEvent('click', function() {
				this.savenow = true;
			}.bind(this));
		}
		// XXX: hack to get the right data in the form
		$each(this.data, function(value, key) {
			if ($(key)) $(key).value = value;
		})
	},
	/*
	 * Method: submitInfo
	 * submit info from EditInfoModalWindow
	 * if $('savenow') clicked - save the full info
	 */
	submitInfo: function(e) {
		e.stop();
		// collect data from the Modal
		this.options.package_info_form_elements.each(function(key) {
			if ($(key)) this.data[key] = $(key).value;
		}, this);
		// check if save should be called
		if (this.savenow) {
			return this.save();
		}
		fd.editPackageInfoModal.destroy();
	},
	collectData: function() {
		fd.saveCurrentEditor();
		$each(this.modules, function(module, filename) {
			this.data[filename] = fd.editor_contents[filename + module.options.code_editor_suffix]
		}, this);
	},
	testAddon: function(e){
		this.collectData();
		this.data.live_data_testing = true;
		this.parent(e);
	},
	saveAction: function(e) {
		if (e) e.stop();
		this.save();
	},
	save: function() {
		this.collectData();
		new Request.JSON({
			url: this.save_url || this.options.save_url,
			data: this.data,
			onSuccess: function(response) {
				// set the redirect data to edit_url of the new revision
				if (response.reload) {
				 	window.location.href = response.edit_url;
				}
				fd.setURIRedirect(response.edit_url);
				// set data changed by save
				this.setUrls(response);
				fd.message.alert(response.message_title, response.message);
				// clean data leaving package_info data
				this.data = {};
				this.options.package_info_form_elements.each(function(key) {
					if ($defined(response[key])) {
						this.data[key] = response[key]
					}
				}, this);
				if (fd.editPackageInfoModal) fd.editPackageInfoModal.destroy();
			}.bind(this)
		}).send();
	},
	setUrls: function(urls) {
		this.save_url = urls.save_url;
		this.test_url = urls.test_url;
		this.add_module_url = urls.add_module_url;
		this.remove_module_url = urls.remove_module_url;
		this.add_attachment_url = urls.add_attachment_url;
		this.remove_attachment_url = urls.remove_attachment_url;
		this.assign_library_url = urls.assign_library_url;
		this.remove_library_url = urls.remove_library_url;
	}
});
