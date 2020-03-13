import apiSend
import checkResult

def api_send_check(case):
    """
    接口请求并校验结果
    :param case: 单条用例
    :param project_dict: 用例文件对象
    :param relevance: 关键值实例对象
    :param rel: 关联值类对象-
    :param _path: case目录
    :return:
    """
    code, data = apiSend.send_request(case)
    checkResult.check_result(case, code, data)



