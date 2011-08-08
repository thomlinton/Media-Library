from fabric.api import *


#
# SETTINGS & COMMANDS
#
python_version = '2.7'
python_executable = 'python%(python_version)s' % {'python_version':python_version}

app_root = '/pub/apps/media_library/'
app_update='git pull'
app_buildout='%(python_executable)s bootstrap.py --distribute && ./bin/buildout -v -c %(build_mode)s.cfg' # % {'python_executable':python_executable}
app_reload='touch ./bin/%(app_driver)s.wsgi'
app_syncdb='./bin/%(app_driver)s syncdb'
app_migrate='./bin/%(app_driver)s migrate'
app_clean_pyc='./bin/%(app_driver)s clean_pyc'
app_collectstatic='./bin/%(app_driver)s collectstatic -v0 --noinput'
app_compress='./bin/%(app_driver)s compress'
app_test='./bin/test'

cmd_reload=app_reload % {'app_driver':'media_library'}
cmd_syncdb=app_syncdb % {'app_driver':'media_library'}
cmd_migrate=app_migrate % {'app_driver':'media_library'}
cmd_clean_pyc=app_clean_pyc % {'app_driver':'media_library'}
cmd_collectstatic=app_collectstatic % {'app_driver':'media_library'}
cmd_compress=app_compress % {'app_driver':'media_library'}

#
# ENVIRONMENT PREPARATION
#
env.hosts = [
    'media@dostoevsky.ninjawirel.us',
]

def set_build_mode(mode):
    print "Build mode: %s" % (mode)
    env.build_mode = mode

def production():
    set_build_mode('production')

def development():
    set_build_mode('development')

def debug():
    set_build_mode('debug')

#
# TASKS
#
def deploy():
    with cd( app_root % {'build_mode':env.build_mode} ):
        run( cmd_app_update )
        run( cmd_syncdb )
        run( cmd_migrate )
        run( cmd_clean_pyc )
        run( cmd_collectstatic )
        run( cmd_compress )
        run( cmd_reload )

def reload():
    with cd( app_root % {'build_mode':env.build_mode} ):
        run( app_reload )

def build():
    with cd( app_root % {'build_mode':env.build_mode} ):
        run( app_buildout % {
                'python_executable':python_executable, 
                'build_mode':env.build_mode})

def bootstrap():
    with cd( app_root % {'build_mode':env.build_mode} ):
        run( app_bootstrap )

def test():
    with cd( app_root % {'build_mode':env.build_mode} ):
        run( app_test )
