<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="Content-Script-Type" content="text/javascript" />
  <meta http-equiv="Content-Style-Type" content="text/css" />
  <meta http-equiv="Content-Language" content="en" />
  <meta name="ROBOTS" content="NOARCHIVE,NOINDEX,NOFOLLOW" />
  <meta name="GOOGLEBOT" content="NOSNIPPET" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Dotclear</title>
  <link rel="icon" type="image/png" href="images/favicon96-logout.png" />
  <link rel="shortcut icon" href="../favicon.ico" type="image/x-icon" />


<script src="js/prepend.js?v=2.16.9"></script>
<script src="js/jquery/jquery.js?v=2.16.9"></script>
<script src="js/jquery/jquery.biscuit.js?v=2.16.9"></script>
<script type="application/json" id="dotclear-data">
{"nonce":"f7b79521eafc1a64e83ab2a914f5569615b2abf7f1524190807262bdad0f903bd96a9c24d5dedb9aa4868fe9cc19823d945b22ef941a7a5c2d95cc28ea2d1b54","img_plus_src":"images/expand.png","img_plus_txt":"\u25ba","img_plus_alt":"uncover","img_minus_src":"images/hide.png","img_minus_txt":"\u25bc","img_minus_alt":"hide","img_menu_on":"images/menu_on.png","img_menu_off":"images/menu_off.png","img_plus_theme_src":"images/plus-theme.png","img_plus_theme_txt":"\u25ba","img_plus_theme_alt":"uncover","img_minus_theme_src":"images/minus-theme.png","img_minus_theme_txt":"\u25bc","img_minus_theme_alt":"hide"}
</script><script type="application/json" id="dotclear_msg-data">
{"help":"Need help?","new_window":"new window","help_hide":"Hide","to_select":"Select:","no_selection":"no selection","select_all":"select all","invert_sel":"Invert selection","website":"Web site:","email":"Email:","ip_address":"IP address:","error":"Error:","entry_created":"Entry has been successfully created.","edit_entry":"Edit entry","view_entry":"view entry","confirm_delete_posts":"Are you sure you want to delete selected entries (%s)?","confirm_delete_medias":"Are you sure you want to delete selected medias (%d)?","confirm_delete_categories":"Are you sure you want to delete selected categories (%s)?","confirm_delete_post":"Are you sure you want to delete this entry?","click_to_unlock":"Click here to unlock the field","confirm_spam_delete":"Are you sure you want to delete all spams?","confirm_delete_comments":"Are you sure you want to delete selected comments (%s)?","confirm_delete_comment":"Are you sure you want to delete this comment?","cannot_delete_users":"Users with posts cannot be deleted.","confirm_delete_user":"Are you sure you want to delete selected users (%s)?","confirm_delete_blog":"Are you sure you want to delete selected blogs (%s)?","confirm_delete_category":"Are you sure you want to delete category \"%s\"?","confirm_reorder_categories":"Are you sure you want to reorder all categories?","confirm_delete_media":"Are you sure you want to remove media \"%s\"?","confirm_delete_directory":"Are you sure you want to remove directory \"%s\"?","confirm_extract_current":"Are you sure you want to extract archive in current directory?","confirm_remove_attachment":"Are you sure you want to remove attachment \"%s\"?","confirm_delete_lang":"Are you sure you want to delete \"%s\" language?","confirm_delete_plugin":"Are you sure you want to delete \"%s\" plugin?","confirm_delete_plugins":"Are you sure you want to delete selected plugins?","use_this_theme":"Use this theme","remove_this_theme":"Remove this theme","confirm_delete_theme":"Are you sure you want to delete \"%s\" theme?","confirm_delete_themes":"Are you sure you want to delete selected themes?","confirm_delete_backup":"Are you sure you want to delete this backup?","confirm_revert_backup":"Are you sure you want to revert to this backup?","zip_file_content":"Zip file content","xhtml_validator":"XHTML markup validator","xhtml_valid":"XHTML content is valid.","xhtml_not_valid":"There are XHTML markup errors.","warning_validate_no_save_content":"Attention: an audit of a content not yet registered.","confirm_change_post_format":"You have unsaved changes. Switch post format will loose these changes. Proceed anyway?","confirm_change_post_format_noconvert":"Warning: post format change will not convert existing content. You will need to apply new format by yourself. Proceed anyway?","load_enhanced_uploader":"Loading enhanced uploader, please wait.","module_author":"Author:","module_details":"Details","module_support":"Support","module_help":"Help:","module_section":"Section:","module_tags":"Tags:","close_notice":"Hide this notice"}
</script><script src="js/common.js?v=2.16.9"></script>
<script src="js/services.js?v=2.16.9"></script>
<script src="js/prelude.js?v=2.16.9"></script>

    <link rel="stylesheet" href="style/default.css" type="text/css" media="screen" />

<script src="js/_auth.js?v=2.16.9"></script>
</head>

<body id="dotclear-admin" class="auth">

<form action="auth.php" method="post" id="login-screen">
<h1 role="banner">Dotclear</h1>

<div class="fieldset" role="main"><p><label for="user_id">Username:</label> <input type="text" size="20" name="user_id" id="user_id" maxlength="32" autocomplete="username"  />
</p><p><label for="user_pwd">Password:</label> <input type="password" size="20" name="user_pwd" id="user_pwd" maxlength="255" autocomplete="current-password"  />
</p><p><input type="checkbox" name="user_remember" value="1" id="user_remember"  />
<label for="user_remember" class="classic">Remember my ID on this device</label></p><p><input type="submit" value="log in" class="login" /></p></div><p id="cookie_help" class="error">You must accept cookies in order to use the private area.</p><div id="issue"><p id="more"><strong>Connection issue?</strong></p><p><a href="auth.php?recover=1">I forgot my password</a></p><p><a href="auth.php?safe_mode=1" id="safe_mode_link">I want to log in in safe mode</a></p></div></form>
</body>
</html>
