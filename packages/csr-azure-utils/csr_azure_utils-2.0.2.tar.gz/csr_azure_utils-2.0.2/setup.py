from __future__ import print_function
from distutils.core import setup
from setuptools.command.install import install
from subprocess import check_call, check_output
import sys, os, platform

project_name = 'csr_azure_utils'
project_ver = '2.0.2'

'''
=======================================================================================
Note
=======================================================================================
This file is crucial to installation of csr_azure_utils. 
Before committing any changes to this file, please test installation of csr_azure_utils
beforehand on your local machine/MacBook and in Guestshell running in CSR.
'''

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        try:
            print("We are running in the postInstallCommand")
            if "centos" in platform.dist()[0].lower() and  "guestshell" in os.popen("whoami").read().strip():
                cwd = os.path.dirname(os.path.realpath(__file__))
                check_call("bash %s/install.sh" % cwd, shell=True)

                print("updating auth-token ExecStart")
                py = sys.executable
                site = check_output('{} -m site --user-site'.format(py), shell=True).strip()
                f = open("auth-token.service", "r")
                data = f.readlines()
                for i in range(len(data)):
                    if "ExecStart=" in data[i]:
                        data[i] = "ExecStart={} {}/csr_cloud/token_svr.py start\n".format(py,site.decode('utf-8'))
                        break
                f.close()

                f = open("auth-token.service", "w")
                f.writelines(data)
                f.close()

                check_call("sudo cp auth-token.service /etc/systemd/user/",
                           shell=True)
                check_call("sudo systemctl enable /etc/systemd/user/auth-token.service",
                           shell=True)
            else:
                print("Skipping auth-service setup, csr_azure_utils couldn't find either guestshell as \
                active user or platform not centos")
            install.run(self)
        except Exception as e:
            print("{}\nUnable to setup the token service via systemd".format(e))

setup(
    name=project_name,
    packages=["csr_cloud"],
    version=project_ver,
    description='Utilities for csr1000v on Azure',
    author='Cisco Systems Inc.',
    author_email='csr-cloud-dev@cisco.com',
    scripts=['csr_cloud/clear_aad_application_list.py',
             'csr_cloud/clear_default_aad_app.py',
             'csr_cloud/clear_token.py',
             'csr_cloud/refresh_token.py',
             'csr_cloud/set_default_aad_app.py',
             'csr_cloud/show_auth_applications.py'
            ],
    # use the URL to the github repo
    url='https://github4-chn.cisco.com/csr1000v-azure/' + project_name,
    download_url='https://github4-chn.cisco.com/csr1000v-azure/' + project_name + '/archive/' + \
         project_ver + '.tar.gz',
    keywords=['cisco', 'azure', 'guestshell', 'csr1000v'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'
    ],
    license="MIT",
    include_package_data=True,
    install_requires=[
        'python-crontab==2.5.1',
        'pathlib==1.0.1',
        'configparser==4.0.2',
        'pyopenssl==19.1.0',
        'msrest==0.6.16',
        'msrestazure==0.6.3',
        'paramiko==2.7.1',
        'future==0.18.2',
        'azure-storage-file==2.1.0',
        'azure-storage-blob==12.3.2',
        'azure-storage-common==2.1.0',
        'azure-storage-nspkg==3.1.0',
        'requests==2.23.0'
    ],
    cmdclass={
        'install': PostInstallCommand,
    }
)

