from tarfile import TarFile
from unittest.mock import MagicMock


def create_tarfile_mock(*members):
    members_mock = []
    for member in members:
        m = MagicMock()
        m.name = member
        members_mock.append(m)

    bundle_mock = MagicMock(spec=TarFile)
    bundle_mock.getmembers.return_value = members_mock

    return bundle_mock
