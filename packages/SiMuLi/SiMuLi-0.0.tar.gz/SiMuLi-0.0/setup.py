# -*- coding: utf-8 -*-

import os
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

if __name__ == '__main__':
    from distutils.core import setup
    extra_files = package_files('SiMuLi')
    setup(name='SiMuLi',
          version='0.0',
          packages=['SiMuLi'],
          description='Simulation and sensitivity analysis for structural dynamics and rigid multibody dynamics in lightweight engineering design',  
          author='E. J. Wehrle & V. Gufler',
          package_data={'': extra_files},
          license='GPL3')
