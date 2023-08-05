import pathlib
from setuptools import find_packages, setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
	name = 'nanome-vault',
	packages=find_packages(),
	version = '2.2.2',
	license='MIT',
	description = 'A Nanome plugin that creates a web interface to upload files and make them available in Nanome',
	long_description = README,
    long_description_content_type = "text/markdown",
	author = 'Nanome',
	author_email = 'hello@nanome.ai',
	url = 'https://github.com/nanome-ai/plugin-vault',
	platforms="any",
	keywords = ['virtual-reality', 'chemistry', 'python', 'api', 'plugin'],
	install_requires=['nanome', 'pycryptodome', 'requests'],
	entry_points={"console_scripts": ["nanome-vault = nanome_vault.Vault:main"]},
	classifiers=[
		'Development Status :: 3 - Alpha',

		'Intended Audience :: Science/Research',
		'Topic :: Scientific/Engineering :: Chemistry',

		'License :: OSI Approved :: MIT License',

		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
	package_data={
        "nanome_vault": [
            "WebUI/dist/*",
            "WebUI/dist/*/*",
            "menus/icons/*",
            "menus/json/*",
        ]
	},
)
