# name: 星空代理签到
# cron: 0 38 9 * * *
#环境变量XKDL，账号@密码多账号换行
import hashlib
import re
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
    SCRIPT_NAME: str = "xkdl"
    FUNCTION_NAME: str = "gogogo"
    DOWNLOAD_URL: str = "https://raw.giteeusercontent.com/kele2233/but/raw/ma/file"
    REPO: str = "Aellyt/kele"
    SCRIPT_FILE: str = "星空代理签到.py"
    SRC_HASH: str = "fd4dba558c57f7a5"
    CODE_PAYLOADS: Dict[str, str] = field(default_factory=lambda: {
        "3.0": "fChSVFBhY2tAUkQyAQAAKthiNUTpuQW5RSnOHWPDL09Pd21GQlZNM1NMb3hGSmRKbGFnMHc3UkszK2Mwb210Vkl2TGVTdHVTODg5NGt6cG9hYVFoNE5aNlFQdm41aWpRbHJmMTFmL28zMjRoT1NneVVCZ2ZyaWovQTVjQW1WSGtvR2xMdWJ0Z3pFQ0ZLTFNJcjVWNXBDdEk3Qzc5QXEvUHlRY3NqRGNNeHNIb1A3TVhVR1RHSDhWMjlQV2FQK3pURXE1SmRGYVUrOHJZeGRvZWJNL3lReVMvM1UweW1lUWo4MjAwcXJ4TnBIYjZqS2krc05QZHd3Y1VyNHNYTmNwQVRMUG0vbkw0clh3bUljUHVYanZSU0cwQjUzQWJYREtoT0dkMFNsdFNuNXR3ZDZYWTViQ2d6a2tpNWpSRHpRazBzNjJ0dlR0dmdybkhPWVBDb05IK3lucVJZOXRreTQzVlpkTWlJWWxyR0RlYnI2Y3NHR2pjSXBHeU5qSlZBVmF1ZFNQWGY1eUV4dDBndG9iV0IrbGordkVsUFlEOFVDSlBhZlpqdEU1WDd5czZERTBMMmJ1dHdVWDNGTW1ROWdwcXF3WFZLeW1rRHdUakRkcTBoMjZtY0lUMmRpaCt5V1NRRnlrMGNpcnZGQ2JIbXZZdE1vcU1hMmQwSXV4cndLWXZqNHZGckVZaDFDVTRpYzF2NTg2VnJFbnRmUUZzbnJocWc4d3BRaFRMenByN0FEbFRhM2VncG5acnNSRFA4S1l1MVAxekhyaEdaejF4Wlo1ckYrcVlIZ2FWU0xBeDdKdWlyL016Q2J1UUVvYitzTGVNS0Q3dUlUNkw0a2Y0NzE4eXNyaGJqWmI5SXpsQ2JaRXJ3by9WZTJUR1djYzVFSXkvVEYyQUlMbU9uTnhhdDVTKzdPNE1HSkd4Wkg0bHl5ajJVeFNVck1vR3lPNmwvYUtoUUpCWkJyRHhtUGsvdDJlczBXeVNkV1M3cE9qeG5PTFE1M0xQaFQzQ3ZSaGhRUjFzd0F3OEdMOTUrM203ZDFIYTF1VUZjakQ2NEYzTzAvT0dqWE5wVitPa1EvanRkMlBWVXArMm9qdXJpVEFZZGtGUzBxVTVvRnhoRGRxWi9ibjlkamIrYWdKUjJ3THZOVFRqTUUvMCtkWGRERG5FSWgrUWlDWm5sMllGNG1sTG1MUVpQTzFmZ0tPL3o0N1NvcElneDhCYTkvQU1KRVAxK1VUZTh0aThiSytKVCtzZGtTcDdYNmZGYUh5aXpBakVSOCswcnJPVEpXaTExUEJrTVFTWXBXbHEzdkptZnRWdTUzZEJiSHo5U1ZpTkVyT1FQcHlGU2diOE84MWRONjRvY1J6bDF4bDNUYWp6TTZzeEhKaUpoMkJkeVE1SysyNkRlZ1lyRFI3OGNkLzdaZUs2MCttcFFBeHF2ejRsQnJQc0NxcmxjZHpDTGZmd05tRXlOWmxRWmxRc3d2TjJia1BFbzRtTXF4V1NTQ3VIbm1IUzNNVEh1S0FMZE1wMW03SXdLNXRNSzVOdnR5T2ljejB6WTZ6cS9ZSFY2djh5eFF6Q0pvTWpvbzJxQVFhZVFHTS9CZDk1YmIxUDVhNllNeUFDQ2NkeDM5ekxPYk4vdGZIUFFLcWRuZFR0S0JpSUVFbEVuZGhHU29QOFJRWVY0UXBBbUozcFhBQTJBdEpqOTllK0RMRmdYY3lRNUpBQ1B4Ym0ySXEvRHJsRUY1aW9RQWdRS0lVL1JkNmd4OWFOTjBsVThZc3liSkdGVHA3K0ZpOW9iRkp3YlEvMUtLdWpSV0doODFQbzIvU1RtQTFWcWU3RWNvSlMxOGIycTVHOU1OUnBHd2loMEtkMm1hRHhMQnZzd3U0V3FVR0VKdkV1QUUxYkErUUZqVWZnWVRhQXZzaHB6SDdyUU5rcDNrRFdONms5cUV1ZWtJVkJudi9YYmJiQUgrQVdxaU1Sc1BNUHNBRklaR29MdEpodnU3SERMeEVUSThKVlJHZmNTcDlsejVyMm1GSUdKOGRIclUrZStjN2MrYXU5T1VJTFpSckJReFR0S0hUdHdqM1BRWVh4YVRvRlpzNGQxSWkyOW9xUHR4TFJvaWxwS2lkNmdWTy9JczlYbXdUNzJDODdjUGU0MmdKMVMyei9VVEFYeDVnNThzdzd3WWFCWWV6ZHhSZmNOMjZqTENvMzV2YkNmalZ4R01vb1k4UHZwNjJnWnYxVDA5bFpmOU55b2tKR2NUR01HYytaeU4rRVA0WWVaQy9JSUNxenNLeGVQRm92eG5BNDBubE8wYXdJZmp2ZHdOWVUwa0l1bmZLM21RYnFqOC96b1hZVjM3cHl5RlRLSUN2MXpVTnZOc0RFa1p2UnUrenZzTWkyODlSeGxGczVhVEFvb0NSRXc0Qm41U09GOHFmbzkwcFRkcWhodVlBZ1hISFZ6UEk4TWQvZG1tQkFBQmRwNzR1TGtKS2hrRjBCc2RDN0NxdmZCem9VRmtwZ0xCcEdMeXdMN2FRbjdEV2QxU2src3VBUmJmNzVOc0N4L056T0ROVjNsKzB5bXJsWE5uWHJGbWhjV0tvY083M3ljVmNFRXBCOUVEOTNudWlkSHpLMHVTZVhMWVpyWG42ckUwMkxGNGZ2ZXJHMW1uMjZkNGlWQ1hiVmFIRUdpWStSTjFoTWNxWHp4VHVNdTJ3MlVQOVovQldQSGZSZFJTSHlxRnB3REJuUVpEQy9XaVFMTDdENDNoOTZqRTUxYnV1UVRUUmdNendDYTBxTGtXZHoyMEJ4Tkg3VmxzN1JWVlZQbnBTNzRtbDhEYlZDbVpGd2VGbTRkWGh2cDM1a3FUaDVKelo0dTZ0ZGxoZzVQUEc0a3B3WkxrZ1pGRlMzWFh2Q0dKYzVSOWV0bUpBU1VIK0lzTkhNOEJwZ0dmS1IzaisrSFBsVHFJbWZVY3NMRFVKbU9jd210a0hSRnd2RFROa3RXTFozUFp2QWRnL0wyQmFnQ00zemUrL0ZPY3MyVDNlS2FUbmJ3S3BMLytjMHByekFOU2FZc2cvME9jalJGL3pjUHpZS01iVlBJRHF2VTNaTjJIbU05LzRKbTBvMnNwc1NUN3FzRzFGTnE5cDZPT293VlF4UDdtRjhvWTFRdU14UmxhZ3pYRWJleDBEWVBHQVhTWUdCUjMxVjZEZGsxZUpTVDQ1b2plUXluSlBWUzdDNVdkaDM0VVp0TGQ4ZXRlSUZZZDJYdndsc3h5ckhEeS9OMVVaOHgxdkpXcWp3YS95ZFp1cDhBVU5rTlUvRFZGTEhJaXA0K09MSytzdllpaThEMkF4WFB4Z2xHZWVDc0IwcEVReVFubEl0MmNPT0ZXM3JQZ2VjUFNrVC9CcW9xQlErWHRPdEhDdjBFY2xSMXhCT0Vwa2hBWFJhOWtuNmtkaTFNOWVwSE5xcnVPQ3BROS82bzJiaDZld2krV2F6WVhtSk5qbWtmL3ZLZHo2aHB2N3BYc3Z5VFRsa0NTSExTRFQ5ZlQyc2FaZDhrVFkxVW5ZbmtnSnR1Rms3NHV0R1dxL21MVnFZL0t2ZGdtYXU3RGZwblV0ZmJxUHNVc1hlZzU3cDN0NXJWeStlUjY2Qmk0QkoybmNSdFVJTTVTTjdsMk83RXJnaU9kcFZnRWNpNy9YYmRsOEFpdTZuMVRRaEpwajBRelJhUEtSTEthdGpSdGpwUTgrVDlSdng2MXNDWm1NWVFNR0JKVWRYYXNrcmt1YS85YVhHUmlKOUZtemh5akpRdTV4S25aVU1TSUE3aFlJSXNGVDJqMEx6S0JHTWZOUnpNVzI2amN6OWQvVk9hM2JtZEVla3lySlFZaGE3T0VRQ3A2cUE4VVRyVDNHR2duRy9BRDhLT29EOWZycTc3bExQNS9GSkc1SGxESWFYK2UxNUM3cU9aZGdYUzRiMG1Sbjh5RHNrUmg2d1hTQzdyaFdYN2s2MHlqTmZNcGU5ZmhHVm1pSU9VandieEhZV3JkOFE4VmN5UUxJTmVFVWxmbE1lMEpZZ2t4cTREWXZSQml0WlNpRjlJc29iUHg3VHpyaUdtWEpXbzI5R0ZIdzIzbXdobThoREsySzZTVDBCU1k5WkphbVZyRlBab3dqb0tkNzhLNDFqYjV4SmdMWEV1V2NhNzdFSDYwa09rUXB0bjNCVndxM1p3Vmlqc0dkdThJMzg4S0taM1pqeXJibUtCU3ZmTWcyd0M2R2NJYmNOOTZtOTRWTnVscnRWbWtTdUlHV1orRDRIQnBrQUtjVEh0N0RLVUdXMWJ1RXZHem5QZC9OWnRod3JDOGNqNkZ2N3lGZSt3MTRZV1ZMTXZQNTlldWRtTk1ubSsrTFNtRVBmOThqRW9iY0RWMWpsaEc1LzJhV1RaWEFUSE00bkw3bnZIOFJWYzRWeDJRRzVqbTFBVDJkajB3akZsdWVJZGVrVVN5SnpHKzZ2VE9raHM0dFFuSVlrOEwvQ2xkRDUzYzFlcmxvcXJmVTJ4a1ZPMHc2NmRRT3VXdWptZFFUNUdVVVJvNHkwcmVZRGhrZDV3NzVBajZiZlY1cGkzaHlKemE2NGNNUW8xbE1EU3YwR2RycVB5QUNjMll5MTEvMnIzMHBVZ2RaZk8xZXNOU3B6NnF1aEVrZWoyeDl1Vjhsd3dMWC9TUnJTc3VPdXBOSUJFWVdJcUlYaGxVZ3ZTWUtJUXRRMlg5YUt0Y1lCNXV3aU0ybGFnemJ5ZFk5VlM4WTdJb2tXN051K1YyUjNLVjVQTCsyQkFDRUpVdGp4SW9VM1ZJbGhSRGpqOEV4cE9uNjhFYnp3dVAwRGl5bmxJZm44YlJyUmkyaW5xQUdERXI2NjQrWEdTUnRTSFRQMm9DeWpGRUoxQmNoRDhybWFXWlJ0Tm1qYUZOMkQrVzdhMWhLNVY2M2VYbHkvRXlCQjR6VFo1cEFNUmtHU3B3WEtEUkpFWkJzZmlqeEUyUGE2aWJvVk1EeTdxTmlSUHBaWE5tWlFYRGVyRm95NjBvMkJETC9xVUJlYUVqV0xWbDUvTEFibzFmOHlGUWxMUGxzZE9HWUR2TXpxYzZGSm96aEUyaHBuYmxBYnNYbXBFaEtvVG9lcUcvVEJHdmxjd1kxMzltNkVIN1M0c3R0by8vQlZyMklNb0c5SGQ4RUF3T3FHUFV6VlNLaE5VQnM2WUxzQzlDSGZwWWRYdjJhclhCWVZYS3MyVmYwd2ZGMU1lL3Z2TWtUUDlRaVFuMjgyVnU0MHN3VzBBYnE4QnJ4MlYxcEJnU2lYTFo4eXpPWWhzZzBmWitZN0VzU2ZCTktaTUhKN0pNUE5tbDdDTXd5dUN6SzBqUWlNalIxWnJjWDMzSzVsT0ZaMVNOMFIyZ1NVbFUrUU8rWTFBSCtvRldmZ1BiSmgzWFNGMmxRMnI0cS93TTBjL1NmVnZ5bld4OUNLQ0Ziay9jVlNOcFZXYlRadlVVamFhLzAwZC9sN3NoNjFWdWcxdW1yTHZXeWZUUFpqUFBXZ1l1cGF0WVRNdlFDK2ZmRHNMUUp0M0RLemVWMDdpbENncmlHMFhqR0NZZ2FBaHphd2tzUE5ycERZekFmc2lKc3hlMjFRZ3M1VjZweUJGS3J2cHFLT09HeTlnbnVoSnNJTUVPYzBBOUdoNlhRRFY4eXBqbTNkUXlkblllb3pwZTFhbEJ2dG9yeFVjblpzM0lOOTA1bHduRHhlcFZHQVRua3FCWkNMek9aNmVKc3Bsa2ZHc0dZWjJqWDVkbEZPTkoxTVVhRDdXMlBYbVpES282Rmx4RG5oUnpkR0g4THdxaFdobUl3RjdxRHgyTlJKTlM3YWcvNjgxRm1QY3ljOVRmdUJSZzY3N2U4WEhUOVRDcmkzVHhQZDhnZmdRMG12VkYzOXpnc3BGSkxGUFpyK3RvMzJPakJwaFNYKzRyUTlnZGNIM1FLRGJYRWJBYjNQZElZSG1EV3ZHQW95dkN4TUpyQkhTNHZuNkQ2UTc0bEpqNHY2cThKdm42c1JQbkFoaGJxZEw0cFk0RkF0aGVxMVM5L2x5U1RubHhTQ2h1QkpFMFVJRGF5cC9OSUliZkdldGhwa0ROWDhETUYwaFJXM1BBaTZHWVpNaFBFKzA4elpaMUxuUUp4Y2toR1psaDZjNGE5ZW9wZFhOTXRjTG13NG1JK3FubFpDSVJVdUZMTm16eVk5Rnh1VGJ1WjFYM2d6VHpVNFJMZ25Vdy9wZFdlWjNnQmROVTkwR1BILy81eEE1TW9vMDg4Zmd1ZzZRd2taUlk1VmRMZXdRekFQalFnL2RNTjNzWEo0K1ZsSnArVHMxRFlTbTIyTXZKbVV4czVZd0xic1lMQjkzdzVtb0haSk9vdmd3ZExrZFVvcDdHdW9RVHVrOGpFa2F4Ny9qaUlRaWxkQk5jS0p1Z0VNZ0JjRHFPYmtuNG5KeXBzcTFiVUxhWHJ2MEw2SklTT245ang5aHI5SDJiNXJ0b2lsbHVocXhKY24xRERtNHd4WEhReUlsaG5KNnJuR1ROUVRGSngzdGhDQVB0amNLYzVvTDMzT3A0ajdtcy8zUmJEanhFMm4zcjE0eUpMckFRU3ppVkNqa0ZTR29aV2p2WHhSYmpLWjdaVmRGcFdSMy8vc0RtT2haWFVCS0diT2wzOEtYWkI5bFFEc1V6emEzb1o5clc0Y2pwcGY5Q2tnbTZHcEpHM0UvRytQWngxbWJCZ1FoTEVFQzNOdG9MYXd2WSsvR3JPQXZrMnh6T0pPbC9yak5vQnh2d0RGNWVrK2p2N1N1Nmk4aGxocXhzR2RNekZHZFpzZ1Z6eG1RaTcxMVVFNHEyQ0s2WWdLN1NBbmZkTGhsakVWZ1lGbkNWWDYreXhEVFpaRlZGekRiMENRWDdhMEsrYllSWGk3VHIwRGJYRXlUbk9qVDNKUVdJbUFQYkkzUEc5eGR4alBMNUI5ck9tRk5TdW5HaGRma1RjaHJ2RzlrV0cwd1NZZ3JKcWtzOFFCN0pjbVZUZVA4TjJzVHBkSUI3WmFoQlFLSStkNlJ3djFvV1RSbmgrNjRBcExZMU1YRDVQMmR5VlJvREN6TzhCS0xwR2tqZnMrL1dIcGtGMEM1eXN0amtLWFdkYmxoaFcyUWZLMFMyVWZkZUlPRmE4TmxrSll5Y3lRTUVCMUtGVHhZbi9TMTJtczdXcVBQR0t1SmxvMmdpYXloSW50TjNidmoyaGFaMStXaFU0LzZDbjhlanFjY0h3NU1hWUQ5UE9VTWd4N2x1aHdUc1JsNzVVVFV1RlFnM1dKN1d6VXVVNzFWWlA4ZGhwTW1mNUtnUm9EOUw5TmlLVWg0NDkrVU44M253S1ZQc2hFbkRlU3dHTEh6MEZIV2NYYTA0Z01SM0tCb3ZobnhxWTU0ekJLeHR4c1JKNFBlTzJsOHc4MTFGZUViVXRKMHNsa1R2bkQyZkdscVpDRmdWTjlkQnlJMjUybEdQMGdua0l2TlpvRy9rM2xjaXVpTVEyUy9hMitHaXNHbVAxUy9PMGxYeVhNNnplQmtvSGtaYnl5N013S3FRc2h5eDltK0UwdUpKNlllaXMwdktZWHNFcldvTnFUSzE2cGJYWGZuZFJRUDJDU3A2U2czZndOakhIMFEwTDJ3Q3R6bC9pb0Zsd3NydmVRUEZxMnlUc3VqMmVJQWp3ZTVFNDVsVlg4QkN4Vy9NS0RFYTI0b0JEN3dPampuUzRhb2xYVVRQTUU5eXVkbnhUWXBZeC9Ka2xNalpaanBJa2t1N1lsNC9ud3V2WS8wU2tJbmJ4VnhyaUFhTzF1ZW1TYTZ2MUoxUkE3RXpzZHFxTk1GY0dXRm1oRzJ5UFBaL2lEUmdnUjdHVDB1YTdVOStPQ0Z1WFArWVJXZEI4ZUxlTVlnRjJBZU5sYkw2QmVhc2RITThuaTUxMjBBTW1aNnB1d2tENVZvcDBEWkp1Tjd5YkViTUJuWjBpRWlXUTJNMTVqOElkdjl5TFJWUGtLK0VDVndRKzFyQm5YNFJMaTAyc09UZmdVNWwrMHlZRU96QURBQU9LakI2ZDVVUGR2Q3V5cnhoU2dxV216U2tlbkZtR0VlWktaUVRtaWs0ckQzZjdzbGZBVDVxazF5ckZxbnowTVNqVy9OUHNnY2E5Vld2SUs5V1psMmV6N1cxcjMxRlc3Zk42SnZ5cTJ4YXdlNEFRcmsrNDY1U3RqTmswaEl4a3IySVhqSUJLVjhYZFNkcXkvYUU2QkUrKzlFYzM2K0ZUZG1hY1ZXdllma05iK3JTMTRtUlZzTml6cXlCd20rS2xPOFdYaWRBWndOOXM4N09ITUY1VDZqQTYzSnlUb1psUjdLam8xeGdzZ1M5bEg4Q29JQXltM2VQZUd4TDNtOFg2cTAyV3Y1OG1nSWtNZzA4Q0dLczZ1UlRmaDV6ZFl2NllPLzRydmhVWVY1RURtNE41NlRIdVdtM2dtRFR2b1hWU0dNTUZoVHZaMm13NzRkQjlhenEwdTdHNTQ1UFZpbHRRVXQ0QzVYZnRTWk1tV09DZWVEeGFVdjhHVlRVZ3pvTHNSK0NRRCt0ZGxkYjZFNGNkTlpPZVBZOWkwbWpPazh3NzVxbkJKSVh6TFc2UDVJeWlNblFDVUVmNURkSUhqMjJvaXRIV3VYUUhJTmMydVBZZlV0a3RaYTVDcmc3SEl0Y3ZaaHo4U2hJZGNzZGM5dWEyajVPa0JwNFBGUkxzQ01pTlVBcklRVVVacmw4RlVMQ1pnaU1NTzI0cXpDeVh3TGZqdmdLUlJxNjVhYzZJL1gxbTRXQnZzdlFWNVdKSUNKSnE0QlUxUm1HMjYxRzBBb2c0VFMvcGd2TXVhMEIrQzRXMG41Y3FhS2NIN3dwNGZjY3NIOEtuL01wUEJFcm5WVFZBUlhzejRmMlErQWFLR3hROXV0RVpVcks5bVkxeVBzeExJelh6Ung4Si9lNjIzbG8ySlE4b2JtSlBxWDFabEp5dVRHRnZxYTBDb0h1YlBJbmIxbFZZV3dvZDFTeDVDOGZwZXp3WjljdGlRNU1iQTBKMXdVT2FKazllbWsxaXlnWlpLTEFIREM4bHRPT2xsNTl3M0RlcHk2SThXUTdoUkNNVzVmTnBaUWZsODNHdmk4b29GeTgvRW4vMEdtUklXaDE1a20rbHBaaW8rUmtpSXllM0I3Q3dQYVhlZWY3TkJzOU9QaEZwNnpTaTRVaSt2Tm5Xb25Jc3Z3OXRjS2Z3MzdycVp6Q0RCZGI4UEtjeGw3Z2J6WXU4UkkrcUMxbU5KeTZXaXZ0ZlNkK1BiT01iV0Y0VEFmc0FyQjZoYWpqSkxuZkdqaENqZmwvSFVUdXdjZmVtVGk3WnBXdWV0NnlkbmppNHNzMVd6eUk2akZ0WmF3Y0IyMWRsUkhkY0ZIMnBnVFFob1V2TU0wcytsOXR5OVByckR0VXZ2TXpjWEpycGpjWEVzRnVtRVFIYm1hZ3V0YytHMlgxalNKZ0RIQXlzREpCQ3JIZEVIRFdRMVRoaVVCRTU4bTU0MGVmQmZuZy95UUl4MDJtV1RoOHh4WnJUeXI4Q0dJblhZSmV6eFJnUktITVRmQXNHZ0liY2hRRDZyZWkxMFE5eXdSK1RRS3F5M0JXeHl3SUFyVkNCcHVkb3RWUGhJQ1MzNVhOdy8yOERtbDdVMWRBZC83cnhkaStvdUxTbkp2aGtpSzJINmM2RE15S0l0ZWtyV0Q3SGg0dk1qc0IvUThnQ1gwcEVRLy9QSUNCcmRxNnpsZUYveWhDbjNmRkw5Njl4SXd3emt4ZzB4ZWRFcUd6VkRaSjhmYXR5dnJoT2ZCZGJ2Tnl1TlJ0bVBVb1c2Nm00czNVNXRaenh4bXYwYkszeGlxaGVib0cxeDdGcTZwMnZOSUxNUUVGNC84MTFDMTd4UThzQjJsZnNWSGI1WEZkT0xTVEpDOWtuV0tIL0M0eHBUdlBlYitBenNKVVBPYUV2cURvclhha2pUT0tocDBUM1RLUGNKVnl6YTNvTldCMTgyR3F1bzRUNmlLVzlTRG1wS0ZtdUlqcGRJeFlWOHdubUlLODZiNXRaSWxaYWxWUVl1eXZtQXB3ZzdiU2RyTitITUs2TDVFK0gzMmxVTzcrbjZacFpzMGloalJFV0M4K242R29NaVBKU1JEOE9WSzg2dnI2QU9MS2pPLzQrenJBNHpEbWtEdG1GZURiZi9VcWpaa1h4TnhVQ05qOVJ0UEl0Nk5QQmZFM1ZuVndKWGRIMlpCTkNqQVNvZUU5U1Bxdi9rSFFkdE1nQnRTeW40dGF5V1dEYitHM29tQ3dDVWs0Y3hYTnV2YXdrcVdRakJsR2tmQ0k3TUJrRmdmTGx0QXZDbUN2ODcwZ3E2OXFvRitBMFNONm1TVXI1dXBmRnd2YWIzT3VraVliSGdXWXNVQStzSjgzZkdVSW9aZ3lXTFVCYjFoUmFiL2NLWjZDOVpTRnB2VlZwTkN6RkNpMHZQRWxTL25XUGRmYjZTZ0tIdXFGNVphamJNdnRRekxWWnQ0clR3UzdqUklra0Znb3ZTQTAwaUp5LzU2VlhSUEsreERnM1JLNEkwTVRtMTRzVHJaMEdlV2podE9ER2ZQRURsUlFlNlp6VEtmUFl2dlIrZWRObW0rNFFtTS9UM0FQSHpUaFJpM2tLS3hUTEJjWUc3YWdlUlVRanZuTTRHUUVMdVZyME9OVm9TRnV5NldTa0lRTmFuWU11YUdiZzRjYmtSMGZYaGZhWVl1UUtIeDB3bHc2bXA1Y0NwOGRLNERacTZKVWNWN1Bwc0Nmd015RGZMN0lBVjRsSVFnc3d6RjVwelN4TjRTK2RPcjNGVHFtb2pqVHM4ZmJoVlBDS0JsWWxQZU8rL3FpYk95ZklZWHVheHdiS2RLREpzNFljSG9keHFGZTBqT291cHQyVU5JNU5oVlRhR0VJUktuLy8rejJOakszakNuUThEUE9ySUJvb21scUNsbWVlbGY3aTVWd2Q5TjREdkd4VTg2Q0NXR2NyakVBbWFiWW5Ob1ZGeStUMms2aDFtaHpwaWNBRW5RdmNxbWlKOFVOWWNNWm03V2hFNnFvZlYxV1dUZVF2b0tRWHgxc05PTkNqdVNuVmVWMjJ0NWpZamVRWG5sU2QyQzRWTzB4MldiT21hQ3JubTZSelJ0dEJsVE5mU0dtNlZGY0R3NnozZHV6VFc0OXpaNWR6QXNkYWxmdzhreDFHdUtOaG5tUmE1anNZeU0yaTRiSmpLVmlscVd2STI2eGJ1RWE5bmdxTzRLRVdkdTFlRHBVSXdDL3UyWDNjSHgyd2NCbUNOc0czMWZVYlYzLzNMd3d1bVVkdmhhb2N2YTJEOHAvbWNsT2t0Mm9aYmtFYXRFdThLRjlvZkY4U3cvWGo2RTFRTCtET2lSbjE1cU1YTEQ4ZE9TRG9ZU3NNdHlXMXZEZDJmNnVjNmg4SEJTNVM1eGRodExIK2VDYjE3RWJnd21ZYVV1R2Y0b0psUlpCcFNIOTljbmRvUndaTWV6enRmQ3YxSVNONDNOcU5EU1h3bGZQdU1ramZHMXk3Um1YejZiMW5mMHBlQUtQREhiTTlUeW1XRFg3RmFubHZqeFVXUTBLbDBJbjRiOVg5UGkyMkVvRS9RZThEWGp5RHdnZU1DMU9rZURaQTMrT2dsa3N3QUVVakd6aHh1eEFFUkttT0NzTVB3NXVyOFk4d0ZDNHNCa2ZhT0NrdnJyM1N4aVF5Q1d0dUxPUkM2N1J1ekVGRWpURkZmanhPVnIwSHBtYkIvc0xUdlhGYlIxc3VCSk9DUUhESmNQZXBES2lPMWhNYjcyNldIVU9yU2kxRnN5WWlmRDljYk55ZjBwL2ZrcTh3dU9mUXp6dTlERzl1bDlrRW5mZmd3ZmNrUDRoWHkvbGhmalp5cWlJRFFvenJFYzhxUmNrcFdVV29kQ2QyRUp3bUluamgyOWNHNWpKbmtDUmpSYzdhTGJ5cEdiU2JTdFYrSFFENXlBYnhRR2FkZzdkenV2MmswU2N6VzhjbGJ3ZWdoalZrRDhTTGJMVm96akN2M3B1dk95WTJUQUZCc3ZTWjd0OHZwN2hvZ0VSVTVrbTZwTzMxZkVaUjBHVXFnSitHS1Joc0U2K1BXMmlyUy9iRHpRUjh4cUZTTERRd3d4UmpJSEk2OGZmK1NxeFNiT2k5SzBISnc2b1d1eXdaWEUzTlNudjlSQVk1REh0OFBTQ0pockJLblZwb1lvSTEvYitrMFNOTGNMUFJ6ZWxXOUtTOWFCUUdWcEJiR2R0dk43a0crVktCd3VCQ0dULy80SmkxSmN5N08wcDZlRXRVdVc3Rnl5TWRzWGI4bDFwTEZjVVluQ1hVM1JpcDE3TU1QWk9Hb1dZNWpjMVJSdUtacW1DamZDRGdYS1AxQU90bHhtQmRWYkZKS2JiemZmNy9pcXVUU2JaT1pTYTE3TzEyL3pUOWJkOTZkZEViTjdLRXA2RkZQNW9XNTgzT0RucHVIR3R4NDZpS2R0MHM0dEFJTTNxY09tTUFOMC84ckkxOFBGRFVReUtEQW90MDBlZlM1VUtDeCs1WUNqMVNqQWdQS292ek4zd2ZrZkdNZk81M01HM3Uxc2NvaVhMRFZhWC9xSFdpb0w0WnRlVXlPTVlqYzJ4RTYxNGpjcm4wdlFWSndFWTFuelFyZ0VjVldyS1g1ejkvWWZMUWZFNGtJVnpqMVBwM0Z4MXdkcTh5NXNRb0tMTGZOVDhaYk0wNW9FWUtRcUZRUEdlRXB4MXlVNUkvSWd3MTh4eldEUTZaSTRaWDhPNWQ5ZWp6REhMcUl3bUZvc3ZZeU91U0NjeVR1ZVlYRjNBUkRjQW5BZENmT2c1SmtTMFpZRWdDSVd2bkRvS2wzRVhpUEFXLzVGSnczemhnTW41OCtseE15YUJMaHgwblA3cCsyS3JHVE8wbmNaeW5mMTR0MSsvS3dFNjBjNmttMUpZSUM5b0RZUzJoVU9ZbkZ6YjhvdHMvYk5aZWk5Ymw4YTlVRGgrdmZFeVBFUGsvU2w0bmxwWG40ZWtCOEFEWDNTb1haeGM0ZS9kT1RyZUJVQlU2Y1dETXJwcjR3bG1EYk9aSm5LemNvMUc4Q2ZnSHRSRFJtQ1pUS3NJQTcrSmJYSTV2NXBvZEpwUm5LMjBsVVlUQUlxV2NacEt1NTNUOXZKQ2VIcWNyaUYwLzVuZHFZMEM4YVozeDNnQ2p2TDZhdTdHV2RnUGZ0b3lEaEVjTWIweEsxL2ZSQlJjUzRHcnVSbmNBNWhqa0RjLzdFOE1NS01sVzZackhXaFNSamh1Z2kzUjFZUlNnRGUyQ0RNbnNVL3NReXNzUk00SUpWdWZJNGZCT0tZeVJhYjVBeW5lRTFZWmtuZkxRZVBGWlgyQWlyTTRINFo4UmdxK0wyOHorSlMxSnp2WWJjeG1xQm9QZHd2a0VWYmwzak02ekxyRXRkUHZXL0hndlMzSkpNc2pqR28vVXdWSERFS0FHblBSb2VaV1dsZ1FjYTk0WGR6VkFyVmJRQk9MRlZ2VTNXSmVXajZMUTd5bzYvM25hRi9EV2RKWW1obTF5ZEVTaFdTa3AwbkVqZ1o4V2dLNnBXcnExSVpDQVAzK05ubjFBWEtwRkMxdU1NU1hiWjhCenBrTVZpb280bklsVHZDNVNMZVZpemsveElla28rYVNZc0U4QkVhSTE1T0xwQzZJNG1xRlVRcGp2ZTFmaGZMazRIWG10Rys0OFVybkhqNWF0MzdVb3Y5aXdydG1UOENiR29iOEFob3ozZnZGTktXTDhUQjBLZ1NJWFdJVlpaR1p0K0pzY0NKQmg1ZmhZV0NNeDZZR3RjMjV4V0lxSlhXWngyWVplZUhzVnQ4NmIrVzhCVGRXRmZYSTJldHcvb3RnakxPTFBmSnpmNXd5Rm5MWUkxdVBZNTMydFRHUjhvdWpOZGRWcDNVcDdDK0IxUUlhNDR3MTNCUkc1R1JBOE1uOFJoYytuMC8wa21wK2pBQ01vSjNjMnhTY09NRmliWDF2b08rckFjdUlidDI5OVcrUjhPdll0SXA2YlQrR1FOcW85MHJMTnVjckxGOGsrcVF1YWNrR2NRZmFwM2pRQ1A5VmNWMnZ2YTNLWVgreEd3V1VOK2lOcjNjRS9yVjIyMDlSbFI5MC9XYm5tZ0lVWnA2ZFVwK0RjVFcweDU2TERjMXFxaDdaaHd4b3NNRTFEWWtTbG9VZVNobk8wVkFCQTBuem94MnpqSmpnc3cyMlNrMTNTYzFINmQwak55elJpaUhlWDJkOUIrTFZvc2kwaFl1RGxPUk9EYUNLSStJcUdvSDVITnByL2ZOT3JKOXp6bFIvaGEyRXpSc2dQMzBKQmY3aGNYeDdxeDN1UjVuQTdVMkJYajI0aHpMTkNqWCtpdTEwbGVnamRIMjhqZ1I2c28wWXRVaytlMU9HYUVSZVp0a1F3OGxQQm00UVdCTitrb1o1d3RUN3hlRUhiK1ZvVFJZVisvY1VjU2JUbjhoTDJpZkp3RXdKZ1pkdkQ1TW4vSjRjeEVGVUpVYzhyOG9KeDRVRnJXck9OUGpoV25WcHFjTFNhbDNwejJLby9zc0hoVDVQeW1DdFdjSmpsdzR2azBKemx2YUFvbCt3RE1qMm5tRzNqU1pQbGpXMHZrRFNQRnd4VjhGV3dvM0hESituOXl4SEl3SWl1Z21WUT09"
    })
    SUPPORTED_PYTHON_VERSIONS: Set[int] = field(default_factory=lambda: {10, 11, 12})
    SUPPORTED_OS: str = "Linux"
    SUPPORTED_ARCHITECTURES: Set[str] = field(default_factory=lambda: {'x86_64', 'aarch64', 'armv8', 'armv7l'})

    def download_url(self) -> str:
        return self.DOWNLOAD_URL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

REPO_MIRRORS = (
    "https://raw.githubusercontent.com/{repo}/{branch}/{path}",
    "https://cdn.jsdelivr.net/gh/{repo}@{branch}/{path}",
    "https://ghfast.top/https://raw.githubusercontent.com/{repo}/{branch}/{path}",
    "https://gh-proxy.com/https://raw.githubusercontent.com/{repo}/{branch}/{path}",
    "https://ghproxy.net/https://raw.githubusercontent.com/{repo}/{branch}/{path}",
)

def _load_so(path):
    import importlib.util
    sys.modules.pop('nxloader', None)
    spec = importlib.util.spec_from_file_location('nxloader', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['nxloader'] = mod
    spec.loader.exec_module(mod)
    return mod

def handle_errors(func: Callable) -> Callable:
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

class EnvironmentChecker:
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

    async def fetch_repo_script(self, repo: str, path: str):
        qp = urllib.parse.quote(path)
        loop = asyncio.get_running_loop()
        for tpl in REPO_MIRRORS:
            url = tpl.replace("{repo}", repo).replace("{branch}", "main").replace("{path}", qp)
            def _get(u=url):
                req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as r:
                    return r.read()
            try:
                data = await loop.run_in_executor(None, _get)
            except Exception:
                continue
            if data and b"CODE_PAYLOADS" in data:
                return data
        return None

    async def remote_fingerprint(self, filename: str):
        url = f"{self.config.download_url()}/{filename}"

        def _head():
            req = urllib.request.Request(
                url, method='HEAD', headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return {
                    'etag': (r.headers.get('Etag') or '').strip(),
                    'size': (r.headers.get('Content-Length') or '').strip(),
                }

        try:
            fp = await asyncio.get_running_loop().run_in_executor(None, _head)
        except Exception:
            return None
        return fp if fp.get('etag') else None

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

ETAG_FILE = '.nxloader.etag'

def _read_etag(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return ''

def _write_etag(path: str, etag: str) -> None:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(etag)
    except Exception:
        pass

def _load_local(path: str) -> bool:
    try:
        _load_so(path)
        return True
    except Exception:
        return False

async def ensure_loader(config, file_manager) -> bool:
    local = 'nxloader.so'
    local_ok = os.path.exists(local)
    cached_etag = _read_etag(ETAG_FILE)

    filename = file_manager.get_so_filename(sys.version_info.minor, platform.machine())
    remote = await file_manager.remote_fingerprint(filename)

    if remote is None:
        if local_ok and _load_local(local):
            logger.info("无法获取远端版本，继续使用本地 loader")
            return True
        logger.error("脚本无法正常运行，请检测更换环境")
        return False

    etag = str(remote.get('etag') or '')
    if local_ok and cached_etag and etag and cached_etag == etag:
        if _load_local(local):
            logger.info(f"loader 已是最新（etag {etag[:12]}）")
            return True
        logger.info("本地 loader 不可用，准备重新下载")

    tmp = f".nxloader_{os.getpid()}.so"
    if not await file_manager.download_file(filename, tmp):
        if local_ok and _load_local(local):
            logger.info("下载失败，继续使用本地 loader")
            return True
        return False

    try:
        os.replace(tmp, local)
    except Exception:
        pass
    _write_etag(ETAG_FILE, etag)

    target = local if os.path.exists(local) else tmp
    try:
        mod = _load_so(target)
    except Exception:
        logger.error("脚本无法正常运行，请检测更换环境")
        return False
    logger.info(f"loader 已更新: {getattr(mod, 'version', '?')}")
    return True

SCRIPT_SHA_FILE = '.script.sha'


async def ensure_script(config, file_manager) -> bool:
    if os.environ.get("NX_SELFUPD") == "1":
        return True
    repo = (getattr(config, "REPO", "") or "").strip()
    sf = (getattr(config, "SCRIPT_FILE", "") or "").strip()
    if not repo or not sf or sf.startswith("__") or "/" in sf:
        return True

    remote = await file_manager.fetch_repo_script(repo, sf)
    if not remote:
        return True

    txt = remote.decode("utf-8", "replace")
    m = re.search(r'SRC_HASH: str = "([0-9a-f]{8,})"', txt)
    remote_fp = m.group(1) if m else ""
    local_fp = (getattr(config, "SRC_HASH", "") or "").strip()
    if remote_fp and local_fp and remote_fp == local_fp:
        return True

    def _norm(b):
        return b.replace(b"\r\n", b"\n").replace(b"\r", b"\n").strip()

    remote_sha = hashlib.sha256(_norm(remote)).hexdigest()
    if _read_etag(SCRIPT_SHA_FILE) == remote_sha:
        return True

    cur = os.path.abspath(sys.argv[0])
    try:
        with open(cur, "rb") as f:
            local = f.read()
    except Exception:
        return True
    if _norm(remote) == _norm(local):
        _write_etag(SCRIPT_SHA_FILE, remote_sha)
        return True

    if "CODE_PAYLOADS" not in txt or f'"{config.SCRIPT_NAME}"' not in txt:
        return True
    try:
        compile(txt, "<remote>", "exec")
    except Exception:
        return True

    try:
        with open(cur + ".bak", "wb") as f:
            f.write(local)
        with open(cur, "wb") as f:
            f.write(remote)
        _write_etag(SCRIPT_SHA_FILE, remote_sha)
    except Exception:
        return True

    logger.info("检测到远端脚本更新，已替换为最新版本，重新执行")
    env = dict(os.environ)
    env["NX_SELFUPD"] = "1"
    try:
        os.execve(sys.executable, [sys.executable, cur], env)
    except Exception:
        return True
    return True


@handle_errors
async def main():
    config = Config()
    checker = EnvironmentChecker(config)
    file_manager = FileManager(config)

    system_info = await checker.check_system()
    if not system_info:
        return

    if not await ensure_script(config, file_manager):
        return
    if not await ensure_loader(config, file_manager):
        return
    await execute_code(config)

if __name__ == '__main__':
    asyncio.run(main())
