from config.config import REPO_TYPE
from repositories import ErrorRepositoryPostgres, ErrorPeriodRepositoryPostgres, ErrorLinkPeriodRepositoryPostgres
from contextlib import contextmanager
from dataclasses import dataclass


@dataclass
class Repositories:
    error_repo: ErrorRepositoryPostgres
    error_period_repo: ErrorPeriodRepositoryPostgres
    error_link_repo: ErrorLinkPeriodRepositoryPostgres


def get_repositories():
    if REPO_TYPE == "postgres":
        return Repositories(
            error_repo=ErrorRepositoryPostgres(),
            error_period_repo=ErrorPeriodRepositoryPostgres(),
            error_link_repo=ErrorLinkPeriodRepositoryPostgres()
        )
    else:
        raise ValueError(f"Unsupported repository type: {REPO_TYPE}")


@contextmanager
def get_repositories_context():
    repos = get_repositories()
    try:
        yield repos
    finally:
        repos.error_repo.close()
        repos.error_period_repo.close()
        repos.error_link_repo.close()


async def get_repository_for_request():
    with get_repositories_context() as repos:
        yield repos
