from setuptools import setup

setup(name='pysuricata',
      version='0.2',
      description='Meerkat\'s package of Computer Vision utilities',
      url='https://github.com/meerkat-cv/pysuricata',
      author='Meerkat',
      author_email='support@meerkat.com.br',
      license='MIT',
      # packages=['pysuricata'],
      packages=['pysuricata', 'pysuricata.video_stream'],
      scripts=['scripts/anno_tools/keep_or_gone', 'scripts/anno_tools/yes_no_reject'],
      zip_safe=False)