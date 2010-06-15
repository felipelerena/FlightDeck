/*
 * File: jetpack/Create.js
 */
/*
 * object Create
 * Create new Add-on/Library
 */

var create = {
	init: function(create_id, create_item, wrapper_id) {

		create_id = $splat(create_id);
		create_item = $splat(create_item);

		var boundSubmit = this.submit.bind(this);
		var self = this;
		create_id.each(function(create_trigger, idx){
			$(create_trigger).addEvent('click', function(e) {
				e.stop();
				if (!fd.options.user) {
					fd.alertNotAuthenticated();
					return
				} 
				fd.addnewDependencyModal = fd.displayModal(settings.create_modal_template, wrapper_id);
				if (create_item && create_item[idx]) {
					$('create-'+create_item[idx])
						.set('checked', 'checked')
				}
				var setName = function(name) {
					if (this.get('checked')) {
						$('create-name').set('value', name);
					}
				}
				if ($('create-addon')) {
					$('create-addon').addEvent('change', function() { setName.bind(this)('My Add-on'); });
					setName.bind($('create-addon'))('My Add-on');
				} 
				if ($('create-library')) {
					$('create-library').addEvent('change', function() { setName.bind(this)('My Library'); });
					setName.bind($('create-library'))('My Library');
				} 
				
				/*
				 * Button New removed from Edit
				if (fd.getItem) {
					$$('#create_form input[type=radio]').addEvent('change', function() {
						if ($('create-library').checked) {
							$('add-new-library-li')
								.removeClass('hidden')
								.show();
						} else {
							$('add-new-library-li').hide();
						}
					});
				} 
				*/
				$('create_form').addEvent('submit', boundSubmit);
				// $('create_form_cancel').addEvent('click', function(e) {
				// 	e.stop();
				// 	this.fade('out');
				// 	(function(){
				// 		this.destroy();
				// 	}).delay(600, this);
				// }.bind(modal));
			}); // addEvent
		}); // each
	},
	
	submit: function(e) { 
		e.stop();
		var type = $$('input[name=choice]:checked')[0].get('value');
		
		var add_to_extension = (type == 'library' && $('add-new-library').checked);
		var data = {};
		data['full_name'] = $('create-name').get('value');
		data['description'] = $('create-description').get('value');
		if (!add_to_extension) {
			this.createNewItem(data, type);
		} else {
			this.createNewDependency(data);
		}
		return false;
	},
	createNewItem: function(data, type) {
		new Request.JSON({
			url: settings['jp_' + type + '_create_url'],
			data: data,
			method: 'post',
			onSuccess: function(response) {
				window.location.href=response.edit_url;
			}
		}).send();
	},
	createNewDependency: function(data) {
		var lib_data = {
			'name': data.name,
			'description': data.description
		};
		fd.getItem().addNewDependencyRequest(lib_data).send();
	}
};
