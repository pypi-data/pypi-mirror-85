from distutils.core import setup
setup(
  name = 'elasticmock_additional_apis',
  packages = ['elasticmock_additional_apis'],
  version = '0.3',
  license='MIT',
  description = 'Extended elasticmock module with additional Elasticsearch index APIs',
  author = 'Tereza Gabrielova',
  author_email = 'terezagabrielova@yahoo.com',
  url = 'https://github.com/Tessg22/elasticmock_additional_apis',
  download_url = 'https://github.com/Tessg22/elasticmock_additional_apis/archive/v_01.tar.gz',
  keywords = ['Tagsunittest', 'mock', 'elasticsearch'],
  install_requires=[
          'elasticsearch',
          'elasticmock',
          'functools',
          'mock',
          'base64',
          'random',
          'string',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
