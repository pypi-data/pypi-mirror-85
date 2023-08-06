

import pathlib
from typing import Tuple
from typing import Union

import pandas as pd
from sqlalchemy.engine import Engine

from comexdown import fs


# ===================================READ==================================== #
def read(filepath: Union[pathlib.PurePath, str]) -> pd.DataFrame:
    df = pd.read_csv(
        filepath,
        sep=";",
        decimal=",",
        encoding="latin-1",
    )
    df = df.rename(columns={col: col.lower() for col in df.columns})
    return df


def get_pais(root: Union[pathlib.PurePath, str]) -> Tuple[pd.DataFrame]:
    pais_df = read(fs.path_aux(root, "pais"))
    pais_bloco_df = read(fs.path_aux(root, "pais_bloco"))
    pais_bloco_df = pais_bloco_df[
        pais_bloco_df["co_pais"].isin(pais_df["co_pais"])
    ]
    return pais_df, pais_bloco_df


def get_uf(
    root: Union[pathlib.PurePath, str],
    mun: bool = False,
) -> pd.DataFrame:
    uf = read(fs.path_aux(root, "uf"))
    if mun:
        uf_mun = read(fs.path_aux(root, "uf_mun"))
        uf = pd.merge(uf_mun, uf[["sg_uf", "co_uf"]], on="sg_uf")
        uf = uf.drop(columns=["sg_uf"])
    return uf


def get_sh(root: Union[pathlib.PurePath, str]) -> Tuple[pd.DataFrame]:
    sh = read(fs.path_aux(root, "sh"))
    ncm_secrom = sh[
        [
            "co_ncm_secrom",
            "no_sec_por",
            "no_sec_esp",
            "no_sec_ing",
        ]
    ].drop_duplicates()
    sh2 = sh[
        [
            "co_sh2",
            "no_sh2_por",
            "no_sh2_esp",
            "no_sh2_ing",
            "co_ncm_secrom",
        ]
    ].drop_duplicates()
    sh4 = sh[
        [
            "co_sh4",
            "no_sh4_por",
            "no_sh4_esp",
            "no_sh4_ing",
            "co_sh2",
            "co_ncm_secrom",
        ]
    ].drop_duplicates()
    sh6 = sh[
        [
            "co_sh6",
            "no_sh6_por",
            "no_sh6_esp",
            "no_sh6_ing",
            "co_sh4",
            "co_sh2",
            "co_ncm_secrom",
        ]
    ].drop_duplicates()
    return ncm_secrom, sh2, sh4, sh6


def convert_date(df: pd.DataFrame) -> pd.DataFrame:
    date = df[["co_ano", "co_mes"]].assign(day=1)
    date = date.rename(columns={"co_ano": "year", "co_mes": "month"})
    df = df.assign(data=pd.to_datetime(date))
    df = df.drop(columns=["co_ano", "co_mes"])
    return df


def get_trade(
    root: Union[pathlib.PurePath, str],
    direction: str,
    year: int,
    mun: bool = False,
) -> pd.DataFrame:
    filepath = fs.path_trade(
        root=root,
        direction=direction,
        year=year,
        mun=mun,
    )
    d = read(filepath)
    if mun:
        d = d.rename(columns={"sh4": "co_sh4"})
        d = d.drop(columns=["sg_uf_mun"])
    else:
        uf = get_uf(root)
        d = pd.merge(
            d,
            uf[["co_uf", "sg_uf"]],
            left_on="sg_uf_ncm",
            right_on="sg_uf",
        )
        d = d.drop(columns=["sg_uf_ncm", "sg_uf"])
    d = convert_date(d)
    return d


## ========================================================================= ##
# -----------------------------------INSERT---------------------------------- #
## ========================================================================= ##
def update(
    engine: Engine,
    df_table: pd.DataFrame,
    db_table: pd.DataFrame,
    table_name: str,
    key: str,
) -> None:
    new_table = df_table[~df_table[key].isin(db_table[key])]
    if len(new_table) > 0:
        new_table.to_sql(
            table_name,
            engine,
            index=False,
            if_exists="append",
        )


def insert_pais(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    pais_df, pais_bloco_df = get_pais(root)
    pais_df.to_sql(
        "pais",
        engine,
        index=False,
        if_exists="append",
    )
    pais_bloco_df.to_sql(
        "pais_bloco",
        engine,
        index=False,
        if_exists="append",
    )


def update_pais(engine, root):
    pais, pais_bloco = get_pais(root)
    db_pais = pd.read_sql_table("pais", engine)
    db_pais_bloco = pd.read_sql_table("pais_bloco", engine)
    update(
        engine=engine,
        df_table=pais_bloco,
        db_table=db_pais_bloco,
        table_name="pais_bloco",
        key="co_pais_bloco",
    )
    update(
        engine=engine,
        df_table=pais,
        db_table=db_pais,
        table_name="pais",
        key="co_pais",
    )


def insert_unidade(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "unidade"))
    df.to_sql("unidade", engine, index=False, if_exists="append")


def update_unidade(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_unidade = read(fs.path_aux(root, "unidade"))
    db_unidade = pd.read_sql_table("unidade", engine)
    update(
        engine=engine,
        df_table=df_unidade,
        db_table=db_unidade,
        table_name="unidade",
        key="co_unid",
    )


def insert_sh(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    ncm_secrom, sh2, sh4, sh6 = get_sh(root)
    ncm_secrom.to_sql(
        "ncm_secrom",
        engine,
        index=False,
        if_exists="append",
    )
    sh2.to_sql(
        "sh2",
        engine,
        index=False,
        if_exists="append",
    )
    sh4.to_sql(
        "sh4",
        engine,
        index=False,
        if_exists="append",
    )
    sh6.to_sql(
        "sh6",
        engine,
        index=False,
        if_exists="append",
    )


def update_sh(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_ncm_secrom, df_sh2, df_sh4, df_sh6 = get_sh(root)
    db_ncm_secrom = pd.read_sql_table("ncm_secrom", engine)
    db_sh2 = pd.read_sql_table("sh2", engine)
    db_sh4 = pd.read_sql_table("sh4", engine)
    db_sh6 = pd.read_sql_table("sh6", engine)
    update(
        engine=engine,
        df_table=df_ncm_secrom,
        db_table=db_ncm_secrom,
        table_name="ncm_secrom",
        key="co_ncm_secrom",
    )
    update(
        engine=engine,
        df_table=df_sh2,
        db_table=db_sh2,
        table_name="sh2",
        key="co_sh2",
    )
    update(
        engine=engine,
        df_table=df_sh4,
        db_table=db_sh4,
        table_name="sh4",
        key="co_sh4",
    )
    update(
        engine=engine,
        df_table=df_sh6,
        db_table=db_sh6,
        table_name="sh6",
        key="co_sh6",
    )


def insert_ppe(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "ppe"))
    df.to_sql("ppe", engine, index=False, if_exists="append")


def update_ppe(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_ppe = read(fs.path_aux(root, "ppe"))
    db_ppe = pd.read_sql_table("ppe", engine)
    update(
        engine=engine,
        df_table=df_ppe,
        db_table=db_ppe,
        table_name="ppe",
        key="co_ppe",
    )


def insert_ppi(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "ppi"))
    df.to_sql("ppi", engine, index=False, if_exists="append")


def update_ppi(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_ppi = read(fs.path_aux(root, "ppi"))
    db_ppi = pd.read_sql_table("ppi", engine)
    update(
        engine=engine,
        df_table=df_ppi,
        db_table=db_ppi,
        table_name="ppi",
        key="co_ppi",
    )


def insert_fat_agreg(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "fat_agreg"))
    df.to_sql("fat_agreg", engine, index=False, if_exists="append")


def update_fat_agreg(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_fat_agreg = read(fs.path_aux(root, "fat_agreg"))
    db_fat_agreg = pd.read_sql_table("fat_agreg", engine)
    update(
        engine=engine,
        df_table=df_fat_agreg,
        db_table=db_fat_agreg,
        table_name="fat_agreg",
        key="co_fat_agreg",
    )


def insert_cuci(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "cuci"))
    df.to_sql("cuci", engine, index=False, if_exists="append")


def update_cuci(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_cuci = read(fs.path_aux(root, "cuci"))
    db_cuci = pd.read_sql_table("cuci", engine)
    update(
        engine=engine,
        df_table=df_cuci,
        db_table=db_cuci,
        table_name="cuci",
        key="co_cuci_item",
    )


def insert_cgce(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "cgce"))
    df.to_sql("cgce", engine, index=False, if_exists="append")


def update_cgce(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_cgce = read(fs.path_aux(root, "cgce"))
    db_cgce = pd.read_sql_table("cgce", engine)
    update(
        engine=engine,
        df_table=df_cgce,
        db_table=db_cgce,
        table_name="cgce",
        key="co_cgce_n3",
    )


def insert_siit(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "siit"))
    df.to_sql("siit", engine, index=False, if_exists="append")


def update_siit(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_siit = read(fs.path_aux(root, "siit"))
    db_siit = pd.read_sql_table("siit", engine)
    update(
        engine=engine,
        df_table=df_siit,
        db_table=db_siit,
        table_name="siit",
        key="co_siit",
    )


def insert_isic(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "isic"))
    df.to_sql("isic", engine, index=False, if_exists="append")


def update_isic(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_isic = read(fs.path_aux(root, "isic"))
    db_isic = pd.read_sql_table("isic", engine)
    update(
        engine=engine,
        df_table=df_isic,
        db_table=db_isic,
        table_name="isic",
        key="co_isic_classe",
    )


def insert_grupo(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "grupo"))
    df.to_sql("grupo", engine, index=False, if_exists="append")


def update_grupo(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_grupo = read(fs.path_aux(root, "grupo"))
    db_grupo = pd.read_sql_table("grupo", engine)
    update(
        engine=engine,
        df_table=df_grupo,
        db_table=db_grupo,
        table_name="grupo",
        key="co_exp_subset",
    )


def insert_ncm(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "ncm"))
    df.to_sql("ncm", engine, index=False, if_exists="append")


def update_ncm(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_ncm = read(fs.path_aux(root, "ncm"))
    db_ncm = pd.read_sql_table("ncm", engine)
    update(
        engine=engine,
        df_table=df_ncm,
        db_table=db_ncm,
        table_name="ncm",
        key="co_ncm",
    )


def insert_uf(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "uf"))
    df.to_sql("uf", engine, index=False, if_exists="append")


def update_uf(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_uf = read(fs.path_aux(root, "uf"))
    db_uf = pd.read_sql_table("uf", engine)
    update(
        engine=engine,
        df_table=df_uf,
        db_table=db_uf,
        table_name="uf",
        key="co_uf",
    )


def insert_uf_mun(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    uf = read(fs.path_aux(root, "uf"))
    uf_mun = read(fs.path_aux(root, "uf_mun"))
    uf_data = pd.merge(uf_mun, uf[["sg_uf", "co_uf"]], on="sg_uf")
    uf_data = uf_data.drop(columns=["sg_uf"])
    uf_data.to_sql(
        "uf_mun",
        engine,
        index=False,
        if_exists="append",
    )


def update_uf_mun(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_uf_mun = read(fs.path_aux(root, "uf_mun"))
    db_uf_mun = pd.read_sql_table("uf_mun", engine)
    update(
        engine=engine,
        df_table=df_uf_mun,
        db_table=db_uf_mun,
        table_name="uf_mun",
        key="co_mun_geo",
    )


def insert_urf(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "urf"))
    df.to_sql("urf", engine, index=False, if_exists="append")


def update_urf(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_urf = read(fs.path_aux(root, "urf"))
    db_urf = pd.read_sql_table("urf", engine)
    update(
        engine=engine,
        df_table=df_urf,
        db_table=db_urf,
        table_name="urf",
        key="co_urf",
    )


def insert_via(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df = read(fs.path_aux(root, "via"))
    df.to_sql("via", engine, index=False, if_exists="append")


def update_via(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    df_via = read(fs.path_aux(root, "via"))
    db_via = pd.read_sql_table("via", engine)
    update(
        engine=engine,
        df_table=df_via,
        db_table=db_via,
        table_name="via",
        key="co_via",
    )


def insert_all(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    insert_pais(engine, root)
    insert_unidade(engine, root)
    insert_sh(engine, root)
    insert_ppe(engine, root)
    insert_ppi(engine, root)
    insert_fat_agreg(engine, root)
    insert_cuci(engine, root)
    insert_cgce(engine, root)
    insert_siit(engine, root)
    insert_isic(engine, root)
    insert_grupo(engine, root)
    insert_ncm(engine, root)
    insert_uf(engine, root)
    insert_uf_mun(engine, root)
    insert_urf(engine, root)
    insert_via(engine, root)


def update_all(engine: Engine, root: Union[pathlib.PurePath, str]) -> None:
    tablenames = (
        "pais",
        "unidade",
        "sh",
        "ppe",
        "ppi",
        "fat_agreg",
        "cuci",
        "cgce",
        "siit",
        "isic",
        "grupo",
        "ncm",
        "uf",
        "urf",
        "via",
    )
    update_pais(engine=engine, root=root)
    update_unidade(engine=engine, root=root)
    update_sh(engine=engine, root=root)
    update_ppe(engine=engine, root=root)
    update_ppi(engine=engine, root=root)
    update_fat_agreg(engine=engine, root=root)
    update_cuci(engine=engine, root=root)
    update_cgce(engine=engine, root=root)
    update_siit(engine=engine, root=root)
    update_isic(engine=engine, root=root)
    update_grupo(engine=engine, root=root)
    update_ncm(engine=engine, root=root)
    update_uf(engine=engine, root=root)
    update_urf(engine=engine, root=root)
    update_via(engine=engine, root=root)


def insert_trade(
    engine: Engine,
    root: Union[pathlib.PurePath, str],
    direction: str,
    year: int,
    mun: bool = False,
) -> None:
    if mun:
        d = get_trade(
            root=root,
            direction=direction,
            year=year,
            mun=True,
        )
        direction = direction + "_mun"
    else:
        d = get_trade(
            root=root,
            direction=direction,
            year=year,
            mun=False,
        )
    d.to_sql(
        name=direction,
        con=engine,
        index=False,
        if_exists="append",
        chunksize=1000,
    )
