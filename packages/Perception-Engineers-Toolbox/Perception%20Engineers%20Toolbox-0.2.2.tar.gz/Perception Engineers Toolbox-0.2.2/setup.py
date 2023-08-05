from setuptools import setup
import pathlib
from PerceptionToolkit.Version import version_str

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='Perception Engineers Toolbox',
    version=version_str,
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=['PerceptionToolkit', 'PerceptionToolkit/plugins'],
    url='https://fahren-sie-sicher.de',
    license='MIT',
    author='Thomas Kübler',
    author_email='mails@kueblert.de',
    description='A toolbox for eye-tracking data processing and analysis',
    install_requires=["tabel", "numpy", "pyyaml", "pillow", "scipy", "scikit-learn", "pomegranate", "matplotlib", "pandas", "h5py", "yapsy"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Scientific/Engineering :: Visualization",
    ]
)
