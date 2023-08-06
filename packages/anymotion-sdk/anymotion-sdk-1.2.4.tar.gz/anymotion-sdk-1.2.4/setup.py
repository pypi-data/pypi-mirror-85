# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anymotion_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22,<3.0']

extras_require = \
{'cv': ['opencv-python>=4.4,<5.0']}

setup_kwargs = {
    'name': 'anymotion-sdk',
    'version': '1.2.4',
    'description': 'AnyMotion SDK for Python',
    'long_description': '# AnyMotion Python SDK\n\n[![PyPi][pypi-version]][pypi] [![CircleCI][ci-status]][ci] [![codecov][codecov-status]][codecov]\n\nThis is the Software Development Kit (SDK) for Python, which allows Python developers to write software that makes use of [AnyMotion](https://anymotion.nttpc.co.jp).\nIt works on Python 3.6 or greater.\n\n## Installation\n\nInstall using [pip](https://pip.pypa.io/en/stable/quickstart/):\n\n```sh\n$ pip install anymotion-sdk\n```\n\nIf you want to use a [CV-based methods](#CV-based-methods):\n\n```sh\n$ pip install anymotion-sdk[cv]\n```\n\n## Usage\n\nTo use AnyMotion Python SDK, you must first import it and tell it about your credentials which issued by the [AnyMotion Portal](https://portal.anymotion.jp/):\n\n```py\nimport anymotion_sdk\n\n# Setup client\nclient = anymotion_sdk.Client(client_id="your_client_id", client_secret="your_client_secret")\n```\n\nYou can also use environment variables:\n\n```sh\nexport ANYMOTION_CLIENT_ID=<your_client_id>\nexport ANYMOTION_CLIENT_SECRET=<your_client_secret>\n```\n\n```py\n# Setup client using environment variables\nclient = anymotion_sdk.Client()\n```\n\nThe following is how to upload an image and extract the keypoints:\n\n```py\n# Upload image file\nupload_result = client.upload("image.jpg")\n\n# Extract keypoint\nkeypoint_id = client.extract_keypoint(image_id=upload_result.image_id)\nextraction_result = client.wait_for_extraction(keypoint_id)\n\n# Get keypoint data from result\nkeypoint = extraction_result.json\n```\n\nYou can get the uploaded data or the keypoint extracted data and so on as follows:\n\n```py\n# Get data of a specific id\nimage = client.get_image(image_id)\nmovie = client.get_movie(movie_id)\nkeypoint = client.get_keypoint(keypoint_id)\ndrawing = client.get_drawing(drawing_id)\nanalysis = client.get_analysis(analysis_id)\ncomparison = client.get_comparison(comparison_id)\n\n# Get all data\nimages = client.get_images()\nmovies = client.get_movies()\nkeypoints = client.get_keypoints()\ndrawings = client.get_drawings()\nanalyses = client.get_analyses()\ncomparisons = client.get_comparisons()\n```\n\nIn `get_keypoint`, `get_drawing`, `get_analysis`, and `get_comparison`, you can use the `join_data` option to get the relevant data at the same time.\n\n```py\n>>> client.get_keypoint(keypoint_id)\n{\'id\': 1, \'image\': 2, \'movie\': None, \'keypoint\': [{\'nose\': [10, 20]}], \'execStatus\': \'SUCCESS\', \'failureDetail\': None, \'createdAt\': \'2020-01-01T00:00:00.000000Z\', \'updatedAt\': \'2020-01-01T00:00:00.000000Z\'}\n\n>>> client.get_keypoint(keypoint_id, join_data=True)\n{\'id\': 1, \'image\': {\'id\': 2, \'name\': \'image\', \'text\': \'\', \'height\': 100, \'width\': 100, \'contentMd5\': \'ecWkdCSrnBa9+EYREt/fbg==\', \'createdAt\': \'2020-01-01T00:00:00.000000Z\', \'updatedAt\': \'2020-01-01T00:00:00.000000Z\'}, \'movie\': None, \'keypoint\': [{\'nose\': [10, 20]}], \'execStatus\': \'SUCCESS\', \'failureDetail\': None, \'createdAt\': \'2020-01-01T00:00:00.000000Z\', \'updatedAt\': \'2020-01-01T00:00:00.000000Z\'}\n```\n\nThe way to output the log to stdout is as follows:\n\n```py\n# Log level is INFO by default.\nanymotion_sdk.set_stream_logger()\n\n# Set the log level to DEBUG.\n# At the DEBUG level, the content of the request and response to the API is output.\nanymotion_sdk.set_stream_logger(level=logging.DEBUG)\n```\n\nFor more examples, see [here](https://github.com/nttpc/anymotion-examples).\n\n### CV-based methods\n\nIf you install the extra package, `download_and_read` is available.\n`download_and_read` returns the downloaded image or video in numpy format.\n\n```py\ndata = client.download_and_read(drawing_id)\n```\n\n**Warning**: Large videos use a lot of RAM.\n\n## Change Log\n\nSee [CHANGELOG.md](CHANGELOG.md).\n\n[pypi]: https://pypi.org/project/anymotion-sdk\n[pypi-version]: https://img.shields.io/pypi/v/anymotion-sdk\n[ci]: https://circleci.com/gh/nttpc/anymotion-python-sdk\n[ci-status]: https://circleci.com/gh/nttpc/anymotion-python-sdk/tree/master.svg?style=shield&circle-token=b9824650553efb30dabe07e3ab2b140ae2efa60c\n[codecov]: https://codecov.io/gh/nttpc/anymotion-python-sdk\n[codecov-status]: https://codecov.io/gh/nttpc/anymotion-python-sdk/branch/master/graph/badge.svg?token=5QG7KUBZ7K\n',
    'author': 'Yusuke Kumihashi',
    'author_email': 'y_kumiha@nttpc.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nttpc/anymotion-python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
