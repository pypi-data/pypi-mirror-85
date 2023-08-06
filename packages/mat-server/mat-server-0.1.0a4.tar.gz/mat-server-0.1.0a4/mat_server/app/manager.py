from mat_server.app.server import Server
from mat_server.domain import use_cases


class Manager:

    def __init__(self,
                 generate_default_config_use_case: use_cases.GenerateDefaultConfigUseCase,
                 check_config_use_case: use_cases.CheckConfigUseCase,
                 server: Server):
        self._generate_default_config_use_case = generate_default_config_use_case
        self._check_config_use_case = check_config_use_case
        self._server = server

    def create_config(self):
        print('初始化 mat 設定 ...')
        self._generate_default_config_use_case.execute()
        print('mat-data 資料夾建立完成')

    def check_config(self):
        print('檢查設定檔 ...')
        validation_report = self._check_config_use_case.execute()
        if validation_report.passed:
            print('設定檔檢查完成')
            return True
        else:
            for failed_reason in validation_report.failed_reasons:
                print(f'[x] {failed_reason}')

            print('設定檔設定錯誤')
            return False

    def get_server_api_router(self):
        return self._server.get_api_router()

    def serve(self, host, port):
        # 檢查環境
        if not self.check_config():
            return

        # 啟動伺服器
        self._server.run(
            host=host,
            port=port,
        )
