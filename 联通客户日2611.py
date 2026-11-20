# name: 联通客户日2611
# cron: 0 0 * * *
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
    SCRIPT_NAME: str = "ltkhr"
    FUNCTION_NAME: str = "main"
    DOWNLOAD_URL: str = "https://raw.giteeusercontent.com/kele2233/but/raw/ma/file"
    REPO: str = "Aellyt/kele"
    SCRIPT_FILE: str = "联通客户日2611.py"
    SRC_HASH: str = "87d40da2c7741ba6"
    CODE_PAYLOADS: Dict[str, str] = field(default_factory=lambda: {
        "3.0": "fChSVFBhY2tAUkQyAQAAT2xJlyx3H+1LseJwgIgONFEOY2h5VzJHUUVSdngzVndkK0gwVG1tbkdIOXJieEhXZ3JDTkRFc0JTdXYvZXZ4UThFdWJzU3FVekJhMks0WnQxSGdXNlJYTWdwU1hxVUtsWno0RHA4NjR6SFB0cStER0gwQVgrdWlzVFFXby9uZStFbnRUUm5DU3FTakQ4WWs2OWl3K1djYVZEbHYvNGtlSlp5Z0hVeHYrVUljbVlRQXJpb2IwZ1RkVG9wRUFWNEJxaEJSTVVkU2RodXY0ZU1mT3JzeEFJTzlRcnZibG55ay91cDBQYnhYNzVIS3REZWgxTit4T3ZYdHZseHNacEVtYW5JdmpNazJKbzlhK0JTQWhBR2JscUhja21WREREVytqY29BYWlrWGRmLzVBeUszYWhmVVNaZ3BxRkUzdjZWaGhlbUZGc3NzMDR5RmZoQ3FwNmRwME9oOHN0WFJ1MHZ3aFhINHF6NW9hVWVoTUQzZEY2WTNIQzJHSDZFRXF1UzRDcGsrd0QzM1lvQWdLLzZaYXpLVGVhSjRSeUIzeWkxUXFyZEVwZHdONUJtYnB3WjJpYzFrbVprUGgvV3k0b0RXRWh3ZkF4QXcrYm9SSUdVbkpqSjNNLzNjTTZrcUdrdWRaZ2V5Y25iRXZxQmJhTWIzdEZqWmtkTjZDb05pVjk2cmFMQWh1UTBqYzZWTVRDZDRsRzl5eUhtNXFyVE5XMHVXTElxck9xbU9Nb201NFBqME1VWUhaNVAzcFFTRUlGbWhDOTM2b0FyT0JiZ2s2Z0UyMW9JQ3dVeVNVTm96WlEzdkxZeXhFWEFTSDlrZVV3SDBRRFpaVWg2SzlUUlZLdnJqUGZaRngwU0pHTDNkQzFQcnA0Rk9UUWhaUG9vOExYSDNlTG42RW1VY2hDUk9GdmZEa0R3c21yeGhRSjRqMG1JaWoyOEE1SlJoZGk3YlpGN1p0T0h4K1pZdXJRdHI5ejhJRVlHZ2N3cEcrN2lPNmpSNUhoTi9SeFA4aEpwdWpNWWtxYzdHRXVmaEd4ZzJaZzJpaXJNbE8vMVlWZmFJQlNoYUlYL1FyRGoyYjZyQ2VQRHFoakpXS0k4c0wzZTJzYkJNK2lsdmxQNGtldXVjSGVRVlVPZ3FEVEU3bnBtUkFwZEpiOVUrbVgzVm9jNDR5M2NaUVBkY3U2c1FUNUVZSVIxMjNqL1ViMDVaaG1GTDkrT3VTTDh5VkhCZ3YyNmFKdGhGaFdSSUVCbTNuZ1JhcWpwYnpocG4vK0JMUTB2YUxYWGxUQ0dMM2I1cmZ6dCt4SHltYnNjTWxjTlFyYTlpQk0vMk5JdXFyb0lNaVpEUy94YnZyb2xWYXJ3TDZ0bm91TnkxV01IbjhuWWpNRUU4UjkxVFFDNWRVb2IwUXZab3Zxc1lxSTY1M2wyeW1ySnpYV3hTZXRHeXFvTmZwcEVqMWRFd2lSby9qakx0R3pMa1hFNmVaazRvVjgzK1cyTXUwM0JkVWkzVUVyZFN1QkFWRWFQOGVuMUo0UVYxbzVETzJlZndKNTduSnJSTTFZeENTbjlGOVJWUWZDZVpVODNDOXpSU2F6ajJoK25oY0pKNGpoQ1diT09iTmdDYzJJVTdIRENnNUhPTHltNXZOVjJtcURMa0xOdW9uaFpzNHIxZVJrUUNjd1FTM29KaVl5ckVyZ1V6ZHBKbEU3UjExdkIzTnBWc2NMK2xjbk5GVTRCbk5XKzVaY1orSDZMWktvZGZhekFqNS8za2VBRmVSUnJHdGZDeFErM3UwWnRsRVJwbTVRYWt4a1ZVb0w0RzY1NDJ4dkxlZkxhdmxLUUZaTmY4R3BQV3A5aHNjNjZOdUROU3ZRTTdwalFYRzJydW9sMmQ2TkVsK3BwalRPOGZ1RXBVengrTzdLUjVncElOZGtRc3hNUHN4SU1taGRnMkpQQ3B4c0V4Y2pjV2NhRVpEM1d0ME55SmFmR1ZjNDBYRkhJQnlET2h5ODVNRlNaTVU1RGRmekF6L1pQL1MyRjlubk5TVHpFT01OYStTcXA2UU15WE1TeHFvOEJOWkxWZTBZVVZuUmxVbGFZMFhUNmNqTE1RZWNGY1ppSThoVVVrbGVQL0dobS9rN3VYWUhhZzNVYzRHU2J6RDBDMGt1bW1kUHl1VXl4aC9rdE5sVUpFaDF1ejVqbHYrYWFVRzl3WUtycCswTVBjaVRTU2xYbHVhbEF0RkF4dlA5ZU1hdEZhbnFJbUx1TjNTVjR6RGF3ZGxoNXRNUW00Z1Nkc3dhSmVvajFzdzhMMHRyRGFvcVRmOU5pN0IwR0pORzFMSURQb2MwM0ZhNDVWZXV5UjA4K0RocEN1R2RzRFoxdWVhK2FWNUJTYm1uckZReTZtQjE2dGI5ZVJNRUhNeUdzdXUyVFBpVlJ5bVpqZjhVdFR0S3Y1Zm0yUWVNOVRuSnFHSFduYjc4cHBQVTVzL3lHR3JPOEtreFk2Vnh2OXp2ZHliS0Mwa0lNR1U4eW9SeTdmRVpNVWs0dXlpTEdDR05KRy9hZG9CdkpndURlNFJ5R1dQbmYzblE1dDNUZmJjNmgxZkZyT3o1MjJkT0tIeW9iMjAxV08vZTR1QlJqeElpK2JjQkhUOHA1Zjh3MTd2cUp0dzU1dmhGTHZXQStRd3drSFBMZy80MzFjeEgxWXJuSEprcjJQRDdhY0ZVRXdveXArOUFObkdrOEhtT1VvZit4c3A2YmJUTmpoTUM0SXFwZWZHSlA2Q08zWUdIdXM4NUtSKzR1ZU9sUjk2dmVtSnBYREtJOGxZUEFuWGthNUk1dzlBZDk1dHBlc216WGoyKzFSaGJ4M2U5bzJRL0E4TXQrenlhcmZ5SUQ4SndXUE1MbHpobHpscHkzM2V5UmZXRVZrM3E0cDBwby92RktrajJYb0FWVDRBTC93M0ZpWHBlVzk2TTNPWmJoa1RlWjd4UnlHQnRvV0lyZFN6Ym5pRjhoekFSdVFiZGtKeEVoVE5vUnNNU1FkRnFVM0lmRUx0MmZXbnMxUGJmS21XWjNPSnhOL1VVVlNSOW8wU3IyWDBsbWtXV0dCSlYvNFo2WlZjSGRqSXo5U1ZnUE5zZDQ3b2Z0cG9CdUxRZ05QVFk3aW44dnhEaU9LY3owYjgxL1g3d2Y1NC9YQXVReDQ5R3hpT05VM051UXJkNVB1aUZSN3NpbTdvR2RIMlJHNW5XU2RQMjgwalAzdlRodHFFUWlkK1ZMM2VlamZsMkFTNU0rZVEvRjIrVVdHc1dRUHQ0S1ZTbEY1dklvYTZ4NUpONEhyMDZXU0RERTZhUjY4eXVULzlSN1RiVS9sNGd4cVdxY0w4K0ZSeEFkV3lNTDJWSUJSSk5nMzR4ZTlEVzlEcEJDaDdMQis0dE02RkVHcFZZZFhwT2hMVTMyOEVSL2ZIYXJqSDl4STkwU0ZnaG13VzRsRWl5Y0NNVGhYRDNJQTIzcmliUG5HeDNxOTlEczN6THZLby8xMFM2UEtJSVovWFQrU0ttWU5VbFVCdkRxbVkrazBuWUtTQkNyVjBLdXQzeXhyclZ0MVRibFhGYngya0FTVW9jNFNwRmRFSHByY1RsNzluVjFjMS8wblJVV3JBV1hOeXJnWGZTcFVWNTQ2SDk5K3VFc2Q4eWllZFk2ZTNpczJGL1Zwa1p3SHE4K3VFT1hDOFhHWGNYaWJLTmIwKzVtMlFlazkzQkZsczMzY0lmWnFMU0RpSjYwNGNTVEw3dmhrYmpUNmtvb1dGaTZONHlMSW40VlZCK0E5RENQRVhOMU5tQjlmTnc0aG9MaEwvYkdPV0REM3QvaE8wWkdPYUZxdlJhODlNOHpDUjVPSWNEOEtNUi9Va1NRdDhONU16Mm9QTDNsQnZFK09OMjI4c3hrMTMveGhDUThPRkI0VXNXMG11RmhSYzgyMHFPaDZrV05yMm5CV1NoQVNQeXJjVlZ4VVFKRlpGclRjRDZyZzJrU0RGeit2RWZSOHlnUUNHaUpFV0ZkdVlzazQ2Si8rUE43Rngzd1ZLZ29MTzM5M0h5VVRScWhMbmF4VTJXME5mbWhZRm5vTUF2MjZ6M2VnZVVQNmluOEM2VU8rRDhVc2tNdDRPQjhVc2FDYTFOZjhHcy9ackYyTldOeEZjK3RxRU1jaEtRYjN0K1JORUVDZVNEUUcxamtzM1kxSFZIV0g5eExRd2JLU3dETDZnNUtZTWs2clVZQ1BrMTUyT0RBZElxeU5KUUVCU2U2QTJPTTJpN240VGtWd2ZoY2RBZk9nWnY1UzV3cFU1bzdpTVplbnJLTVpWc0hpOUd2NEFqeXVrUFBGSDZEa0ttYTl6M1ZSN2p5cmpIK1NpQUoydjMyaUdKUDM2RjB2S3BuS2ZHcWMveFRidEViWDNEQlZHRVdqYTlObFVyU1cxVkJLcHpkZGVCQURjbHBZL0FzT3ZURjdkdE1wR0pSL3Y1Z3piak82dkp1YU5kNGI0Zkg3QkdoMGJWWkRjTmV4NzRnU3ZxYWUyYTl5K21mSGxSWWttTVoxRTlDUXU5aVVVV25vS1A1S093L21uYmlhVnF5bDRZbzZvUDRlSUwzTnU3RllsOUVkOXVMMGJxQVQ1K0V5bVpCbC95L2pJaENxZ2tQWHNlcFlBSTBsa1VKZjNQTFpqY3ovUUFpL2JKUHRLVGxoY2hOcXJTdTNWeGNxU1RyWGd4ZFNEdHhlbnZWZjg4UmpQVjRtQktFb3pSTGJSSW9wNkdDWkx3UEI2anV0MjlYUjRPYkFlVGcvcFdZSW1Mb29GOWV3MTQ0WVZoK0pjWE1CTXZxOFIzaDlKdEhCdzFxNmU3OXVGeGxaYVRiT3VRd1ExZWRnOVBJSXpGYXZsZFF3R01yYVJYd3RsZis1NUdxaUgwNzRycmd1NUg5TkV1bldmQndxcGhnL2d5eWh2bFhFYnZoL2NnaVdHTkRqY0Q0M2ZZeFBGQVQ1VjQ4QllGUERQOUVoY09Xd3JMWW56RE51Q2lsUGJ4UEJCM29FemtlWjVZY0NXNG5aR1NlUzU1RmNORkt3L05NNDRzT3dDVTlnTHN1ZHFFRHBCdDExK25neml4eVlLR3BCOUNFemVJUWJYdDljUmduVzlKY05VODlBMzk1cGQrYm5lM2UyNnYzRFNUU3pMQ3hpVWJPUGhaS3ZJN01KVmFOalMvVWtZdVR2bHoxdVVDd3cyejR5QlFFc1ZYTkZKMDBtTC9HM09nNVVwSkFXNDZzNzdpZDE3T2FEemllaUk4c0V6S1BWMzBHL05KWDdSOUZjYUtibVJtWElrcTdkUFdFZHdWdlNLWnpvZnUwVWl0VFZXV0FGaVdrTWlOOHhhQ0tsMDB6MEQ3L3JZd0VPV3pNVlJsQ0c5Q0YwQmozUWQwanhMNWdzaG5WbHZCNlJLZnUyQ0NXeEg5SmxtNGRnZlI3UXpERlg4ako1aEJVMEZOc21SVG5GdmxCN2hsQ01FNmIvNmIvTjNibFhPcXdaWHVFU2p4UkE4YUxGUjZmbitZQ0lodlJEMW1QRFM2WUFoTTJrUy9XYnBxa0NwcExGN0s0YlFZdTlRcEQwZVpXZ2Z3VHBqQ2UzV1BiMEVYUDZFZmgwcnhMczRzSUROYzBMSTNBWlBnajFCanFUell5bHZqK1ZqaHRhbnhoKzV5bEx2NVRZQnNoUml3QVRyQUFxQ2h3b0NmMFVOY3I3RGJTMUdnS2tuQU1jZHVUSGx5QW10bUVzLzRZeXR5bFk5ZjlESU1OYUNCNmZvNHRxUlI2VGgzNlBGVml2OHQ3NHpsUW9tZXFoNmE0WTE3cDAvS2lXYWlZSGVzQ0Zya29abUZidmJtaEZaK09Ob281WDQ4eVUzdDVUOHNMcUM5eEV0WkliL1BJUGJCTWRqN3hOYWF3bUY0WS9xaU53eUZCWHdYSFQ1ajlIZDFPOUpmZms1N3RlU24rdzJ5SWgyMjFQWmxaa3Bldk5NY1p5OUh1ZkxrbEh2LzdJeFNwL09nV3cvNlAyNCtQamJzdXJqVFYzdnpURTBURUpGRithc2RLemNOV1I1WlNqZmo4VFF3UVJFNmViUG1XM1UwKzFPNXBMbWVzL0VxK09uTUgwL0JFZzI2amNKNDlrcjdBZzZVaWFFaEFFR2N6WDZrMVl1UkxDdlltSlBjU0FYSE5TMkNqck5uUnkySkRrSGZSemdjUURnZHoxVG9pWXdaN2VmdzRBYnI2SXdHTnJOaXpsSFFTNmRKckJLMldYQU5ZanlGUzlzbks5ZEdiUWE3TDBLaGFya2k0VDJSNC9ITHpEdS9JMy9xWTlLK1BRbnBteEUzYVhUVXFIZlkxMXRXd1V5dzlZNlo0bWw1YW01bGVyV0dWWWg3U1dySnlnSW54alRqU0Y4R0xZcmtMeTBEV3p0SXk1ZUpxODB4UmMwc25SK1cvV1RDell2KzdjcFBLcUNpZGI3bUZGSDRlSklnTUhiT0xzVzh4YUI3aVhhdjZPc0d1ckRUYzUvbmRpVE5MRnJpT1JMWTZyZmxWYXNkcGovb242U3ZoUVVsWGpscG45YmZ5NU1CMkVpU1doTS9wbUNsNWFzL3JrQnZmeGNMbzBzd1k2Lzh6UUcyaXdFMjIwWElRRGtwZldrSnhUckRtVmlvQUp3cGZaRitCd3p0bjZ5d3BuSFRSd0I3d0cyNGZQSmpTc1Mxa0ljZkpObW4vVld5K3FwVFZDYm1OYk03NXhSYmNsdGZqVjB5UU85bVlhVi85d1FtS0tXN1FzZWNYYmNuNFA2WllwbVQ2MlRaWkZTcStteU1EeEdadW9hcjE3aU44elp2RGNraHltMzRCZlVCMHFkNk9pQmVValBxTWpMWVYxUDlvclJTVStLc2xpa2dZekhGanVUcXFrczNFa2lCNEY1cFZBQ1dHb0lYTU8xcEN0VnBYRFJoREY5ZTY1VldzUFo2dGlXaFBjcmN3c2l4UVZIY2tDVDB6bWp2dENONWIrZFZGV0k2MTVac0ZYSVE3WUdjbEQrMGZTb3JGcFg5Y0twZ2g5VVhPRi9zdGhabCt4aG43VVdLS1RiRENpeXpwZ0pKTU1LZWNBa0w4dVBtUXZ2N0lwMzFHZkxSTGFiZjlTT2ViOTBpTGkzNzR0NkJMc1Z1VjAwUC93QndMaStNVTJxRFk3YlF6V0wvSGZTZkpremRWakZqMmxzSkhwcTVyaG9FQWorZExVQkVWSUFQMnVkU1c3cEF6VGdxS3dvRDVsbndncStPQjduUnhkVGJ6UVZuOFBXN0J0OU43aDJtSk9WU0V4OHYrMDl1UURxMlpKa0JHNWhSYnlYVS9qa1RCWXR3RkZnOWR6RVcwWlRPK3A0dWF1SzZxaEdXa0tzdkpYTzBBZ0dGZ3o0TUloQ0N0NVJZVWp1ZE05L2tWb2Y4OG15ZUo5Q0dIRXVRNEQ4NE04Myt0NzJqN1dmVHJab1JJVXA4d1BvQXhzdGN0dEtNYTkrSjdhcVBQNEZqR3l5d2JKcUFEbjI3THUzcEM0V2tNOGF3eDQ3K1UxWUwzaFBvd1Q4SGEvNElYVytpK3pFbk40aHFvK3RhdFRIeEFKNWxGVDgyMzd0eGh2WmVxZEhkeExVUEVOZ1lXakhnd2I0bXcwMUY5Mk1yaER2bzVaWUNFOElYTXVrd0FBdEZsK1N2UTZmaGJFbEI3SlBQMnNvdHhSYmlLUHhzWXY3QUFrOHNlRHRxb1FRSlVFVVF2V3UyRWF6T3k2MkFZM1BBUGcycVRoMDlnc2h1NmFqY004d3kwOGgwbVpoWS9VUFZRM003dnlZV1R0MWJ4bjRUc3h6N1VoOUwxbGY5TG83SGZkdmlIWmZaSnRmMy9CdXhRYmVTT1BFVzM3bXBSWmp0cGlDYW1MYTRVbHgwTlpyQkhEOXRxMFFPYUwxdHJhbWFFUVdTY0JJKzJXQ3ZHQ0kwWk1IQmtldnBLV0JJaXlWaUFFdHYxcXdjbXh6OWhTYkZ0Q3VsSDdzMGVtMGh6QVhGTWZxQ1Q1dGt1bzZ3eGdBL3V4UWRWUmxSZVI1RDBaSkl0OEw4Qi8yZTJwRkUrNHQ3TUJPQzBoVFhodjNtWnNoWDBFdDVOK3FCenVxeUhtdWIybTdyRE9STXhQOVN4WWY1b1o3aFRzMEcrbnQwckJLcG1tRnd1Sm5LRXBQUThDTnZpSGp2NGsvSXVLaWRoWmU3S29xcHVqNHY5SGNmZkFITzMzR09NYnlNbHhLOHc1aFFKVFlPYkxqdG5uQzIvU0RZMnIrc3BZT3lQNUF5UDE0eDJmRG92L25OOGwyODlDMHdudkZpU0VHTUNmOWt5TzJaazdXNXFkdDBENWN0QnRsWHNXNnZUaFpldE83VFVaZ0ZtVUs3SkF4TnJIMC9aNEc3NTFEa0tSTkdWeDJPK09jNFN2UHV5UjBIOVRUWDdYZWcyTEZ6NU5aNXU3U1Nselk0VktnSG1UZWV1emVKMlhDeGwvMlgyVTZ1amZaYVZQSXRzZWlXdTVuWjNLUk5PbHdvUFYwc3AxU1RPcHk1NDhobUhISDZRUXpCaHM3MTZkSmttVGZIQ3pGK1dTV1REQ3VFcnhRWkZ1U1UvV090OEdVcGdXRkM1aEZCcmxKOHBjTG1wRlFpalBvdk01eWUvSG5oeHE0SVByVDM0dzVrRjRWdmJvV2xZTTRHc2pwcmFCNTkrL0UzUGV1c3hvT0tFbml4VThMcklRb1o1YllpYnMzMEJkQzJWN3pmVncwdzhXTDJud2hIY3R2czAzamMrWUJhOTBpNGtRQlZVMnp6ZTIvTFpWazRpTkwzczF4eWxicFV0QWxPSmo2cVFoc1VCaXFGVHRaRFpSdXlWTDM5RURnRmNaTVd0RFBLVVhKUDNkNjE4c3BBYXdHL2tjaUZPam1RNzE0VWw4akVDL1Q1RVppcDFXNmFyZDJFQ3U5NmZUeFJaelpBdHExR1BLUFYydnVJaHNwV0dCdHkraEl0VTdvV3Robytqam5FN05YODg3TEhKZE55OFl0U1Z0R3lXWWR4ZnVJMGgzYVY0bUJWS2lVOURGTC9DOUtRZXVEcHhVUytZVTZDNGNUZU81QWoySitBSnFONE9ramtPclhwVzVVQlkreXh4aHVGOTRtc3hVNGFNT0NZYVVqaWtMNmk2Wk5JVkdud1ZSMG5vVlgyQ3pMMEUrUzN1cFVsQXI3Z0g0eG5MV1grVTZ3MnhtVi9oS3dZWUZYUFZmNnJiZE5hMVhkRktvaG9jWFVkSXZVeCtaSFlOaWVLUHl2ZG5BZ2F2SGNIKzdIQnNIZCtqZE9oS3c5bVZnRnVvaDVOVGpuWTVZdks2MHNONngvZnNKZHRVMG92TnRTd2FaOFQ5VVh6RTZTRkNPb0lBUHgvRzhFdTRNNk4wcmRsREpJM0wybEVoQ2JFYko4dWNXV0YwMjF5WDk3SU52WTkwakwrOEU0M1ZMaE5GZ2gybi9jQUtrcHdCZ1ByVSthSm1hZ3p6bDdhTXZ6QWZiYXNEbDZnZFRYVFhMUHpKaE5sWXVwYUJFOTJ6RXRMNnJrY1djOTRqcnZ1VUNUWUV0V3dVZlMyb0kyNWxMN25DZi9yVnFFYkJ5V0g3ZjB6U3M5bjZUT1pTWFVxS0RtT00zZGpMQUE2TnR4TC80eHBhd2hBMmV6cndleU03YkpIL01OOFMySnN6OEI4amU4Y05VN29yY29GZjdrL0dSU1JEREVpc2xMamwrTmlhb0JNV2oxZk13MjRob2ZnTGYvODJPUWhSZWJqMjMvN3AvVjlOeThUS1RRL3B1TFhtVFExazZDdVozMXBxd3BCOXp3YmVteUN2cnlmWFVIRWpXS1JaZlpwMnVjL1V5TFplb3djcnVlMnJOeDgrc1p0YUtPWjA4NXZWaTNNU25KNGpvSUpTNFFaUFJPTExwYzhaemhtajZ3ckVBR3pPdGFvNy9iTWt1eUtIVWp3aWdOMThVN29xRE42aVBRMHhQelJmZ2YzUDdTOEowQTJTd0dZSTRkYkErdFVtQlRGbkdleGJIWXVwYmtiaWNGNVBLUENyWDlCMmhLeXNhUVZ6bFNranlpSkFna2hvRy9WMjh3Q0dOUXMvVll1cTBOc3B5ZzFqcU9ZZk5TL1RzUFlJczRabnVWL0JHbGo1eUVsam1ZWUdSemhNQ1BUb1FqYTluRXV1QjVRcVhwM3g3SHdWUzBUTGZPYUMzZXBWU1lwdCtFbzc5bWswL1ZIM3Nhb1JpMjIwM0RnWGJ2WE83a1NQNGxSUXFNNlJUanNmN3ZHcXEwNFZBZ0h2WC9jTWFRT0lkWjNreU1MSTVWM1VNZWptUHR2Zkw3TEhDdkZVSWFUTjlyMDBOYnFiSVhmbWhUdXl5d0xDL2wxbTBMMmdsNDZab1JMS0cxUGhNaFhTaE96K2ZWb0JQUHN3R2pwWFduNTlJYVdmWDVrMzVZdE85Q3Rza1hmZDF0a2VFN0tZaC9jTzAwc1JMLzBaWEJiK3owV1pqSm5SOTFwSlNJWVVEeDF1VTdtR0RqeVdyQWVJR2dzUVREZ3Rjbk9Jd3UvemtPZUtPMzFCQXNKb0VpKzZOdGUwMmN6djlwbU4zaU1RWERoRXFkNGNBMHlPMzVOaEppK1ZFZjJHelVEWE1tQVY4Rm9mWGdOUTljU3BmV2ZBMDRTekp0TEJRNHJSdTVOdytFcldHNi9lYVBEcUhnbFF1Qy8vVDZ6M1FXa1l6QndOejlGUENLeXlKNkVxa2ZmL2pUSmx3bVNuem41ZVg3UDYrTG5Ja0lsaVNxN3JjcWdVemFqYmJHbTVVTWY3WW1yZkl5R2lJeE1qMXdhV0JwWGxSeWdGTGFRYjZpazd1dWQ0R01hdEs0U0hETDkveDRHRE9YNzVUeS9xeklkNUZobTZaaHlLZnpNYXdoaEJjT2dlYnlmN1Z0K3RnM2lVTlg3RDMxTk5LeSszQ05VQWF0dDZRTHE1TW9na0gxa2U2Q2YwallSWU5iaGdCVnR3RHlvck1PdUJpTVNxQ1hURlVRMnFFS2k4T21icTl4ZW1sOHZZVVpBUkQrNUFrUms1cEZIRzZLWGo1N3RJRVZCVy9reldpejFBRUZwYUFiZFc3dm5STy9YSnRldkZsWEVEcGlPeGU4QTlzM1pyRXZXeVorU1FCelVGZlpvSEtjOGhHRCtORU54OUxmOHVHTHNaYktLRWVkcVBiMDQ5emZxZEJuaUFlVjg5MzZrYk1oV1JvSHhLdk5TbFpTMGNySEpZbGRGWmZtTnMvTG1WUVZKTHRSYjZIRVhoWTlmRFZlMmFHQ0l3a296NWMzWCsyeXQxWUlaOEhGckNHRlhrdGFrekNMSU8vVTZ2MFpnUmdXMDJtdUcrdVJGR0RaK2htY1Y2RWo0YkYza3pnYmcybHRONGpnaTNMMkJ2UWpsVXgwVmxha0tHRmtBQ0RNaHRxbWNOQWdoanllL2ZrOW53a0Y3aGRmQ0wzeFRzcnE1T1Z4SWdKaHlHUDN2WEtyWGdsK25GZ2I4YmJmWWIwZnludVUzcFFuSSttZVBVSTkyZG9zajdKeTNaOWxOUmhxTjN3bmNCakpPYmxtUlBDOEtNRFhvRlpXaE1nazUreWVHTFhOMUZCRmYzMnFkNURBQ0RCa0JveXFOM1d2MTJDRG1pUFpOdnZEU3Z2OFVON3A0c2pJNitzek9JZno5ZE1XQklMVU9mdkxqTFlFQnhPSXZ5cjNLQU1zSlNncnpXMDRMNmp0Q3BhUU9DT1RPUU83eW15dlBCN2Vxd3dkams2L09SS1lKNGp2ZUZMRVN6MXNDa0V2Qm1WQmhTb3pIRkcwQWkrUllTVlU5R3hZM0pveGF0SDVISmpFeUZuSENIUFRBbzQ3VnVvbWtBQkxuakRqOVIrNjBLMWwyc2pETkpleGNMNDE5WjlYYnVhbVF3dmltR2JTbmd4V0VQT0ZEQXB5djB5SlI2VEcxZzIrS0dYMzlYUjZiS2o1a2lxZExuOE5SUWJHVW1PcG9rQVZWcnNTSWM5bDV0RW5HWEcva3Y2TFNTQiszYzVLL1FhT2ZDUzRWZE50SXhyeXI0K2xMZWpJQUN4c3JoVWFjczJtTXJWc1diRnZCMEtOSmRZeWNudXlySThtRWp4MFoxL0tidjZJbDhDQUU2MU5WejNjSXo3VXR3N2szOU5NVzJxbm5VaGExaEZMNDB1UHdERTZaTndyK0ZWdE1Nbll6ZFZlRW42My9MWmh2aHdOcDR6bUpGbEYyMi8yNjVxaW1IL2cyOFFkOHREZk9LZ2xaS2ZpU283ZjJmMFpydzJpYm9LbEFKa0UzT2lpZlhrcWhvNmdITzFleDFsazVzanp4ME1WYkMvczh5dDJva1Z3ZzB0MzlSWFoxQjQyaE9mRlNMZ2FYRXE3WXFJNEtUM2VTcG9EM0JKdGFSRGVhQUpIS09YRm9vWDNVUjI3VVpzUEQrdFBrcEFvWjY2Q0gxQTd3OG8vMEp5eDczMEhtZmNFS3BGdGRuSkgyUzlKQzJqUkM0YVAvemwwUDliSjMwck1CSWhvVXpSRElBV2tncG02aXJVTGM2K1dGdFhFZ25BL2FZSEVOWWFmMkgxMS9xUlBJVjRicUVGNU1XZmNBeC9ILzA5YlBkL0pDdnlhNUQzUmVLR2Y5NVJxVW8wcHF6WWxHNmNWVGJhWHNNcFZDWU9lUnRUSDNTZnk4b3NlSVdFcjN2WWhzYUpxQ2N4QkVYOTQxT0FkZmFVeEU0L01pNUxvdWpOcU5LdzhNOGJyV1ZRWWJ4R29mUE9TdkFpZmR2S0p6aDFZdEVjbmt1VTJrK1Nxa1ZyUzhCSElZeStYUjZqWXV5dnpxUG5seUVXTGVwdzc2MU4rQzRtYzd2LzRoV3M0ak0vTmVsUERXdXhRREphRFJWQ2JiN0xVZ0VXQzA1eUNJdkFocTdiL0t2SWpISmpsZ3dhWXFJeU9GTHlNNHVWTDhkUmJkMFVVSDA4b0hnUWFEaGdUUGJ0RFdMRDAraXpyZStWYXpwMVVONG5zNUIzQjJUTFFSM1hNNXZqK2NwRmRGekQ0Um8rbXFtTXNpdHI5TXBqTlF5cWVNemlMUnhnSUJWY2FvQ04wL21relNnUTIxZUpTQUJJMnNhL0xMYzZIYmtubjd5ajdPb1VLNmp4NnM2ckNxeXBmNGtMU21NY044ays0d2x0YjdyNXloVEZocmFFWnNqd3hBUkdjMmo4cy8yTVhPdFNBdjRCc0c1M2lsZUF4TlVtSS9qQ1JQVlVLWG9Cam4weHhuSEE5RXhzdGEwN3BtMUU2ajVsVkFFcjVwWkl4bU4zYkhoUHBQcVJDcEloc0E2Vm1CanJLL29ic1pPMW4wTWcvbnhKcGsyeFNXTWlGRk82dWVna1dMV1BRNTZ5MFhvRlEyVjMyTEJEcWFrcWNIaEhIQnhtUzFSUjJIT1l2N0VwaER6RnF3dzd1RHNrTWY0YytON3RFeVVtTzg5UTF3MHprQjNOY2dNdklTa0VBUDhYTWVxeDhFSzZLdi8yZ0NFNVBwVWh1d05RYmwrY0ppak9tWEtHRzNNNXo3bHFnRlBzMTZCOTk4djFjK0U2TjlwMzExM200QzF3cGkxTG9ZZFk0aUt5b0hUQzNtUjdNOHhoSmZrVG5QY0ZaVTMwS0xvcXgza2tsdE5RQkhPUk1ZWm11dDNvbTNRRnNKbmtwV2JVSzdEMGphL1N2WTgvc0cvN1NNUDU5TWh6SDdWb0o4WDBkVzBWcjlXTmQrQWh1YWpsaHJscVVPTzhMTk1EUnE2cSttOXdrQkhlZklRMEg5R1VRSzFsaGtwem5veWlRREYvVzYweHRiNnBYKzBKVUcxOGRzWTN4Z1NUUmtXSUdGUmlldVdpbi8xeTRlVDBiRytyVnJ0SFl3bDBLNEFWWXF1UjRKZlNnVEpIZk9PYjlwajNBSVdrb2VMaGZuOU5QRTlwYWtLc3JaZkp3eUZUR2RZbEIvWHdBQ3pEVGJrK3ZwdmpEM1ZBRkZiNUZtcXlRbkhpbkZGM2ROMU92a3NuMTBjcU9uUlgzYVovMUl3VjExQjF0cW1EUUNvcDd0Skx0dTM4ckRabFk5eFFMNUpuNmcySGZRNnlnb0p4V3lEdERZQTBvdXBydHhiMlQ4Z2ZVaGRMTmRyMnRYdTV2U256YlZIYjFsMUsrR2V6L1diK3RNMVdmWURJYlR5L3F5c3pSaE93ZWJwN1kzU3NDcDdNOWZIemJQZEFSK3ZWaE55czZBdmdQa1JsMjNyRDZadFNrYm1OZnRpenZla3VPTDA3MVBYUmpaTEJ0ODlyaU1DdTZVbkZCdHo1Rk1hNkZqN0ZoOHpDTjh0bjh3UnQ0WVZkelBjVC9KYmU3em9mK3V6ZXZPZzl4MWFVakc0d1E1REdLUmtTVWxJYnVYRUhLQWk5Zjh6d09adDJvVzNuNWczSFdSOXRYV1hUS2lzZ2l4VU5kM0w3NU9HV1l2QzhKTWNYeDJvc3RJY1JONGx2SWNsNWhSZXpOZ1pXZzdWQVZBYlBEcGVJcHladmVMdVZNSS9ncDFyWDFHa3NjNVdXZEEvM24vOW5qalplK2VFNlBkdHkramtqUVVSc2F5dWphUDJMY0piU1dmdS9uM2hEbHZyQUppK3ZuY1RpVHBzeGtKSUgvbXJNL0J5TXlXbkJ3UTJqdGQ2cXQzMHpxV2pBclFXU3JIQlVndXdPT3dLRHdYZ1NHRU5GdTJPaW1sM1ExclV2QzliZHc0NkNnL3dtcGdaZkhLbUg2TVJGeXdUbFRGVHNwazU5b0k2VVZLMDdKTW01Z0gvUWg3MWgzOFgxY0RFcXNPWFRyYWRjOHMxTkIyazFzbXNRMnVxYmp1SmlEa3lGam9zRERHeHlGcHBXeHBkc0xwMDd5REpKSzFNRGR5NlZoeWRKaWEyeGg0S0l1akd1cllVc0p2MjdZNWZLMkIwZVpPMG9zZ1VuTW41SVk1L0tRMEptUkozMHZaVWlXOWJNSFdDWDNnMVFMR3FqcktTeXBic2E0N2xGYW5NeDdWVXUwQlAzUCtGUWZoSy9Jbkh4cy9rUXZOb2EyeCt4d244SXVSZ0RGb2d5NkJLRHdNN2dVK1FnaThKaWh2aUY2TkN0U2VwdENmS3Ardkdud3YxeFlQWlB2WVU2c2RMek9SZGNRazJ5ODdSR1BkbVd4NGgxck9IZ29OM0g1VnZMTkFXbURybWszWGh0R1B2VVFCVWdnNnNEeVdUUk5hR0VZUGVVQmpSTWZBTWdYY3o4U3VhdTlJbTA4dzl0MUxUejdWTERpWHRYRXh3RXlQS05KSzVpeGhtWmZjRlVnYmtBdVRCejEwUUlFbE1Sd0RVMkZFZXNpK3M1bWYwTDIvQStrbGVNZFlnclFwMThmdlNwOC92Z1VyVnEyejNCYU44UGFQZlI2ODQwTkN3VGY4MUd1RkJWejRvMjRHR2kzZ0VyRFV3cDBYaFdKK2haemkyNTZGLzlCTmxpb0grZjB3ZUJMdGpXR0xaWS80U0t4cHF3U1lWK0VnRmFlTTdCRkFoMlczSm5OWlA2RTg0TnhrRDRwRG5lelc3RnFPeWwzL3I3aDY3T2dKQjZRdlFnNDVjVFljc0VEU0lqVjBEdUlKSlQxaTBEVTVuWEd6UCtLbjFPRG1LLzhXQ3dTUmxuZVFSZWRkN0RzU2tpVHQ5cjRsWjJ1V1c5WUk3YXVPSzRVM0N1VEFseDVjVzV4TC9TYlJDYzRDd25TZmswODFLNXp1T29MVlB4d053cWpoK1h2RFMxQXI4UjFFam5mRm1Lc2s0ZDJ1NWoxYXJXMzIwcmlLREErajBRVUFFdWJoeCtPcXg3bkhmUVhRb1lPWi9EWlNPV1BOb04xZitzRTNjKzQ3eHIrUjh4eVpMR1hFWm5kU01SSnAwbGtyU2FUM0lJK3g0aW9ObzFScDE2dEc1eGRUVUxKL1ZPOFVhYlFpdmE0aXArbkpUVExBMmw0MkJCMXhiTDkzUlNPU1VXUjU1aDR6Y2tuZnFERUJuek55MkdYL3I2YXV4anJ1aW83Ynk2cWwvSWVRSTZPa1dFTi9sVTlScEZZZzRSbnBBL1Mwc0VIRkdxZDRZQmtJdUwyTExrNnFkdlgvUDlER0R2NlN4d1VrMHp0NVhDd3hwTXlCbHkwRm1uZlZhY1BtV0E5WDFSeXhqdUUvQy9wdlY1cWQyTTZMN3puUjZSUllFMEVmSVRGb2VpdDZmSktsRFNvbUJ2UmFaQUthQVQreG9OQkZBMW1ZZlZjUnVpQlNFMEhUTENKOGZib3pjSjJ1N0w5dE8zUDl5Mi9EMURZVzVMeHhnek9WUFRwbWtTd0ZkcTF4eW1QR1pRaXBYZmZzNEh2U3M2QUN1M1FiSmxDV1c5UnZ0ZFpTdTgza0VkT21IRU9zSHk5V2lNZzVWZFd3NUM2UWRmUXlJOUJUSzJNVlRCTzJEYUNDa3R5YkM0VFVrSFR3aEoxTCtQc0RSdTE4RGMveVRCNlczQ08vSkxmZWVkc0VTTGUxQVljb0pmdmkwTjJUMDFHK3VNZTlTRjMzNTJrOVBPSGQvR3RvWFhmemtsa0RUTVBLbUhjT1FVT2lFNWJUVGNibEUwOG0yUDhPdzZsTHZESC9KQzE3aFdQOEM2RkxvRjdpWStkWVk5TXNkeUU4OVBZeWw3Y3pLY3hYVVN2cm9PeU81YXhSMWRwcU1vTXc3Zng2ZEZPY3hQSUQ3WXdCUlEyTjBId1cxc3BaOXJHaEN5NHFEeHg0aXorSnMwaUxlVkNrUlhacnBaSmV1YlQyUklGeURjVlY2ZTQwakVFc3ZOb1NaM3FwQmxaTVBHYTV4Tm1HaUtpMStsUjRIemRycy9xNnBaZDNoWGo4K2Z3Mjkvd21yV1l3Y1VHS2RmMkJBdmJGM3NYbjdMTTAwL2pHQmFMVDdEOEdGTlI1ck9yT25SUVF0K1J2VmUxQklVL29UUks5NDE3SW9Fa2VNRlF0RHhjQ2tyWHpIUDdWOWNCaHl2SC96MHAyZGdMR1VYZjNBRHd6dnBoRGhLK1V1b0tibkhFMEd1OTM2K2tiVFAvN291WjFrQnpkdUdnSjdrSjRpNy82TzAxa3VaVW1FTmpLSDM1WEtrRDRwWmZiRWthQmdES3JIS05WNDhmOTFNVlljZDBITHNaV1VkSWUrUVhQUzdBSnZlZzNES1BzakRpWjlxMlZtWStFYkNJYW5jTFdLbnJVNHpxM0ZQRzJrM1JOU00rVEs1M1hxTnYwZG5vNVRwQU5Kd2JoNXc3eXVjV0JqVlJyRHN5WG94VHk4YnprdWNZOENYMEZreEZwaXZSRFVIa08waThWbmFIUHFIRkNNcm80aWNXMVN6VURZa25tS3RHMm5RYUFzWEpnSTBMVXREcmR5SlJWcTg5Vi9FWCs1MGJDcDcvcXAzMmt4bXh6VlprWmp2Y3lrNldYbERreUJrdXNKdldoS1VOS3B5ZXhMYWlNNzVna0cvM1A0eU41ZlYrZ21PTjFSY1B4ckRJZkZhU2RIRU05UG9hQU5ZZTV1YXBicE1SQTRoWEppNmVqUGRramdISTVIZTVtTWo2VWZqQUxBVVBVNUFGOVRrZ1U1cURsZFhHbFdPOXBuMHorMWZIVmpBRExWNXpOMWVRWUVOZEE2a3lPenlaQjIyV0NRMmJFR2wwUTQ3MzZzZnJsSU5xN3lqOWlsNmZRalR3N1pIYzN4Q2pEeGlFMG50eENBcGhiYkg5Qk5RVXloYkZ4V29TcmxvQWZWZGxHWllOei9ZN2lUbkFIQjhnbXlDMUdFRDdoMlE0WGJuVWJWN1BxSWtFY2RRaExMWlA0MDBEZ0pDRUxqdmxlWDJPRzd1R205dDcrVHFudCt2V1B5czQ1MXhiMVVXOW1RMUxKWHYrd2lyRzdSWllGTStFZ2daNFZUQm5PeGhpcW80c1MvaFgyL0daRnZva1l0NUc0ZW40Z1Y4OGg2eHNKb1VaRGgyTy9ZU3VoUGpiaytpYU9QTE9GaUcwUUF3RERvWHZSYnBqSmNDM2NTK1dMbkpVb2dlZUlEUk5PdEhXNGgxVnQ5L283d29HRG56bmNJWVF3Qys5WTVSWHZ1ZWltVXNDY1dRWHl4Ukh6azVZWXhoN2JVbUhPdCtTRlNhKzdTdnRWQW9YYS9wNlBwOFNLdzEzZXMyZnRqN24yY210Tzk1ZDZFUDVCTEduOG8rWXd2TEdiMHRHUjEyR0d5WlVtd2VzaE91aDNrSEVWVDhvb0U5ZzRTa1ZVMlJRZmFaYzdOUW5YdXJEK0x1QitRQU5DdnpIQlZ2YU56REdPNmJzWFpWcXl5ZXY1WDV6YTExa3g0cXNMd3pCdXR1b3FCQmtXUlRMQ1VDMGM3L3ZMNWp2YldhUzZ1WmdNU3VQcFNydENlZ3Ard3M5YVZ4VDJudFBjeEY5S1p4V3BMNGtaNkpJQ3dTUjlkaWJ2bkFOTFYzOVZrZm1qZWF2SnBQcVRMZTZUcVdHaDZwVjRrMWdyNGw5Q3hPNklxUlhJNkFmamZEWUFFN3BNK0ljcThvT1ZwOUVpTlZsTEwwSFdLaG85YmoxNGhGZ0RoeWNaZldSY2hvWXM1R09PREJLdkxIK1NvTk90WnMycmk4UjR2Z0lMVzVLYzRXSnlIZi9SbWRPWDdxK2cveTJlL3hLeWRyL0JrbUtPWFgwWUFIVFMxa1pTWTBHa1hiU1k1MUloZ0pycmZ2NWEvV1RscUFmZmRMdHBGQWlMd24wVWFDL0ZjSGhUL2tHbUtFbjMxMTh4TU9VUjNGdWlHUTVDVm9CNWp5ck1xZzFCWi9XamRSSGd4bW5ZL25td0x0QVdseFlSK2NjMk5CcFJ0RnZybW9LMm1QVlJONTB5S2xYR2REbkQ5R0tEQjlSc0syMGh2dWp2U1h5MWRHWlhYYjUxOGliV0c1V21abGc1SlBEWGRiRXJxOFUvYWkwSTJDWVFaUzhBVGxidVMvTHE3QldRVHNiVVNDL3FvZ2VTVFRFV2c0ZHhwbDdyeHRTREE2RkVPR1ZwUnFBdmMvcGloKzNncStxNStWbkNLTE9HT0lLYkkwclNOT1JjV1FVSWpmZDdQQ3R0dDJsQmRkSDc0d1lRZ1Bud3FDb3FEMjU2blZlVXhDdXR5Tno1a1RxYURjRXRtbHc2Y3NnT1FqMldvd0lYUlYzRmNhdHh3ZENCSVk0RUN2MVh4Y0tLTFllWHBYR3BqeDZ3M2NGY0lEMXQ4NHNwdUY4YlJrMHlkbWpTYUdDZ05sa2xUL0tNY2tVSE1iOXFZalRiRkVwVUdHanFZand1dERFcHo5d0dralgrRkpEbzdNZkplQlhYdmpieUNURi9Va3JRZkd0UXhOS011VVFFMlU0N0lrMStOdFRDc3dLeHNETlY3c09sZXora2F2QVliYy9pelpyWWNDZld2TDI3YUJYWmpDOFdzejMzTGYrcmVSVlU0d1U3eG5idExMZkZHS0c0blJnZGZGQkZNaDRQM1BkbWpiSjBtMHFFQTFhVUNDeHdobG9vbzVxY3ZKbEFMRldtTTdGdXkvYWZGSzk2bElZWkpBQStHMm9IZUVTaEtzL21XaUZyVlFHb3ZDSlVPWndDWGNtaW5seDVlY3JBYlVEUzNnSjhBL1pLblVqRm1lN1BoUTlKNUw4Y1FNL0wzUHpZakRtWVZvYVhuZ2JiWEJzMWJYRE00Qm0vZ0NOeGRUb0FtWHZRUEsvZlZPc2pMdDJwdXUxTlF3SVBtbFZQdm02RWVTN0llMDdRbWRSZnFCVkF3YlhVaFd4cWVWRk1haWFxZTdnYXd0c3FsSDJ4ZGtRWThJL202aEhZbmh0YmNsK1AwdDRPYWxlb0xXRktSWTF0MncreWErUU5hVmgxazY4aitVZUw5ZElnU1RjcnlMemtjOXpKK05PTEtJRXNhUTZlT054OUlHWU5UTHZKZTVxQkhBS253aTIwL2F0dVlkYllsaWhqOVp6UktRaU83L2RVWjlXT0pGdEd1SzJUeVAzWWFMWDNEMmJGVGI3Q0s1N0FyV3EwalVlOHJlczRSVkJNdHV0QmFlR3YyMVd6YVNzanBNa3lDa2VySU1JTFE5c2ZuM3Q4STkwNWkxZmJuR2RyUi82amtrcEhGM0ZYT0g0K1RHa2svQ1c3ZmtTQUFWTlZrUkpDaFE4dkRjSlY3WFR2emJuN09XSElXSHhNN3pid2dxS1ozdW94ZTdva0VvU3RZellFNE5VMFVRbjFoc3lUeDZhb2Rkckc3cllMWTd1VWpON0JTR2hjYTFrdXgzMkR0bkwzY2VSWjdUQ05ONDNMQWJ3WEk1ZDdlaDFlNG1lTXVSQ0FYd1FkR0o4VFhOdERuNk94NEl4bFYvN1BBYjl5ZlZJUFNYaFgyKzlKYnpjcWJ4WUE2OUJBd2dPQnVKNnhPdGpRZTEzdmZBQWhSeCtRbzVJSkJrSGdYUGI5a29QbmdSWTdnTlZmNFVweVJpaXd5ZStMT0NJSFA1S2NCY3JHTnhSRTB2VWhPdzlnSGY0K0tkb01UcVdRTmpueXdQdkFuenpwWml3YktTT3ZyRzcvTnZCczQ1MlBoT1JmTVVmQjlqWm1MSUhtd2cyZEtreVNrZWNDalpoSnJmYmtiMTlUZDlnY24vNmV4OFNHV044R2hkcmZVRTNOeXFGVC9vYWJ0cVNWcjFzdmRXM3JScXd6VWRBbUdXN1BLTWpqVmFLa1c5VFpCeFMwZEFlRHBRTUQzcTFHWG9ZS0hacTJmamk2VE92MS9Nc3Zra1BDSVVKQmNVN3l4QWJvTW51VUNKWlA2dVZPK3hOSEJnWUpENit2T2w3cVZWeDZCQUp4YkVyNHZwOUdSMi9CdCsrVGY5UEJFaVZnQUZMWVdpY25YUUtkK2dMUHI1Z29RdS9PSjBDUVpueloxOVRtWlVlVXlLdGdwbXdsM1VGanZRN2VZRzVWQ0dQSmVxa0ZPSW5sdTBkOUloRUxhWXJnRlpkL0RKTVZaRTA2Q2xzMXRMTjF0c0tUdUYxdUltQWp4YmJqblJaZlhrYjJQRTcrQUVLUDlRMEhGWkpNTGJWeG9OTm9tOEdPMkMwNUVQVTQvZ1Z6aG9xOGpzdFdwOGlubG5qeEZlbDM1VjFraW4zZ3JxYm1rWWhyUGRHYWRjTTdQMFJmZ2ZTU3RYa01qMFRzVUE4ZitlK05WOVowUTNqV3FGVjBsN0hnUnVXUk5PY2tyNG9wMEs5dkVjN0M3ektEZWFqSGJja1FrWWMxM01EdGZuS0RsV2s1cHFKK2FKYnBINGVFTzZqdGNXVkZPemt2QnBRUEkwclZ1TEFJS0U0NWxzVWFzaHJ3Mkx1MUdNVFFUSnEybUdJUmQ0S09EWlpMVUhVSW1aS25hV082b3hQRWNXaEN5V29CT1NhZ25mdml4TklMT2xFRTdYSzN4NXd3YWVHRmtFeWZoWXlCU2k1clJOa1hWTTJBYTRtWHRpWTZjV1NSYklOT25LckphVlllV0ltOW1qZU0zN0VqMGpId0MxaHo4SkRFOTRzdC8zYkRqM3JGK1NuUHRVSW1JdjJqY2IxOVJpUnFVZnp3bjMyUnM4RFFWVk9USHhORHZGRGxyTEtSTTZlOTBVb1NaV2VwOVAxVlRmZ1Fvd0hQNEZuM1o4WlVEVkFZK3BTclFLNVpHNzFZMmhTRnVsMXlFVzFiWC9vS0VDVjFzbzVEV0FMMFlER0Ewc1JSS0JGZGxhR05aVVNmTk9HaDlpQnZIcjJjQ2RpeUlYQW04bHlzYWY2MWVjZ1ozaXIzdDNVQkJKOXFJU2JiUXJCVUxxU2lyaWUydElPTGVUOVVwYkZ4UE5JVlJ3Rld1dXpWNnI4MngrbzJkWis5UEtBUmV5Y1ZGLzhFSmdKZUdyTlJyT1JWb3c5NE9vUVFocE1pUFpCdTBFd1lYZkhFMEt5RVdIR1V5L1BGZG1qMFJuT3R0dWxrUlJtUzhrN0xoVURNY0FRTnNqeTNvVFpLZjF3WWhvYWdkcXJxUHZWcWdFZlNDY1NXTlZJOUx6cEw1STJFbU1MQlBIOXZVWkNVZ1dUNjVCNUxPNEFVNzRnS21pbFUydUs5YXQrb2FIVFUxYWc4OUJJTE9iZDRWY1dlRU1VZ0tVSmxBTDBMdXowdEd0Zk1RbjhvaXJkT0U4TU0wTlR1aTgxV0VHbkpZNzZuN0tDRlUweW8zS1FhZ3FIVFIvL1J2QkVscHpYSTBCYmxhSXhPTi9WdGl1aTdKdEdDdEtqVkpPVjEzR1greEdEQlgxVUZoMERDcFhXb1RYbEhCKzdIcngxVy9UdVJXSGVKVkErUVhyaGk0NExNZllTaFFJV0I1b1dJUVVoZG5IL3IxbnFpZlFXeFI5a1RCeG5FN1Z3anRlVXVkQWVvc2FTYWVJNlJ0QUM3Zkg1aDRPRDBZVkhwd20zQzVtNVVIUmdiai9kRVhid2ZYdVJwNjVUK045QXMyV0oxOTBGMlJRQlFSbXo0VS9BQllUWXQ0OUNnOU41QmZVL0t4cXJWRHJGRHlMQ3RXc1NSaU5kMG9JOW11Rm1VTWhEVjVhYlNVK01sQWVDQWxUYktYQnJFd1RsM3ova2xJNE4xZ3lqNlhueVZ2MUFaSTRuUW96dE5rRW5kcGUzditwSTladno1QU02eHdhSG5abHY3RHp4OC9LNjJWSXliczNuemdWSzRFOU05UnVnUUpyMlFPWUt1TEFqN0wzc1lmL09LcDFvc0FGTHpZd2U2NFR0K3Q3UDd5djVkcC9Rdk11c1VMLzA0ZC9ONFpKRmNoRG1zUXYrcnlScDQ5NFEvMVVPRzhKT0VWUWYxVVlGbnI5cmd4cEdiaEZwdEgrYUlEcHlYMWZCVi9jY1M1eFBraVdXZTY0WEQweEk1dHFVSUlCUmhrcHpPdUhKQldyRHljTVFZQkhNZDZuUDNORkM1aFBhOFI1YktvalpYNVM1MXU0MVYySVZaQitUK2RZcG9hQ1A4VTRIby9YZEp6YlZNbWltNldyVEFsUVZGU210Snh2VE9wekZNckJEL0srcm5VbzU2YlljTDBtTFM4NWI2cEZPNmp4eFFGUWpvTDZOSng3Z2VwYjNhOTd6cTRocUJ6WHphektoRWZYNnlzYUZjR0Q0Q3dmQVk4OERLZkdhSVdBcVpSeno0eEZ0djNvM1d6Ym1BSjJUMFVxKzFWSHpUS3c5WXB5V2MxL0hTcmxFSkFQbGp2L1lOZHdJSHVDRG5uVjZkVzJraXkrWE9qR0xwYlVGS2RYNXVSUTdwRUNnS3l4Q0tuUXBEV0U4N0xQRXFkZXBiMkRWdDc3NHRQRWxQbUpDMzhUVWo3aC82dUgwa3ozRWFFRzNnbUppQ2hpSzN5MlFkT2wxbks1L2RYMjNkTlJtc0hFQXAwYytJTXJKUDZ1V0FKUExObm1ocjJxTVZKbEd2TmRGaVlCZGhOWEhISmJObDlDMzhpWDcyK0NzQm9XSEZkc0ViUGNhb3NBVWVqd0F1Y0doZGRwWlRKL0NhZmEyRWJZZUpUemVkTTdlQkhhWHJ5S1czTmE2MFp1V0VJZTlVbXR6OW9HQ2NaT0VOaTUwbVpKY0tFdGRHdzl1NEt0SG51WWRXdGJJRHdvbWFBS1BZdnpzREZjZm9DUUh5VTBpN05NNjljYk5uYnkvT0VrS2ZZRXdrVmhKYUhIWUpqWk10L2g4WUJtYVhQZVozcXMvZ2VTRjVGckkyeTA2cmdnK1BaNTcxd1g4L1FrVC90WFV6SDFDaHlqZ3ovVXh4UFJsdUZwUlhTWkxSMWlJSXQrQ3FvcWRRQW9DTkJPMHRIK2ZzWXUrRWM4d3RWS1pvMFdMUnZnOTFRTC8vWFNFR05UN0R1K0NCWHkyYnpoTHF1SVJRTmMyRkMxdXJhSjJWYU5QODhlZzgzdDRuNDRiM2dseUpOOFFleFJlZ3RoWVZzcnhtWWY3Yyt0RGpvaFlmVy82QzlTQTVwUHI1bjdwT2QvZEUyQzBzekptTmRTeXVRTmpHbmxmbWdhbG9DN09wV2pqZXBCZEt5aGpvWlJ4TWFHa1BodkFjVk5mN01va1UxUTFvazVySCtSQXdMQ1V2MC9Nb1FEdUIrWm5RdWJVZElqSCtGQ0VOZVZzY2dhR2VuZ2x2RjM1MU5hUXlyREZTak5vNDVOaU4xTWhzdEZVMXFkMEJUUXVPbjBPTU5qL2hEdGJRQk03K0xpUC93ZDZCS3o2bzlrdUZWd051Y1doK2F6UlBLcXlxMVFsQit6ZWpaVVpCRjNrOHFpQ2VuMHlvem8vR09xMHppTUlRMktkWDluNjl5ZUJSRXVLcTA0VEdFYytRajh1cm4vdExINDhlY1h0VjhWaTQzRERpWDM2dzU2MHViako0azcyK21ITmJRdDJKa2YrTldOM1lKd2Jjd256a1Z4M1V1N2pMZ0tvcEp4T3VNVUxXZ3pCUXFsSTJSRENWY29HVVU4OWRjVXY4UjZJNE5sRGpjYjZZUjlQYlg1TXpSeUpzLy9Lb0dWeHpBL3FNSHl4dmx0MXRLYktCYURuY3lrYWM5RWZKZkV0RW9TY3BKSWFNMXhTWVQ0VlR3c2M0YXJ6WUhFTXNZZ0ZYekVydCtvbjJsbjNUZ0o3WXA1SWlPRitSKzZORW0rNDQ5dUFtVXRhU1ZBNE5kSWxKR0ZtQlQrd1RJMnd4OG9CZklnWGdqUCtkU29LL1NQZXpyZm43eHpmQzRqTENnQm5yQkJHZWFOaUtmdWZXQXJxOWpkbGNFamRaYncxaDVLK2JTVXlzdENUTWtYNzBGbGNHbWRaek1PU0pCamVSSmkweWJWSjdsM3JHejVQWUNObnB0UUpHVzlkNTJsSGVsSTdLT3RXaHNCdFdoNjE1bUpkSWs3TkVKZ0NWRzlqdWt1RzN0ZXBZR3hsekwvK1kxNEtObVBvTnRkUnRNdGZCSHhkMGZYMmcwbmo5Nk15d0lyNTJ6QkVQNU04aWpnNTc4aW5TRGFMbXJzV2ZxNzNPNHlYSzY5UHpBbUtoNmRGSXNZaCsrZWJ3RUdUazNhcVNhZDlHMDJaYjJFam02RXBzc2lmaUZCQ2lhdW4xbUltTmpOTWgyNEt1TEZlVFBDM3QyNVZxUzFWQTBrWEQ2MktSeVNzOGxjU3ZicUo3Rm8xbDRNOHFMNTMzS1dBWFFWWFRmUGtKOTRvbDQxdDZQaDZjT3BJcU90OENCK3Y3Wk9JclQvWmIwSGFMTzM5aDNTTlNUSWtZODNvK2hPSklELzFTaTREbnhkTVlYdVRSY0NEaHFwZHdyVUgwWXJnemgxNmZpd2JYbTcyMG54QlB5SGVmcjBTc2kreDRCTEVDdWNIeUo0M0RNZlZaLyt4L0ZGaUlCWUFYWUtKWlFBQk9pVmJ5MTlFMXBjNlVlWHVLakFsR1ZCMHR2SDdYblNHVGNFMnBIKzJldjhIN1dWalBaS2FjdmVJVzVOc0dHRFkwcEtCRkltb2N6NEZkazNWWUQ4OHZZK2I0V2tXR0s4dmNTaVV4aUowQ21UL3pTRmxTNUZRUUtvaVRPQ255SG80NWgwazJwVjBqQlUvb21HbTVRdXViWUw4cHljb3g2MEZNRSt6NVZ4SE80UVdCMHpoT2xJejErbU5udG9yVGdvSXdZZTRKdjl4TkdXaXdnZFNRZEN0VVNqRGpHSXVKNXFEcXpNdjladkNuSWs4OXNOWUc2VzBDWnE2ZXN5RGhGRkZkY1IwR0dyblNCZ2xBN1JsOVhGS2laTHFmQ0NlUFQwZXhieXB6NEJ4cnJyVksxdUZWMVQvQ2gxZDBUUFNlRjVxL2poZHhCY2ZOa3l1K1plMm9IdHBsUk96ck5YYWR3dXZHemc5Mkl6SkV4bzl4SVhNd2NhZEJHMHN0UzZPQWQ2YWkrKzhqcWZNb0pVNVpRclMyVjEveFZIdzhVaHZUWTU2RGU1TExyL3pOUk1GbGIrQzQxaFlEdXRXQitSU0VGUXpKbVNWS1RzL2N4dFpjMUZLOTdBMmVvZFVaZUs0S29ncDQ3NzlSNDFST0w1ajNxTlM2bnpkeWZPQVl0QzVxMGdRb3JqWGphdWp1WW80MUZRSm1vaUtiSkIzclkyUHdTM3hLQmpyWERReUtpcmY3RnV6UUhTRCtFbUhucjZJQldSaEFkRHA3dktZTjhuSnRDMnNoSVUrVFE5aUlhUVNYa3F4N2dydmRkUS9GYW44TGN5ZWFoMlVHWFgrTmdycCtUVkZCL2JpUHdCbG1lQkJPbFY5cXVnaFdRRW1wdFJud2VheUFKNXJBVW1FSUZZNXhNa2l1T21JZzRTa2o4dVF5cXZLZFYzTWF4TVQzOHU2bG1Oa3Q3VCt1T1hpR3hQdWlydFhhRDhobE5KL0RYQ3krWHp6YkQ1NURHM2F3cWRsak9zaE9UM1p5RmZ3dm9mNW1vT2R2Z3ZYSlBXa3phT0N1R2diRWR2MmJaenZRN2w0T1llcXJEWUk1clRQb3pVYjRXUGYwZWMrVEZ2c2thSlVWblJEOS93aU5ieUhqL0pkNk5TWm1EaGMvbVRpMFp5UnNUUGVWMXlqQ0R6a3plRHhQeXBJM0FzWkZMbXozeTZLYVR5cnYwSVhxWHUyZEtac0pXTWttZy9NQUEyZ1JJbU4zQ25FMDdlbk85U1FvcGd4MS9Md1JhcE5NV0RmL1R4c3lvVnlGQUV1ZFVGUDVGdTJFc0hCWkZLVDJoVHI0cXh3a3dsNzhOa1k4YUNRU0Yrb3Y1blZCeFdwSm5MWFJsUlM2b1VSd3hlOUg5RE5wRkYxT0J5ZFBWS1VOb1Y1SFNUQ0NpL1dmcjhHRzRmeklsRkdyeXlsemNMVzVINUZBenZlUjdVZWtMZEgvcU1pZUNIQkR3RWxZaDhtTTZXSEJwYUtQRFNBWHdkTVlqZXJoMWRPQWJrUU91NWZSejJieVRScmxuVzdkcU1VNFpacFBTbUhkTkpIRGJBY1RyZnd2WHA2dzNOaVplNFF6VS9pREpiTXNPQ3dDazZtZGdSVFFEU1BWMmhZODVxdTd0WVBiRU5VYWI4QnNjNVFDTFY5akFXMDV2b0RPYmNmdU1jMnBJOW5RRkVWdytCb29ScUt6Q1ltN0k2MXlWVmxYYzdqM3Q4LzFkN2Q5TERIMW1maDhJN1djaWdTVC90TUhhM09VPQ=="
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

    async def fetch_repo_script(self, repo: str, path: str):
        url = "https://raw.githubusercontent.com/" + repo + "/main/" + urllib.parse.quote(path)
        def _get():
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        try:
            return await asyncio.get_running_loop().run_in_executor(None, _get)
        except Exception:
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
    # 逻辑指纹相同即视为同一版本：payload 的 AES-CBC IV 随机，
    # 同一份源码+同一个 key 每次生成的字节都不一样，不能拿字节比。
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
