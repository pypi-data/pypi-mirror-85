import os
import pkg_resources

from .config import URL


def deploy(env):
    """Publishes package to corresponding PyPi."""
    print(
        f"Deploying bhej version {pkg_resources.get_distribution('bhej').version} to Test PyPi."
    )
    comfirm_responses = ["y", "yes", "Y", "Yes"]

    env_check = input(f"You're deploying to {env}. Does this look correct? [y/n]")
    if not env_check.strip() in comfirm_responses:
        print("Aborting")
        return

    url_check = input(
        f"config.URL is currently set to {URL}. Does this look correct? [y/n] "
    )
    if url_check.strip() in comfirm_responses:
        if env == "staging":
            print("Uploading.")
            os.system(
                "poetry config repositories.testpypi https://test.pypi.org/legacy/"
            )
            os.system("poetry publish --build -r testpypi")
        elif env == "prod":
            print("Uploading.")
            os.system("poetry publish --build")
        else:
            print("Invalid env, aborting.")
            return
    else:
        print("Aborting.")
        return


def deploy_staging():
    """Deploys to Test PyPi"""
    deploy("staging")


def deploy_prod():
    """Deploys to Prod PyPi"""
    deploy("prod")
