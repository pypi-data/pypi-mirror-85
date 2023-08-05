# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['solvent']

package_data = \
{'': ['*'],
 'solvent': ['sites/action.greene2020.com/stop-the-steal-rd/*',
             'sites/action.iowagunowners.org/action/re-open-iowa-for-business/*',
             'sites/action.iowagunowners.org/sign-up/*',
             'sites/defendyourballot.formstack.com/forms/voter_fraud/*',
             'sites/iqconnect.lmhostediq.com/iqextranet/EsurveyForm.aspx/*',
             'sites/nolabels.salsalabs.org/071020trumphandlingcovid--19/index.html/*',
             'sites/oneclickpolitics.global.ssl.fastly.net/messages/edit/*',
             'sites/reopennc.com/@/*',
             'sites/secure.anedot.com/greene-for-congress-inc/stop-the-steal-rd/*',
             'sites/secure.donaldjtrump.com/official-2020-strategy-survey/*',
             'sites/steube.house.gov/@/*',
             'sites/steube.house.gov/contact/newsletter/*',
             'sites/steube.house.gov/contact/newsletter/newsletter-subscribe-thank-you/*',
             'sites/trumpvictory.com/free-yard-sign/*',
             'sites/unlockmichigan.com/thank-you/*',
             'sites/unlockmichigan.ivolunteers.com/Account/Register/*',
             'sites/unlockmichigan.ivolunteers.com/Account/ThankYou/*',
             'sites/unlockmichigan.ivolunteers.com/Register/extrapetitions/*',
             'sites/www.donaldjtrump.com/landing/the-official-2020-strategy-survey/*',
             'sites/www.facebook.com/login.php/*']}

install_requires = \
['pomace==0.4b2']

entry_points = \
{'console_scripts': ['solvent = solvent:main']}

setup_kwargs = {
    'name': 'solvent',
    'version': '0.0.22',
    'description': 'Kills off fake grass.',
    'long_description': None,
    'author': 'Solvent',
    'author_email': 'solvent@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
