from typing import List, Tuple, TypedDict
import json
from validators import url

class LogInfo(TypedDict):
    username: str
    password: str

type SignLoc = Tuple[bool, bool, bool, bool, bool]

class Vitri_ky_3tra(TypedDict):
    bacsi: SignLoc
    dieuduong: SignLoc

class Patient(TypedDict):
    url: str
    note: str
    ky_xetnghiem: bool
    ky_todieutri: bool
    vitri_ky_3tra: Vitri_ky_3tra

class Config(TypedDict):
    bacsi: LogInfo
    dieuduong: LogInfo
    patients: List[Patient]

def save(config: Config, filename="config.json"):
    res = {
        "bacsi": {
            "username": config["bacsi"]["username"],
            "password": config["bacsi"]["password"],
        },
        "dieuduong": {
            "username": config["dieuduong"]["username"],
            "password": config["dieuduong"]["password"],
        },
        "patients": [
            {
                "url": p["url"],
                "note": p["note"],
                "ky_xetnghiem": p["ky_xetnghiem"],
                "ky_todieutri": p["ky_todieutri"],
                "vitri_ky_3tra": {
                    "bacsi": p["vitri_ky_3tra"]["bacsi"],
                    "dieuduong": p["vitri_ky_3tra"]["dieuduong"],
                },
            }
            for p in config["patients"]
        ],
    }
    with open(filename, "w") as f:
        json.dump(res, f, indent=4)

def load(filename="config.json") -> Config:
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return {
            "bacsi": {
                "username": "",
                "password": "",
            },
            "dieuduong": {
                "username": "",
                "password": "",
            },
            "patients": [],
        }

def is_bs_valid(config: Config) -> bool:
    return (
        (len(config["bacsi"]["username"]) > 0)
        & (len(config["bacsi"]["password"]) > 0)
        & (len(config["patients"]) > 0)
        & (
            all(
                [
                    url(p["url"])
                    and ("chi-tiet-nguoi-benh-noi-tru/to-dieu-tri/" in p["url"])
                    for p in config["patients"]
                ]
            )
        )
    )

def is_dd_valid(config: Config) -> bool:
    return (
        (len(config["dieuduong"]["username"]) > 0)
        & (len(config["dieuduong"]["password"]) > 0)
        & (len(config["patients"]) > 0)
        & (
            all(
                [
                    url(p["url"])
                    and ("chi-tiet-nguoi-benh-noi-tru/to-dieu-tri/" in p["url"])
                    for p in config["patients"]
                ]
            )
        )
    )
