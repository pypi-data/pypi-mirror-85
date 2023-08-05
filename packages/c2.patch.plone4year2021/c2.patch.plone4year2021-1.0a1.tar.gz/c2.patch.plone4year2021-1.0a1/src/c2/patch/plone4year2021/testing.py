# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import c2.patch.plone4year2021


class C2PatchPlone4Year2021Layer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=c2.patch.plone4year2021)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "c2.patch.plone4year2021:default")


C2_PATCH_PLONE4YEAR2021_FIXTURE = C2PatchPlone4Year2021Layer()


C2_PATCH_PLONE4YEAR2021_INTEGRATION_TESTING = IntegrationTesting(
    bases=(C2_PATCH_PLONE4YEAR2021_FIXTURE,),
    name="C2PatchPlone4Year2021Layer:IntegrationTesting",
)


C2_PATCH_PLONE4YEAR2021_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(C2_PATCH_PLONE4YEAR2021_FIXTURE,),
    name="C2PatchPlone4Year2021Layer:FunctionalTesting",
)


C2_PATCH_PLONE4YEAR2021_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        C2_PATCH_PLONE4YEAR2021_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="C2PatchPlone4Year2021Layer:AcceptanceTesting",
)
