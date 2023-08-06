import sys
from nomad.metainfo import Environment
from nomad.metainfo.legacy import LegacyMetainfoEnvironment
import aptfimparser.metainfo.aptfim
import nomad.datamodel.metainfo.general
import nomad.datamodel.metainfo.common_experimental

m_env = LegacyMetainfoEnvironment()
m_env.m_add_sub_section(Environment.packages, sys.modules['aptfimparser.metainfo.aptfim'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.general'].m_package)  # type: ignore
m_env.m_add_sub_section(Environment.packages, sys.modules['nomad.datamodel.metainfo.common_experimental'].m_package)  # type: ignore
