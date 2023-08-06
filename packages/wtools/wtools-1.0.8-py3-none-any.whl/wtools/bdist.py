#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os, tempfile, shutil, platform, tarfile, json, glob, sys, subprocess, gzip
import jsonschema
import waflib
from waflib import Logs, Build, Scripting, Errors, Context
import wtools


def options(opt):
    opt.add_option('--bdist-prefix', dest='bdist_prefix', default=None, action='store', help='package installation prefix, overrides ${PREFIX} when packaging')
    opt.add_option('--bdist-bindir', dest='bdist_bindir', default=None, action='store', help='binary installation prefix, overrides ${BINDIR} when packaging')
    opt.add_option('--bdist-libdir', dest='bdist_libdir', default=None, action='store', help='library installation prefix, overrides ${LIBDIR} when packaging')
    opt.add_option('--bdist-algo', dest='bdist_algo', default='tgz', action='store', help='bdist compression type (tgz|tbz2|zip)')
    opt.add_option('--bdist-outdir', dest='bdist_outdir', default=None, action='store', help='location to store the binary dist')
    opt.add_option('--bdist-includes', dest='bdist_includes', default=None, action='store', help='additional paths and/or files to include')
    opt.add_option('--bdist-devel', dest='bdist_devel', default=False, action='store_true', help='bdist development package')
    opt.add_option('--bdist-host', dest='bdist_host', default=None, action='store', help='bdist host, overrides os.environ["HOST"] on configure')
    opt.add_option('--bdist-provides', dest='bdist_provides', default=False, action='store_true', help='bdist package contents')
    opt.add_option('--bdist-recipe', dest='bdist_recipe', default=None, action='store', help='binary distribution packaging recipe')


def configure(conf):
    conf.find_program('createrepo', var='RPM_CREATEREPO', mandatory=False)
    conf.find_program('dpkg-scanpackages', var='DPKG_SCANPACKAGES', mandatory=False)

    # configure packaging type to be used
    devel = conf.options.bdist_devel
    conf.env.BDIST_DEVEL = ["1"] if devel else []

    # print (debug) package contents <name>.provides file?
    conf.env.BDIST_PROVIDES = ["1"] if conf.options.bdist_provides else []

    # configure compression algorithm to be used
    bdist_algo = get_bdist_algorithm(conf)
    if bdist_algo:
        conf.env.BDIST_ALGO = bdist_algo

    # define out (default) installation prefixes when creating binary dist(s)
    if conf.options.bdist_prefix:
        conf.env.BDIST_PREFIX = conf.options.bdist_prefix
    if conf.options.bdist_bindir:
        conf.env.BDIST_BINDIR = conf.options.bdist_bindir
    if conf.options.bdist_libdir:
        conf.env.BDIST_LIBDIR = conf.options.bdist_libdir

    # define output location for the created binary distribution
    if conf.options.bdist_outdir:
        bdist_outdir = conf.options.bdist_outdir
    else:
        bdist_outdir = getattr(Context.g_module, Context.TOP, conf.srcnode.abspath())
    
    bdist_outdir = os.path.abspath(bdist_outdir)
    conf.env.BDIST_OUTDIR = bdist_outdir

    # configure additional files to be included
    if conf.options.bdist_includes:
        includes = conf.options.bdist_includes.split(':')
        conf.env.BDIST_INCLUDES = [os.path.abspath(i) for i in includes]
    
    # define default packaging settings
    name = getattr(Context.g_module, Context.APPNAME, 'noname')
    version = getattr(Context.g_module, Context.VERSION, '1.0')
    host = get_bdist_host(conf)

    # binary distribution recipe
    if conf.options.bdist_recipe:
        nrel = configure_bundles(conf, version, host, devel)
    else:
        nrel = 1
        conf.env.BDIST1_RELEASE = "{}{}{}-{}".format(name, '-devel-' if devel else '-', version, host)
        conf.env.BDIST1_FILTER_EXCLUDES = []
        conf.env.BDIST1_FILTER_INCLUDES = []
        conf.env.BDIST1_FILE_PATTERNS = []
        conf.env.BDIST1_FILE_ISFLAT = []
        conf.env.BDIST1_IS_PKGREPO = []
    conf.env.BDIST_NREL = str(nrel)


def configure_bundles(conf, version: str, host: str, devel: bool) -> int:
    path = conf.options.bdist_recipe
    try:
        s = os.path.join(wtools.location, 'data', 'bdist-recipe.schema.json')
        with open(s) as f:
            schema = json.load(f)
        with open(path) as f:
            recipe = json.load(f)
        jsonschema.validate(recipe, schema=schema)
    except Exception as e:
        conf.fatal('bdist({}) recipe failure; {}'.format(path, repr(e)))        

    patterns = recipe['global']['pattern'] if 'pattern' in recipe['global'] else []
    isflat = 'isflat' in recipe['global']
    isrepo = 'isrepo' in recipe['global']

    bundles = recipe['bundles']
    nrel = len(bundles)
    for i in range(nrel):
        b = bundles[i]
        conf.env['BDIST{}_RELEASE'.format(i+1)] = "{}{}{}-{}".format(b['name'], '-devel-' if devel else '-', version, host)
        conf.env['BDIST{}_FILTER_EXCLUDES'.format(i+1)] = b['filter']['excludes'] if 'excludes' in b['filter'] else []
        conf.env['BDIST{}_FILTER_INCLUDES'.format(i+1)] = b['filter']['includes'] if 'includes' in b['filter'] else []
        conf.env['BDIST{}_FILE_PATTERNS'.format(i+1)] = patterns
        conf.env['BDIST{}_FILE_ISFLAT'.format(i+1)] = ['1'] if isflat else []
        conf.env['BDIST{}_IS_PKGREPO'.format(i+1)] = ['1'] if isrepo else []
    return nrel


def get_bdist_algorithm(ctx) -> str or None:
    opt = ctx.options.bdist_algo
    if not opt:
        return None
        
    opt = opt.lower().lstrip('.')
    
    if opt in ('gz', 'tgz', 'tar.gz'):
        return 'gz'
    elif opt in ('bz2', 'tbz2', 'tar.bz2'):
        return 'bz2'
    else:
        ctx.fatal('BDIST: illegal compression algorithm({})'.format(ctx.options.bdist_algo))


def get_bdist_host(ctx) -> str:
    if ctx.options.bdist_host:
        return ctx.options.bdist_host

    if 'HOST' in os.environ:
        return os.environ['HOST']

    try:
        import distro
        host = "-".join(distro.linux_distribution()[:2])
    except:
        if hasattr(platform, 'dist'):
            host = "-".join(platform.dist()[:2])
        else:
            host = "%s-%s" % (ctx.env.DEST_OS, ctx.env.DEST_CPU)

    return host.replace(' ', '_').lower()


class BundleContext(Build.InstallContext):
    '''create binary distribution (release|develop).'''
    cmd = 'bdist'

    def __init__(self, **kw):
        super(BundleContext, self).__init__(**kw)

    def _get_task_generators(self):
        tgens = []
        for group in self.groups:
            for tg in group:
                tgens.append(tg)
        return list(set(tgens))

    def execute(self):
        self.restore()
        if not self.all_envs:
            self.load_envs()

        tmp = tempfile.mkdtemp()
        try:
            self.options.destdir = tmp

            if 'BDIST_PREFIX' in self.env:
                self.env.PREFIX = self.env.BDIST_PREFIX
                self.env.BINDIR = self.env.BDIST_BINDIR if 'BDIST_BINDIR' in self.env else os.path.join(self.env.BDIST_PREFIX, 'bin')
                self.env.LIBDIR = self.env.BDIST_LIBDIR if 'BDIST_LIBDIR' in self.env else os.path.join(self.env.BDIST_PREFIX, 'lib')
            else:
                self.env.BINDIR = self.env.BDIST_BINDIR if 'BDIST_BINDIR' in self.env else self.env.BINDIR
                self.env.LIBDIR = self.env.BDIST_BINDIR if 'BDIST_LIBDIR' in self.env else self.env.LIBDIR

            self.bdist(tmp)
        finally:
            shutil.rmtree(tmp)

    @property
    def algorithm(self) -> str:
        algo = get_bdist_algorithm(self)
        return algo if algo else 'gz'

    def bdist(self, tmp: str):
        algo = self.algorithm
        staging = os.path.join(tmp, 'staging')
        includes = self.env.BDIST_INCLUDES

        # (0) display BUNDLING variables
        if self.options.verbose >= 2:
            for key in self.env.keys():
                if not key.startswith('BDIST'):
                    continue
                Logs.info('%20s : %s' % (key, self.env[key]))
        
        # (1) build component files and install in temporary directory
        self.options.destdir = staging
        self.execute_build()

        # (c) terminate if nothing has been installed
        if not os.path.exists(staging):
            Logs.warn('bdist skipped; nothing has been installed')
            return

        # (2) copy additional files to release directory
        for include in includes:
            if not os.path.exists(include):
                continue
            quiet = None if self.options.verbose else Context.STDOUT
            if os.path.isdir(include):
                self.cmd_and_log('cp -a %s/* %s\n' % (include, staging), quiet=quiet)
                Logs.info("+copy %s/* (to %s)" % (include, staging))
            else:
                self.cmd_and_log('cp %s %s\n' % (include, staging), quiet=quiet)
                Logs.info("+copy %s (to %s)" % (include, staging))

        # (3) create tar files with requested compression type
        nrel = int(self.env.BDIST_NREL)
        for i in range(nrel):
            self.bundle(i+1, tmp, src=staging, algo=algo)

    def populate(self, i: int, src: str, dst: str):
        patterns = self.env['BDIST{}_FILE_PATTERNS'.format(i)]
        isflat = self.env['BDIST{}_FILE_ISFLAT'.format(i)]
        isrepo = self.env['BDIST{}_IS_PKGREPO'.format(i)]
        ex = self.env['BDIST{}_FILTER_EXCLUDES'.format(i)]
        inc = self.env['BDIST{}_FILTER_INCLUDES'.format(i)]
        deb = False
        rpm = False

        if not patterns:
            shutil.copytree(src,dst,symlinks=True)
            return

        if self.options.verbose >= 2:
            Logs.info('populate({})'.format(dst))

        efiles = []
        files = []
        antipatterns = [p.lstrip('!') for p in patterns if p.startswith('!')]
        patterns = [p for p in patterns if not p.startswith('!')]

        for pattern in patterns:
            files += glob.glob(os.path.join(src,pattern), recursive=True)

        for pattern in antipatterns:
            efiles += glob.glob(os.path.join(src,pattern), recursive=True)

        files = [f for f in files if f not in efiles]

        sources = []
        for f in files:
            b = os.path.basename(f)
            msg = 'file({}) '.format(f)
            if any(x in b for x in ex) and not any(x in b for x in inc):
                if self.options.verbose >= 2:
                    Logs.info(msg + 'SKIP')
            else:
                if self.options.verbose >= 2:
                    Logs.info(msg + 'USE')
                if f.endswith('.deb'):
                    deb = True
                elif f.endswith('.rpm'):
                    rpm = True
                sources.append(f)

        if isflat and not os.path.exists(dst):
            if self.options.verbose >= 1:
                Logs.info('mkdir -p {}'.format(dst))
            os.makedirs(dst)

        for s in sources:
            if isflat:
                d = os.path.join(dst, os.path.basename(s))
                if self.options.verbose >= 1:
                    Logs.info('cp {} {}'.format(s,d))
                shutil.copyfile(s, d)
            else:
                d = os.path.join(dst, os.path.relpath(os.path.dirname(s), src))
                if not os.path.exists(d):
                    if self.options.verbose >= 1:
                        Logs.info('mkdir -p {}'.format(d))
                    os.makedirs(d)
                shutil.copyfile(s, d)

        if isrepo:
            if rpm and self.env.RPM_CREATEREPO:
                cmd = self.env.RPM_CREATEREPO[0]
                Logs.info('cd {}; {} .'.format(dst, cmd))
                subprocess.run([cmd, '.'], cwd=dst)

            elif deb and self.env.DPKG_SCANPACKAGES:
                cmd = self.env.DPKG_SCANPACKAGES[0]
                Logs.info('cd {}; {} -m . | gzip -c > Packages.gz'.format(dst, cmd))
                res = subprocess.run([cmd, '-m', '.'], cwd=dst, stdout=subprocess.PIPE)
                with gzip.GzipFile(os.path.join(dst, 'Packages.gz'), mode='wb+') as gz:
                    gz.write(res.stdout)

    def bundle(self, i: int, tmp: str, src: str, algo: str):
        release = self.env['BDIST{}_RELEASE'.format(i)]
        outdir = self.env.BDIST_OUTDIR
        ext = 'tar.gz' if algo == 'gz' else 'tar.bz2'
        dst = os.path.join(tmp, release)

        # (1) copy files from staging to bundle archive
        self.populate(i, src, dst)

        # (2) create bundle archive
        fname = os.path.join(tmp, '%s.%s' % (release, ext))
        with tarfile.open(fname, 'w:%s' % algo) as tar:
            tar.add(dst, arcname=release)

        # (3) move bundle to output directory
        if not os.path.exists(outdir):
            Logs.info('mkdir -p {}'.format(outdir))
            os.makedirs(outdir)
        quiet = None if self.options.verbose else Context.STDOUT
        self.cmd_and_log('mv %s %s\n' % (fname, outdir), quiet=quiet)
        Logs.info("+install %s/%s (from %s)" % (outdir, os.path.basename(fname), os.path.dirname(fname)))

        # (4) export a list of what the bundle provides
        if self.env.BDIST_PROVIDES or self.options.bdist_provides:
            fname = os.path.join(outdir, '%s.provides' % (release))
            with open(fname, "w+") as f:
                for root, _, files in os.walk(dst):
                    for fname in files:
                        f.write('%s\n' % os.path.relpath(os.path.join(root, fname), dst))
