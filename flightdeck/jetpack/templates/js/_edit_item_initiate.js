{% load jetpack_extras %}
{# requires type, item and version #}
item = new {{ type|capfirst }}({
	slug: '{{ item.slug }}',
	name: '{{ item.name }}',
	description: '{{ item.description|escapejs }}',
	creator: '{{ item.creator }}',
	edit_url: '{{ item.get_absolute_url }}',
	update_url: '{{ item.get_update_url }}',
	version_create_url: '{{ item.get_version_create_url }}',
	switch_description_id: '{{ item|tab_link_id:"description" }}',
	{% ifequal type 'jetpack' %}
		try_in_browser_url: '{% url jp_create_xpi %}',
	{% endifequal %}
	version: {
		{% ifequal type 'jetpack' %}
			manifest: '{{ version.manifest|escapejs }}',
			switch_manifest_id: '{{ version|tab_link_id:"manifest" }}',
		{% endifequal %}
		author: '{{ version.author }}',
		name: '{{ version.name }}',
		counter: '{{ version.counter }}',
		content: '{{ version.content|escapejs }}',
		description: '{{ version.description|escapejs }}',
		is_base: {{ version.is_base|yesno:"true,false" }},
		update_url: '{{ version.get_update_url }}',
		{% if version %}
			edit_url: '{{ version.get_absolute_url }}',
			add_dependency_url: '{{ version.get_adddependency_url }}',
			addnew_dependency_url: '{{ version.get_addnewdependency_url }}',
			set_as_base_url: '{{ version.get_set_as_base_url }}',
		{% endif %}
		switch_content_id: '{{ version|tab_link_id:"content" }}',
		switch_description_id: '{{ version|tab_link_id:"version_description" }}'
	}
});

