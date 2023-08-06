import enum

from fibrenest_db_models.common import *
from sqlalchemy.dialects.postgresql import INET, MACADDR
from sqlalchemy import Text, text, BigInteger, Index


class ONTSwapType(enum.Enum):
    old_to_new = 'old_to_new'
    old_to_old = 'old_to_old'
    new_to_new = 'new_to_new'


class ONTSwapStatus(enum.Enum):
    pending = 'pending'
    started = 'started'
    success = 'success'
    failed = 'failed'


class NotificationSendType(enum.Enum):
    task_registered = 'task_registered'
    task_success = 'task_success'
    task_failed = 'task_failed'


class ONT(Base):
    __tablename__ = 'ont'

    id = Column(Integer, primary_key=True)
    sn = Column(String(length=64), nullable=False, unique=True)
    portid = Column(Integer, nullable=False)
    slotid = Column(Integer, nullable=False)
    frameid = Column(Integer, nullable=False)
    ontid = Column(Integer)
    model = Column(String(length=64))
    netbox_siteid = Column(Integer)
    olt_ip = Column(INET, nullable=False)
    sitename = Column(String(length=256))
    ont_registered = Column(Boolean, nullable=False, default=False, comment='If the ONT is registered on the OLT or not')
    ont_register_datetime = Column(DateTime)
    prov_type = Column(Enum(CPEProvTypeENUM), comment='Provisioning type of the ONT. Valid values: bridge or gateway')
    s_vlan = Column(Integer)
    c_vlan = Column(Integer)

    subscription = relationship('SUBSCRIPTION', back_populates='ont')

    def __repr__(self):
        return repr(self)


class RADACCT(Base):
    __tablename__ = 'radacct'
    __table_args__ = (
        Index('radacct_bulk_close', 'nasipaddress', 'acctstarttime'),
        Index('radacct_start_user_idx', 'acctstarttime', 'username')
    )

    radacctid = Column(BigInteger, primary_key=True, server_default=text("nextval('radacct_radacctid_seq'::regclass)"))
    acctsessionid = Column(Text, nullable=False)
    acctuniqueid = Column(Text, nullable=False, unique=True)
    username = Column(Text)
    realm = Column(Text)
    nasipaddress = Column(INET, nullable=False)
    nasportid = Column(Text)
    nasporttype = Column(Text)
    acctstarttime = Column(DateTime(True))
    acctupdatetime = Column(DateTime(True))
    acctstoptime = Column(DateTime(True))
    acctinterval = Column(BigInteger)
    acctsessiontime = Column(BigInteger)
    acctauthentic = Column(Text)
    connectinfo_start = Column(Text)
    connectinfo_stop = Column(Text)
    acctinputoctets = Column(BigInteger)
    acctoutputoctets = Column(BigInteger)
    calledstationid = Column(Text)
    callingstationid = Column(Text)
    acctterminatecause = Column(Text)
    servicetype = Column(Text)
    framedprotocol = Column(Text)
    framedipaddress = Column(INET)
    qos_profile = Column(Text)
    framedipv6address = Column(INET)
    delegatedipv6prefix = Column(INET)
    acctipv6inputoctets = Column(BigInteger)
    acctipv6outputoctets = Column(BigInteger)
    cpe_mac = Column(MACADDR)
    user_group = Column(Text)

    def __repr__(self):
        return repr(self)


class ONTSWAP(Base):
    __tablename__ = 'ont_swaps'

    id = Column(Integer, primary_key=True)
    swap_type = Column(Enum(ONTSwapType), nullable=False, comment='Type of ont swap')
    swap_status = Column(Enum(ONTSwapStatus), default='pending')
    old_sn = Column(String(length=64), nullable=False, comment='OLD ONT SN')
    new_sn = Column(String(length=64), nullable=False, comment='NEW ONT SN')
    old_portid = Column(Integer, nullable=False)
    old_slotid = Column(Integer, nullable=False)
    old_frameid = Column(Integer, nullable=False)
    old_ontid = Column(Integer, nullable=False)
    old_siteid = Column(Integer, nullable=False)
    old_olt_ip = Column(INET, nullable=False)
    old_sitename = Column(String(length=256), nullable=False)
    old_ucr = Column(String(length=64), nullable=False)
    old_ont_register_datetime = Column(DateTime)
    old_ont_expunged = Column(Boolean)
    old_ont_expunge_datetime = Column(DateTime)
    new_db_record_created = Column(Boolean)
    new_db_record_created_datetime = Column(DateTime)
    user = Column(String(length=256), nullable=False, comment='user who requested the swap')
    task_request_datetime = Column(DateTime)
    task_finish_datetime = Column(DateTime)
    notification_sent_type = Column(Enum(NotificationSendType))
    notification_sent_datetime = Column(DateTime)
    error = Column(String(length=256))

    def __repr__(self):
        return repr(self)
