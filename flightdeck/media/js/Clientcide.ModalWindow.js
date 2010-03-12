/* 
 * File: Clientcide.ModalWindow.js
 */

var ModalWindow = new Class({
	initialize: function() {
		// this.create();
		this.modal;
	},

	create: function(content) {

		this.modal = new StickyWin({
			content: content,
			relativeTo: $(document.body),
			position: 'cetner',
			edge: 'center',
			closeClassName: 'closeModal',
			draggable: true,
			dragHandleSelector: 'h3',
			closeOnEsc: true,
			destroyOnClose: true,
			allowMultiple: false
		});
		this.modal.show();
		
		return this.modal;
	},

	destroy: function() {
		this.modal.hide();
	}
});