# Copyright (C) 2017-2020  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

"""SWH's deposit api URL Configuration

"""

from django.conf.urls import url
from django.shortcuts import render

from ..config import COL_IRI, CONT_FILE_IRI, EDIT_SE_IRI, EM_IRI, SD_IRI, STATE_IRI
from .deposit import APIPostDeposit
from .deposit_content import APIContent
from .deposit_status import APIStatus
from .deposit_update import APIUpdateArchive, APIUpdateMetadata
from .service_document import APIServiceDocument


def api_view(req):
    return render(req, "api.html")


# PUBLIC API
urlpatterns = [
    # simple view on the api
    url(r"^$", api_view, name="api"),
    # SD IRI - Service Document IRI
    # -> GET
    url(r"^servicedocument/", APIServiceDocument.as_view(), name=SD_IRI),
    # Col IRI - Collection IRI
    # -> POST
    url(r"^(?P<collection_name>[^/]+)/$", APIPostDeposit.as_view(), name=COL_IRI),
    # EM IRI - Atom Edit Media IRI (update archive IRI)
    # -> PUT (update-in-place existing archive)
    # -> POST (add new archive)
    url(
        r"^(?P<collection_name>[^/]+)/(?P<deposit_id>[^/]+)/media/$",
        APIUpdateArchive.as_view(),
        name=EM_IRI,
    ),
    # Edit IRI - Atom Entry Edit IRI (update metadata IRI)
    # SE IRI - Sword Edit IRI ;; possibly same as Edit IRI
    # -> PUT (update in place)
    # -> POST (add new metadata)
    url(
        r"^(?P<collection_name>[^/]+)/(?P<deposit_id>[^/]+)/metadata/$",
        APIUpdateMetadata.as_view(),
        name=EDIT_SE_IRI,
    ),
    # State IRI
    # -> GET
    url(
        r"^(?P<collection_name>[^/]+)/(?P<deposit_id>[^/]+)/status/$",
        APIStatus.as_view(),
        name=STATE_IRI,
    ),
    # Cont/File IRI
    # -> GET
    url(
        r"^(?P<collection_name>[^/]+)/(?P<deposit_id>[^/]+)/content/$",
        APIContent.as_view(),
        name=CONT_FILE_IRI,
    ),  # specification is not clear about
    # FILE-IRI, we assume it's the same as
    # the CONT-IRI one
]
