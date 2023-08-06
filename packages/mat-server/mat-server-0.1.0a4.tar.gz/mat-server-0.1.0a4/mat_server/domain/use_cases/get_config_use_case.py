from mat_server.domain import base_types, repositories, entities


class GetConfigUseCase(base_types.UseCase):

    def __init__(self,
                 mat_config_repository: repositories.MatConfigRepositoryBase):
        self._mat_config_repository = mat_config_repository

    def execute(self) -> entities.MatConfig:
        return self._mat_config_repository.get_config()
