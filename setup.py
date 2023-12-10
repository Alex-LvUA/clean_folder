from setuptools import setup, find_namespace_packages

setup(name='clean_folder',
      version='1',
      py_modules=['clean_folder'],
      description='cleaning and soting all in folder',
      author='Oleksandr Komarov',
      author_email='***@yahoo.com',
      license='MIT',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['clean-folder=clean_folder.clean:start']} # 'назва для виклику=папка.файл.py:функція(точка входу)

      )
