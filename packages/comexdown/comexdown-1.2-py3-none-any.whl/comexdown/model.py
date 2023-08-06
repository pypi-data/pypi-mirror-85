from sqlalchemy import BigInteger, Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey


Base = declarative_base()


class Exp(Base):

    __tablename__ = "exp"

    co_exp = Column(Integer, primary_key=True)
    data = Column(Date, index=True)
    co_ncm = Column(Integer, ForeignKey("ncm.co_ncm"), index=True)
    ncm = relationship("Ncm")
    co_unid = Column(Integer, ForeignKey("unidade.co_unid"))
    unid = relationship("Unid")
    co_pais = Column(Integer, ForeignKey("pais.co_pais"), index=True)
    pais = relationship("Pais")
    co_uf = Column(Integer, ForeignKey("uf.co_uf"), index=True)
    uf = relationship("Uf")
    co_via = Column(Integer, ForeignKey("via.co_via"), index=True)
    via = relationship("Via")
    co_urf = Column(Integer, ForeignKey("urf.co_urf"))
    urf = relationship("Urf")
    qt_estat = Column(BigInteger)
    kg_liquido = Column(BigInteger)
    vl_fob = Column(BigInteger)


class Imp(Base):

    __tablename__ = "imp"

    co_imp = Column(Integer, primary_key=True)
    data = Column(Date, index=True)
    co_ncm = Column(Integer, ForeignKey("ncm.co_ncm"), index=True)
    ncm = relationship("Ncm")
    co_unid = Column(Integer, ForeignKey("unidade.co_unid"))
    unid = relationship("Unid")
    co_pais = Column(Integer, ForeignKey("pais.co_pais"), index=True)
    pais = relationship("Pais")
    co_uf = Column(Integer, ForeignKey("uf.co_uf"), index=True)
    uf = relationship("Uf")
    co_via = Column(Integer, ForeignKey("via.co_via"), index=True)
    via = relationship("Via")
    co_urf = Column(Integer, ForeignKey("urf.co_urf"))
    urf = relationship("Urf")
    qt_estat = Column(BigInteger)
    kg_liquido = Column(BigInteger)
    vl_fob = Column(BigInteger)


class ExpMun(Base):

    __tablename__ = "exp_mun"

    co_exp_mun = Column(Integer, primary_key=True)
    data = Column(Date, index=True)
    co_sh4 = Column(Integer, ForeignKey("sh4.co_sh4"), index=True)
    sh4 = relationship("Sh4")
    co_pais = Column(Integer, ForeignKey("pais.co_pais"), index=True)
    pais = relationship("Pais")
    co_mun = Column(Integer, ForeignKey("uf_mun.co_mun_geo"), index=True)
    mun = relationship("UfMun")
    kg_liquido = Column(BigInteger)
    vl_fob = Column(BigInteger)


class ImpMun(Base):

    __tablename__ = "imp_mun"

    co_imp_mun = Column(Integer, primary_key=True)
    data = Column(Date, index=True)
    co_sh4 = Column(Integer, ForeignKey("sh4.co_sh4"), index=True)
    sh4 = relationship("Sh4")
    co_pais = Column(Integer, ForeignKey("pais.co_pais"), index=True)
    pais = relationship("Pais")
    co_mun = Column(Integer, ForeignKey("uf_mun.co_mun_geo"), index=True)
    mun = relationship("UfMun")
    kg_liquido = Column(BigInteger)
    vl_fob = Column(BigInteger)


class Ncm(Base):

    __tablename__ = "ncm"

    co_ncm = Column(Integer, primary_key=True, autoincrement=False, index=True)
    co_unid = Column(Integer, ForeignKey("unidade.co_unid"))
    unid = relationship("Unid")
    co_sh6 = Column(Integer, ForeignKey("sh6.co_sh6"))
    sh6 = relationship("Sh6")
    co_ppe = Column(Integer, ForeignKey("ppe.co_ppe"))
    ppe = relationship("Ppe")
    co_ppi = Column(Integer, ForeignKey("ppi.co_ppi"))
    ppi = relationship("Ppi")
    co_fat_agreg = Column(Integer, ForeignKey("fat_agreg.co_fat_agreg"))
    fat_agreg = relationship("FatAgreg")
    co_cuci_item = Column(String(5), ForeignKey("cuci.co_cuci_item"))
    cuci_item = relationship("Cuci")
    co_cgce_n3 = Column(Integer, ForeignKey("cgce.co_cgce_n3"))
    cgce_n3 = relationship("Cgce")
    co_siit = Column(Integer, ForeignKey("siit.co_siit"))
    siit = relationship("Siit")
    co_isic_classe = Column(Integer, ForeignKey("isic.co_isic_classe"))
    isic_classe = relationship("Isic")
    co_exp_subset = Column(Integer, ForeignKey("grupo.co_exp_subset"))
    exp_subset = relationship("Grupo")
    no_ncm_por = Column(String(1024), index=True)
    no_ncm_esp = Column(String(1024), index=True)
    no_ncm_ing = Column(String(1024), index=True)


class Unid(Base):

    __tablename__ = "unidade"

    co_unid = Column(Integer, primary_key=True, autoincrement=False)
    no_unid = Column(String(1024))
    sg_unid = Column(String(256))


class Pais(Base):

    __tablename__ = "pais"

    co_pais = Column(Integer, primary_key=True, autoincrement=False)
    co_pais_ison3 = Column(Integer)
    co_pais_isoa3 = Column(String(3))
    no_pais = Column(String(1024))
    no_pais_ing = Column(String(1024))
    no_pais_esp = Column(String(1024))


class PaisBloco(Base):

    __tablename__ = "pais_bloco"

    co_pais_bloco = Column(Integer, primary_key=True)
    co_pais = Column(Integer, ForeignKey("pais.co_pais"))
    pais = relationship("Pais")
    co_bloco = Column(Integer)
    no_bloco = Column(String(1024))
    no_bloco_ing = Column(String(1024))
    no_bloco_esp = Column(String(1024))


class Uf(Base):

    __tablename__ = "uf"

    co_uf = Column(Integer, primary_key=True, autoincrement=False)
    sg_uf = Column(String(2))
    no_uf = Column(String(32))
    no_regiao = Column(String(32))


class UfMun(Base):

    __tablename__ = "uf_mun"

    co_mun_geo = Column(Integer, primary_key=True, autoincrement=False, index=True)
    no_mun = Column(String(256), index=True)
    no_mun_min = Column(String(256), index=True)
    co_uf = Column(Integer, ForeignKey("uf.co_uf"))
    uf = relationship("Uf")


class Via(Base):

    __tablename__ = "via"

    co_via = Column(Integer, primary_key=True, autoincrement=False)
    no_via = Column(String(128))


class Urf(Base):

    __tablename__ = "urf"

    co_urf = Column(Integer, primary_key=True, autoincrement=False)
    no_urf = Column(String(128))


class Sh6(Base):

    __tablename__ = "sh6"

    co_sh6 = Column(Integer, primary_key=True, autoincrement=False, index=True)
    no_sh6_por = Column(String(1024), index=True)
    no_sh6_esp = Column(String(1024), index=True)
    no_sh6_ing = Column(String(1024), index=True)
    co_sh4 = Column(Integer, ForeignKey("sh4.co_sh4"))
    sh4 = relationship("Sh4")
    co_sh2 = Column(Integer, ForeignKey("sh2.co_sh2"))
    sh2 = relationship("Sh2")
    co_ncm_secrom = Column(String(5), ForeignKey("ncm_secrom.co_ncm_secrom"))
    ncm_secrom = relationship("NcmSecRom")


class Sh4(Base):

    __tablename__ = "sh4"

    co_sh4 = Column(Integer, primary_key=True, autoincrement=False, index=True)
    no_sh4_por = Column(String(1024))
    no_sh4_esp = Column(String(1024))
    no_sh4_ing = Column(String(1024))
    co_sh2 = Column(Integer, ForeignKey("sh2.co_sh2"))
    sh2 = relationship("Sh2")
    co_ncm_secrom = Column(String(5), ForeignKey("ncm_secrom.co_ncm_secrom"))
    ncm_secrom = relationship("NcmSecRom")


class Sh2(Base):

    __tablename__ = "sh2"

    co_sh2 = Column(Integer, primary_key=True, autoincrement=False, index=True)
    no_sh2_por = Column(String(1024))
    no_sh2_esp = Column(String(1024))
    no_sh2_ing = Column(String(1024))
    co_ncm_secrom = Column(String(5), ForeignKey("ncm_secrom.co_ncm_secrom"))
    ncm_secrom = relationship("NcmSecRom")


class NcmSecRom(Base):

    __tablename__ = "ncm_secrom"

    co_ncm_secrom = Column(String(5), primary_key=True, autoincrement=False, index=True)
    no_sec_por = Column(String(1024))
    no_sec_esp = Column(String(1024))
    no_sec_ing = Column(String(1024))


class Ppe(Base):

    __tablename__ = "ppe"

    co_ppe = Column(Integer, primary_key=True, autoincrement=False)
    no_ppe = Column(String(1024))
    no_ppe_min = Column(String(1024))
    no_ppe_ing = Column(String(1024))


class Ppi(Base):

    __tablename__ = "ppi"

    co_ppi = Column(Integer, primary_key=True, autoincrement=False)
    no_ppi = Column(String(1024))
    no_ppi_min = Column(String(1024))
    no_ppi_ing = Column(String(1024))


class FatAgreg(Base):

    __tablename__ = "fat_agreg"

    co_fat_agreg = Column(Integer, primary_key=True, autoincrement=False)
    no_fat_agreg = Column(String(128))
    no_fat_agreg_gp = Column(String(128))


class Cuci(Base):

    __tablename__ = "cuci"

    co_cuci_item = Column(String(5), primary_key=True, autoincrement=False)
    no_cuci_item = Column(String(1024))
    co_cuci_sub = Column(Integer)
    no_cuci_sub = Column(String(1024))
    co_cuci_grupo = Column(String(5))
    no_cuci_grupo = Column(String(1024))
    co_cuci_divisao = Column(Integer)
    no_cuci_divisao = Column(String(1024))
    co_cuci_sec = Column(Integer)
    no_cuci_sec = Column(String(1024))


class Cgce(Base):

    __tablename__ = "cgce"

    co_cgce_n3 = Column(Integer, primary_key=True, autoincrement=False)
    no_cgce_n3 = Column(String(128))
    no_cgce_n3_ing = Column(String(128))
    no_cgce_n3_esp = Column(String(128))
    co_cgce_n2 = Column(Integer)
    no_cgce_n2 = Column(String(128))
    no_cgce_n2_ing = Column(String(128))
    no_cgce_n2_esp = Column(String(128))
    co_cgce_n1 = Column(Integer)
    no_cgce_n1 = Column(String(128))
    no_cgce_n1_ing = Column(String(128))
    no_cgce_n1_esp = Column(String(128))


class Siit(Base):

    __tablename__ = "siit"

    co_siit = Column(Integer, primary_key=True, autoincrement=False)
    no_siit = Column(String(128))


class Isic(Base):

    __tablename__ = "isic"

    co_isic_classe = Column(Integer, primary_key=True, autoincrement=False)
    no_isic_classe = Column(String(1024))
    no_isic_classe_ing = Column(String(1024))
    no_isic_classe_esp = Column(String(1024))
    co_isic_grupo = Column(Integer)
    no_isic_grupo = Column(String(1024))
    no_isic_grupo_ing = Column(String(1024))
    no_isic_grupo_esp = Column(String(1024))
    co_isic_divisao = Column(Integer)
    no_isic_divisao = Column(String(1024))
    no_isic_divisao_ing = Column(String(1024))
    no_isic_divisao_esp = Column(String(1024))
    co_isic_secao = Column(String(1))
    no_isic_secao = Column(String(1024))
    no_isic_secao_ing = Column(String(1024))
    no_isic_secao_esp = Column(String(1024))


class Grupo(Base):

    __tablename__ = "grupo"

    co_exp_subset = Column(Integer, primary_key=True, autoincrement=False)
    no_exp_subset_por = Column(String(128))
    no_exp_subset_esp = Column(String(128))
    no_exp_subset_ing = Column(String(128))
    co_exp_set = Column(Integer)
    no_exp_set = Column(String(128))
    no_exp_set_esp = Column(String(128))
    no_exp_set_ing = Column(String(128))


def create_schema(engine) -> None:
    Base.metadata.create_all(engine)
