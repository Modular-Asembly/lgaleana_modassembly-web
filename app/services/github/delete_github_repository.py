import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_github_repository(org_name: str, repo_name: str) -> str:
    """
    Logs the action of deleting a GitHub repository.

    Args:
        org_name (str): The name of the organization.
        repo_name (str): The name of the repository.

    Returns:
        str: A success message indicating the repository deletion was logged.
    """
    logger.info("delete_github_repository called with org_name: %s, repo_name: %s", org_name, repo_name)

    # 2) Logs the action of deleting the specified repository under the organization
    logger.info("Logging deletion of repository '%s' under organization '%s'.", repo_name, org_name)

    # 3) Returns a success message indicating the repository deletion was logged
    success_message = f"Repository '{repo_name}' deletion under organization '{org_name}' logged successfully."
    logger.info("delete_github_repository result: %s", success_message)
    return success_message
