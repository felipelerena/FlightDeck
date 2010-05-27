let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 /private/tmp/------------Jetpack
badd +53 ~/Projects/FlightDeck/flightdeck/jetpack/views.py
badd +187 ~/Projects/FlightDeck/flightdeck/jetpack/models.py
badd +169 ~/Projects/FlightDeck/flightdeck/jetpack/tests/module_tests.py
badd +7 ~/Projects/FlightDeck/flightdeck/jetpack/managers.py
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/admin.py
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/urls.py
badd +16 ~/Projects/FlightDeck/flightdeck/jetpack/errors.py
badd +10 ~/Projects/FlightDeck/flightdeck/jetpack/default_settings.py
badd +1 /private/tmp/---old
badd +62 ~/Projects/FlightDeck/flightdeck/jetpack/views_old.py
badd +7 ~/Projects/FlightDeck/flightdeck/jetpack/managers_old.py
badd +8 ~/Projects/FlightDeck/flightdeck/jetpack/models_old.py
badd +4 ~/Projects/FlightDeck/flightdeck/jetpack/tests_old.py
badd +3 ~/Projects/FlightDeck/flightdeck/jetpack/urls_old.py
badd +1 /private/tmp/----------Jtemplates
badd +4 ~/Projects/FlightDeck/flightdeck/jetpack/templates/package_browser.html
badd +4 ~/Projects/FlightDeck/flightdeck/jetpack/templates/package_browser_addons.html
badd +23 ~/Projects/FlightDeck/flightdeck/jetpack/templates/package_browser_libraries.html
badd +15 ~/Projects/FlightDeck/flightdeck/jetpack/templates/package_browser_user_addons.html
badd +15 ~/Projects/FlightDeck/flightdeck/jetpack/templates/package_browser_user_libraries.html
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates/_package_browser_addons_list.html
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates/_package_browser_libraries_list.html
badd +25 ~/Projects/FlightDeck/flightdeck/jetpack/templates/_package_browser_addon.html
badd +7 ~/Projects/FlightDeck/flightdeck/jetpack/templates/_package_browser_library.html
badd +1 /private/tmp/----------Jtemplates_old
badd +37 ~/Projects/FlightDeck/flightdeck/jetpack/templatetags/jetpack_extras.py
badd +21 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/editor.html
badd +7 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/edit_item.html
badd +11 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_addnew_dependency_window.html
badd +16 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_dependency_list.html
badd +2 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_dependency_list_item.html
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_dependency_content_textarea.html
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_editor_menu.html
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_edit_page_title.html
badd +6 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_edit_item_parts.html
badd +2 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_edit_item_info.html
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_edit_recently_modified.html
badd +5 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_edit_editors.html
badd +5 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_dependency_add.html
badd +29 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_create.html
badd +1 /private/tmp/----------JGtemp
badd +25 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/gallery.html
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/_gallery_item_link.html
badd +1 /private/tmp/----------JJSON
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/capability_created.json
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/capability_updated.json
badd +11 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/dependency_added.json
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/dependency_removed.json
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/jetpack_created.json
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/jetpack_updated.json
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/version_absolute_url.json
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/version_updated.json
badd +4 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/xpi_created.json
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/json/versions.json
badd +1 /private/tmp/----------JJS
badd +21 ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/js/_edit_item_initiate.js
badd +1 /private/tmp/---------JJavascript
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/Capability.js
badd +52 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/Jetpack.js
badd +120 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/CapDependency.js
badd +38 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/Create.js
badd +37 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/Editor.js
badd +39 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/Bespin.js
badd +79 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/CodeMirror.js
badd +10 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/FlightDeck.Editor.js
badd +33 ~/Projects/FlightDeck/flightdeck/jetpack/media/js/FlightDeck.Browser.js
badd +1 /private/tmp/------------JCSS
badd +16 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Base.css
badd +54 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Browser.css
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Editor.css
badd +11 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Editor_Area.css
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Editor_Menu.css
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.File_Listing.css
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Forms.css
badd +72 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Layout.css
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Modal.css
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Reset.css
badd +21 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/UI.Sidebar.css
badd +1 ~/Projects/FlightDeck/flightdeck/jetpack/media/css/edit.css
badd +1 /private/tmp/-----------Base
badd +3 ~/Projects/FlightDeck/flightdeck/base/views.py
badd +67 ~/Projects/FlightDeck/flightdeck/base/templates/base.html
badd +6 ~/Projects/FlightDeck/flightdeck/base/templates/_header.html
badd +109 ~/Projects/FlightDeck/flightdeck/media/js/FlightDeck.js
badd +26 ~/Projects/FlightDeck/flightdeck/media/js/Clientcide.ModalWindow.js
badd +23 ~/Projects/FlightDeck/flightdeck/media/js/FlightDeck.Roar.js
badd +12 ~/Projects/FlightDeck/flightdeck/media/js/FlightDeck.Modal.js
badd +118 ~/Projects/FlightDeck/flightdeck/settings.py
badd +1 ~/Projects/FlightDeck/flightdeck/urls.py
badd +34 ~/Projects/FlightDeck/flightdeck/settings_local-default.py
badd +33 ~/Projects/FlightDeck/flightdeck/settings_local.py
badd +1 ~/Projects/FlightDeck/flightdeck/utils/os_utils.py
badd +39 ~/Projects/FlightDeck/flightdeck/base/templates/homepage.html
badd +1 /private/tmp/------------Person
badd +30 ~/Projects/FlightDeck/flightdeck/person/views.py
badd +34 ~/Projects/FlightDeck/flightdeck/person/templates/dashboard.html
badd +10 ~/Projects/FlightDeck/flightdeck/person/templates/profile.html
badd +12 ~/Projects/FlightDeck/flightdeck/person/templates/_profile_info.html
badd +29 ~/Projects/FlightDeck/flightdeck/person/templates/registration/login.html
badd +9 ~/Projects/FlightDeck/flightdeck/person/urls.py
badd +1 /private/tmp/------------API
badd +61 ~/Projects/FlightDeck/flightdeck/api/views.py
badd +1 ~/Projects/FlightDeck/flightdeck/api/models.py
badd +7 ~/Projects/FlightDeck/flightdeck/api/default_settings.py
badd +15 ~/Projects/FlightDeck/flightdeck/api/tests.py
badd +2 ~/Projects/FlightDeck/flightdeck/api/templates/module_doc.html
badd +19 ~/Projects/FlightDeck/flightdeck/api/templates/package_doc.html
badd +5 ~/Projects/FlightDeck/flightdeck/api/urls.py
badd +1 ~/Projects/FlightDeck/flightdeck/api/templates/_modules_list.html
badd +1 ~/Projects/FlightDeck/flightdeck/api/templates/_entity_property.html
badd +1 ~/Projects/FlightDeck/flightdeck/api/templates/_entity_method.html
badd +1 ~/Projects/FlightDeck/flightdeck/api/media/js/API.Browser.js
badd +1 ~/Projects/FlightDeck/flightdeck/api/media/js/Browse.js
badd +1 ~/Projects/FlightDeck/flightdeck/api/templates/api.html
badd +12 ~/Projects/FlightDeck/flightdeck/api/media/css/API.Browser.css
badd +1 /private/tmp/------------scripts
badd +18 ~/Projects/FlightDeck/scripts/install.sh
badd +117 ~/Projects/FlightDeck/scripts/upgrade.sh
badd +12 ~/Projects/FlightDeck/scripts/environment.sh
badd +1 ~/Projects/FlightDeck/scripts/setenv.sh
badd +3 ~/Projects/FlightDeck/scripts/rundevserver.sh
badd +1 ~/Projects/FlightDeck/scripts/config.sh
badd +9 ~/Projects/FlightDeck/scripts/config_local-default.sh
badd +3 ~/Projects/FlightDeck/scripts/config_local.sh
badd +1 ~/Projects/FlightDeck/scripts/django-admin.sh
badd +1 ~/Projects/FlightDeck/scripts/graphviz.sh
badd +6 ~/Projects/FlightDeck/scripts/initiate.sh
badd +1 ~/Projects/FlightDeck/scripts/runserver.sh
badd +1 ~/Projects/FlightDeck/scripts/syncdb.sh
badd +1 ~/Projects/FlightDeck/scripts/test.sh
badd +16 ~/Projects/FlightDeck/tools/pip-requirements.txt
badd +1 ~/Projects/FlightDeck/scripts/cfx.sh
badd +17 ~/Projects/FlightDeck/tools/git-exclude
badd +30 ~/Projects/FlightDeck/apache/config_local-default.wsgi
badd +1 /private/tmp/------------AMO
badd +4 ~/Projects/FlightDeck/flightdeck/amo/default_settings.py
badd +1 tmp/-----------DOCS
badd +15 ~/Projects/FlightDeck/Docs/mozillaaddonbuilderstyle.sty
badd +22 ~/Projects/FlightDeck/README
badd +22 ~/Projects/FlightDeck/INSTALL
silent! argdel *
edit ~/Projects/FlightDeck/flightdeck/jetpack/templates_old/editor.html
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 21 - ((20 * winheight(0) + 29) / 59)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
21
normal! 0
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=1 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
