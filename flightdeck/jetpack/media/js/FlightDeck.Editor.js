/*
 * Extending Flightdeck with Editor functionality 
 */

FlightDeck = Class.refactor(FlightDeck,{
	options: {
		file_selected_class: 'UI_File_Selected',
		file_normal_class: 'UI_File_Normal',
		file_listing_class: 'UI_File_Listing'
	},
	initialize: function(options) {
		this.setOptions(options);
		this.previous(options);
		var file_selected_class = this.options.file_selected_class;
		var file_normal_class = this.options.file_normal_class;
		var switch_mode_on  = function() {
			$$('.' + file_selected_class).each(function(el) {
				el.switch_mode_off();
			});
			this.removeClass(file_normal_class)
				.addClass(file_selected_class);
		};
		var switch_mode_off = function() {
			this.removeClass(file_selected_class)
				.addClass(file_normal_class);
		};
		$$('.'+this.options.file_listing_class + ' li').each(function(file_el) {
			file_el.switch_mode_on = switch_mode_on;
			file_el.switch_mode_off = switch_mode_off;
		});
		$$('.'+this.options.file_listing_class).each(function(container) { 
			container.addEvent('click:relay(li a)', function(e, el) {
				var li = $(el).getParent('li');
				if (!li.switch_mode_on) li.switch_mode_on = switch_mode_on;
				if (!li.switch_mode_off) li.switch_mode_off = switch_mode_off;
				li.switch_mode_on();
			});
		});
		this.enableMenuButtons();
	},
	/*
	 * Method: getItem
	 */
	getItem: function() {
		// item is currently a global 
		return this.item;
	},
	/*
	 * Method: enableMenuButtons
	 * Switch on menu buttons, check if possible
	 */
	enableMenuButtons: function() {
		$$('.' + this.options.menu_el + ' li.disabled').each(function(menuItem){
			var switch_on = true;
			if (switch_on) {
				menuItem.removeClass('disabled');
			}
		}, this);
	}
	
});
