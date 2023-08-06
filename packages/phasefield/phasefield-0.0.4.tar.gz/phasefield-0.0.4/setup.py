import os, sys
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

builddir = os.path.abspath(os.getcwd())

def inVEnv():
    # if sys.real_prefix exists, this is a virtualenv set up with the virtualenv package
    if hasattr(sys, 'real_prefix'):
        return 1
    # if a virtualenv is set up with pyvenv, we check for equality of base_prefix and prefix
    if hasattr(sys, 'base_prefix'):
        return (sys.prefix != sys.base_prefix)
    # if none of the above conditions triggered, this is probably no virtualenv interpreter
    return 0

def get_install_prefix():
    # test if in virtual env
    if inVEnv():
        return sys.prefix
    # use system default
    return None



# compute number of cores for building like petsc does it
def compute_make_np(i):
    f16 = .80
    f32 = .65
    f64 = .50
    f99 = .30
    if (i<=2):    return 2
    elif (i<=4):  return i
    elif (i<=16): return int(4+(i-4)*f16)
    elif (i<=32): return int(4+12*f16+(i-16)*f32)
    elif (i<=64): return int(4+12*f16+16*f32+(i-32)*f64)
    else:         return int(4+12*f16+16*f32+32*f64+(i-64)*f99)
    return

def dunecontrol():
    addModules = 'bash ./addModules.sh'
    status = os.system(addModules)
    if status != 0: raise RuntimeError(status)

    optsfile = open("config.opts", "w")
    optsfile.write('CMAKE_FLAGS=\"' + ('-DCMAKE_INSTALL_PREFIX='+get_install_prefix() if get_install_prefix() is not None else '') +
                   ' -DBUILD_SHARED_LIBS=TRUE -DDUNE_ENABLE_PYTHONBINDINGS=TRUE'+
                   ' -DDUNE_PYTHON_INSTALL_LOCATION="none"' +
                   ' -DDUNE_GRID_GRIDTYPE_SELECTOR=ON' +
                   ' -DALLOW_CXXFLAGS_OVERWRITE=ON' +
                   ' -DUSE_PTHREADS=ON' +
                   ' -DCMAKE_BUILD_TYPE=Release' +
                   ' -DCMAKE_DISABLE_FIND_PACKAGE_LATEX=TRUE' +
                   ' -DCMAKE_DISABLE_DOCUMENTATION=TRUE' +
                   '\"\n')
    optsfile.write('MAKE_FLAGS=\"-j ' + str(compute_make_np(os.cpu_count())) + '\"')
    optsfile.close()

    configure = 'dunecontrol --opts=config.opts configure'
    status = os.system(configure)
    if status != 0: raise RuntimeError(status)

    install = 'dunecontrol --opts=config.opts make install'
    status = os.system(install)
    if status != 0: raise RuntimeError(status)

class BuildExt(build_ext):
    def build_extensions(self):
        dunecontrol()
        self.extensions.pop(0) # empty extension was added to run `dunecontrol`
        for ext in self.extensions:
            ext.extra_compile_args += ['-std=c++17', '-fvisibility=hidden']
        build_ext.build_extensions(self)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="phasefield",
    version="0.0.4",
    author="Matthew Collins and Andreas Dedner",
    author_email="a.s.dedner@warwick.ac.uk",
    description="Interface problem solver based on the phase-field methodology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.dune-project.org/dune-fem/phasefield",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent"],
    zip_safe = 0,
    package_data = {'': ['*.cc']},
    ext_modules=[Extension("", [])],
    cmdclass={'build_ext': BuildExt}
  )
