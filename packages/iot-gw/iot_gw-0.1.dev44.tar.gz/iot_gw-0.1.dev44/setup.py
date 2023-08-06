import setuptools

with open('readme.md','r') as fh:
    readme = fh.read()

def local_scheme(version):
    return version.format_choice("","")


setuptools.setup(
    name="iot_gw",
    use_scm_version={
        "root": ".", 
        "relative_to": __file__,
        "local_scheme": local_scheme
    },
    author="A. LE CANN",
    author_email="arnaud@lecann.com",
    description="IoT gateway",
    long_description = readme,
    long_description_content_type="text/markdown",
    url="https://github.com/arnlec/iot-gw",
    packages=setuptools.find_packages(),
    install_requires=[
        'pyjwt==1.7.1',
        'cryptography==2.7',
        'flask==1.1.1',
        'paho-mqtt==1.4.0',
        'PyYAML==5.2'
    ],
    setup_requires=['setuptools_scm'],
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    python_requires='>=3'


)