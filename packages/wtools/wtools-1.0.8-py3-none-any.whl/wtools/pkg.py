#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os, sys, tempfile, shutil, json, subprocess, tarfile, glob, platform, pathlib
import jsonschema
import waflib
from waflib import Logs, Build, Scripting, Errors, Context
import wtools


SYSTEMD_LOCATIONS = ('/etc/systemd/system', '/usr/lib/systemd/system', '/usr/local/lib/systemd/system')


def set_pkg_default(conf, key, value, islist=False):
    if key in os.environ.keys():
        value = os.environ[key]
        value = value.split(':') if islist else value
    conf.env[key] = list(value) if islist else value


def options(opt):
    opt.add_option('--pkg-prefix', dest='pkg_prefix', default=None, action='store', help='package installation prefix, overrides ${PREFIX} when packaging')
    opt.add_option('--pkg-bindir', dest='pkg_bindir', default=None, action='store', help='binary installation prefix, overrides ${BINDIR} when packaging')
    opt.add_option('--pkg-libdir', dest='pkg_libdir', default=None, action='store', help='library installation prefix, overrides ${LIBDIR} when packaging')
    opt.add_option('--pkg-type', dest='pkg_type', default=None, action='store', help='packaging type (rpm|deb|ipkg)')
    opt.add_option('--pkg-rpm', dest='pkg_rpm', default=False, action='store_true', help='use rpm packaging')
    opt.add_option('--pkg-deb', dest='pkg_deb', default=False, action='store_true', help='use debian packaging')
    opt.add_option('--pkg-recipe', dest='pkg_recipe', default=None, action='store', help='packaging recipe file')
    opt.add_option('--pkg-platform', dest='pkg_platform', default=None, action='store', help='(cross) platform package information')
    opt.add_option('--pkg-platform-id', dest='pkg_platform_id', default=None, action='store', help='(cross) platform identifier')
    opt.add_option('--pkg-nostrip', dest='pkg_nostrip', default=False, action='store_true', help='do not strip binaries in packages')
    opt.add_option('--pkg-outdir', dest='pkg_outdir', default=None, action='store', help='location to store packages')
    opt.add_option('--pkg-dummy', dest='pkg_dummy', default=False, action='store_true', help='skips packaging')


def configure(conf):
    if conf.options.pkg_dummy:
        conf.env.PKG_DUMMY = ["1"]
        return

    if not conf.options.pkg_nostrip:
        conf.find_program('strip', var='STRIP', mandatory=False)

    conf.find_program('rpmbuild', var='RPMBUILD_BIN', mandatory=False)
    conf.find_program('dpkg-deb', var='DPKG_DEB_BIN', mandatory=False)
    conf.find_program('ipkg-build', var='IPKG_BUILD_BIN', mandatory=False)

    # configure packaging type to be used
    pkg_type = get_pkg_type(conf, detect=True)
    if pkg_type:
        conf.env.PKG_TYPE = pkg_type

    # define out (default) installation prefixes when creating package(s)
    if conf.options.pkg_prefix:
        conf.env.PKG_PREFIX = conf.options.pkg_prefix
    if conf.options.pkg_bindir:
        conf.env.PKG_BINDIR = conf.options.pkg_bindir
    if conf.options.pkg_libdir:
        conf.env.PKG_LIBDIR = conf.options.pkg_libdir

    # define out location for created package(s)
    if conf.options.pkg_outdir:
        conf.env.PKG_OUTDIR = conf.options.pkg_outdir
    else:
        conf.env.PKG_OUTDIR = getattr(Context.g_module, Context.TOP, conf.srcnode.abspath())

    # detect cross compiler prefix (if any) and/or target platform
    if 'RPM_TARGET' in os.environ:
        conf.env.PKG_RPM_TARGET = str(os.environ['RPM_TARGET'])
    if 'ARCH' in os.environ:
        conf.env.PKG_ARCH = str(os.environ['ARCH'])
    else:
        arch = str(conf.env.DEST_CPU)
        if arch in ('x86_64', 'x86-64'):
            arch = 'amd64'
        conf.env.PKG_ARCH = arch

    # define default packaging settings
    conf.env.PKG_NAME = getattr(Context.g_module, Context.APPNAME, 'noname')
    conf.env.PKG_VERSION = getattr(Context.g_module, Context.VERSION, '1.0')
    set_pkg_default(conf, 'PKG_SUMMARY', 'package description')
    set_pkg_default(conf, 'PKG_RELEASE', '1')
    set_pkg_default(conf, 'PKG_LICENSE', 'GPLv2')
    set_pkg_default(conf, 'PKG_GROUP', 'Development/tools')
    set_pkg_default(conf, 'PKG_URL', 'https://example.com')
    set_pkg_default(conf, 'PKG_RELOCATIONS', '')
    set_pkg_default(conf, 'PKG_DESCRIPTION', 'detailed package description')
    set_pkg_default(conf, 'PKG_REQUIRES', '') # MUST be RPM style dependencies use comma separators
    set_pkg_default(conf, 'PKG_SECTION', 'misc')
    set_pkg_default(conf, 'PKG_MAINTAINER', 'john.doe@example.com')
    set_pkg_default(conf, 'PKG_IGNORES', ['README.md', 'CHANGELOG.md', 'include'], islist=True)
    set_pkg_default(conf, 'PKG_EXCLUDES', [], islist=True)
    set_pkg_default(conf, 'PKG_INCLUDES', [], islist=True)
    set_pkg_default(conf, 'PKG_TRANSLATIONS', [], islist=True)
    set_pkg_default(conf, 'PKG_CONFIG', 'default')

    # use recipe file containing packaging meta-information
    parse_pkg_recipe(conf, conf.options.pkg_recipe)

    # use platform file containing information on provided package information
    parse_pkg_platform(conf, conf.options.pkg_platform, conf.options.pkg_platform_id)

    # overwrite recipe with environment variables
    parse_pkg_environment(conf)

    # determine DEBIAN style dependencies when not defined yet
    if not 'PKG_DEPENDS' in conf.env:
        conf.env.PKG_DEPENDS = debian_get_depends(conf.env.PKG_REQUIRES)


def detect_pkg_type(ctx):
    if sys.platform != ctx.env.DEST_OS:
        return None
    if platform.machine() != ctx.env.DEST_CPU:
        return None

    try:
        with open('/etc/os-release') as f:
            s = [s.lstrip('ID_LIKE=') for s in f.read().splitlines() if s.startswith('ID_LIKE')]
            s = [t.lower() for t in s[0].split()]

        if set(s) & set(('debian', 'ubuntu')):
            return 'deb'
    
        if set(s) & set(('rhel', 'fedora', 'centos', 'suse')):
            return 'rpm'

    except Exception:
        pass

    return None


def get_pkg_type(ctx, detect=False):
    pkg_type = ctx.options.pkg_type
    if not pkg_type:
        if ctx.options.pkg_rpm:
            pkg_type = 'rpm'
        elif ctx.options.pkg_deb:
            pkg_type = 'deb'
        elif detect:
            pkg_type = detect_pkg_type(ctx)

        if not pkg_type:
            return None
    
    pkg_type = pkg_type.lower().lstrip('.')
    if pkg_type not in ('rpm', 'deb', 'opkg', 'ipkg', 'ipk'):
        ctx.fatal('Illegal packaging type: %s' % ctx.options.pkg_type)
    
    if pkg_type in ('opkg', 'ipkg', 'ipk'):
        pkg_type = 'ipkg'
        
    return pkg_type


def get_pkg_value(conf, key, pkg):
    val = pkg[key]
    key = key.lower()

    if key == 'name': # special treatment for package name
        if not len(val) or val.isspace():
            val = str(conf.env.PKG_NAME) 
        return val.replace(' ', '').replace('--', '-').replace('_', '-')
    elif key == 'requires': # join RPM requires
        return ', '.join(val)
    else:
        return val


def parse_pkg_recipe(conf, fname):
    if not fname or not os.path.exists(fname):
        return

    with open(fname) as f:
        s = json.load(f)

    with open("%s/data/pkg-recipe.schema.json" % (wtools.location)) as f:
        schema = json.loads(f.read())

    try:
        jsonschema.validate(instance=s, schema=schema)
    except Exception as e:
        conf.fatal('package recipe error({}): {} '.format(fname,e))
        
    for k in s['global'].keys():
        conf.env['PKG_%s' % k.upper()] = s['global'][k]

    packages = s['packages']
    conf.env.PKG_COUNT = str(len(packages))
    i = 0
    for pkg in packages:
        i += 1
        for k in ("description", "requires", "name", "ignores", "excludes", "includes", "translations", "config"):
            if k in pkg:
                conf.env['PKG%i_%s' % (i, k.upper())] = get_pkg_value(conf, k, pkg)
        if 'requires' in pkg:
            conf.env['PKG%i_DEPENDS' % i] = debian_get_depends(conf.env['PKG%i_REQUIRES' % i])


def transform(rule: str, pkg: dict) -> str:
    rule = rule.replace('(', '').replace(')', '')
    name = pkg['name']
    ver = pkg['version'] if 'version' in pkg else None
    aliases = [name] + pkg['aliases'] 
    
    if not any(x in rule for x in aliases):
        return rule

    rules = []
    for r in rule.split(','):
        x = r.strip().split(' ')
        for a in aliases:
            if a == x[0]:
                x = [name, x[1], ver if ver else x[2]]
        rules.append(' '.join(x))

    return ', '.join(rules)


def parse_pkg_platform_requires(conf, pform: dict):
    nrel = int(conf.env.PKG_COUNT)
    packages = pform['packages']

    for p in packages:
        for i in range(nrel):
            key = 'PKG{}_REQUIRES'.format(i+1)
            requires = conf.env[key]
            if requires:
                conf.env[key] = transform(requires, p)

            key = 'PKG{}_DEPENDS'.format(i+1)
            depends = conf.env[key]
            if depends:
                conf.env[key] = debian_get_depends(transform(depends, p))


def parse_pkg_platform(conf, fname: str or None, pformid: str or None):
    if not fname or not os.path.exists(fname):
        return

    with open(fname) as f:
        s = json.load(f)

    with open("%s/data/pkg-platform.schema.json" % (wtools.location)) as f:
        schema = json.loads(f.read())

    try:
        jsonschema.validate(instance=s, schema=schema)
    except Exception as e:
        conf.fatal('platform recipe error({}): {} '.format(fname,e))

    native = (conf.env.DEST_OS == sys.platform) and (conf.env.DEST_CPU == platform.processor())
    platforms = s['platforms']

    if pformid:
        if ':' not in pformid:
            conf.fatal('illegal platform identifier specifier identifier(<ID:VERSION>)')
        pi, ver = pformid.split(':', maxsplit=1)

    elif native:
        with open('/etc/os-release') as f:
            s = f.read().splitlines()
        x = [i.replace('"', '') for i in s]
        d = dict([i.split('=', maxsplit=1) for i in x])
        pi = d['ID']
        ver = d['VERSION_ID']

    else:
        mach = subprocess.check_output([conf.env.CC, '-dumpmachine'])
        ver = subprocess.check_output([conf.env.CC, '-dumpversion'])
        pi = '{}-{}'.format(mach, ver)

    i = 0
    for pform in platforms:
        ids = [pform['id']] + pform['aliases']
        if pi not in ids or ver not in pform['versions']:
            i += 1
            continue

        conf.env.PKG_PLATFORM_ID = str(i+1)
        parse_pkg_platform_requires(conf, pform)
        return # success

    if pformid:
        conf.fatal('platform({}:{}) not found in "{}"'.format(pi, ver, fname))
    else:
        Logs.warn('platform({}:{}) not found in "{}"'.format(pi, ver, fname))


def parse_pkg_environment(conf):
    pre = ['']
    env = os.environ
    try:
        num = int(env['PKG_NUM'])
        if num > 1:
            pre += [str(i) for i in range(1, num+1)]
    except:
        pass

    for k in env.keys():
        for p in pre:
            if k.startswith('PKG%s_' % p):
                v = env[k]
                conf.env[k.upper()] = v.split(':') if isinstance(conf.env[k.upper()], list) else v

    for p in pre:
        d = 'PKG%s_DEPENDS' % p
        if d not in conf.env.keys():
            conf.env[d] = debian_get_depends(conf.env['PKG%s_REQUIRES' % p])


def debian_get_depends(v: str) -> str:
    if not v:
        return ''
    else:
        s = [i.split() for i in v.split(',')]
        keys = [i[0] for i in s]
        values = []
        for vals in [i[1:] for i in s]:
            vals = ['<<' if v=='<' else v for v in vals]
            vals = ['>>' if v=='>' else v for v in vals]
            values.append(vals)
        s = []
        for k,v in zip(keys,values):
            s.append("%s (%s)" % (k,' '.join(v)))
        return ', '.join(s)


class PackageContext(Build.InstallContext):
    '''package binary build results using DPKG, RPM or IPKG.'''
    cmd = 'pkg'

    def __init__(self, **kw):
        super(PackageContext, self).__init__(**kw)

    def _get_task_generators(self):
        tgens = []
        for group in self.groups:
            for tg in group:
                tgens.append(tg)
        return list(set(tgens))

    def get_pkg_environment(self, c: int) -> dict:
        env = dict()
        for k in self.env:
            if not k.startswith('PKG_'):
                continue
            env[k] = self.env[k]

        if self.options.pkg_outdir:
            env['PKG_OUTDIR'] = self.options.pkg_outdir

        if c:
            for k in self.env:
                pre = 'PKG%i_' % c
                if not k.startswith(pre):
                    continue
                env[k.replace(pre, 'PKG_')] = self.env[k]
        return env

    def get_pkg_environments(self) -> list:
        cnt = []
        try:
            cnt = int(self.env.PKG_COUNT)
            cnt = [i for i in range(1, cnt+1)]
        except:
            cnt = [0]
        envs = []
        for c in cnt:
            envs.append(self.get_pkg_environment(c))
        return envs

    def execute(self):
        self.restore()
        if not self.all_envs:
            self.load_envs()

        if self.options.pkg_dummy or self.env.PKG_DUMMY:
            Logs.info('skip packaging')
            return

        try:
            srcdir = tempfile.mkdtemp()
            self.options.destdir=srcdir

            if 'PKG_PREFIX' in self.env:
                self.env.PREFIX=self.env.PKG_PREFIX
                self.env.BINDIR=self.env.PKG_BINDIR if 'PKG_BINDIR' in self.env else os.path.join(self.env.PKG_PREFIX, 'bin')
                self.env.LIBDIR=self.env.PKG_LIBDIR if 'PKG_LIBDIR' in self.env else os.path.join(self.env.PKG_PREFIX, 'lib')
            else:
                self.env.BINDIR=self.env.PKG_BINDIR if 'PKG_BINDIR' in self.env else self.env.BINDIR
                self.env.LIBDIR=self.env.PKG_BINDIR if 'PKG_LIBDIR' in self.env else self.env.LIBDIR

            self.execute_build()

            for env in self.get_pkg_environments():
                try:
                    tmp = tempfile.mkdtemp()
                    self.package(srcdir, tmp, env)
                finally:
                    shutil.rmtree(tmp)
        finally:
            shutil.rmtree(srcdir)

    def get_pkg_prefixes(self) -> list:
        try:
            c = int(self.env.PKG_COUNT)
            pre = [''] + [str(i) for i in range(1, c+1)]
            return ['PKG%s_' % p for p in pre]
        except:
            return ['PKG_']

    def package(self, srcdir: str, tmp: str, env: dict):
        pkg_type = get_pkg_type(self) if self.options.pkg_type or self.options.pkg_rpm or self.options.pkg_deb else self.env.PKG_TYPE
        name = env['PKG_NAME']
        version = env['PKG_VERSION']
        release = '%s-%s' % (name, version)

        if self.options.verbose >= 1:
            Logs.info('package({}:{})'.format(name, version))

        # (0) define destination directory; i.e. 'waf --destdir'
        if pkg_type == 'rpm':
            destdir = os.path.join(tmp, release)
        elif pkg_type == 'deb':
            destdir = os.path.join(tmp, 'debian')
        elif pkg_type == 'ipkg':
            destdir = os.path.join(tmp, 'ipkg')
        elif not pkg_type:
            self.fatal("No packaging type (e.g. --pkg-type=deb) configured or specified!")
        else:
            self.fatal("Illegal packaging type '%s' specified!" % pkg_type)
        
        # (0) display packaging variables
        if self.options.verbose >= 2:
            for key in self.env.keys():
                for pre in self.get_pkg_prefixes():
                    if key.startswith(pre):
                        Logs.info('%20s : %s' % (key, self.env[key]))

        # (1) copy installed files to temporary directory
        ignores = env['PKG_IGNORES']
        ignore_patterns = shutil.ignore_patterns(*ignores)
        shutil.copytree(srcdir, destdir, ignore=ignore_patterns, symlinks=True, ignore_dangling_symlinks=True)

        # (2a) remove files not matching includes pattern
        includes = env['PKG_INCLUDES']
        excludes = env['PKG_EXCLUDES']

        if len(includes):
            paths = []
            for i in includes:
                wildcard = os.path.join(destdir, i)
                paths += glob.glob(wildcard, recursive=True)

            for root, _, files in os.walk(destdir):
                for f in files:
                    path = os.path.join(root, f)
                    if path not in paths:
                        if os.path.exists(path) or os.path.islink(path):
                            if self.options.verbose >= 1: Logs.warn('rm -r {}'.format(path))
                            if os.path.isdir(path): shutil.rmtree(path)
                            else: os.unlink(path)

        # (2b) remove files matching excludes pattern
        elif len(excludes):
            for e in excludes:
                wildcard = os.path.join(destdir, e)
                for path in glob.iglob(wildcard, recursive=True):
                    if os.path.exists(path) or os.path.islink(path):
                        if self.options.verbose >= 1: Logs.warn('rm -r {}'.format(path))
                        if os.path.isdir(path): shutil.rmtree(path)
                        else: os.unlink(path)

        # (3) rename files and directories based on translations pattern
        translations = env['PKG_TRANSLATIONS']
        if len(translations):
            for f,t in translations:
                src = os.path.join(destdir,f)
                dst = os.path.join(destdir,t)
                if os.path.exists(src):
                    if os.path.exists(dst) and os.path.isdir(dst):
                        shutil.rmtree(dst)
                    shutil.move(src, dst)

        # (4) cleanup; remove empty trees
        root = pathlib.Path(destdir)
        paths = sorted(root.glob("**"), key=lambda p: len(str(p)), reverse=True)
        for path in paths:
            try:
                path.rmdir()  # remove directory if empty
                if self.options.verbose >= 1:
                    Logs.warn('rm -r {}'.format(str(path)))
            except OSError:
                continue  # catch and continue if non-empty

        # (5) strip debug/uneeded symbols from binaries and shared libraries
        self.strip_symbols(destdir)
        
        # (6) create actual package
        if not os.path.exists(env['PKG_OUTDIR']):
            Logs.info('mkdir -p {}'.format(env['PKG_OUTDIR']))
            os.makedirs(env['PKG_OUTDIR'])
        if pkg_type == 'rpm':
            self.rpm_create(tmp, env, destdir, release)
        elif pkg_type == 'deb':
            self.deb_create(tmp, env, destdir, name, version)
        elif pkg_type == 'ipkg':
            self.ipkg_create(tmp, env, destdir, release)

    def strip_symbols(self, path: str):
        '''Remove debug symbols and relocation information'''
        if not self.env.STRIP or self.options.pkg_nostrip:
            return

        quiet = None if self.options.verbose else Context.STDOUT
        cmd = self.env.STRIP
        if isinstance(cmd, list):
            cmd = cmd[0]
        cmd += " --strip-all"

        def isbin(fname):
            if os.path.islink(fname):
                return False
            with subprocess.Popen(['file', fname], stdout=subprocess.PIPE) as proc:
                s = proc.stdout.read().decode('UTF-8')
                return '%s: ELF ' % name in s

        for root, _, files in os.walk(path, topdown = False):
            for name in files:
                fname = os.path.join(root, name)
                if not isbin(fname):
                    continue
                self.cmd_and_log('%s %s\n' % (cmd, fname), quiet=quiet)

    def deb_create(self, tmp: str, env: dict, destdir: str, name: str, version: str):
        '''Create DEBIAN style package (.deb)'''
        dpkg = destdir
        cmd = self.env.DPKG_DEB_BIN
        if not cmd:
            self.fatal("Cannot create package; 'dpkg-deb' command not found.")
        if isinstance(cmd, list):
            cmd = cmd[0]

        # (1) create package staging directries
        for d in ('DEBIAN', ):
            p = os.path.join(dpkg, d)
            os.makedirs(p)
            os.chmod(p, 0o777)
        
        # (2) copy archive to package staging
        self.debian_export_control(os.path.join(dpkg, 'DEBIAN'), tmp, env, destdir)

        # (3) detect config files and add to DEBIAN/conffiles
        conffiles = []
        for root, _, files in os.walk(destdir, topdown = False):
            if os.path.basename(root) != 'etc':
                continue
            etc = root[len(destdir):]
            for f in files:
                conffiles.append('.%s/%s' % (etc,f))
        if len(conffiles):
            fname = os.path.join(dpkg, 'DEBIAN', 'conffiles')
            with open(fname, 'w+') as f:
                f.write('\n'.join(conffiles))
                f.write('\n')
            os.chmod(fname, 0o777)

        # (4) remove symlinks to shared libraries in DEBIAN/preinst and DEBIAN/postrm
        preinst = []
        for root, _, files in os.walk(destdir, topdown = False):
            if os.path.basename(root) != 'lib':
                continue
            lib = root[len(destdir):]
            for f in files:
                if os.path.islink(os.path.join(root,f)):
                    preinst.append('[ -f {0}/{1} ] %% rm {0}/{1}'.format(lib,f))
                    preinst.append('true')
        if len(preinst):
            fname = os.path.join(dpkg, 'DEBIAN', 'preinst')
            with open(fname, 'w+') as f:
                f.write('\n'.join(preinst))
                f.write('\n')
            os.chmod(fname, 0o755)

            fname = os.path.join(dpkg, 'DEBIAN', 'postrm')
            with open(fname, 'w+') as f:
                f.write('\n'.join(preinst))
                f.write('\n')
            os.chmod(fname, 0o755)

        # (5) add services from /etc/init.d to DEBIAN/postinst and DEBIAN/prerm
        services = []
        for root, _, files in os.walk(destdir, topdown = False):
            if not any([root.endswith(x) for x in SYSTEMD_LOCATIONS]):
                continue
            for f in files:
                if not os.path.islink(os.path.join(root,f)):
                    services.append(f)
        if len(services):
            fname = os.path.join(dpkg, 'DEBIAN', 'postinst')
            with open(fname, 'w+') as f:
                for service in services:
                    f.write('#!/bin/sh\n')
                    f.write('systemctl enable %s\n' % service)
                    f.write('systemctl start %s\n' % service)
                    f.write('\n')
            os.chmod(fname, 0o755)

            fname = os.path.join(dpkg, 'DEBIAN', 'prerm')
            with open(fname, 'w+') as f:
                for service in services:
                    f.write('#!/bin/sh\n')
                    f.write('systemctl stop %s\n' % service)
                    f.write('systemctl disable %s\n' % service)
                    f.write('\n')
            os.chmod(fname, 0o755)

        # (6) ensure all package content has correct access mode
        for root, dirs, files in os.walk(tmp):
            os.chmod(root, 0o755)
            for f in files:
                fn = os.path.join(root,f)
                if os.path.exists(fn):
                    os.chmod(fn, 0o755)
            for d in dirs:
                os.chmod(os.path.join(root,d), 0o755)

        # (7) create actual DEB and save result
        release = env['PKG_RELEASE']
        arch = env['PKG_ARCH']
        cmd += " --build debian %s/%s_%s-%s_%s.deb" % (tmp, name, version, release, arch)
        quiet = None if self.options.verbose else Context.BOTH
        res = self.cmd_and_log(cmd, cwd=tmp, quiet=quiet)

        try:
            deb = res.split()[-1]
            deb = deb.rstrip('.').strip('\'').strip('`')
        except Exception as e:
            Logs.error('[ERROR] fatal internal error; %s' % repr(e))
            raise(e)

        quiet = None if self.options.verbose else Context.STDOUT
        dest = env['PKG_OUTDIR']
        self.cmd_and_log('mv %s %s\n' % (deb, dest), quiet=quiet)
        Logs.info("+install %s/%s (from %s)" % (dest, os.path.basename(deb), os.path.dirname(deb)))

    def debian_export_control(self, path: str, tmp: str, env: dict, destdir: str):
        '''Exports DEBIAN control file'''
        control = str(DEBIAN_CONTROL)

        for k in env:
            v = str(env[k])
            if k == 'PKG_DEPENDS':
                v = self.debian_get_depends(v)
            control = control.replace('__%s__' % k, v) 

        fname = os.path.join(path, 'control')

        if self.options.verbose >= 3:
            Logs.info("========================================")
            Logs.info("DEBIAN CONTROL FILE (%s):" % fname)
            Logs.info(control)
            Logs.info("========================================")
        
        with open(fname, 'w+') as f:
            f.write(control)
        os.chmod(fname, 0o777)

        return fname

    def debian_get_depends(self, v: str) -> str:
        if not v:
            return ''
        else:
            return '\nDepends: %s' % v

    def ipkg_create(self, tmp: str, env: dict, destdir: str, release: str):
        '''Create IPKG/OPKG style package (.ipk)'''
        ipkg = destdir
        cmd = self.env.IPKG_BUILD_BIN
        if not cmd:
            self.fatal("Cannot create package; 'ipkg-build' command not found.")
        if isinstance(cmd, list):
            cmd = cmd[0]

        # (1) create package staging directries
        for d in ('CONTROL', ):
            p = os.path.join(ipkg, d)
            os.makedirs(p)
            os.chmod(p, 0o755)

        # (2) create package recipe's and meta files
        self.ipkg_export_control(os.path.join(ipkg, 'CONTROL'), tmp, env, destdir)

        # (3) detect config files and add to CONTROL/conffiles
        conffiles = []
        for root, _, files in os.walk(destdir, topdown = False):
            if os.path.basename(root) != 'etc':
                continue
            etc = root[len(destdir):]
            for f in files:
                conffiles.append('.%s/%s' % (etc,f))
        if len(conffiles):
            fname = os.path.join(ipkg, 'CONTROL', 'conffiles')
            with open(fname, 'w+') as f:
                f.write('\n'.join(conffiles))
                f.write('\n')
            os.chmod(fname, 0o777)

        # (4) remove symlinks to shared libraries in CONTROL/preinst and CONTROL/postrm
        preinst = []
        for root, _, files in os.walk(destdir, topdown = False):
            if os.path.basename(root) != 'lib':
                continue
            lib = root[len(destdir):]
            for f in files:
                if os.path.islink(os.path.join(root,f)):
                    preinst.append('[ -f {0}/{1} ] %% rm {0}/{1}'.format(lib,f))
                    preinst.append('true')
        if len(preinst):
            fname = os.path.join(ipkg, 'CONTROL', 'preinst')
            with open(fname, 'w+') as f:
                f.write('\n'.join(preinst))
                f.write('\n')
            os.chmod(fname, 0o777)

            fname = os.path.join(ipkg, 'CONTROL', 'postrm')
            with open(fname, 'w+') as f:
                f.write('\n'.join(preinst))
                f.write('\n')
            os.chmod(fname, 0o777)

        # (5) add services from /etc/init.d to CONTROL/postinst and CONTROL/prerm
        services = []
        for root, _, files in os.walk(destdir, topdown = False):
            if not root.endswith('/etc/init.d'):
                continue
            for f in files:
                if not os.path.islink(os.path.join(root,f)):
                    services.append(f)
        if len(services):
            fname = os.path.join(ipkg, 'CONTROL', 'postinst')
            with open(fname, 'w+') as f:
                for service in services:
                    f.write('#!/bin/sh\n')
                    f.write('/%s enable\n' % service)
                    f.write('/%s start\n' % service)
                    f.write('\n')
            os.chmod(fname, 0o777)

            fname = os.path.join(ipkg, 'CONTROL', 'prerm')
            with open(fname, 'w+') as f:
                for service in services:
                    f.write('#!/bin/sh\n')
                    f.write('/%s stop\n' % service)
                    f.write('/%s disable\n' % service)
                    f.write('\n')
            os.chmod(fname, 0o777)

        # (6) create actual IPKG and save result
        cmd += " -oroot -groot ipkg %s" % (tmp)
        quiet = None if self.options.verbose else Context.BOTH
        res = self.cmd_and_log(cmd, cwd=tmp, quiet=quiet)

        try:
            ipk = res.split()[-1]
        except Exception as e:
            Logs.error('[ERROR] fatal internal error; %s' % repr(e))
            raise(e)

        quiet = None if self.options.verbose else Context.STDOUT
        dest = env['PKG_OUTDIR']
        self.cmd_and_log('mv %s %s\n' % (ipk, dest), quiet=quiet)
        Logs.info("+install %s/%s (from %s)" % (dest, os.path.basename(ipk), os.path.dirname(ipk)))

    def ipkg_export_control(self, path: str, tmp: str, env: dict, destdir: str):
        '''Exports IPKG control file'''
        control = str(IPKG_CONTROL)

        for k in env:
            v = str(env[k])
            if k == 'PKG_DEPENDS':
                v = self.ipkg_get_depends(v)
            control = control.replace('__%s__' % k, v) 

        fname = os.path.join(path, 'control')

        if self.options.verbose >= 3:
            Logs.info("========================================")
            Logs.info("IPKG CONTROL FILE (%s):" % fname)
            Logs.info(control)
            Logs.info("========================================")
        
        with open(fname, 'w+') as f:
            f.write(control)
        os.chmod(fname, 0o777)

        return fname

    def ipkg_get_depends(self, v: str) -> str:
        if not v:
            return ''
        else:
            return '\nDepends: %s' % v

    def rpm_create(self, tmp: str, env: dict, destdir: str, release: str):
        '''Create Red Hat style package (.rpm)'''
        rpmbuild = os.path.join(tmp, 'rpmbuild')
        cmd = self.env.RPMBUILD_BIN
        if not cmd:
            self.fatal("Cannot create package; 'rpmbuild' command not found.")
        if isinstance(cmd, list):
            cmd = cmd[0]
        
        # (1) create package staging directries
        for d in ('BUILD','RPMS','SOURCES','SPECS','SRPMS'):
            p = os.path.join(rpmbuild, d)
            os.makedirs(p)
            os.chmod(p, 0o777)
        
        # (2) copy archive to package staging
        self.rpm_create_archive(rpmbuild, release, destdir)

        # (3) create package recipe's and meta files
        spec = self.rpm_export_spec(os.path.join(rpmbuild, 'SPECS'), tmp, env, destdir)

        # (4) ensure all package content has correct access mode
        for root, dirs, files in os.walk(tmp):
            os.chmod(root, 0o755)
            for f in files:
                fn = os.path.join(root,f)
                if os.path.exists(fn):
                    os.chmod(fn, 0o755)
            for d in dirs:
                os.chmod(os.path.join(root,d), 0o755)

        # (5) detect and activate systemd service(s)
        services = []
        for root, _, files in os.walk(destdir, topdown = False):
            if not any([root.endswith(x) for x in SYSTEMD_LOCATIONS]):
                continue
            for f in files:
                if not os.path.islink(os.path.join(root,f)):
                    services.append(f)

        # (6) create actual RPM and save result
        target = self.env.PKG_RPM_TARGET
        quiet = None if self.options.verbose else Context.BOTH
        cmd += ' -bb {}'.format(spec)
        if target:
            cmd += ' --target={}'.format(target)
        if services:
            cmd += ' --define="rpm_systemd_services {}"'.format(' '.join(services))
        cmd += ' --define="_topdir {}"\n'.format(rpmbuild)
        res = self.cmd_and_log(cmd, quiet=quiet)

        try:
            rpm = [r for r in res.splitlines() if r.startswith('Wrote:')]
            rpm = rpm[0].split()[1]
        except Exception as e:
            Logs.error('[ERROR] fatal internal error; %s' % repr(e))
            raise(e)

        quiet = None if self.options.verbose else Context.STDOUT
        dest = env['PKG_OUTDIR']
        self.cmd_and_log('mv %s %s\n' % (rpm, dest), quiet=quiet)
        Logs.info("+install %s/%s (from %s)" % (dest, os.path.basename(rpm), os.path.dirname(rpm)))

    def rpm_create_archive(self, rpmtop: str, release: str, destdir: str):
        fname = os.path.join(rpmtop, 'SOURCES', '%s.tar.gz' % release)
        with tarfile.open(fname, 'w:gz') as tar:
            tar.add(destdir, arcname=release)

    def rpm_get_requires(self, v: str) -> str:
        if not v:
            return ''
        else:
            s = 'Requires: %s' % v
            return s
        
    def rpm_export_spec(self, path: str, tmp: str, env: dict, destdir: str):
        '''Exports RPM specification file'''
        spec = str(RPM_SPEC)

        for k in env:
            v = str(env[k])
            if k == 'PKG_REQUIRES':
                v = self.rpm_get_requires(v)
            spec = spec.replace('__%s__' % k, v)

        config = env['PKG_CONFIG']
        if config in ('config', 'noreplace'):
            c = 'config(noreplace)' if config == 'noreplace' else 'config'
            for root, _, files in os.walk(destdir, topdown = False):
                p = root[len(destdir):]
                if not p.startswith('/etc') or p.startswith('/etc/systemd'):
                    continue
                for f in files:
                    spec += '%{} {}/{}\n'.format(c, p, f)

        fname = os.path.join(path, '%s.spec' % env['PKG_NAME'])

        if self.options.verbose >= 3:
            Logs.info("========================================")
            Logs.info("RPM SPEC FILE (%s):" % fname)
            Logs.info(spec)
            Logs.info("========================================")
        
        with open(fname, 'w+') as f:
            f.write(spec)
        os.chmod(fname, 0o777)

        return fname


#------------------------------------------------------------------------------
RPM_SPEC = '''
%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Summary: __PKG_SUMMARY__
Name: __PKG_NAME__
Version: __PKG_VERSION__
Release: __PKG_RELEASE__
License: __PKG_LICENSE__
Group: __PKG_GROUP__
Source: %{name}-%{version}.tar.gz
AutoReq: no
__PKG_REQUIRES__
URL: __PKG_URL__
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
__PKG_RELOCATIONS__

%description
__PKG_DESCRIPTION__

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}
cp -a * %{buildroot}

# Only post, preun and postun if any systemd service.
%if 0%{?rpm_systemd_services:1}

# See https://fedoraproject.org/wiki/Packaging:Scriptlets for the order and
# conditions.

# On upgrade only (before new install and old uninstall)
%pre
    if [ "$1" -eq 2 ]
    then
        systemctl disable --now %rpm_systemd_services
    fi

# On uninstall only, not on upgrade
%preun
    if [ "$1" -eq 0 ]
    then
        systemctl disable --now %rpm_systemd_services
    fi

%postun
    systemctl daemon-reload

# After new install and old uninstall
%posttrans
    echo "posttrans: $1"
    systemctl daemon-reload
    systemctl enable --now %rpm_systemd_services

%endif # End of rpm_sytemd_services


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/


'''


#------------------------------------------------------------------------------
IPKG_CONTROL = '''
Package: __PKG_NAME__
Version: __PKG_VERSION__
Architecture: __PKG_ARCH__
Section: __PKG_SECTION__
Priority: optional __PKG_DEPENDS__
Maintainer: __PKG_MAINTAINER__
Description: __PKG_SUMMARY__
Source: __PKG_URL__
'''


#------------------------------------------------------------------------------
DEBIAN_CONTROL = '''
Package: __PKG_NAME__
Version: __PKG_VERSION__
Architecture: __PKG_ARCH__
Section: __PKG_SECTION__
Priority: optional __PKG_DEPENDS__
Maintainer: __PKG_MAINTAINER__
Description: __PKG_SUMMARY__
Source: __PKG_URL__
'''

