from mat_server.domain import base_types, repositories, entities


class CheckConfigUseCase(base_types.UseCase):

    def __init__(self,
                 mat_config_repository: repositories.MatConfigRepositoryBase):
        self._mat_config_repository = mat_config_repository

    def execute(self) -> entities.ValidationReport:
        validation_report = entities.ValidationReport()

        # 必須要有 proxy host 設定
        if self._mat_config_repository.get_proxy_host() is None:
            validation_report.add_failed_reason('必須要有 proxy host 設定')

        return validation_report
