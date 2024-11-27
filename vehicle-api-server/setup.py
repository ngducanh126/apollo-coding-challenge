from setuptools import setup, find_packages

setup(
    name="vehicle_api_server",
    version="0.1",
    packages=find_packages(), 
    install_requires=[
        "Flask==3.0.0",
        "strawberry-graphql[flask]==0.199.1",  # For GraphQL support
        "pytest==7.4.0"  # For testing
    ],
    include_package_data=True, 
    entry_points={
        "console_scripts": [
            "run-server=app.server:app.run",  # CLI shortcut for REST server
            "run-graphql=app.graphql_server:app.run",  # CLI shortcut for GraphQL server
        ],
    },
)
