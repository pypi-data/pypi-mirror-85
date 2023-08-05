import sys
from nomad.metainfo import Environment
from nomad.metainfo.legacy import LegacyMetainfoEnvironment
import mpesparser.metainfo.mpes
import nomad.datamodel.metainfo.general
import nomad.datamodel.metainfo.common_experimental

m_env = LegacyMetainfoEnvironment()
m_env.m_add_sub_section(Environment.packages, sys.modules['mpesparser.metainfo.mpes'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.general'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.common_experimental'].m_package)  # type: ignore
