# -*- encoding: utf-8 -*-
from distutils.version import StrictVersion
import re
import sys

from halo import Halo

from suite_py.lib import logger
from suite_py.lib.handler import aws_handler as aws
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler.drone_handler import DroneHandler
from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.handler.github_handler import GithubHandler


BUCKET_NAME = "prima-artifacts-encrypted"


class Rollback:
    def __init__(self, project, config, tokens):
        self._project = project
        self._github = GithubHandler(tokens)
        self._repo = self._github.get_repo(project)
        self._captainhook = CaptainHook(config)
        self._drone = DroneHandler(config, tokens, repo=project)

    def run(self):
        if self._project == "prima":
            stacks_name = [
                "ecs-task-web-vpc-production",
                "ecs-task-consumer-api-vpc-production",
                "ecs-task-cron-vpc-production",
                "batch-job-php-production",
            ]
            artifacts = aws.get_artifacts_from_s3(BUCKET_NAME, "prima/")
            versions, prima_version_mapping = self._get_versions_from_artifacts(
                artifacts
            )

            version = self._ask_version(versions)
            self._rollback_stacks(stacks_name, prima_version_mapping[version])

        elif aws.is_cloudfront_distribution(self._project):
            with Halo(text="Loading releases...", spinner="dots", color="magenta"):
                versions = self._drone.get_tags_from_builds()
            version = self._ask_version(versions)
            build = self._drone.get_build_from_tag(version)
            self._drone.launch_build(build)
            logger.info("Build relaunched, check the status on drone")
            self._captainhook.rollback(self._project, version)

        else:
            stacks_name = aws.get_stacks_name(self._project)
            prefix = f"microservices/{self._project}/"

            if len(stacks_name) > 0:
                artifacts = aws.get_artifacts_from_s3(BUCKET_NAME, prefix)
                versions, _ = self._get_versions_from_artifacts(artifacts)

                if len(versions) > 0:
                    version = self._ask_version(versions)
                    self._rollback_stacks(stacks_name, version)
                else:
                    logger.error("No releases found. Unable to proceed with rollback.")
                    sys.exit(-1)

            else:
                logger.error("No stacks found. Unable to proceed with rollback.")

    def _ask_version(self, choiches):
        version = prompt_utils.ask_choices("Select release: ", choiches)
        release = self._github.get_release_if_exists(self._repo, version)
        logger.info(f"\nDescription of the selected release:\n{release.body}\n")
        if not prompt_utils.ask_confirm("Do you want to continue with the rollback?"):
            sys.exit(-1)
        return version

    def _get_versions_from_artifacts(self, artifacts):
        with Halo(text="Loading releases...", spinner="dots", color="magenta"):

            versions = []
            prima_version_mapping = {}

            for artifact in artifacts:

                if self._project == "prima":

                    tags_object = aws.get_tag_from_s3_artifact(
                        BUCKET_NAME, "prima/", artifact
                    )

                    for tag_object in tags_object:
                        if tag_object["Key"] == "ReleaseVersion":
                            versions.append(tag_object["Value"])
                            prima_version_mapping[
                                tag_object["Value"]
                            ] = artifact.replace(".tar.gz", "")

                else:
                    if re.match(
                        r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}-production.tar.gz",
                        artifact,
                    ):
                        versions.append(artifact.replace("-production.tar.gz", ""))

            versions.sort(key=StrictVersion, reverse=True)
        return versions, prima_version_mapping

    def _rollback_stacks(self, stacks_name, version):
        aws.update_stacks(stacks_name, version)
        self._captainhook.rollback(self._project, version)
        logger.info(f"Rollback completed successfully. Production version: {version}")
