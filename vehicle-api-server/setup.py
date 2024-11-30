from setuptools import setup, find_packages

setup(
    name="vehicle_api_server",
    version="0.1",
    packages=find_packages(), 
    install_requires=[
        "Flask==3.0.0",
        "strawberry-graphql[flask]==0.199.1",
        "pytest==7.4.0",
        "Flask-Limiter>=2.0.1",
        "flask-cors",
        "marshmallow==3.19.0",
    ],
    include_package_data=True, 
    entry_points={
        "console_scripts": [
            "run-server=app.server:app.run",  
            "run-graphql=app.graphql_server:app.run",  
        ],
    },
)
