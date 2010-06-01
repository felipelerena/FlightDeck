{% load base_helpers %}
fd.item = new Package.View({
	// data
		id_number: '{{ revision.package.id_number|escapejs }}',
		full_name: '{{ revision.package.full_name|escape_js }}',
	// TBC
});

