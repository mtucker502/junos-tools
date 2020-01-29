from setuptools import setup

# parse requirements
req_lines = [line.strip() for line in open(
    'requirements.txt').readlines()]
install_reqs = list(filter(None, req_lines))

setup(
    name='junos-tools',
    version='0.1.1',
    packages=['junos_tools'],
    python_requires='>=3',
    url='https://github.com/mtucker502/junos-tools',
    license='MIT',
    author='mtucker502',
    author_email='github@netzolt.com',
    description='Various tools for Juniper Junos devices',
    install_requires=install_reqs,
    classifiers = [
        "Programming Language :: Python :: 3",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT",
        "Programming Language :: Python :: 3.7",
    ],
)
