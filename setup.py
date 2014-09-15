from setuptools import setup, find_packages
setup(
    name="django-sticky-crumbs",
    version="0.1.1",
    packages=find_packages(),
    author="Susel Ruiz Duran",
    author_email="suselrd@gmail.com",
    license='NEW BSD LICENSE: http://www.opensource.org/licenses/bsd-license.php',
    description="Easy to use, shared breadcrumbs system for Django framework.",
    long_description="*django-sticky-crumbs* is a breadcrumb system to Django "
        "framework that allow you to define the views you want to leave a crumb, "
        "an to define the desired display names for them. It works as a "
        "pluggable middleware that add a breadcrumbs instance/iterable in your "
        "request object. Between requests, breadcrumbs object lives in user session.",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
    install_requires=["Django>=1.6.1", ],
)
