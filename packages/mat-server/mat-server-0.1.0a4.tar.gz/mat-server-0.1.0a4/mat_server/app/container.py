import codecs
import mimetypes
import os
import shutil

import requests
import uvicorn  # type: ignore
import yaml
from dependency_injector import containers, providers

from mat_server.app.cli import create_cli
from mat_server.app.manager import Manager
from mat_server.app.server import Server
from mat_server.domain import use_cases
from mat_server.infrastructure import helpers, repositories


class DomainContainer(containers.DeclarativeContainer):
    ProjectDataHelper = providers.Singleton(
        helpers.ProjectDataHelper,
    )

    DataRetrieverHelper = providers.Singleton(
        helpers.DataRetrieverHelper,
    )

    FileHelper = providers.Singleton(
        helpers.FileHelper,
        os_module=providers.Object(os),
        codecs_module=providers.Object(codecs),
        shutil_module=providers.Object(shutil),
        mimetypes_module=providers.Object(mimetypes),
        yaml_module=providers.Object(yaml),
    )

    RequestHelper = providers.Singleton(
        helpers.HTTPRequestHelper,
        requests_module=providers.Object(requests),
    )

    MatConfigRepository = providers.Singleton(
        repositories.MatConfigRepository,
        file_helper=FileHelper,
        data_retriever_helper=DataRetrieverHelper,
    )

    CheckConfigUseCase = providers.Singleton(
        use_cases.CheckConfigUseCase,
        mat_config_repository=MatConfigRepository,
    )

    GenerateDefaultConfigUseCase = providers.Singleton(
        use_cases.GenerateDefaultConfigUseCase,
        project_data_helper=ProjectDataHelper,
        file_helper=FileHelper,
    )

    CheckIfMockResponseExistsUseCase = providers.Singleton(
        use_cases.CheckIfMockResponseExistsUseCase,
        mat_config_repository=MatConfigRepository,
    )

    GetConfigUseCase = providers.Singleton(
        use_cases.GetConfigUseCase,
        mat_config_repository=MatConfigRepository,
    )

    GetMockResponseUseCase = providers.Singleton(
        use_cases.GetMockResponseUseCase,
        mat_config_repository=MatConfigRepository,
        file_helper=FileHelper,
    )

    GetProxyServerResponseUseCase = providers.Singleton(
        use_cases.GetProxyServerResponseUseCase,
        mat_config_repository=MatConfigRepository,
        request_helper=RequestHelper,
    )


class AppContainer(containers.DeclarativeContainer):
    DomainContainer = providers.Container(DomainContainer)

    Server = providers.Factory(
        Server,
        get_config_use_case=DomainContainer.GetConfigUseCase,
        check_if_mock_response_exists_use_case=DomainContainer.CheckIfMockResponseExistsUseCase,
        get_mock_response_use_case=DomainContainer.GetMockResponseUseCase,
        get_proxy_server_response_use_case=DomainContainer.GetProxyServerResponseUseCase,
        server_serve_func=uvicorn.run,
    )

    Manager = providers.Factory(
        Manager,
        generate_default_config_use_case=DomainContainer.GenerateDefaultConfigUseCase,
        check_config_use_case=DomainContainer.CheckConfigUseCase,
        server=Server,
    )

    create_cli = providers.Callable(
        create_cli,
        Manager,
    )
