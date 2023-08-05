from bluedot_rest_framework.utils.oss import OSS
from bluedot_rest_framework.utils.wechat import mini_program, official_account


class CreateQrcode:

    def miniprogram(_id, page):
        res = mini_program().wxa.get_wxa_code_unlimited(
            scene=_id, page=page)
        path = f"mi/qrcode/{_id}.jpg"
        OSS().put_object_bytes(res, path)
        url = f"https://spgchinaratings.oss-cn-beijing.aliyuncs.com/{path}"
        return url

    def offiaccount_event_live(scene_str):
        res = official_account().qrcode.create({
            'action_name': 'QR_LIMIT_STR_SCENE',
            'action_info': {
                'scene': {'scene_str': scene_str},
            }
        })
        res = official_account().qrcode.get_url(res['ticket'])
        path = f"mi/qrcode/{scene_str}.jpg"
        OSS().put_object_internet(res, path)
        url = f"https://spgchinaratings.oss-cn-beijing.aliyuncs.com/{path}"
        return url
