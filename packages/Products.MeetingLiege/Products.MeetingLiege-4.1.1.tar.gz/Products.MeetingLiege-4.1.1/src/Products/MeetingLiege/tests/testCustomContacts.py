# -*- coding: utf-8 -*-

from collective.contact.plonegroup.utils import get_own_organization
from collective.contact.plonegroup.utils import get_plone_groups
from OFS.ObjectManager import BeforeDeleteException
from Products.MeetingLiege.tests.MeetingLiegeTestCase import MeetingLiegeTestCase


class testCustomContacts(MeetingLiegeTestCase):
    ''' '''

    def test_OrgNotRemovableIfUsed(self):
        """An organization may not be removed if used in :
           - MeetingConfig.archivingRefs."""
        self.changeUser('siteadmin')
        cfg = self.meetingConfig
        own_org = get_own_organization()

        # create a new organization so it is used nowhere
        new_org = self.create('organization', id='new_org', title=u'New org', acronym='NO1')
        new_org_id = new_org.getId()
        new_org_uid = new_org.UID()
        cfg.setUseGroupsAsCategories(False)
        self._select_organization(new_org_uid)
        self.assertTrue(new_org_uid in cfg.listActiveOrgsForArchivingRefs())
        cfg.setArchivingRefs((
            {'active': '1',
             'restrict_to_groups': [new_org_uid, ],
             'row_id': '1',
             'code': '1',
             'label': "1"},
            {'active': '1',
             'restrict_to_groups': [],
             'row_id': '2',
             'code': '2',
             'label': '2'},))
        self._select_organization(new_org_uid, remove=True)

        with self.assertRaises(BeforeDeleteException) as cm:
            own_org.manage_delObjects([new_org_id])
        self.assertEquals(cm.exception.message, 'can_not_delete_meetinggroup_archivingrefs')
        cfg.setArchivingRefs((
            {'active': '1',
             'restrict_to_groups': [],
             'row_id': '1',
             'code': '1',
             'label': "1"},
            {'active': '1',
             'restrict_to_groups': [],
             'row_id': '2',
             'code': '2',
             'label': '2'},))

        # now it is removable
        own_org.manage_delObjects([new_org_id, ])
        self.assertIsNone(own_org.get(new_org_id, None))

    def test_ExtraSuffixesForFinanceOrgs(self):
        """Finances related organizations get extra suffixes."""
        self.changeUser('admin')
        self._createFinanceGroups()
        vendorsPloneGroupIds = get_plone_groups(self.vendors_uid, ids_only=True)
        vendorsPloneGroupIds.sort()
        self.assertEqual(vendorsPloneGroupIds,
                         ['{0}_administrativereviewers'.format(self.vendors_uid),
                          '{0}_advisers'.format(self.vendors_uid),
                          '{0}_creators'.format(self.vendors_uid),
                          '{0}_incopy'.format(self.vendors_uid),
                          '{0}_internalreviewers'.format(self.vendors_uid),
                          '{0}_observers'.format(self.vendors_uid),
                          '{0}_prereviewers'.format(self.vendors_uid),
                          '{0}_reviewers'.format(self.vendors_uid)])
        financial_group_uids = self.tool.financialGroupUids()
        financeGroupUID = financial_group_uids[0]
        financePloneGroupIds = get_plone_groups(financeGroupUID, ids_only=True)
        financePloneGroupIds.sort()
        self.assertEqual(financePloneGroupIds,
                         ['{0}_administrativereviewers'.format(financeGroupUID),
                          '{0}_advisers'.format(financeGroupUID),
                          '{0}_creators'.format(financeGroupUID),
                          '{0}_financialcontrollers'.format(financeGroupUID),
                          '{0}_financialmanagers'.format(financeGroupUID),
                          '{0}_financialreviewers'.format(financeGroupUID),
                          '{0}_incopy'.format(financeGroupUID),
                          '{0}_internalreviewers'.format(financeGroupUID),
                          '{0}_observers'.format(financeGroupUID),
                          '{0}_prereviewers'.format(financeGroupUID),
                          '{0}_reviewers'.format(financeGroupUID)])
