from dataclasses import dataclass
from enum import Enum


class SchoolDistrict(Enum):
    SB = "sbstudents.org"
    MTS = "mtsdstudent.us"


@dataclass
class GenesisConfig:
    root: str
    email_suffix: str
    login: str
    auth: str
    main: str


sb_genesis_config = GenesisConfig(
    root="https://parents.sbschools.org/genesis",
    email_suffix="sbstudents.org",
    login="/sis/view?gohome=true",
    auth="/sis/j_security_check",
    main="/parents",
)

mt_genesis_config = GenesisConfig(
    root="https://parents.mtsd.k12.nj.us/genesis",
    email_suffix="mtsdstudent.us",
    login="/sis/view?gohome=true",
    auth="/sis/j_security_check",
    main="/parents",
)


def get_genesis_config(school_district: SchoolDistrict) -> GenesisConfig:
    if school_district == SchoolDistrict.SB:
        return sb_genesis_config
    elif school_district == SchoolDistrict.MTS:
        return mt_genesis_config
