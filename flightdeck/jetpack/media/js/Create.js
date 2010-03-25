/*
 * File: jetpack/Create.js
 */
/*
 * Class Create
 * Create new Jetpack/Capability
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
				fd.addnewDependencyModal = fd.displayModal(settings.create_modal_template, wrapper_id);
				if (create_item && create_item[idx] && create_item[idx]) {
					$('create-'+create_item[idx]).set('checked', 'checked');
				} 
				
				if (fd.getItem) {
					$$('#create_form input[type=radio]').addEvent('change', function() {
						if ($('create-capability').checked) {
							$('add-new-capability-li')
								.removeClass('hidden')
								.show();
						} else {
							$('add-new-capability-li').hide();
						}
					});
				} 
				$('create_form').addEvent('submit', boundSubmit);
				// $('create_form_cancel').addEvent('click', function(e) {
				// 	e.stop();
				// 	this.fade('out');
				// 	(function(){
				// 		this.destroy();
				// 	}).delay(600, this);
				// }.bind(modal));
			});
		}); 
	},
	
	submit: function(e) { 
		e.stop();
		var prefix = $$('input[name=choice]:checked')[0].get('value');
		var add_to_extension = (prefix == 'capability' && $('add-new-capability').checked);
		var data = {};
		data[prefix+'_name'] = $('create-name').get('value');
		data[prefix+'_description'] = $('create-description').get('value');
		if (!add_to_extension) {
			this.createNewItem(data, prefix);
		} else {
			this.createNewDependency(data);
		}
		return false;
	},
	createNewItem: function(data, prefix) {
		new Request.JSON({
			url: settings['jp_' + prefix + '_create_url'],
			data: data,
			method: 'post',
			onSuccess: function(response) {
				window.location.href=response.absolute_url;
			}
		}).send();
	},
	createNewDependency: function(data) {
		var cap_data = {
			'capability_name': data.capability_name,
			'capability_description': data.capability_description
		};
		fd.getItem().addNewDependencyRequest(cap_data).send();
	}
};
