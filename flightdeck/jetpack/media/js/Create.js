/*
 * File: jetpack/Create.js
 */
/*
 * Class Create
 * Create new Jetpack/Capability
 */

var create = {
	init: function(create_id, wrapper_id) {
		$(create_id).addEvent('click', function(e) {
			e.stop();
			var modal = fd.displayModal(settings.create_modal_template, wrapper_id);

			$('create_form').addEvent('submit', this.submit.bind(this));
			$('create_form_cancel').addEvent('click', function(e) {
				e.stop();
				this.fade('out');
				(function(){
					this.destroy();
				}).delay(600, this);
			}.bind(modal));
		}.bind(this));
	},
	submit: function(e) { 
		e.stop();
		var prefix = $$('input[name=choice]:checked')[0].get('value');
		var data = {};
		data[prefix+'_name'] = $('create-name').get('value');
		data[prefix+'_description'] = $('create-description').get('value');
		new Request.JSON({
			url: settings['jp_' + prefix + '_create_url'],
			data: data,
			method: 'post',
			onSuccess: function(response) {
				window.location.href=response.absolute_url;
			}
		}).send();
		return false;
	}
};