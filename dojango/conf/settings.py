import os
from django.conf import settings

DEBUG = getattr(settings, "DEBUG", False)
DEFAULT_CHARSET = getattr(settings, 'DEFAULT_CHARSET', 'utf-8')

DOJO_VERSION = getattr(settings, "DOJANGO_DOJO_VERSION", "1.2.0")
DOJO_PROFILE = getattr(settings, "DOJANGO_DOJO_PROFILE", "aol")

BASE_MEDIA_URL = getattr(settings, "DOJANGO_BASE_MEDIA_URL", '/dojango/media')
BUILD_MEDIA_URL = getattr(settings, "DOJANGO_BUILD_MEDIA_URL", '%s/release' % BASE_MEDIA_URL)
BASE_MEDIA_ROOT = getattr(settings, "DOJANGO_BASE_MEDIA_ROOT", os.path.abspath(os.path.dirname(__file__)+'/../media/'))
BASE_DOJO_ROOT = getattr(settings, "DOJANGO_BASE_DOJO_ROOT", BASE_MEDIA_ROOT + "/dojo")
# as default the dijit theme folder is used
DOJO_THEME_URL = getattr(settings, "DOJANGO_DOJO_THEME_URL", False)
DOJO_THEME = getattr(settings, "DOJANGO_DOJO_THEME", "tundra")
DOJO_DEBUG = getattr(settings, "DOJANGO_DOJO_DEBUG", DEBUG) # using the default django DEBUG setting
DOJO_SECURE_JSON = getattr(settings, "DOJANGO_DOJO_SECURE_JSON", True) # if you are using dojo version < 1.2.0 you have set it to False

# set the urls for actual possible paths for dojo
# one dojo profile must at least contain a path that defines the base url of a dojo installation
# the following settings can be set for each dojo profile:
# - base_url: where do the dojo files reside (without the version folder!)
# - use_xd: use the crossdomain-build? used to build the correct filename (e.g. dojo.xd.js)
# - versions: this list defines all possible versions that are available in the defined profile
# - uncompressed: use the uncompressed version of dojo (dojo.xd.js.uncompressed.js)
# - use_gfx: there is a special case, when using dojox.gfx from aol (see http://dev.aol.com/dojo)
# - is_local: marks a profile being local. this is needed when using the dojo module loader
# - is_local_build: profile being a locally builded version
_aol_versions = ('0.9.0', '1.0.0', '1.0.2', '1.1.0', '1.1.1', '1.2.0',)
_google_versions = ('1.1.1', '1.2.0',)
DOJO_PROFILES = {
    'google': {'base_url':'http://ajax.googleapis.com/ajax/libs/dojo', 'use_xd':True, 'versions':_google_versions}, # google just supports version >= 1.1.1
    'google_uncompressed': {'base_url':'http://ajax.googleapis.com/ajax/libs/dojo', 'use_xd':True, 'uncompressed':True, 'versions':_google_versions},
    'aol': {'base_url':'http://o.aolcdn.com/dojo', 'use_xd':True, 'versions':_aol_versions},
    'aol_uncompressed': {'base_url':'http://o.aolcdn.com/dojo', 'use_xd':True, 'uncompressed':True, 'versions':_aol_versions},
    'aol_gfx': {'base_url':'http://o.aolcdn.com/dojo', 'use_xd':True, 'use_gfx':True, 'versions':_aol_versions},
    'aol_gfx-uncompressed': {'base_url':'http://o.aolcdn.com/dojo', 'use_xd':True, 'use_gfx':True, 'uncompressed':True, 'versions':_aol_versions},
    'local': {'base_url': '%(BASE_MEDIA_URL)s/dojo', 'is_local':True}, # we don't have a restriction on version names, name them as you like
    'local_release': {'base_url': '%(BUILD_MEDIA_URL)s', 'is_local':True, 'is_local_build':True}, # this will be available after the first dojo build!
    'local_release_uncompressed': {'base_url': '%(BUILD_MEDIA_URL)s', 'uncompressed':True, 'is_local':True, 'is_local_build':True} # same here
}

# we just want users to append/overwrite own profiles
DOJO_PROFILES.update(getattr(settings, "DOJANGO_DOJO_PROFILES", {}))

# =============================================================================================
# =================================== NEEDED FOR DOJO BUILD ===================================
# =============================================================================================
# general doc: http://dojotoolkit.org/book/dojo-book-0-9/part-4-meta-dojo/package-system-and-custom-builds
# see http://www.sitepen.com/blog/2008/04/02/dojo-mini-optimization-tricks-with-the-dojo-toolkit/ for details
DOJO_BUILD_VERSION = getattr(settings, "DOJANGO_DOJO_BUILD_VERSION", "1.1.1")
# this is the default build profile, that is used, when calling "./manage.py dojobuild"
# "./manage.py dojobuild dojango" would would have the same effect
DOJO_BUILD_PROFILE = getattr(settings, "DOJANGO_DOJO_BUILD_PROFILE", "dojango")
# This dictionary defines your build profiles you can use within the custom command "./manage.py dojobuild
# You can set your own build profile within the main settings.py of the project by defining a dictionary
# DOJANGO_DOJO_BUILD_PROFILES, that sets the following key/value pairs for each defined profile name:
#   profile_file: which dojo profile file is used for the build (see dojango.profile.js how it must look like)
#   options: these are the options that are passed to the build command (see the dojo doc for details)
#   OPTIONAL SETTINGS (see DOJO_BUILD_PROFILES_DEFAULT):
#   base_root: in which directory will the dojo version be builded to? 
#   used_src_version: which version should be used for the dojo build (e.g. 1.1.1)
#   build_version: what is the version name of the builded release (e.g. dojango1.1.1) - this option can be overwritten by the commandline parameter --build_version=...
DOJO_BUILD_PROFILES = {
    'dojango': {
        'profile_file': '%(BASE_MEDIA_ROOT)s/dojango.profile.js',
        'options': 'profile=dojango action=release optimize=shrinksafe.keepLines cssOptimize=comments.keepLines'
    },
    'dojango_optimized': {
        'profile_file': '%(BASE_MEDIA_ROOT)s/dojango_optimized.profile.js',
        'options': 'profile=dojango_optimized action=release optimize=shrinksafe.keepLines cssOptimize=comments.keepLines',
        'build_version': 'dojango-optimized-with-dojo%(DOJO_BUILD_VERSION)s',
    },
}

# these defaults are mixed into each DOJO_BUILD_PROFILES element
# but you can overwrite each attribute within your own build profile element
# e.g. DOJANGO_BUILD_PROFILES = {'used_src_version': '1.2.2', ....}
DOJO_BUILD_PROFILES_DEFAULT = getattr(settings, "DOJANGO_DOJO_BUILD_PROFILES_DEFAULT", {
    # build the release in the media directory of dojango
    # use a formatting string, so this can be set in the project's settings.py without getting the dojango settings
    'base_root': '%(BASE_MEDIA_ROOT)s/release',
    'used_src_version': '%(DOJO_BUILD_VERSION)s',
    'build_version': 'dojango-with-dojo%(DOJO_BUILD_VERSION)s',
})
# TODO: we should also enable the already pre-delivered dojo default profiles

# you can add/overwrite your own build profiles
DOJO_BUILD_PROFILES.update(getattr(settings, "DOJANGO_DOJO_BUILD_PROFILES", {}))
DOJO_BUILD_JAVA_EXEC = getattr(settings, 'DOJANGO_DOJO_BUILD_JAVA_EXEC', 'java')
