# name: 联通客户日2611
# cron: 0 0 * * *
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
    CODE_PAYLOADS: Dict[str, str] = field(default_factory=lambda: {
        "3.0": "fChSVFBhY2tAUkQyAQAAT2xnBVHP6JM2WUdSxoWTv4giaWFuL3M4SjY3YmthbVFvV3BZUkVoVFduV0ZJTzNJMzZsd0tJSXExS1hGK3AvaHdCS0tNeTRraEJKMHV6V1R2bGEwdG1lOGZ4U0M4MU8zZHdLNkVkT1VZR0Vub1JTdDZJU3pDZVRadkVERmxKL21OcjU2UlBORGljQVVtbUtaVk5lZjBldlB4Wnp4K2oxV2E4cWhtZjBVb1JCVzl0QmVnb2ZieUZNcVNncWJOZnJIbjNQQzlIdmJZNFZZUi85bnVJVGRNSlVDQzhlYUpPQXl6eXZZTUxTVGlxL3dPRHJPSkFtT3NjUUJ5ZnNseTU1MlNjSVA4eUtiR1FkNEZlWEVBUkJSZE1QNmpHY094YWtwODNQTFhyVjRjaUdDUkR2eEZPWEtOU1ZZaytKQVg4UUg1aGFxQkRZMHduZlV5MHIwbThYblVrVGJlRmg5RlpsejU4REN4dTcyOTNIQ0psWFFjNkFEK0YzSm4vZWw3TDdabzQrWEtrZUpoNVdXZis5dW52eUI5ZGFZeFVYS2ZJYmt5c2JGSG54VXhIUHNhYWNOeC82RFBWbDBXNkpNZFBjNDluNG40SDNiZzFOWXhhQTMvdnNoQkdlcTNLc1RHS1cydXh5UGl3b09sUGpIaHB1NEoxdDZXQWdrRlo1TGsxbVgyc3VTcXhORWpXZC9FMW5CZndBa21iMEpWZ1RnWjNxQTVsb3BObmNQWkFaQ0ozTmkyVVFSME9MaEhVSjhzVVhoQmREUE1FNzIxYVhaQ0dkZ1U0dEowdzhjbkJ6RnhyOE1LTlVETGVqeXNFMVB2QjBZTEFySzU4ZWNpRjg2MGJRTVB4Z1NrUTN3dWJsb1NRejB6NFlDYVdjSFFDRmdRa0o5SDBiemRELzRQREJTakNWZEIyTnlDeWUwU1lVL2N3RHh0LzdiMFdWekFxekgvRXAya2FCNjdRUmtrMllxb2RuOWs1VmVGZy9rYlpuVmdndnN2RXZQNFlCQnpWWElVY2syS1E2MDk0bS9HU0ZDVlNBbHpaV0R2cTBuS3lpNkFHeGNpbmYrOHE2R0VGdnQ2ejZ0TzJOandST0NJZnpkUmxtNy96T2ZOa3pGeFEvejIzOUxpb0pCY3lLVjBXZmw3b2R1eEFWZ1E4MldqWWgxcEJ4K2REdlMvUXNYTm1XNkVqUG5jVWtJYXQ1TDVIdVNuN3NqclM4SjV3NmtQcDRNZ2MvVkE2QXI4OVJ3TUhTSEJXREN2NzRZUmtyWlRDbzRVaDJBS0F4a3p5dTltNldlRFV5bjQ1VXh2OStKVVhxOGVwSDdCUHg5ZVhDbmlFb0QzQnpacWZWd0hoZEljVFhXNUFCVTIrUDZPWVlvYkpyY29uS05vYmFXdmt1NzdrSXZhUm14d3dwZFZmNjFiUUdkODlTN0pFMzRPdGhBR0xsYUdEeVNMY1dLRGx0VU8zbXhYWnIwdU5odjg4dWpmREl0aGVCMi9ncG5RLzA3cThvZ1hhaUdlbzFzNlEzMUkrRFhBZnh6TzJxdkl5ZWNVWVVhUDRza0ZTSm1vekRPbWs4eEd0Z2xTcW4reHJkQyt5UWNTbTNRNlNCMjZzQ1ZEY29KRU1KcjRiaG14Z0c5N2pIMU1YbXBINFlWbGRuN21mODM2R2xtdGtxbzFqNXFiYUxEbmxBT1cyRXFFdDhMZk5aTEpLNWNPcURvZzhmbys0T2VnMDRicXhuMVpHVGMxcEhJb1VKelpXZG41ckU5ZDkrdUdZRkNBNVlDeC85d2s4aW1TN1dpSkkrbHdKT05DQk8rRUc0allsZkJHUjU1ckRRbHRmOUx2T25LWmlYYnloTVRBa1NYS2pWOXo3dFpKNS8xbGE3cXQ3NTh4cTJxN292eHpDbzlGWlJzYmlNdzN4Snd1QmNHMEU5eDI3Q0E1RHlPY0o4U1hEcm5rU21GdThUTmJVNW1JTXh0REsxQ251eDBpb3U4aGVoUVltYitCV3piOExDeVNhSEVXT3BuT2srSHBtaFJiRkpYaVVneFBJMFpiQ2pJOUxKcW5GZDJYUjdzaktmcWxmL1UzOVBJaUZwcklZSy9lYkMzdXN2RUZmK3ozT3NCZTRvTnlwRnd3U25DQlNsZTQzUk9LWjk0bWw1aGFTYVpQZnhvWTRQTTdsVUZBTWluWDkwVUFialVHL3JBMzJJOXQ0c255ZDJzdy9Nd1lHdXMxbkcvVzRxS1VvdmErUnFraURHSDJWdDV4amdFS29NSFdXRk1DQnMwclk0eEN0MlhxZ2dOaDZnS1pKYmhPUGVJVVYyU01jOWdNemFkZXdBdDdBeUlxZFRESGhpVXZCdlJvMHpYWEtHc0lwekRpa2gxMG5NMTY2YjBoK1RVNmVmMUwzQ2FiWHhsMFdLRi91WW5Ba1J3V3JrUUlLSm0rems5TVRsUkZVUnhpM1g3ODBJc3RMWlM1ZS9XWFl6Ykw2U2swV2laeEN2NFBPV21aUVVxT0VacjJETnFpZ2ZOSzE5dXRaMTJjSXhORGpXWmp2RXh0SDFCNTZ0Qms1K210KzVmd0UxaVY3bHFuWlM4NC9HaEpmQnQxU0xuTnp6a3pEck53am5GZmtEbE1xMmtVV0M0SEtOTzNIaXdaZ1BxYllkWFpHd3I5dXpSL3h0Z1dpTzJvbmpod0Fmb25OeXFXVXpabDdRNUFyeXZ1K0FrVlJSSmk4aEUzZWQ5K1g0Mm15eG0rU2xWWU1uS05rRXFSeFc4Zm56cDlrcEdTNkNDeXpGR2V2TmIvL1h1akJ5NlBWTHl6WTFhZnFOYXdjUDA5YlpUTllYcU8xMUJpeldFcHBGaXpBakhOTGo1R2lweVRIMlpBODA5SkJLTWU2RUJmcEdld2hEamdhU09VMEZwL3NuOG54N1dKWTB3am53anZYcCtJaHEwTkVJaURkMG4vbWJQTDFlSGg3MmdhR2hSTEdpWjk1MmNEWHNtK1hXeXhlT1BkTENpRnhHN0RrWHZmaHhjTmJnOTcyYVVlOVdTK1pDYk9ULzQ3eFpFM2RuQStsQlpSQ2xuSTFnYlpkWjBrZitZM0NQS29rNWwvQy8xZVl0N1NKY2pVczJpZkVEMWY4dHQ4QytPb3RVdXg2UXhuMlljemdOT1BqU2kydTBjZ21Nb3JQMW45WFp5VStBTXJoM0d5TFVUYndzUEIyV0MrSHhxbDJibzRVYlYxWEo5NTh2WWRCbVlBaEdzSGk0YlNWNVNBdWFHV2tqTThSTTcreVIrSVhUL2dJMnlGSURvRGM0QmtNUDRYTlJDenprWnd2QUtSZVBxcU1Fa0N6K0NhQXB1aUZsZkJMKzQ2SWpsNHdVNjlSZ3J2a09hVGdmRHRSWS9mdC82N3BrcFVBTzVYMzJwQ1d5OVhuL3c5N2NaVzJIejNrSGJnTlMxallpeUpReU1yRU9mRmowM3BzTnFPTGYrS1ptNTFUdW94OWEyTU9pSk84OGNWa1Z3ZGhjeSs4NVBaQUwyeGxXYU9GK2MwYnpRMFBiclNGc0tRWG1YZ1NIS1Q0MXJETE0wS2ttemoyWE9SWmV0YkwvaTI0NWxOeFNjMWtadkZnWFpZdnlOT2duQnRadnJKMklIeVZwMW5aMk14T2NRSEtaTFNwQkY1aWtIcjlYRUZhbWpnbXM3aFNHK1lTZXZacVR1SmVOZE8rRW1weGFxNHF2ZUpISy9vRjVmSWhvQmVncmdhM01XZjRTMW1ubGw1RXhER3IwUTFPS2hEVENjU2pNZDhicUVOT2VGVFQzeW9GMitrU2V5WmM1dWowODZpWko4Z1EzUk1aV09TZTlwb2ErMi9KMWdTVHo5ZFJiRGFsbFFuMGdWQk13NkhxVm54aWFERmxtcWV6MHpSMENCOUVZeHc3U1hXWlBOTm9YM3RUamZMWUJock5iK3hzNUxxZXNiWVBXZlpQTE1YY2tmdks5KzdVeFB4WkRPZkFyd3ZWOTVZUGtrM1NFL3lJRTl1MVo5UERXckswMVVZeUUyT0prTzFuSSs0czlqU0NyWDlKQmJnUGttMk1VNG5pWU4rYW9LY1ZscUU2RXFvSEtCZGMyWFN1S3RoemJMVEVGaHhKalFkV2t4QlJzSmU0MFNEemtwSlE3UDUzVUNLZTNKL0g3U01ISjlOUi94aDVPajJJZjR3d0NMWXZad2lKS1RQQ1pEUTljcEhGSnFCRndwRk5LUWd5azlzUElVYjhPOE02Z2JwOFRadmZHbmpTeGhRSndhclNJRWNvcTJlR24wVUxXUnpxbXZnVW1XVnNuSDdNR2F3bk5WZFJjSjJTc0VCNzJ3dCt0aUlwOUtCMUx4bU5MbExKeDJWWThSRm5JQzJMeWJHeUc0d3RzMEVEWjRUMEd0Z1VSaCsrdkRkUHFYWWtibTNnWXc4OHlpODVEcEdDY0NNMEtyS1ZoSDhZS2hYOGRxODExYnV6YlVvSUVTUFBzTHZhbjJiNEQ2MjhWbzl6aFVGa3FaNDZMcTRyVE1ncWY4alZhclg1SFpKck8wc1duQjJzS2FnSGNLRVp0R2htd3hwWkFuZHNDL0g5M0hYbm1hNzlORFdoTXg1eWlCL203RFNGNFE2amx0TFFtVGNncVFpUkNTTVFKbHE1NzdWdWJmWUZHRzZjSWRudm56ZEpaaDAwL0FPdHYrVm5OZmt5Y0IzenZPeUQ1QWVPYWg4Mml4S0dYa2ZGR2NHU0g3cFpYTVhwTDlmb1RoaDBQdzMyYk1oaUNoSWZEbzBWUFgvc3VGUmpuaTNtUTMxN2gvUWp0VGtVOHBtdUZ6dytqZU9EQjdMd3B2eDN4eHBIL1gzTU9vb0RDZ0FYSkx1MWlXQ3FGL3BBeGcrbk02eTBIeG1qY1VoUU5pNm14R1ZRb3lpSGhINGN4VXBkTGZyenVGdFAvaVc3Z0I5alNjSkpzNWo3aTlxMjdrYlBZT2h5MSsyYjlhUDZENlcrNHFKcE9UdUtQMkJBMFEvdVF1UXRWUzZ5ZUJCMS9VMU1vMVJLeUgwQ25aM2JaYU9zTzdmdGFhdkMxMUFuWHNVMFV0ZXkxY2NjWnF3N0hoNEJ1S0xwUFBqdGZYSDFaNG5HT2puNHNVbEhVb1hscXJtU294M1VZREhic1VsdGNlZ1lLZmE3U0xpTkNkSXBwRHpUQjZLeTRyS3FSMCttTUIxTVhFVGNyS001MTI1NmhabERYaHRIajVmeFViUUR3VVhKR2ZxVE84aGwxTGdxa0pIc3k0NlNSU0F0VnVKNEFwTlgrU2g1NTRzTG9ZbldaZWNFQ2hheThNcEttRDFHaWxQMS8rb2hCNm1rUiszSk1nQ00xVEUyL1RpcXllWjVBZUpScW1RMjNFc2lVekUzTmVoMnYxWER2cmkxU0w3R3lwTVQ1NWtPSkdtU0FUay9VUmtQdUNpMmRQbnNuMTJ6ZGZmTFJwRGFtZE9pOG1ZcVdjbXpFRlVvYXBCNWpNREFWWi9TZmtwMUVvUllWeVNZYk0yMVZMSlpDT1BGYXpNK3hwK3MzaDJnUjFmejhRelNrTnRjYzI0a3lML3Q4c21CdzV0cjhvQnhTTnN0eDA2M3JBWDR1ZUJ3ZVBGMytTTndhNlNDZEtYOG9vRFZCQ1lvS2VGaTNHbnV1eGlnd3kyZ1ovMVB1RDU0dnZzVWdlT0sxdXVYckNaS0dlcTJJYlMrT2c0TzlWeFNrWXowSXZiQ3J1NFJFRFVxWnRMMm5tSjZoaTRFOExhUkV5TE9IaTZYaExweWNWWGRqQ3hhaXk1d3pjMG1Wd0RCTVpzbjhwZExrNUxCemFzamErT05KWTFDT3B5bUdvQk1IMmN4Q1BXV0JRY3RrcTRoNVlNWW4zVHBsVis0TTcvSmNrYlY1SE9iOElaZG1oV3RCUDZrb0NzT0dQS0FXZEphUXdwSWJ6SlhPTC9sem84eFYramRpajNQbkh0UXlkT1A2dlNaaDNpbHhWYWloQVd5UC8zOU9WSE1DMjlXKzRqMTdjV1REam9EUE9YcVB5bVd1ZUFhUzVZdW9sMUJCaXY1WUFSSVBZTmhDUEZkZ0VuUWZBR2ZCVzdWM1FEd2tldmg3Mm1zVzNUUUhWU2VlRVN4M3M4ZlRFdjdHNk1FWUtCZmxXWmExRERYbmdGWVZTWDJsYVhxNHV5enIrZ2x4TGJTNmU0SlZXSGlVdW52TWx5R2pRWHpkOGZEKzBEZDc3Qmt1OWtJUVZHM3hPbEdNREJOTXBXbjNydm1oNjRCc1BQNk1kWWNHUFlBRWQrR2cvRExuU1libVI1MVZMRGJkd0NNVUVZKzFyemZCMndUKy8wdHVsUGlWV2FCTE0rT0dueVhFRGRscHUvSWhvWDk2UzJiM2FJcFdwTFpEQklHQzdRRElaU1ZjSlVxeWU1SW9LSmFaT2hhL2xXc0hkTTZFY282VXJ6L1Qya0VSL1Q4RWNvQytqcUJIN3gwL25pcmtMODhCNHpvNEJGS0xoTUVNQXB1S001eUp3eWExeE5UV0FjUitXazIzSnd3N20zMHB4WENtb2svVEw0b3B5K2xzdmszWDBIcUxhSTYwQjJTWXl2WjljYVhrY0ltM2V2NVo3RVBlUXd0U1d2dzZtTjJlT1gxYXZrRFk1bzJ3dGwzendoOUU1d0lFNm5OWFh6QWZwckdjNWR6TDVuYjhMYTVOTndtUDdFRXFjUnFiOHcxTVpDTmZYS0VXWGFicVZOS3A1QWh6cjRzQkM3NE9ON0Q1K3pLaTk1RlBNeWlMM2VRcTFKK3I5cTJXMmxJTnRRWTA4OU80Mkg0T3pZN1JpUEppUUFoOHVoeTRGM2VERDE1RGR4VmE1MEdKYytyZFZOaVQ2UHZ1cmUzQjFpN3VEcFJ4NTFUVjZKQjFnaHVJRHBpL013L0ZhaDRwV2hOeTZ3S1JxRUNJSGFJM2FvNWtLdE9ic0U0L21PRkNHYmRrbDJWTjFya0gxcXFGc0J1ME1oYURQbjBkbWcxQ3NNUDl1VDl1eEg2bnpRb1N6TmpjZnVBTjczcGh3QUlvL3JLaTNjM1pXK2pXYXZuekRsbXRvdWt0OGZsTG5hZy95RlFDclJ6MVFMdlZEc1V6VWJkajl0eGRhSFN6YjAzL3llZGE5ZnZCQjZrYzFSNEE0YnB6UVg1NElaT0lvWjNDQjM3QTdOS29PWUlsNitpMmJySmpGWlRpVmRtZ09TQ3JYQzlLVWJRMXpoUzlyQ2ZnSmhGT09xUjkzR0dXWnRmTlJJNTgyT1haOTZUUkNBbUYrZHZzNFF2YVBMV2dlODQvdUlrWUhhbXZaK25BQzk5S0FURzdWeFhLaUhtRHZ0NGd4Qi9sbkYxam4vYTk4Yy81NU55UzJrNC9oQnNIVXNON2l3dUlBNnFBdGFVVkE1QjNLTWp2dFNoRUpZd3pRM2Y2bUFXK3VLcEJUaHJIUzhGY0k2NVlicXowMXpxSkdMVWZoM084dmxXSXBKRCtYVWhUMTBXNWlJNXlvZVl2QVkvT1EwWFNoOS9Kb21oZ1NLM0R4YUdYY3Irb0JMRXZxVW1DMUpKWEcwcnNjZEdjZWpRK2oyeno1c3pienM0aHFEUkFORitKRDZCNmYrQStycnRIbE9vM2ZMOTd3aytqbnZpNTZBZFEwYWcxM1pGMkFxQi9keDVDTFpsd3lTTHQ2UDAwSnl3Qmp6MGpyNFJKeCt2cGNRSVlPdEFXRnVYdldTUjNjdmpkOUt4SFpWU2dlOGUzeGpnOVdzZjNySGVWVEhqb21QS1NxaEkybUxiaHdhSHg5WTBaQXlmcGRHdlU5Y1F6R2EzcTBuZVQ0bEx1VXcrSklqLzJTeGt6bmVsY3hHMTZDUmxZOFpvZ3RJc3o4UUh4N29KZDNMejR5cDRKV3YxYmlKRkhYbDlKbmUrT0FVYjNyZk5GVERDZ2ltMGk4T1lmeTFoY28wd3JCZktJaG5lR0tYcVRxR01NcERFUWtURWRrSjRlN3k2NFhZL1daRXRieWxwUmVyQUkrbFJCUVdscWRwWjc1RW14QUNTVjBYKy9EaThQajhmaHlPUURzTGJuYjl1SWNzU3pSRHd6MFVlaGFmTHlXN3graHZBK0ttbnRiKzVGOVN5NlFFSlpzZTMwWHE2NG5lSHZkVUlkZ3l1Nkt4S3NOTWxkVWJiQUJ2ck56WWJncm93dVdhQTZDTW9jMUlSU3hUVkFYT0E1ZVZsTXV1TkNjK09BWGhkNzF6RUJIWHFMWGJwQjdjQjJzN2ZwZm4yNDBhbXNBaWlDZ1RMVVo3WGhKY0VNckp3ejRVcjFNUlBTb1I3OWxzcFFQWEdBWlFBeVp0RFZkWFJPNWhieFlSalVsUjQ5NGJ0Y0dGdkNKT0J2b0NJZ3B1MEN4dS9IWlJtTW0zLzYrZjJ4emV3Rmpkc1RoQ2IzMmN2QU51NytrWXNBZXduQkNHSitrOUZmenRvNDZ5OFh0ckhKL3JOTzdHZDZ2dzNQdm5sNlV2R3NZWlpDY09ySmJESW41M3lkTFJVZHFQQUFLTlU4ZEtWZU9TSVhCQmN1aEhqMmcrRmdicE9MRFN0RVpvRkhlbzdjYnFwcjYxYzd3ak1KblBQdEQrclFsaWVFWVU2MW12bGVGSkcya28rWnpjZW1MempPWUkyQ0tRekRuQkJieTkzdTF1VnhKYnlWNE1za3dNNzZzWllpS284aFFjTkVlcmVCL1RocHkrSlN5R3BLNC91S0M1RTlmWEMzZmk5YTIwV3gyV3Baem9OUEF0N0YvYm9IMUQ1M3RWRUNhWkJKUitpTkYxdnJBMXRiYncrUjhRUDJadytxRUhYR3Vmdm5haG9CK2t5cnpacDBNVUVVNE5KckF0RkxISEhRUjBtQ1BsS1pLaSs3dlVNaDAzUnNYOURYZFpvZnpQcllZWG5oMGVxZ2VzakZiaUdjdVNKRXU5VEFNVHpudGxYTjlJMHY2TjEyVnNvV285MlZrdFBtdU4wdGdJbFc3V3Zza1pDbzcyTERmSWU3RzUzZHMwR1VXTEpnR1JVbzJzcFkvejIrdzlHZFBKYVByWU1EekdCYmZwN1hLRkVaSDE2UVRId2dOUWJMRGlDc0JWVzJIREpvRmwrSVJiZFBFRmFFZlNRZXhSY1ZwQW45Tm43NU5MTFZWQk5kaVo0cEdkK0U4OGhMR1pITWxKOTI4d25ETHBtZ3dpMWROMko1L0VhcFpnVWdTQTZyTWt5MW1lMDRnWEMyak5TQzhZdy9xcndPeU1Vb0hIY3k0MlFVaWI0TFFJWlJLNGU2NTBSajhrUXRhRDFoQ2JDZVRKeG0xcisrN3J3dkhDWERmaU1QNFhFbUhjNFRsb1BDcktNOFZsc1N6eXZiQWFPeXFQUVpyUVR6Y2VtQU8xNXpCbXlzS2RTY3JEUkZhdzQzYjRsZ1B1aHFTSlRtRmM1bzhpSFpvV2haY25QZXFSRkJsQWo0MFV4dk0xUTg0NW5EQXNTdHBFZE5nekxuK0szaXBMNzUvUjREbWY1eGppS3kvVWw4elVOL0NKNGhTMitFVFlNYmVpN3RJSlhHM3VBN2dCUnE5OWlEeEhrOWNWNW1zK3JDVTcwcWNaRyt3QlZBTzhpVDhCMHBaK3dUUzdVNm5CM1pNNjZGUStoQkFxL0d5MitDN1k3d1VTbEZ4NGFDVWd6RDMyWE9OVm5mMnNpYUsxMjlhRGpxWC9lRG5rcExQam5aTTBvR1cyRGJzL3E0OTh3VHlVa1FFazByWWJYRHErZjdlZXdBKzlzRFhoVmllL2hlc05DL3dlU2lCaEtvQ3hiWmNtWUxPRW8zNmFMVzFXSTRQNVdKcWxvVk96bWpoeEplcHlUdGFKNFU2U095MGYxK3pZMDJvWTc5QzUzRTY2TXlWN3RhbDIwOWh1YlJ0cG13RWdHWSsxSmZ1NlpNT0FVN3gyK2YweUxpaDRhY2dOT0dHM1krQ09lWnNHYjlOYm01TkR3WC9QQTlzRVpsc3AwSlRkU3JtTzl5ZVd6SDlnSGdOakYvNWhiQSsydGh6Y20zSVlZNVBBaUZpVm9WTFJsTlEwMmtycEl2L1lRelo2ejJ4andGa2cxRjNqUnU2RGtoL0hNK0J4RU9KRVBBeW1YeUI2cWJsYUxTTnBBYjJtam8vMmhHOWZrTG1iQmNWcTJ5b20wazF6Q21JbGhvL1lIalozZURuUzM2UDJ4T3RTaC9xRGhmdGMrWnJUdkpUTTNsRFJiQ1FKOEM0ZTUwMmVZWjZCWFFWbXRlYmgzRmdIY2kvT3VTWlZlaWZCbUp6aHVhRUNUMEdQalI0dW9COXZMaXcwWEZrRjI2V2EyV05mVVJqcHBJYlBrSE5XU2x3U2JpRTM4VnFVM3lvdXJCelpGK2ZrZHhhYk0rdVNldlN3VEd3TlhsSzAxZkNtMHd4aTZQWnRrSXRUQ3dJOHZKenUxR0MyNjZNcG0xcVJxMW5yNGJBbW9SR0dibHJVdlJyTmRLVkEzYW1GdkE5WWVxRjRDeEh6S2VlNE1IcTB6aituRkZYYzBjZThLdE9KcUE0cmxlb0RIOWh6NWdzOHF2UkZCQWZQN01LSW1XeHFyOG9GVWJIZlVIdnJFK0VMbjZhYWNzc1hNNVBqWGVKR0ZLQURoQkh0elphcjZMN3VZNkdKODgvV3UvY3pVWVJsd1dRK3BYTlRHeGh2RnBKcHNHc0RwcUwrVnFyYndCbzJYaWZpYjBmclh1Y1R0R2xncHptQUxtcmFsN3ZXUzEyRkZuYkRhS0lCaUMrWFBHVS9yK0R1MHRGMEsyMWJlM1dHTXh6dE1TWGpESHJoU1NxR2c0NjdnbU1BTUFYd2hGcmZ6VlNVd0RxZlgxT3VKVXlEVGIxSVZSbEtEOUpWd0hDOWQvcFN5OTg0MHlwWmVGenFDU0ZSUWNQRWJnc2xrajhiWVFnemg4cTIxNm9wRGFqczFCbTZJdVJwZVpxK0FyTUlHcFZUeHF5ZFAyVkdmZ2ZXRTBzc2YvZTJMYUpjTWltSERlUUJiZGxMTUJhenpPUjVjRnRFYzIvL3BUWHgxTHFZc1QzN0ExYlNZOG5Cd1pkK0JVZDFrMCtkbnV3eTVjeEdZbGVycGZtcldpTFpLWUlybTVpd2pXUzNTNHFCSTQ4WmlXejJBakc1aGUxckpGQzd5QnhwS2gwUlo2MFpNU0c2S1AxbGlRZHFsL1pUV3MyQjNuaXBQQmRoNDRQai94KzhidnpGZVIvREpSYjQ2YU5uN2NYK2tYVFpzM1FkZ05OK3VZNTVHZUVNdnhudm5ET1RCUWRQdzJkNGQ0eDVTTzhPemg0YXhpZGFyY3B4SVdhSmF2VGJaZXRHZnM3QVNFQzk5Q2dxVWFoNFdnQ3NlTUFFTjh0cmxLdHVDNE1sWEUvWTZ4U3VIbzlCeGdxNlhOVjBzVDhPTmdZYUV6SXJvZFJ4a01qdnNHN3Q2aTl0TG9aVVA2UzN5K21kUHArcFpRYVF3OVpNeVNjUWhqUHJCZ01ERFZOeEVGM2phSTVzK3Bja3hxUENOMk8vcXA1Y3FXN3FBK0t1UzRLZUlKVk5LM1VOUnArQXQyWEZWT0Q5OVFuWlFXUnNPeUk2elNtYTlhYzVjY3ZwZ2EwZm95SnBUWGNXUUNJWld3KzkwVysrSTR2WWZDYk1WczladXprUzZWNUxnckNXdlJpWWtrSGlJMm5aazV2VlY4UFUwbFBKYlpJVkJQS2M2OUtMY0ZWRmZ2UDVNcE84SmUrdmNDZGVjam5zdi9hNGQvME5MK2JEcUZ2VGhlbXBPTDM0SC9mZnkya2loR2ttZXJ2N0tCRjIwd3RXRmxlZzFOckZkdVhpVWRaWW80MlhidGFZSlp3V0prWTB2djBWNEZITS82QlBZc01jc0JNOXNBemR4TzlXeEg4S1BpNHFpWllCYnA1R3daZTBKRThrZHY3UWM2VCtHU3EwNEJHeUdYQzhGRGM0TkUyNzJJRHRsNFoxclNqQlVHWE5mc3J0cHBCZmR3VUtuUlJCck5kMVFaY3EwYTR3bjcvc2duSnF4dEVhR29mRjZweCtpT0xtNzZYanFyS0N4RkxYVC80TDlCemJ0UG9pUUZ5K2dsTTl4MTBLRmdNQzlZMHp5b3VHdHFzc2lBMkQ2ME9GWmhrVWw4b28vOVpmcDYrK3orWGRKTjVSMHFzWnhRZE5wNTBVdm1BRmhzVmRUMWdwWmV2RzdqbEZvaHB0N1llZ3VVbEdyZW96aVMwblZqemdJTGRwU2lqYk5zbUhFdHB1ZWxLQ1p2czgrazhhWDhQT2N1V05Gd3M4dUk5L3lMMU40ZmR1Z3VzSWRNQlFMalh5MHkrKzVVc3dyZDh5eWpOdkRQaitvLzhEZ21yNC96YTlKQ3FTY0NrWjFJYjBNSlhvYXdraE00R05qU3hJaWlzb0VvZnd1a1Y1SHpZMFFWWDl5NG9RM3djTC9ZSHo1cVExTjd5djFJVU5SN3UrSXRNUWttMk1Mc1lobkk1UFlNOGZQVkwxOWs5OGtVL0xIdXphSlJtSE4xMG10QkFNZGdWcCtLMUxMM1JNOWkxRmRZWFNXVWFmZjUrN1BCMFlycmJXRExsOGJMRFJ1alVZWUlsVlBiUEtyeitwSSt5bFN3UTd5Zmo1Zm9odE5FbFFTTTRFRm9FU2JBTi9lN0IrdG1JTm5sam5ZRzVCaFQ0MGw2eXRGdlhwL3VOMGFoWmlJM2FSQitERWM5NUpYQ3dBbXpuQlVkbGFOV09xVTgxWWM1MlFOUEgxcEJvblhRbjZ6bWwzNERta1ppbVcrOXZ0VDFDZSt3MkF1YUhJNDIxL1dFOEJjQ3RXY1NjaVJvVDVxRWFoOUlRUk4yVXM0U3V5QnlibDR1SVdIL213bGlUa04wdEQ0aEQyWGRZRTRRQ3FyQ2lQREhRSnlPU3N2bC8zMWdBUklrd1RoSnZkTCs2VUpqOVNFejJ6WWoxYWlQL0VGNmlYWG92cFFEZXQrT3dYbkVnb3EvUnZFNnd4V01CUUwxd3Z4aXB0N2hkTDd6TzFCeVh6eU02aDB2OVhJdm1GTGZrTlJrUXpzUkdJUDBlZE5wNTcvTXVRMjFBTDNBWkg1bHRZdXF4RERHN2R5Q2tDbEdXOHg2SmhtSzNvN2lSVG5PUmNwWjVzTEREUU9EUXJNYXlKSlRWNnhpTnBoUDdsVmNNQ2xHcVl2UkQ5cWxUaVhrYmp2ajllQ25vcTFjM3VTVWw0aVNWQ0g5dnNNZmVJNDB0djZsZmVkMGhHaWZHODNQbzBkMGl4Ykg2WllhU3FiQ09qMkJycWszWkhFMmE5RjZPcmcwWk5vZ0J0MER0eml5V0pkcERUUis5ZWhDcDVzdXlZTDdVRkpxOFZhVDFKeXRaUmV3eGhwRFlkMlNnNWduOExOVUdSRklNZHQvaUJWM01MNUVvMEVxeFFycFhEdGkweXZtdk9DWHUzM1NVeDV1NUZWdE1EaWNrbUhzenNWeCtXVTdqOWRSWmt6bGx1dVE1ZUkvN0U3eVJoZER3Vmc4bEIxOHA5Q1JzMTFoajZiN1gyT2FveFRXOW1WanhFcmsrM3ZueW9vc3pvUEd4TDRlNWVvVU90MGdtWFNOREJCOHdxM3ZRV3NLUXBOMWlleVlBdDRUeG5tSzNJVCszYTFQdnJjK3ZXRDYzZjdiWGZ2VzdBNkJ2cldTQ294bXB3MUJTUXRhQnZLWExXL2dhQmVidjRqRHZCMW9wcGVmaVhvbTNqZmdmQWxXNkJCSDhoMCtPdFNBcm9rQ25ZQkxjbS83WmhqSzdwc0ZRZGxXVmhiclNMQXhxSWtGbC9UZXNCL1NtZlJhckxnUHhYVVVjMCtpZnhpdEhDQnVQUHhPQmh5TUtjaXpPS0RYeW81M2NiL2tNRnpvOW1Rc3BxM2xvc1BOWDZFVGlpWWpFYXBKNFd6NmFoODZjK0Y1UVR3WnovdVVZdk01bndRMTM0Y056L3VuWUZiU2FBMXBIYlhrQlMrZyt4bzIyd1BXUFNvdGduQ0VBZ2R0bWpKS1BraU9sa2tndnNqR0tpcjVNbEE2YnpjVU9CZTBzU3JpMXdpK3Nic0NleG91N25NUktXQVBESklBeVV6RWpDNDB3MmdhY1pFdXBMQ01xQzFvOUNsc2pJby92OUVESHVKUEJDajVVVWFQSnJ5MWtUeEpweTJnWnJEK1BnbEg4RGVMd3lHYVpPTDdNczBQWTFJL05RZ21xZzZrWmQ4K0ptSVdPYXZobXFCUlVmZDIyUll6YVcxSXdKTHA4a3pHSW9GZkY1d0tvMmJwTWdhVHFrV0NkK1k0NDh4S01VSXNHVFhsLzVNazVEUWdNUk9LeURReW5hSUc2Wnd3UVgxQ05KNXZQZ1JPUU5zYTJDaTdpbk9WQUxvWTlHZW5MdkQ5R3pFK0pPSm5OcFlCUTFZdUVVRWt1SDFEY0ZaRjhYakdPdDZ5ZFBka1BkMTZHR1pROGw1Z2NpOWRvSjluVHY2N1JKaXZXY3Y1MW5XVEtRQjJPS21ROTNvSHZ2bnNlSCt6ek1JdE9taHh5aUNlN3BuWmV4TmErQU1aeXRQeFBvVW9McUh5azlONDR5Ym5oTElrb2JMSWxLWFV1Vk9ybjFaUitMR21lOTdGZnhwUjNha3NkZVlVRVppYVlUNTlFMUcyMlptcloxWUw4S2dyV0dNeW8wcVZQUmtEWlhqQkd2ajZjRnZiSlk4SVhyWm5Ub1JDUDBHT3VrVG1uaFc2cWVOVGJMbjZLU3RDdlo0UzlkTnlaUjl5MzV4cnpsWk1yYkVGc1FpUkZyOFRlemdBYWd4OEplV3lOMFR0eDhqS3NBVjg0Mm1XZjJldmc2SU5ZVjlMbXBsc1p2UzZqUEFtTE52Yk1kQlVabkY4U1VRNG5OeWtlSUF3NkhiOGVQRlN0OWhQNHJxZU1HT1kxd2RxamJQeXZFcXRXcXQxbUpiVGJxU2RhUi9yTFNsL1RpaVdaQ3NIZlJVdjdWME9tZGQ1QmpKSFErWWpRT1hwVVJYVWVlK1dQNzQvWE92ZjZ4WllLWHVZL2hkQU45OUozem40MzdZRTF1RDc2ZDIrOW8rNXZyenpKRFRRN1Y2eDVWYnFjdXBzSisvaVZabncxQUtzOG9sVlpCWjFXNFlIclJJUXdqV282bEUxZHNjK05MNFFha09QNkI0elZhVm9tZTRicUQzOC9BTkRocmVvOHk5ZnBxMk50b2poQUZubmJJanprNVNuZkZwS21lSDBaajNaMW8zQ0gwZ0JRUnRKNStnVlVDSjl2UzJQb2RRdUFPaGpVdEVndzltNGpndFpOczhnZ29sYktyMVFFS0JEQTF6endjZERySGhmVXJHV1FudmpLTG1iOGordk82RlhXQzhxb2ZaV1d4SE5SdXFuaHNjYndndUt3bnlCYWJFNDFwWnZpcExkTXBVcXBJUVNrOFNYOHNwUVljWk9SUGMzSWlzb3YxVi9jR0hYeU1jZFhNV0NJSWFOWDAyZFRMc3J3NXZnTTdzenhRNUVjd2NnNkdsdEJucHJmd3c4MDNhZ2V6MzhxbjhqaFZEZk9sN3JVRXQ5SjV6eWcrV00vb0FLZERGMXVjMCtrTkhram9UOGkyRTFkbWJ2b25rVStsQmtzeWtSWTFlOW0zQ1hFUXNWM3ZWY3NrYTVyM29EbFVtRElBdjc1cm9yTHdtMmx2YUFsVHdhS09hc3RlTWQ1ajJ2THFXMW1icGtvVndNM25VTDczZlNJc1ZHTDliSlI1Tk8waThmdWUxYVBhU1VWMEJMNFFTK1ZBT0loeE5pc3FORnBXbG80V2kzdVY1aGxKYjh0ZHVhc2JuZS9RYW10dlR0UW5WSUJtcy91TkllR3lrSFIrZkJwcE9ia1lXZ21CbFdvTmpLNmxqS2l3dHBMRjB0eE1PMDd1c21RWGNLMVlSZ0wvcHZlVzZDREYzZTdxRTJPclNQeUcyYWhMd2laZ1lvU3ZCTDY5U0hzUE9DNE9QWlU3SE9oaDZFRVd6M1p4RE8vdmNwcldTNC9JZ05HbjZ2UDRGOW16bnRNeW8xd1lZcGJqaEdHYWhNaGhFWlFZQ3hmM0R1WjVyc1o2TXIvRGVvYnhtaU41MEJKYkVzdXR2WkJ0dHFDa1dxKzJ2dU5rQWF5WXdKQkVha3BUSkNRNUZVMXFrMEVxZ3BZdzI3aThZTDhkaE1WNndsQTNBQjZvdVhPTHJ4U0VHdk1naEtKVUZHS0tvajg4TWZaNzJDRk9tTUpRSTZ5UGFxUklIRjBjZU5RaUJ0bFRTbmNxb2U5ZVBWbEQ1RDRoR1FOZUpiazlaWkVPVjJSUHk5WlR4QktXdEtza0tsL0xCQWxzdGxoSktoMWswMVJLbTM3TlI1UGhlU1cvNUFIUTMvUTI2NVIrVGxkVG1sNi85dUFWMzdGbjYybGdacW42bWR3TWFDUEdGNkw0SDZORU4xRDdrMVBCU0N4SUkydng1bGw5R3RmTGg3bk11eVd3R2t2THpReVZ1K09vZTV6WGN0OENMNmhqbncxUVY2ZDNuck9GWm9DcHZMSTdTWExZb0RManBjUHVzd0Rmc05xRzZxWFFOcWpCbmI1dnZyY29nblVNTlVScDYzZ21EQ3oxaTUxb1NjaUExcGpER3AxUFpMbTBZQUJOaTlGSTZqY0RIamNLRkVBZE1LRDNkR1JHWlNXbXhybUptYWY4aXJzSldvMHFOUXBoQ3M0ZzEwZGdEK1Q4MEQ1VUJwT0VPdm1PVFUvSDE1RWhIMzlxNkc3eS84c2swU0hDUVJudmpOQ1pIU0tETnRCa0lKUlgxeG1qZ0w3TnNTYVd1a0d1SGlsUWVlZ3NVY2d3SFk5b1o3V09ORWNJRUpWWmM4czg5RTFtS2JjQmdDNnJPNnVJTkZOeFFsc05oUGpicWtOT0JQajJEWGw3T25obUp3VHoxN1BCT25VVEFHUzQwTFB3cmZOQmhYRlM1Sms0RjRhWXY4SFpreEptc1JvK2tOYk1oQ1pWdTM3MWFBWUlCbHRrOWFBbWVGNFlyR0ZVaGJlSlNSSXBPQ3R0aTJuWWpXQmtTay9tL0pueGdkczRjbXdNT1MxVXZXNHlzbW1vNzlLd0ZORytvR1hBYnlHd3JaeXhCcFM0blQ0ZmErbC9mQ0ZGZTBSZG5pU0NrODBjTTdwQUEwTGgzZmtXd1FSRDdoeGQxZ0tBemNkY1EzVlpVeDJtcW1kWUY0RXFhem5QN0daZlBVMWczRisyQ1R3cmczRVZQL0NBQ1R3eENqdWhTbDQ5OHlwTWFnSHY2TXZIR3JsSkJrenNyenZKMWdrSUt0WmE3cFBselY3ZEJBMzFxeFBFYU5IV3Y0Yk55LzlKRGpGMkFEVXhVZ1lwcFVNZE1UNGQ3T3pjYUdVWmtGNDVNanl0TGRUOGRXcWhFZnVUUUZxT2NrM3NFV1dJbUIxdjltK01xNUVrblQxelM0UC8vaDFYSFZPS0dIZmYyVVBVNVNkL01Xa3hrTnRWTXZSRys1bzQydHBLN0UwVjJkd0cxL0ljeUs5RnFITFNtcGpkUFZacmtLS1o2V2pNMXZNTDZvMWFwN1VYOVdVOXczY1hlVkFYWUxPZnUyL25iK0ZweERud2dkZTJya2kyaFBOR1J2aGZiNDR4UHhtSzY3TVhDQU1sbnBnMjFVY1RtdE9nUnFSTjE3R0lPQzNtTUJCWWpFWlA2ZWYwdmFtRklqa2dpbjVpbmJsU3kzN3FLUW4yZW9oZU1tWVg3N0tMN1QzeG1EQkt2TTRGajFCZ2x6Ri9BY090V1FEd3JIUWdnYU5lSW9pdnlZZHFSTHNuYjJVOWtNc2xEMXVBSm8xWTJxR2tVMEhlSHFoN3ZnTzRaMXBud3hEbUxWMkFOQ0N3R0p4dVJFSG4xOGpiV1VjZnlxcmMvZDBQOCttRUk4VGxGY2RWSiszb3dtcVZmcWlhZllBT0IxRXVhYWtDeE1PNXdqWUZ3d3k2Q1A2eklHR0ozT0ZNWGo5SnR2UjFldkU3QTIrYlRibFczdXdpdi9XNUU3U0ErR2lmM3JiY25ORWwvSmFCOHZhR2lBVGZXcmdNVmxJWUdEZHJSR0cxQ2Y4dExBKzJkeEhDUGZ0WUdmNlZ1TFZWcThnMHBGWDhjRlV2YUJpRFFkY3FxVytldHlUR3NweHhBMXRXN3Y3akV6Sk1wUStEOGF4M0hTSGdMU1ZuOXczZ1JBNEhQY28zeEdVSzl1SURxL1YzandDbUFCMGExU3E5KzNsckIrYUNmYnplQ0NrT2ZWdFBRbXBwVi9lQkIrb0lpYUhsU3cwK2dRTHVveHZyS1hHaUdXMENjNUpnNHg0RVdHTFdrYmJobnVPNnlPU0JWVnRVSTNYcVZjcG0xRUcreTZNdGtOY2UxRU1leFMyZEd6ZGNuUzJPKytncVlWY2E5TkR4TzFFaXJ0NmFBWEE4L0dDUFRLS1ZRaU9kZHo4OUFkTm4xUGk1WXZCSEdyUGZtZldLdFQwSzFvQ3V3d2tJc09pV0R0VG5XSklhUXQxYWtsT0x0OXJMeWtQZEE5RXU4YXF6bC9jdzhoS29pdTNXcllKTmEyTDk1S3V3cUNQZzZnVEQ3clA4SVU5R2pJaUlmdTEvSlpmazg0RzBCYVlLMFFLUTdkeUtzaTNFaW1zUEprR2xnOVFPanpWUmRnNnQ2RmkwUTdITEs0Q3BBT0hDaFpTNWNlS2l0RlZwb2lmNk9RWkgzZnZzT2tVaFdxaG1Ucmo1R1A4YWdQT0dJRFdmT25ybTZmb2w2T0p4TTkxNEg3R2hSNmNndGM4VmdROTBKWXE0b1RqN0xHbGtLelZiM2hvK0pKN295MGNYS0RBY1pkQW1WazkrbFIzYmN3d01iZjA4czBZeWxtRXEyRmtvcVFNdjFWUTA0MnlLdnEwOGlETmRFeCtGdklsdHFFWk5CbmpGbTBSYWlvUFZabnJ1NGMvV3MrZHhGTmFaNkp6ZkxaNWlTU1A3RGxFeGEvQ0dpbjhxMlRFcjNpcnlwYUlLdXdEeDZPbFNsOFdmakVFOURQZTNxOCtOUVFrZTl2SnBlUS9pVFhEanBLYmtKa3ZNNDlGOGIrNWs5UFZPZTNiN2lEdGEzUDdTSVFQMmdBRTdMeDQ2KzZ0Z0FRbXN4ci9EenNvM1VBWU00WFhDNEZnaGFqN3ZKWDdVNjJXL09uYVplSG5MNm5RNTZPaHpUanlHYXFxZTZlUHFKS0ZhNGpYY1k0QUE5WUV0RFhCUkxqTHVIYzNWL09yWm1yVm0yaVByVTF3U1QvNkpna1JRV0dEaDlqY1d4bVNPRE1rYm5lT3l6Yzc1QkV1ckNCcmw4ekRTOTJCb0FGZUxHTVBTTWQ0VnF4SmZ2SjhlSURobnlrcitOWFBxdzdOcGtRNnk0b2diSGlveVFHMHd6WEk1T1pYRGR6QzRVNVBhQWRGVHRCTVh4WUFxVktsTWJUK3JuSmZ3Sk91ZFg5RU1KdWg0UXVzZnNZckpwMEZlNzZLUGx3dWdyZ094OUF6c2laQ0FXajlWQS8rcDUzOW44TDRPb3BaUVR0YW1kOUJXQVlzdVI5eldVMWhrUXExSTZzYStJUTYxdWl3RVRxbTROVldSekxRU1JJeW12ZkszQjFYL0hKZDZzV1BoWGJXditQRUJYb2Y0bS9CTlJxQU5tZ0JKZzZOaTVCR2hMc1J2NGRNU3lJK0c4aGo1ajFHamlzQXJJb1BQN3VzeTJOZnViSE9nbGZoUmpkR3Y5RzN0VHk1V3Azdjc4cU5Lbm95aVNWVEhncDRucktucWFicGdPdExJbzFpSk1jbm8ySUd3R3o0TURTWXFOMFRkZ0laNjd2U2Z2UG1lcmNBa0RNK0MyWTM1aXQ3RFlVOUd1RXZESTh5ODhKSzI1Ulh2bmpjb0habXpyaGJabHNjQTF4YVZEN3ZBaTd0MVk0MXpCSTFPNnMxVmRJekVRMU91a3NxRjRSNFpWeWNsR1YxU01mWUxRc00wc1pXMDRaTlI2Q2lHNFNCRW1uRFhxd1hNNE1QNkRXS1pyZGt3aXBEdlhYblJ1V0Z3STRFZi9Nd3BhRVNFY3FQMkZjVm5FbzZQazlQTnBKV2NrMzQ5UndrMzI5T0IrRFdNYkhlMm5qR1dJYzZCdERpL01neEJua25TbmNUcThRa0F0cHBWcTdMbzdvTVRRNHpBVW1JTmxoWWdhM2VxZFRZMnNCK3FzOEVwUUkrTnJyYSsxbzlEVTNLMWl2dEpMaEtDV0RZb3AwempHZ09IZFc2TzluWTBXNVluRjArSS9vVmFoK1VETlRSNUZZcGpSTUptRTlWemZUYlFKU2ZtMXJKYVJOeUt6U1AxVmVzVjlhbmlnZ0VMV2d4eUs4bXljbUpjcmlDY2F1UVI2TUZaZEVIejRaRXhJM1BBMmJGeU83cEtWZ2ZXbkkxYnhEU2xqSlNEOWxiQzAwNUVBa2Nvdmcrc2drb0pnWG9GTjljQjdMZjFPYjFkL2J2V2w3Y2VsdWYzK3VxV1B5NkFrM2dsa2VzdERyeWRic0tWS0VHVmJTRTVPbmZIUW80bkE1SzhWQ1hIUy8zWDQyMGRhemFGVmhtZ3ZHOU1qeTZ1MTN0cmZNeHgzNlgwSUMybmkxN1RPSmtBeCtQSnYxZGcwdkJmbmhLTXcvelRLWklmTm5jTUpwVElwb2R5T3d4RFZmc1FYOEJ0OU04dkdrU1lLM2lvTnoxT2ZBRFBTU0NaT2ZVMXZuRG1YR2gyalJTajVCZm8wdFZ0ZlNTSDBlRmFqSE51WE04bXFXRHgwUmt5Y1JtWFo5MzB5clZsNU5GZEttVGRFbmxtOTcwanI4OWZ3TkhQdnZqaWxnc0RkY3NtR1VBQUtzblhhMGxCVU5nQmRZZHdRd2xESCsxSWF6ZFhCZHRaNm94eXJTckJyOXFrMWlaVzVUZXBWWFlEMnBCOThWL2dkdUwzZ2lNSmJQYnlUMVhiSHdDdWlHNmZYYnc0YWNnazIwTkNzSnl6c2ZnekpSTThFcGt1dmdSZ1V1V2VkSnY0NFp3NlpjL2VJNWpVUmFRek1PVTVJSFdnUEh6aXVUSmVpVnhQSWR0enJqZWc3UmpuQlZ0SFRhZEdJQUhjRXZKdlNBc29vaEE2WktlNGl3SmZqa05JYlc5L09XTGliK2NiUm9zLzkrbVFEeitkVEJOZGZCMzcvdkNtY0RkRjhNRTI0Y0wvelpBSGJMWHgyaUE3ekVzT2RVSCtKS0hTc21rclhQNWxTbHBEc3dMWUV1U28zZkQyVTFWT0lPRndobUh3TjRmdEptSzJvaDFZREt5NDZoOTJpMnhjQ2oyRFJyVS9nOXEzOEZMTHZVbUQxU2p2ck1jdnpKVUt5NzVveUZFV2hKWUR2YXlMMWE4QXBpREk4a1JxaW11MzQ2MjQ1K000Y05EQmJ1QTc3eEEvcVFnNDlhdEliY1ZQTlFBNnc1a1pRTS9YVG9DRVNRY2JGaUVYbjA5L01oVVRwWFVhSFBOS3QxUFJmejF1dGNmSUVPQUh1eTBVcXZvbmw0em1zR25YclpvUi9Ob29ZQUZWQ0ZwbkgyMUg5ODlteSttVHdrVTlEb2FNM3o1WjBnQmZ6Qmc5WHQ5NXEya0pGdCsyVFowYzIvaUVXbnN1ck12M0RxOEFDY1FZbXgxUlVhbGFUcFBpbzU0Q1E0dmdBK3ZlVUVlZkxTWGFWalRLbllKSDZ6YVhpQTBZNGpXQzNVUDU3aGc1M241L0NEWTFXTVNGYit6NlV2bmpWeHpMTG4zY0w2UmgzbWpqN2NoVDJxbWU5VlFhaklmOW12QzlvQzlYRXBHSEovRmRYd1dISHhoaElYMmVNSkh1MlZheDltdmNpc2hERFFnakJIQUdEai9LbXl6cXNxdHl1NmVaUXhiN0ZJT0F3YVRYTXBwd2dtM05lTEVLeERQdlhERThmK2xvOUFFeHUxR3NMSHFuVnlmcFZQMlZNVDdHbDV4eWdjMjlDK1JjN2VLR0dGYmZNK3FpcmYvcVlVNGVRSlo2ODJoMjhDMCtNQys4TnU1b1dZbzBTZk01Lys1VExQWFlEL0N2em9jL1FMM2I1QkVkWEhndkhIdDFnQTd0OFFYSTROYnNTMGpxR0w5QkwwbU51eEZBVlg4LzZyUUxmRzJLcEVNL0djNGVQbHdMWGJFcXhGMkFNUTg3WU9GOVc4QlJObmJ3ajhlTGNzRXBNN3pXUTdvYVFxVEI1UGE4YUFHdTMxZ29kSEVTcWdZMWN6S1g3dEgwYU1UaEV3R2ZrQzJ5SlFoR2tHcm5jRXcwazBCT0phT0VWRURJeG9pLytuQVdTTGVLS0F4N3dhcDl0b20xNHh5RXRkL0tIcExBQTZPQ2hEaGJGMVN1a2Q2QityVkxSWGpOSWRFZHBZblZiWGM0b0xiVVJpcTV3WmE2OUdzL0F4TjVZSEV5RUZvQkpYV1pPYUppdDU0bGExSFVaU0pUYm5obktqSWJyTGpHUC8xbURBWTlHeldaY0Fjcm5qdVFOWGV4UE12RVF4dVd3ZTdUaDFxbmNwYmF6WDVFZ1B1QUx0V2ZOSkdlQnVNOEVMUTFlTXZyL1JTd1JhRWxUZks4eTFiRDNsd3hpdnhHNnROZ2JJMXJaSGROMklxaVJtcWpFSldnYTEvK0Q0REM4YWdIdDlmQUE4OGdJOTVJVkNFTDZXVC9nZit4TXNPMU5PNVdOTnF6NHBndWQ2amRETnByamRkNTYrRDJIM1VhS1p1Tzgya0hkYWx5blNOVGtSb0h6Z2Q1L1RoZ1NPS3pXS0JtODRPczNtM1g2TXJSUTBERlhTMjdpTldSM0dBdk94bndQZFg0RmdldVpLOGJQKzlXdTk2N1JpZTM3RjVtVjE0UmhlZ3hvc0Nvc1N5WHVHbWE0QjNQMlRhdmJxOU1PaTJ0RmhDMmpTQTUvNkI0QnU2RGhiZWQ3L3F3QWh0UUtjYUlNeWZZa1hZakpxN2l0RlhnelFwbUNFa1V2RkhTV2dCajBnMGkwYU5IUThqVE5CVnhvcDhMZ25ITzlib0h0ZTZ0ekQ0SmdySllnOG9DeHcvMmZ4Sjdxdy9xN3JTR2R0RFBqeEVVdEN2a1hIdVl2M2VLb1ZVRjlwNlZzNmtmTU5SVHN6d2VVVkw2K1hFbTdsV2JxUVlJRHpZSHpCbkRyeG5Ba056TGRneXBuaFRYOEZxNytFdnZ1NlQwTTNRcFBCNDlTSVhybHdmZkdBZUxzREJla1hhK1JCMXptZWc5bkVVNUhFOFdzSUFDWnpVeVR5SUpzK3ZDV1FNQ21sY2xvUFpmTTc4YVVQZC9PbFl2dmxEK3dyL004STZ5L2ZpTHlTaXUzSVlmMGNEdlNJSThOdmxuTVZ3RWlTelZYS1gyWFNLc2daMDk2cGhyMXhsL1ZuRG9FWStEdFlHOUVzQld1UDRuelFKNzNtS0x4L3M1bHRNakxYV2UvT1ptZTE3SmJ0YlNBaHNkem4xU1p1VHJLNVR3cU82MS9LTkVlaERXSjBxUWJ2bFR4Tmp4bWU3MWRnM2xXK1N5bTZMZ2hlR2Z5YXV4eUVTNnRCL2hMWUFRQ0x6MHNMRGtRMEF2MXFKd1htOEZDWUdhNGIxdkpoRlBrRnY3RnNiSFFOWWRtYVdqeU80QlZPVURzT1pXbFU4cG9keFp3bmNOYldxbjdQMUtmL1ZuM3lWRUt4Z2dkU3hhdEZ5VGxwSHRHL0g2aUNrS1FsSlpPb3hHemJFQjNSMnBPUTd0VHdDUHMrTkFCZFR6WnA0T0V2WkI2S293cy9rWEF2MlBJb3pHV0YycWlnallVdmF1aXVDWHp2VXRmUGNPNXZ4TWVjcURoTmRWd2Z4SjNnVzhDbU5jdDA4ZU9wUHdQNlVRRlphRkt5bjJBS2RwQTlTazFCRm9ua3h2c3VuQ2lJMVpUZTV5bHB0cjlwSnhlU3pKMDVpc21ZaWR4UGlyQ3M4VFVnd0Q1N0YxK2IzbmpNajE4VGxWcDhjdkZFQklkQjJCOWI5ZG9tUzJES3dVTCtYRk1ObVhTSXU2TUtHckRnenhKcHVGdEFBREdyWFNWMjgvZ2lWaG5McFBmdWdCcXl4blBnMXQ4M1kybk5raUZnTEZzT1p1ZnZ0WVFOOWhjTFk2aWltZFhjY0RJbThubEdtUmJaUjNReHV3NmRYREx3ZDJlL3BrRFF0UVo2clBZRjlpWFZSUWxxN3FUVlZ6UFFKVEM1VisrRFBkcFZLTC9ZaU1ZbjhSRjdTVjlpd1NMcDBHR1F4TkJPWVdCMEVraGdWaGxSQUNzN3Y0OXFqYVA5VUN4Qk03Ym5VTUJTTjRLQ29MVnk4Q3BWVlhRTkJWWEVNazVvSTVraVY5UFFreXpLU1hqTzJhRTRaNWhWSlFCdHVKRW5ha1cyMHNPTUU4Z0sxSE04d3dBRW5ZOHU3dEtCQzVRV2NNK2VkK0tkTnFwVm9tTDE5WnQ3UnZQSy9JRDluNjVURmJVdTZnYVl5TGptNXdyWlpNbHMvRVVjeHJHL0krTnpiajE1akt2cXVZdjVVbktuQlVJSUw4d0NaWnVlNzNFVVIxQXZrclJTeGNnTnhhZG45NTJpMXlJNVU2SDhOY01pTXVocUxLdGdPcGI0OUU0cEhVZmxydVEzVVU2OVFZOVJCa3RoY1phM0pEWlRYZjVEdW1MNnJsUU9lMHNYdFppdElDOWNkeWZQTitQRlJOaU1QTCtmQmNYQXZicTNDeEhyZ0FaOS9USWp5cVRXTEpmbHQvcUR0bmsxdlBTbGdmYzV6YXFZK1FjM0YxL2srdit0YlhURmQwUklrODMxZS9uTDdHUXk3cmE5RHAvd3RwUWZBZGlUdUd2bVRMeW5Ta0szc0FNOU1kd3A5aE4xZXBPb3BMWFVkZnBTNmZJK1FIdDBqZ1RqSHlET2ZOT0RqNWpGZUdXUEwya1NrWmRUVFlTalhwN2I4UzVITmc4bWdiVUFpYkFieTM4MWxYaGtJakN0SkV0ay9zVVdVMTFrejYrZWswNmRVVG03Z1pYU0g2bnBZZXFmbE5qZmhjRlZWRmtoaVRvSUlPN0hUa24vdkdWQjk4WGNmKzZZVGE1QUtCbGwxMUtMZk1semdsakpDSFJnMG03R0drUlFMb0Z6WWdWOFVGSjJkS2o3V1lBaFBzQ0M4ZDUwMlpVOUxJU0xPQjNzMm95NjJ5dnpKUloxblFLSXJBdWtORWZQOGdNVDE3N3dlS1R1aXdNTUcxbVVMbXNWLytrYnBITUZTM0VscEtvdFhnODBFa3YrTXJmcFNFclNyVng4RHoxaURicDJpbUgwdVpHcEFFVDY0eC9QZzIxd01ERWM0bHpuRFlwWHQxU3B3K2pOUEpnV0ZBalZpV2FjREJuUTh3YXMvUW9ET0xQb3V4Q2FxM0tRNXRiNHJlekZCSVBYdHdpK1luT3B4MlVBclpscCtVaFZSODg4NHdrK2lISTQwLy9tRGV6dlp5bWRvU3VUWW00RlJFcWFITVpXaUFmdk9QNm9udlZBN1lBeHMwWkpMWUhXanlGS0VYN2hXdXNRcXdIT1BhbzBablEvOG1iNU5DcE9FY2p1S2poTDFyMXlXOEVCWGszZ3EzekxGVlo4dThPejg2bjZoRzhRN3FheGVlVVJlVXE1dTB1aDBxYmczWDdrYkFUbjZiZ25mVTZrWFJ4N1o1c3MyNzhxaFB6eURpN3VMdXV4bmRmRUNURWpDK0VlVGMwUnc3YWk2MW5LSXFEOVRCWkpKV2NDVVFOSngxUXZoYUlhMG54Q25iSy82R1ZWV1pKQXdrSlhGVStZV0FjYVRGd1JvaGw3bGJGaDQ2dE53TEJaTWxDTnUyeW4xQUpiTWdTc1J5UGtTdG83Z2lCeUE5UU1KSktlOW1qZHd4M3hYSlArSXh6ZndCWnd5VFFRZjliYlBlelRSS2JzR2g0Wis5UlVRTGozeVM1MlpqZ2swQnlKOCtzTHB1VG9sSWgzcVp0UWY0RTRzSGdiQnJZeThQK0lLSHZDTW53cituYnREcTZrdDhvTFNoSGtpYnBvUWE0bHcwZkF6WmZGYVM2Tm84YUJqSFg5RHdZUVFidGZzNUtrZmFKZWtqT0FLNjFEdG1oT2c5Tk9qYldwQWxiSmthcVZ5NmZVakFFWEczQXIzbkdJVzZBNGhXMXNDNS9tUDcrTG5DOG5JMWZyQ0lwdTZCdHVYSXBnUkhQb0FvdlpiNDhOL1lod0hNaHBNNUZVcE13ZDNZUm5oSFZhN1Q5MExTUGhqOE5KdjFNUEpxS0RjdjFrQmVDbUZMOEZVTzY1YkJZYytaRHMxSkM0ZU9NdlNodFZ1VWlCcGpndjN3Y2VuWEIvK1RwY3V1ZjVsWjdTb2xLMHVtTlhoUnpBUkR0dmlXcXhOQ25UekpIVlJ2REViMUJkYXdzKytyaWtwTWdjWXhFc01KNU9NTHhrdnByZURRWC9sSEFjSm9IZlFGc05SbXh4SDdxSW1wM0Mra1JBTkFDUTUxL1BYSmlOdVNtcHRIOFZWMkYxSHRXSUxZK1VCWWhrOERRUzc4OWlmOE1VakhyQzQzYm56bFhpMDQ1N2M5aTJHanN1NlhFMEwzcnY3TWp0OGhxOVEvVjEyRmhsRDJoeVRzd1JVZ293Nk4vME43N09aSzkyc09SWWNZNHpLZjcxS2h4YnFQS1JBcHNIcmZFQnlBWXd4YlNZUXYxOTF5d2NDb1QzOHR4bndLd25iL2g0VWltMjYxOEVHQW9sSDkySjFiQnFCaUl3a2ltMUJQbjZZWFpuWkZibFUxeUswSG1LWCsrSURFKzhUS0dXVm5zM2laL0JKeDJraGdBS0syblBwZ2RvaFZyc2FwVXNLQmpSYXNsN3Zic0pvNE93NWpCWjEvTnhUS0N5RmFiL3hvMnRjMWdzL3Nod245d3pqdHoxOEkzT0l1a05ZRmpkVXgxUEZmZG8wVmFvQ3JUbUVZMEgyZHJWbnQ1VjNrMmdhOVhQTDVGOWJ3MlNwN1p3cXRPdldvQlNQeUt3NVlOUjgvNloyUjd5djl3RXRVSWJGVk9jUll5ZmJucHVlWUlPSmpqVGUydURhUVhxL2c5M3g2NEo5bkVQWHFlejBCRm02SnVxMzBvV2dVbEF1NEZPQUJ1enZFPQ=="
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

    cur = os.path.abspath(sys.argv[0])
    try:
        with open(cur, "rb") as f:
            local = f.read()
    except Exception:
        return True
    if remote == local:
        return True

    txt = remote.decode("utf-8", "replace")
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
