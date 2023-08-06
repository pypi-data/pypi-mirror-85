from DobotRPC import RPCClient
import asyncio
from typing import List, Any

IP = '127.0.0.1'
PORT = '10001'


class RPC(object):
    def __init__(self, ip, port):
        self.__rpc_client = RPCClient(ip, port)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__rpc_client.wait_for_connected())

    def send(self, method, params=None):
        res = self.__rpc_client.send(method, params)
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(res)


class Pyimageom(object):
    def __init__(self):
        self._r_client = RPC(ip=IP, port=PORT)

    def image_cut(self, img_base64: str):
        return self._r_client.send('image_cut',
                                   params={'img_base64': img_base64})

    def feature_image_classify(self, img_base64s: List[Any], lables: List[int],
                               class_num: int, flag: int):
        return self._r_client.send('feature_image_classify',
                                   params={
                                       'img_base64s': img_base64s,
                                       'lables': lables,
                                       'class_num': class_num,
                                       'flag': flag
                                   })

    def feature_image_group(self, img_base64: str):
        return self._r_client.send('feature_image_group',
                                   params={'img_base64': img_base64})

    def find_chessboard_corners(self, img_base64: str):
        return self._r_client.send('find_chessboard_corners',
                                   params={'img_base64': img_base64})

    def calibration(self, image_point: List, robot_point: List):
        return self._r_client.send('calibration',
                                   params={
                                       'image_point': image_point,
                                       'robot_point': robot_point
                                   })

    def image_point_to_robot_point(self, x: float, y: float):
        return self._r_client.send('image_point_to_robot_point',
                                   params={
                                       'x': x,
                                       'y': y
                                   })

    def load_matrix_data(self, matrix: dict):
        return self._r_client.send('load_matrix_data',
                                   params={'matrix': matrix})

    def export_matrix_data(self):
        return self._r_client.send('export_matrix_data')

    def color_image_cut(self, img_base64: str):
        return self._r_client.send('color_image_cut',
                                   params={'img_base64': img_base64})

    def color_image_classify(self, img_base64s: List[Any], lables: List[int],
                             class_num: int, flag: int):
        return self._r_client.send('color_image_classify',
                                   params={
                                       'img_base64s': img_base64s,
                                       'lables': lables,
                                       'class_num': class_num,
                                       'flag': flag
                                   })

    def color_image_group(self, img_base64: str):
        return self._r_client.send('color_image_group',
                                   params={'img_base64': img_base64})

    def set_background(self, img_base64: str):
        return self._r_client.send('set_background',
                                   params={'img_base64': img_base64})
