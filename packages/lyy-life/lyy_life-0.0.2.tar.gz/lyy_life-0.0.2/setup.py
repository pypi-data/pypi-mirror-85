#from distutils.core import setup
from setuptools import setup, find_packages

VERSION = '0.0.2'

tests_require = []

install_requires = []

setup(name='lyy_life', # 模块名称
      url='https://github.com/yongyaoli/lyy_life',  # 项目包的地址
      author="yixin2009",  # Pypi用户名称
      author_email='731969968@qq.com',  # Pypi用户的邮箱
      keywords='python liyy common ',
      description='common libary.',
      license='MIT',  # 开源许可证类型
      classifiers=[
          'Operating System :: OS Independent',
          'Topic :: Software Development',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: Implementation :: PyPy'
      ],
      python_requires='>=3.5',
      version=VERSION, 
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='runtests.runtests',
      extras_require={'test': tests_require},

      entry_points={ 'nose.plugins': [] },
      packages=find_packages(),
)
