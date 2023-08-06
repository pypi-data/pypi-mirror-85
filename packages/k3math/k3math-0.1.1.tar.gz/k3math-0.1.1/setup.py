import setuptools
setuptools.setup(
    name="k3math",
    packages=["."],
    version="0.1.1",
    license='MIT',
    description='k3math is a toy math impl',
    long_description="# k3math\n\n[![Build Status](https://travis-ci.com/pykit3/k3math.svg?branch=master)](https://travis-ci.com/pykit3/k3math)\n[![Documentation Status](https://readthedocs.org/projects/k3math/badge/?version=stable)](https://k3math.readthedocs.io/en/stable/?badge=stable)\n[![Package](https://img.shields.io/pypi/pyversions/k3math)](https://pypi.org/project/k3math)\n\nno desc\n\nk3math is a component of [pykit3] project: a python3 toolkit set.\n\n\n# Install\n\n```\npip install k3math\n```\n\n# Synopsis\n\n```python\n\nxs = [1, 2, 3, 4]\nys = [6, 5, 7, 10]\n\n# Fit polynomial curve with 4 points, at degree 0, 1, 2, 3:\nfor deg in (0, 1, 2, 3):\n    poly = Polynomial.fit(xs, ys, degree=deg)\n    print 'y =', poly\n\n    # Evaluate y(5) with polynomial\n    y5 = Polynomial.evaluate(poly, 5)\n    print 'y(5) =', y5\n\n    # Plot the curve and points\n    lines = Polynomial.plot([(poly, '.')], (-1, 6),\n                            width=30, height=10,\n                            points=zip(xs + [5],\n                                       ys + [y5],\n                                       ['X', 'X', 'X', 'X', '*']))\n    for l in lines:\n        print l\n\n# y = 7\n# y(5) = 7.0\n#                     X\n#\n#\n#\n# ...............X.........*....\n#      X\n#           X\n# y = 3.5 + 1.4x\n# y(5) = 10.5\n#                              .\n#                          *...\n#                     X....\n#                .....\n#           .....X\n#      X....X\n# .....\n# y = 8.5 - 3.6x + x²\n# y(5) = 15.5\n#                              .\n#                             .\n#                           ..\n#                         .*\n#                      ...\n# ..               ...X\n#   ...X....X....X.\n# y = 12 - 9.166667x + 3.5x² - 0.333333x³\n# y(5) = 12.0\n#\n# .                     ...*....\n#  .                  X.\n#   .               ..\n#    .            ..\n#     .         .X\n#      X....X...\n\n```\n\n#   Author\n\nZhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n#   Copyright and License\n\nThe MIT License (MIT)\n\nCopyright (c) 2015 Zhang Yanpo (张炎泼) <drdr.xp@gmail.com>\n\n\n[pykit3]: https://github.com/pykit3",
    long_description_content_type="text/markdown",
    author='Zhang Yanpo',
    author_email='drdr.xp@gmail.com',
    url='https://github.com/pykit3/k3math',
    keywords=['math', 'python3'],
    python_requires='>=3.0',

    install_requires=['semantic_version~=2.8.5', 'jinja2~=2.11.2', 'PyYAML~=5.3.1', 'sphinx~=3.3.1', 'k3ut~=0.1.7'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ] + ['Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: Implementation :: PyPy'],
)
