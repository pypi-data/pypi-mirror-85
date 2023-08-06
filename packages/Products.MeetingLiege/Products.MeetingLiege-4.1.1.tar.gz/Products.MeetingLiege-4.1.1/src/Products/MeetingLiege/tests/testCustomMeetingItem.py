# -*- coding: utf-8 -*-

from DateTime import DateTime
from datetime import datetime
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import createContentInContainer
from plone.indexer.wrapper import IndexableObjectWrapper
from Products.MeetingLiege.config import COUNCILITEM_DECISIONEND_SENTENCE
from Products.MeetingLiege.config import FINANCE_ADVICE_LEGAL_TEXT
from Products.MeetingLiege.config import FINANCE_ADVICE_LEGAL_TEXT_NOT_GIVEN
from Products.MeetingLiege.config import FINANCE_ADVICE_LEGAL_TEXT_PRE
from Products.MeetingLiege.config import TREASURY_GROUP_ID
from Products.MeetingLiege.setuphandlers import _configureCollegeCustomAdvisers
from Products.MeetingLiege.tests.MeetingLiegeTestCase import MeetingLiegeTestCase
from Products.PloneMeeting.utils import org_id_to_uid
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


class testCustomMeetingItem(MeetingLiegeTestCase):
    """
        Tests the MeetingItem adapted methods
    """

    def test_InitFieldsWhenItemSentToCouncil(self):
        '''When an item is sent from College to Council, fields 'title' and 'privacy'
           are initialized from what is defined on the College item.'''
        # create a college item
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        item.setLabelForCouncil('<p>My label for council</p>')
        # before we used field 'privacyForCouncil' to init privacy on Council item
        # now use the field MeetingItem.otherMeetingConfigsClonableToPrivacy
        item.setOtherMeetingConfigsClonableToPrivacy((self.meetingConfig2.getId(), ))
        # make item sendable to council
        item.setOtherMeetingConfigsClonableTo('meeting-config-council')
        # send the item to the council
        meeting = self.create('Meeting', date=DateTime('2014/01/01'))
        self.presentItem(item)
        self.closeMeeting(meeting)
        # the item has been sent, get it and test that relevant fields are correctly initialized
        newItem = item.getBRefs('ItemPredecessor')[0]
        self.assertEqual(newItem.getPredecessor().UID(), item.UID())
        self.assertEqual(newItem.getLabelForCouncil(), '<p>My label for council</p>')
        self.assertEqual(newItem.getPrivacy(), 'secret')

    def test_FieldsKeptWhenItemSentToCouncil(self):
        '''When an item is sent from College to Council, following fields are kept :
           - labelForCouncil;
           - financeAdvice;
           - decisionSuite;
           - decisionEnd;
           - toDiscuss.
        '''
        # create a college item
        self.changeUser('pmManager')
        item = self.create('MeetingItem')

        # make item sendable to Council when 'itemcreated'
        cfg = self.meetingConfig
        usedItemAttrs = cfg.getUsedItemAttributes()
        if 'decisionSuite' not in usedItemAttrs:
            cfg.setUsedItemAttributes(usedItemAttrs + ('decisionSuite', ))
        cfg2 = self.meetingConfig2
        usedItemAttrs2 = cfg2.getUsedItemAttributes()
        if 'decisionSuite' not in usedItemAttrs2:
            cfg2.setUsedItemAttributes(usedItemAttrs2 + ('decisionSuite', ))
        cfg2Id = cfg2.getId()
        cfg.setItemManualSentToOtherMCStates(self._initial_state(item))
        cfg.setToDiscussSetOnItemInsert(False)
        cfg.setToDiscussDefault(True)
        cfg2.setToDiscussSetOnItemInsert(False)

        # create a college item
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        item.setOtherMeetingConfigsClonableTo((cfg2Id, ))

        item.setLabelForCouncil('<p>My label for council</p>')
        item.setOtherMeetingConfigsClonableTo('meeting-config-council')
        item.setDecisionSuite('<p>My decision suite</p>')
        item.setDecisionEnd('<p>My decision end</p>')
        item.setToDiscuss(False)
        # send College item to Council and compare
        new_item = item.cloneToOtherMeetingConfig(cfg2Id)
        self.assertEqual(new_item.portal_type, 'MeetingItemCouncil')
        self.assertEqual(item.getLabelForCouncil(),
                         new_item.getLabelForCouncil())
        self.assertEqual(item.getDecisionSuite(),
                         new_item.getDecisionSuite())
        self.assertEqual(item.getDecisionEnd(),
                         new_item.getDecisionEnd())
        self.assertEqual(item.getToDiscuss(),
                         new_item.getToDiscuss())

    def test_FinanceAdviceAskedDependingOnFinanceAdviceField(self):
        '''Finance advice is asked depending on MeetingItem.financeAdvice selected value.'''
        # create finance groups
        self.changeUser('admin')
        self._createFinanceGroups()
        _configureCollegeCustomAdvisers(self.portal)
        self.changeUser('pmManager')
        # create an item with relevant adviceFinance
        item = self.create('MeetingItem')
        # by default, no adviceFinance asked
        self.assertEqual(item.getFinanceAdvice(), '_none_')
        item._update_after_edit()
        self.assertEqual(item.adviceIndex, {})
        # ask finance advice
        financial_group_uids = self.tool.financialGroupUids()
        item.setFinanceAdvice(financial_group_uids[0])
        item._update_after_edit()
        self.assertTrue(financial_group_uids[0] in item.adviceIndex)
        self.assertEqual(len(item.adviceIndex), 1)
        # now ask another advice finance
        item.setFinanceAdvice(financial_group_uids[1])
        item._update_after_edit()
        self.assertTrue(financial_group_uids[1] in item.adviceIndex)
        self.assertEqual(len(item.adviceIndex), 1)

    def test_ItemReference(self):
        '''Test item reference generation. It uses CustomMeeting.getItemNumsForActe.'''
        # use categories
        self.changeUser('siteadmin')
        cfg = self.meetingConfig
        self.create('meetingcategory',
                    id='maintenance',
                    title='Maintenance',
                    category_id='maintenance_cat_id')
        cfg.setUseGroupsAsCategories(False)
        cfg.setInsertingMethodsOnAddItem((
            {'insertingMethod': 'on_list_type', 'reverse': '0'},
            {'insertingMethod': 'on_categories', 'reverse': '0'}))
        cfg.setItemReferenceFormat('python: here.adapted().getItemRefForActe()')

        self.changeUser('pmManager')
        # remove recurring items
        self._removeConfigObjectsFor(cfg)
        # create 5 items using different categories and insert it in a meeting
        resItem1 = self.create('MeetingItem')
        resItem1.setCategory('research')
        resItem2 = self.create('MeetingItem')
        resItem2.setCategory('research')
        # use proposingGroup 'vendors' so it is not viewable by 'pmCreator1'
        devItem1 = self.create('MeetingItem', proposingGroup=self.vendors_uid)
        devItem1.setCategory('development')
        devItem2 = self.create('MeetingItem')
        devItem2.setCategory('development')
        maintItem1 = self.create('MeetingItem')
        maintItem1.setCategory('maintenance')
        meeting = self.create('Meeting', date='2015/01/01')
        # make sure item reference is correct no matter it seems we are in the 'available items'
        # view, this is because we use getItems(theObjects=False) that is sensible to being
        # in the 'available items' view
        self.request.set('HTTP_REFERER',
                         '{0}/@@meeting_available_items_view'.format(meeting.absolute_url()))
        self.presentItem(resItem1)
        self.presentItem(resItem2)
        self.presentItem(devItem1)
        self.presentItem(devItem2)
        self.presentItem(maintItem1)
        # no itemReference until meeting is frozen
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True)],
                         ['', '', '', '', ''])
        self.freezeMeeting(meeting)
        # check that item references are correct
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True)],
                         ['development1', 'development2', 'research1', 'research2', 'maintenance_cat_id1'])
        self.assertEqual([item.getId() for item in meeting.getItems(ordered=True)],
                         ['o3', 'o4', 'o1', 'o2', 'o5'])
        # change position of items 1 and 2, itemReference is changed too
        changeOrder = resItem1.restrictedTraverse('@@change-item-order')
        changeOrder(moveType='down')
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True)],
                         ['development1', 'development2', 'research1', 'research2', 'maintenance_cat_id1'])
        self.assertEqual([item.getId() for item in meeting.getItems(ordered=True)],
                         ['o3', 'o4', 'o2', 'o1', 'o5'])
        # move depItem2 to last position
        changeOrder = resItem2.restrictedTraverse('@@change-item-order')
        changeOrder('number', '5')
        # now depItem1 reference is back to 'deployment1' and depItem2 in last position
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True)],
                         ['development1', 'development2', 'research1', 'maintenance_cat_id1', 'research2'])
        self.assertEqual([item.getId() for item in meeting.getItems(ordered=True)],
                         ['o3', 'o4', 'o1', 'o5', 'o2'])

        # if we insert a new item, references are updated
        newItem = self.create('MeetingItem')
        newItem.setCategory('development')
        self.presentItem(newItem)
        # item is inserted at the end
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True)],
                         ['development1', 'development2', 'development3',
                          'research1', 'maintenance_cat_id1', 'research2'])
        self.assertEqual([item.getId() for item in meeting.getItems(ordered=True)],
                         ['o3', 'o4', 'o7', 'o1', 'o5', 'o2'])

        # now if we remove an item from the meeting, reference are still correct
        # remove item with ref 'research1', the first item, the item that had 'research2' will get 'research1'
        self.backToState(resItem1, 'validated')
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True)],
                         ['development1', 'development2', 'development3', 'maintenance_cat_id1', 'research1'])
        self.assertEqual([item.getId() for item in meeting.getItems(ordered=True)],
                         ['o3', 'o4', 'o7', 'o5', 'o2'])

        # delete item having reference 'development2'
        # only Manager may delete an item
        self.changeUser('admin')
        self.deleteAsManager(devItem2.UID())
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True)],
                         ['development1', 'development2', 'maintenance_cat_id1', 'research1'])
        self.assertEqual([item.getId() for item in meeting.getItems(ordered=True)],
                         ['o3', 'o7', 'o5', 'o2'])

        # if we change the category used for an item, reference are updated accordingly
        # change category for resItem1 from 'research' to 'development'
        resItem2.setCategory('development')
        resItem2._update_after_edit()
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True)],
                         ['development1', 'development2', 'maintenance_cat_id1', 'development3'])
        self.assertEqual([item.getId() for item in meeting.getItems(ordered=True)],
                         ['o3', 'o7', 'o5', 'o2'])

        # test late items, reference is HOJ.1, HOJ.2, ...
        self.changeUser('pmManager')
        lateItem1 = self.create('MeetingItem')
        lateItem1.setCategory('development')
        lateItem1.setPreferredMeeting(meeting.UID())
        lateItem2 = self.create('MeetingItem')
        lateItem2.setCategory('research')
        lateItem2.setPreferredMeeting(meeting.UID())
        self.presentItem(lateItem1)
        self.presentItem(lateItem2)
        self.assertEqual(lateItem1.getItemReference(), 'HOJ.1')
        self.assertEqual(lateItem2.getItemReference(), 'HOJ.2')

        # right now test if the getItemNumsForActe has to be generated by a user
        # that only have access to some items of the meeting.  Indeed, let's say
        # a MeetingManager is on an item and removes it from the meeting, getItemNumsForActe
        # is not recomputed as not called on the item view, if another user access an
        # item or the meeting, this time it will be recomputed
        self.assertEqual(lateItem1.getItemReference(), 'HOJ.1')
        self.assertEqual(newItem.getItemReference(), 'development2')
        self.backToState(lateItem1, 'validated')
        self.backToState(newItem, 'validated')
        self.changeUser('pmCreator1')
        # no more reference for lateItem1 and depItem2
        self.assertEqual(lateItem1.getItemReference(), '')
        self.assertEqual(newItem.getItemReference(), '')
        # pmCreator1 is not able to access every items of the meeting
        # if we get the reference of other items, it is correct,
        # make meeting modified so we are sure that item reference are recomputed
        # with pmCreator1 as current user
        meeting.notifyModified()
        meeting.updateItemReferences()
        self.assertEqual([item.getItemReference() for item in meeting.getItems(ordered=True,
                                                                               unrestricted=True)],
                         ['development1', 'maintenance_cat_id1', 'development2', 'HOJ.1'])
        self.assertEqual(devItem1.getItemReference(), 'development1')
        # no more in the meeting
        self.assertEqual(resItem1.getItemReference(), '')
        self.assertEqual(resItem2.getItemReference(), 'development2')
        self.assertEqual(lateItem2.getItemReference(), 'HOJ.1')

    def test_InsertingMethodOnDecisionFirstWord(self):
        '''
          Test our custom inserting method 'on_item_decision_first_words'.
        '''
        cfg = self.meetingConfig
        self.changeUser('pmManager')
        self._removeConfigObjectsFor(cfg)
        insertingMethods = ({'insertingMethod': 'on_item_decision_first_words', 'reverse': '0'},)
        cfg.setInsertingMethodsOnAddItem(insertingMethods)
        # no decision, it will get minimum possible index value
        item1 = self.create('MeetingItem')
        item1.setDecision('<p></p>')
        item1Id = item1.getId()
        item1_order = item1._getInsertOrder(cfg)
        # decision < 6 chars
        item2 = self.create('MeetingItem')
        item2.setDecision('<p>EMET</p>')
        item2Id = item2.getId()
        item2_order = item2._getInsertOrder(cfg)
        # beginning with 'A'
        item3 = self.create('MeetingItem')
        item3.setDecision('<p>ACCORDE un avis de ...</p>')
        item3Id = item3.getId()
        item3_order = item3._getInsertOrder(cfg)
        # beginning with 'O'
        item4 = self.create('MeetingItem')
        item4.setDecision('<p>&nbsp;OCTROIE un avis de ...</p>')
        item4Id = item4.getId()
        item4_order = item4._getInsertOrder(cfg)
        # begin with a space then EMET
        item5 = self.create('MeetingItem')
        item5.setDecision('<p>&nbsp;</p><p>EMET</p>')
        item5Id = item5.getId()
        item5_order = item5._getInsertOrder(cfg)
        # use 'zzzzzz', it will get maximum possible index value
        item6 = self.create('MeetingItem')
        item6.setDecision('<p>zzzzzz</p>')
        item6Id = item6.getId()
        item6_order = item6._getInsertOrder(cfg)
        # use same beginning of sentence as item2 and item5 but
        # with an extra letter that will be taken into account
        item7 = self.create('MeetingItem')
        item7.setDecision('<p>EMET un avis</p>')
        item7Id = item7.getId()
        item7_order = item7._getInsertOrder(cfg)
        # result should be item1, item3, item2, item5 (equals to item2) then item4
        self.assertTrue(item1_order < item3_order < item2_order ==
                        item5_order < item7_order < item4_order < item6_order)
        # every items use proposingGroup 'developers' that is in position 1
        # if we use 'vendors' for item1, item1_order will become higher than item6_order
        insertingMethods = ({'insertingMethod': 'on_proposing_groups', 'reverse': '0'},
                            {'insertingMethod': 'on_item_decision_first_words', 'reverse': '0'},)
        cfg.setInsertingMethodsOnAddItem(insertingMethods)
        for item in item1, item2, item3, item4, item5, item6, item7:
            self.assertEqual(item.getProposingGroup(), self.developers_uid)
        self.assertEqual(item1._findOrderFor('on_proposing_groups'), 1)
        item1.setProposingGroup(self.vendors_uid)
        self.assertEqual(item1._findOrderFor('on_proposing_groups'), 2)
        # now order of item1 is higher than order of item6
        self.assertTrue(item1._getInsertOrder(cfg) > item6._getInsertOrder(cfg))

        # now insert items in a meeting and compare
        meeting = self.create('Meeting', date='2015/01/01')
        for item in item1, item2, item3, item4, item5, item6, item7:
            self.presentItem(item)
        # items should have been added respecting following order item3, item2, item5, item4, item6, item1
        self.assertEqual([item.getId() for item in meeting.getItems(ordered=True)],
                         [item3Id, item2Id, item5Id, item7Id, item4Id, item6Id, item1Id, ])

    def test_GetItemWithFinanceAdvice(self):
        '''Test the custom getItemWithFinanceAdvice method.
           This will return the item an advice was given on in case the item
           is the result of a 'return college' item or if it is a council item and
           item in the college had the finance advice.
           Moreover, when an advice holder is linked to another item, the finance group
           gets automatically red access to the new item.
        '''
        self.changeUser('admin')
        cfg = self.meetingConfig
        cfg2 = self.meetingConfig2
        cfg2Id = cfg2.getId()
        cfg.setItemAutoSentToOtherMCStates(cfg.getItemAutoSentToOtherMCStates() + ('itemfrozen', ))

        # add finance groups
        self._createFinanceGroups()
        # configure customAdvisers for 'meeting-config-college'
        _configureCollegeCustomAdvisers(self.portal)
        # define relevant users for finance groups
        self._setupFinanceGroups()

        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        financial_group_uids = self.tool.financialGroupUids()
        item.setFinanceAdvice(financial_group_uids[0])
        item._update_after_edit()
        self.assertTrue(financial_group_uids[0] in item.adviceIndex)
        self.assertEqual(item.adapted().getItemWithFinanceAdvice(), item)
        # give advice
        self.proposeItem(item)
        self.do(item, 'proposeToFinance')
        self.changeUser('pmFinManager')
        item.setCompleteness('completeness_complete')
        item.setEmergency('emergency_accepted')
        createContentInContainer(item,
                                 'meetingadvicefinances',
                                 **{'advice_group': financial_group_uids[0],
                                    'advice_type': 'positive_finance',
                                    'advice_comment': RichTextValue(u'My positive comment finance')})
        # finance group has read access to the item
        financeGroupAdvisersId = "{0}_advisers".format(item.getFinanceAdvice())
        self.assertEqual(item.__ac_local_roles__[financeGroupAdvisersId], ['Reader'])

        self.changeUser('pmManager')
        # duplicate and keep link will not consider original finance advice
        # as advice for the duplicated item
        form = item.restrictedTraverse('@@item_duplicate_form').form_instance
        form.update()
        data = {'keep_link': True, 'annex_ids': [], 'annex_decision_ids': []}
        duplicatedItem = form._doApply(data)
        # the duplicatedItem advice referent is the duplicatedItem...
        self.assertEqual(duplicatedItem.adapted().getItemWithFinanceAdvice(), duplicatedItem)
        # the finance advice is asked on the duplicatedItem
        self.assertEqual(duplicatedItem.getFinanceAdvice(), financial_group_uids[0])
        self.assertTrue(financial_group_uids[0] in duplicatedItem.adviceIndex)
        # finance group get automatically access to the duplicatedItem as it is linked manually
        self.assertEqual(duplicatedItem.__ac_local_roles__[financeGroupAdvisersId], ['Reader'])

        # delaying an item will not make original item the item holder
        # the finance advice is asked on the delayed item too
        meeting = self.create('Meeting', date='2015/01/01')
        self.presentItem(item)
        self.decideMeeting(meeting)
        self.do(item, 'delay')
        # find the new item created by the clone as item is already the predecessor of 'duplicatedItem'
        clonedDelayedItem = [newItem for newItem in item.getBRefs('ItemPredecessor')
                             if not newItem == duplicatedItem][0]
        self.assertEqual(clonedDelayedItem.adapted().getItemWithFinanceAdvice(), clonedDelayedItem)
        # the finance advice is asked on the clonedDelayedItem
        self.assertEqual(clonedDelayedItem.getFinanceAdvice(), financial_group_uids[0])
        self.assertTrue(financial_group_uids[0] in clonedDelayedItem.adviceIndex)
        # finance group did not get automatically access to the clonedDelayedItem
        self.assertTrue(financeGroupAdvisersId not in clonedDelayedItem.__ac_local_roles__)

        # now correct item and 'accept and return' it
        # this time, the original item is considered the finance advice holder
        self.do(item, 'backToItemFrozen')
        self.do(item, 'return')
        # find the new item created by the clone as item is already the predecessor of 'duplicatedItem'
        clonedReturnedItem = [newItem for newItem in item.getBRefs('ItemPredecessor')
                              if newItem not in (duplicatedItem, clonedDelayedItem)][0]
        # this time, the item with finance advice is the 'returned' item
        itemWithFinanceAdvice = clonedReturnedItem.adapted().getItemWithFinanceAdvice()
        self.assertEqual(itemWithFinanceAdvice, item)
        self.assertEqual(itemWithFinanceAdvice.queryState(), 'returned')
        # the info is kept in the financeAdvice attribute
        # nevertheless, the advice is not asked automatically anymore
        self.assertEqual(clonedReturnedItem.getFinanceAdvice(), financial_group_uids[0])
        self.assertTrue(financial_group_uids[0] not in clonedReturnedItem.adviceIndex)
        # finance group gets automatically access to the clonedReturnedItem
        self.assertEqual(clonedReturnedItem.__ac_local_roles__[financeGroupAdvisersId], ['Reader'])

        # send the clonedReturnedItem to Council and check with the council item
        clonedReturnedItem.setOtherMeetingConfigsClonableTo('meeting-config-council')
        self.presentItem(clonedReturnedItem)
        self.assertEqual(clonedReturnedItem.queryState(), 'itemfrozen')
        # still right, including sent item
        self.assertEqual(clonedReturnedItem.adapted().getItemWithFinanceAdvice(), item)
        self.assertEqual(
            clonedReturnedItem.getItemClonedToOtherMC(cfg2Id).adapted().getItemWithFinanceAdvice(),
            item)
        # now test if setting an optional finance advice does not break getItemWithFinanceAdvice
        clonedReturnedItem.setOptionalAdvisers((financial_group_uids[0], ))
        clonedReturnedItem.updateLocalRoles()
        self.assertTrue(financial_group_uids[0] in clonedReturnedItem.adviceIndex)
        self.assertEqual(clonedReturnedItem.adapted().getItemWithFinanceAdvice(), item)
        self.assertEqual(
            clonedReturnedItem.getItemClonedToOtherMC(cfg2Id).adapted().getItemWithFinanceAdvice(),
            item)

        # now test when the item is in the council
        # the right college item should be found too
        # use 2 items, one that will be classicaly accepted and one that will 'accepted_and_returned'
        itemToCouncil1 = self.create('MeetingItem')
        itemToCouncil1.setFinanceAdvice(financial_group_uids[0])
        itemToCouncil1.setOtherMeetingConfigsClonableTo('meeting-config-council')
        itemToCouncil2 = self.create('MeetingItem')
        itemToCouncil2.setFinanceAdvice(financial_group_uids[0])
        itemToCouncil2.setOtherMeetingConfigsClonableTo('meeting-config-council')
        # ask emergency so finance step is passed
        itemToCouncil1.setEmergency('emergency_asked')
        itemToCouncil2.setEmergency('emergency_asked')
        itemToCouncil1._update_after_edit()
        itemToCouncil2._update_after_edit()
        self.assertTrue(financial_group_uids[0] in itemToCouncil1.adviceIndex)
        self.assertTrue(financial_group_uids[0] in itemToCouncil2.adviceIndex)
        self.presentItem(itemToCouncil1)
        self.presentItem(itemToCouncil2)
        # accept itemToCouncil1 and check
        self.do(itemToCouncil1, 'accept')
        itemInCouncil1 = itemToCouncil1.getItemClonedToOtherMC('meeting-config-council')
        self.assertEqual(itemInCouncil1.getFinanceAdvice(), financial_group_uids[0])
        self.assertEqual(itemInCouncil1.adapted().getItemWithFinanceAdvice(), itemToCouncil1)
        # finance group gets automatically access to the itemInCouncil1
        self.assertEqual(itemInCouncil1.__ac_local_roles__[financeGroupAdvisersId], ['Reader'])
        # accept_and_return itemToCouncil2 and check
        self.do(itemToCouncil2, 'accept_and_return')
        itemInCouncil2 = itemToCouncil2.getItemClonedToOtherMC('meeting-config-council')
        self.assertEqual(itemInCouncil2.getFinanceAdvice(), financial_group_uids[0])
        self.assertEqual(itemInCouncil2.adapted().getItemWithFinanceAdvice(), itemToCouncil2)
        # when college item was accepted_and_returned, it was cloned, the finance advice
        # is also found for this cloned item
        clonedAcceptedAndReturnedItem = [newItem for newItem in itemToCouncil2.getBRefs('ItemPredecessor')
                                         if newItem.portal_type == 'MeetingItemCollege'][0]
        self.assertEqual(clonedAcceptedAndReturnedItem.adapted().getItemWithFinanceAdvice(), itemToCouncil2)
        # finance group gets automatically access to the itemInCouncil2
        self.assertEqual(itemInCouncil2.__ac_local_roles__[financeGroupAdvisersId], ['Reader'])
        # roles are kept after edit or transition
        itemInCouncil2._update_after_edit()
        self.assertEqual(itemInCouncil2.__ac_local_roles__[financeGroupAdvisersId], ['Reader'])
        # only available transition is 'present', so create a meeting in council to test...
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.meetingConfig2.setUseGroupsAsCategories(True)
        self.meetingConfig2.setInsertingMethodsOnAddItem(({'insertingMethod': 'on_proposing_groups', 'reverse': '0'},))
        self.create('Meeting', date='2015/01/01')
        self.do(itemInCouncil2, 'present')
        self.assertEqual(itemInCouncil2.queryState(), 'presented')
        self.assertEqual(itemInCouncil2.__ac_local_roles__[financeGroupAdvisersId], ['Reader'])

        # duplicate and keep link an 'accepted_and_return' college item,
        # the financeAdvice will not follow
        form = itemToCouncil2.restrictedTraverse('@@item_duplicate_form').form_instance
        form.update()
        data = {'keep_link': True, 'annex_ids': [], 'annex_decision_ids': []}
        duplicatedItem2 = form._doApply(data)
        self.assertEqual(duplicatedItem2.adapted().getItemWithFinanceAdvice(), duplicatedItem2)

    def test_GetLegalTextForFDAdvice(self):
        self.changeUser('admin')
        # add finance groups
        self._createFinanceGroups()
        # configure customAdvisers for 'meeting-config-college'
        _configureCollegeCustomAdvisers(self.portal)
        # define relevant users for finance groups
        self._setupFinanceGroups()

        self.changeUser('pmManager')
        item1 = self.create('MeetingItem', title='Item with positive advice')
        financial_group_uids = self.tool.financialGroupUids()
        item1.setFinanceAdvice(financial_group_uids[0])
        item1a = self.create('MeetingItem', title='Item with positive with remarks advice')
        item1a.setFinanceAdvice(financial_group_uids[0])
        item2 = self.create('MeetingItem', title='Item with negative advice')
        item2.setFinanceAdvice(financial_group_uids[0])
        item3 = self.create('MeetingItem', title='Item with no advice')
        item3.setFinanceAdvice(financial_group_uids[0])

        self.proposeItem(item1)
        self.proposeItem(item1a)
        self.proposeItem(item2)
        self.proposeItem(item3)
        # do not fail when called and things are still not on
        self.assertEqual(item1.adapted().getLegalTextForFDAdvice(), '')
        self.assertEqual(item1a.adapted().getLegalTextForFDAdvice(), '')
        self.assertEqual(item2.adapted().getLegalTextForFDAdvice(), '')
        self.assertEqual(item3.adapted().getLegalTextForFDAdvice(), '')
        self.do(item1, 'proposeToFinance')
        item1.setCompleteness('completeness_complete')
        self.do(item1a, 'proposeToFinance')
        item1a.setCompleteness('completeness_complete')
        self.do(item2, 'proposeToFinance')
        # use change-item-completeness view to change completeness
        # so completeness_changes_history is updated
        changeCompletenessView = item1a.restrictedTraverse('@@change-item-completeness')
        changeCompletenessView._changeCompleteness(
            new_completeness_value='completeness_complete',
            bypassSecurityCheck=True,
            comment='')
        item1a.updateLocalRoles()
        item2.setCompleteness('completeness_complete')
        self.do(item3, 'proposeToFinance')
        item3.setCompleteness('completeness_complete')
        item3.updateLocalRoles()
        item3.adviceIndex[item3.getFinanceAdvice()]['delay_started_on'] = datetime(2012, 1, 1)
        item3.updateLocalRoles()

        self.changeUser('pmFinManager')
        advice1 = createContentInContainer(
            item1,
            'meetingadvicefinances',
            **{'advice_group': financial_group_uids[0],
               'advice_type': 'positive_finance',
               'advice_comment': RichTextValue(u'My good comment finance')})
        advice1a = createContentInContainer(
            item1a,
            'meetingadvicefinances',
            **{'advice_group': financial_group_uids[0],
               'advice_type': 'positive_with_remarks_finance',
               'advice_comment': RichTextValue(u'My good with remarks comment finance')})
        advice2 = createContentInContainer(
            item2,
            'meetingadvicefinances',
            **{'advice_group': financial_group_uids[0],
               'advice_type': 'negative_finance',
               'advice_comment': RichTextValue(u'My bad comment finance')})

        # send to financial reviewer
        self.changeUser('pmFinController')
        self.do(advice1, 'proposeToFinancialReviewer')
        self.do(advice1a, 'proposeToFinancialReviewer')
        self.do(advice2, 'proposeToFinancialReviewer')
        # send to finance manager
        self.changeUser('pmFinReviewer')
        self.do(advice1, 'proposeToFinancialManager')
        self.do(advice1a, 'proposeToFinancialManager')
        self.do(advice2, 'proposeToFinancialManager')
        # sign the advice
        self.changeUser('pmFinManager')
        self.do(advice1, 'signFinancialAdvice')
        self.do(advice1a, 'signFinancialAdvice')
        self.do(advice2, 'signFinancialAdvice')

        # strange case where delay_started_on is None,
        # in this case, the completeness_complete time action is used
        self.changeUser('admin')
        self.do(item1a, 'backToProposedToDirector')
        item1a.adviceIndex[item3.getFinanceAdvice()]['delay_started_on'] = None
        item1a.updateLocalRoles()

        financialStuff1 = item1.adapted().getFinancialAdviceStuff()
        financialStuff1a = item1a.adapted().getFinancialAdviceStuff()
        # positive_with_remarks 'advice_type' is printed like 'positive'
        self.assertEqual(financialStuff1['advice_type'], financialStuff1a['advice_type'])
        financialStuff2 = item2.adapted().getFinancialAdviceStuff()
        advice1 = item1.getAdviceDataFor(item1, item1.getFinanceAdvice())
        advice1a = item1a.getAdviceDataFor(item1a, item1a.getFinanceAdvice())
        advice2 = item2.getAdviceDataFor(item2, item2.getFinanceAdvice())
        advice3 = item3.getAdviceDataFor(item3, item3.getFinanceAdvice())
        delayStartedOn1 = advice1['delay_infos']['delay_started_on_localized']
        delayStartedOn2 = advice2['delay_infos']['delay_started_on_localized']
        delayStartedOn3 = advice3['delay_infos']['delay_started_on_localized']
        outOfFinancialdptLocalized1 = financialStuff1['out_of_financial_dpt_localized']
        outOfFinancialdptLocalized2 = financialStuff2['out_of_financial_dpt_localized']
        comment2 = financialStuff2['comment']
        limitDateLocalized3 = advice3['delay_infos']['limit_date_localized']

        res1 = FINANCE_ADVICE_LEGAL_TEXT_PRE.format(delayStartedOn1)
        res1 = res1 + FINANCE_ADVICE_LEGAL_TEXT.format('favorable',
                                                       outOfFinancialdptLocalized1)
        res2 = FINANCE_ADVICE_LEGAL_TEXT_PRE.format(delayStartedOn2)
        res2 = res2 + FINANCE_ADVICE_LEGAL_TEXT.format('défavorable',
                                                       outOfFinancialdptLocalized2)
        res2 = res2 + "<p>{0}</p>".format(comment2)

        res3 = FINANCE_ADVICE_LEGAL_TEXT_PRE.format(delayStartedOn3)
        res3 = res3 + FINANCE_ADVICE_LEGAL_TEXT_NOT_GIVEN

        res4 = '<p>Avis favorable du Directeur Financier du {0}</p>'.format(outOfFinancialdptLocalized1)

        res5 = '<p>Avis défavorable du Directeur Financier du {0}</p>'.format(outOfFinancialdptLocalized2)
        res5 = res5 + "<p>{0}</p>".format(comment2)

        res6 = "<p>Avis du Directeur financier expiré le {0}</p>".format(limitDateLocalized3)

        self.assertEqual(item1.adapted().getLegalTextForFDAdvice(), res1)
        # when 'delay_started_on_localized' is None, the last action "completeness_complete" time is used
        self.assertIsNone(advice1a['delay_infos']['delay_started_on_localized'])
        # positive_with_remarks_finance is rendered as positive, so same result as res1 here
        self.assertEqual(item1a.adapted().getLegalTextForFDAdvice(), res1)
        self.assertEqual(item2.adapted().getLegalTextForFDAdvice(), res2)
        self.assertEqual(item3.adapted().getLegalTextForFDAdvice(), res3)

        self.assertEqual(item1.adapted().getLegalTextForFDAdvice(isMeeting=True), res4)
        self.assertEqual(item1a.adapted().getLegalTextForFDAdvice(isMeeting=True), res4)
        self.assertEqual(item2.adapted().getLegalTextForFDAdvice(isMeeting=True), res5)
        self.assertEqual(item3.adapted().getLegalTextForFDAdvice(isMeeting=True), res6)

    def test_MayGenerateFDAdvice(self):
        '''An advice can be generated when:
            -at least one advice is asked.
            -the advice is not hidden OR the user is in
                the right FD group OR the advice is no
                longer editable
        '''
        self.changeUser('admin')
        # add finance groups
        self._createFinanceGroups()
        # configure customAdvisers for 'meeting-config-college'
        _configureCollegeCustomAdvisers(self.portal)
        # define relevant users for finance groups
        self._setupFinanceGroups()

        self.changeUser('pmManager')
        item1 = self.create('MeetingItem', title='Item with advice')
        # if no advice is asked, mayGenerate returns False.
        self.assertFalse(item1.adapted().mayGenerateFDAdvice())

        financial_group_uids = self.tool.financialGroupUids()
        item1.setFinanceAdvice(financial_group_uids[0])
        self.proposeItem(item1)
        self.do(item1, 'proposeToFinance')
        item1.setCompleteness('completeness_complete')

        self.changeUser('pmFinManager')
        advice1 = createContentInContainer(item1,
                                           'meetingadvicefinances',
                                           **{'advice_group': financial_group_uids[0],
                                              'advice_type': 'positive_finance',
                                              'advice_comment': RichTextValue(u'My comment finance')})
        # if advice is hidden, it can only be seen by advisers of the finance group.
        advice1.advice_hide_during_redaction = True
        self.changeUser('pmManager')
        self.assertFalse(item1.adapted().mayGenerateFDAdvice())

        self.changeUser('pmFinController')
        self.assertTrue(item1.adapted().mayGenerateFDAdvice())
        self.do(advice1, 'proposeToFinancialReviewer')

        self.changeUser('pmFinReviewer')
        self.assertTrue(item1.adapted().mayGenerateFDAdvice())
        self.do(advice1, 'proposeToFinancialManager')

        self.assertTrue(item1.adapted().mayGenerateFDAdvice())

        self.changeUser('pmCreator1')
        self.assertFalse(item1.adapted().mayGenerateFDAdvice())

        item1.adviceIndex[item1.getFinanceAdvice()]['delay_started_on'] = datetime(2012, 1, 1)
        item1.updateLocalRoles()

        self.assertTrue(item1.adapted().mayGenerateFDAdvice())

    def test_GetOfficeManager(self):
        self.changeUser('pmManager')

        # simple item following the workflow until it is validated.
        itemValidated = self.create('MeetingItem')
        self.do(itemValidated, 'proposeToAdministrativeReviewer')
        self.do(itemValidated, 'proposeToInternalReviewer')
        self.do(itemValidated, 'proposeToDirector')
        self.do(itemValidated, 'validate')
        # item directly validated from the created state. This one has no
        # informations about office manager because he didn't go through
        # the state "proposedToDirector"
        itemDirectlyValidated = self.create('MeetingItem')
        self.do(itemDirectlyValidated, 'validate')

        # Item that gonna be postponed and directly presented to another meeting
        itemToReturn = self.create('MeetingItem')
        self.do(itemToReturn, 'proposeToAdministrativeReviewer')
        self.do(itemToReturn, 'proposeToInternalReviewer')
        self.do(itemToReturn, 'proposeToDirector')
        self.do(itemToReturn, 'validate')

        # Item that gonna be postponed, presented to another meeting and then
        # postponed and presented a second time.
        itemToReturnTwice = self.create('MeetingItem')
        self.do(itemToReturnTwice, 'proposeToAdministrativeReviewer')
        self.do(itemToReturnTwice, 'proposeToInternalReviewer')
        self.do(itemToReturnTwice, 'proposeToDirector')
        self.do(itemToReturnTwice, 'validate')

        # Creates a meeting, presents and postpones the items.
        meeting = self.create('Meeting', date='2014/01/01 09:00:00')
        self.presentItem(itemToReturn)
        self.presentItem(itemToReturnTwice)
        self.decideMeeting(meeting)
        self.do(itemToReturn, 'return')
        self.do(itemToReturnTwice, 'return')

        # Gets the items which have been duplicated when postponed.
        itemReturned = itemToReturn.getBRefs('ItemPredecessor')[0]
        itemReturnedOnce = itemToReturnTwice.getBRefs('ItemPredecessor')[0]

        # Put back the meeting in creation to add the duplicated item into it.
        # Presents and postpones again.
        self.backToState(meeting, 'created')
        self.presentItem(itemReturnedOnce)
        self.decideMeeting(meeting)
        self.do(itemReturnedOnce, 'return')
        itemReturnedTwice = itemReturnedOnce.getBRefs('ItemPredecessor')[0]

        # Checks if we have the infos of the office manager when we are supposed
        # to have it.
        pmManagerObj = self.portal.portal_membership.getMemberById('pmManager')
        pmManagerObj.setProperties(description='0497/696969     brol')

        self.assertEqual(itemValidated.adapted().getOfficeManager()['fullname'], 'M. PMManager')
        self.assertEqual(itemValidated.adapted().getOfficeManager()['phone'], '0497/696969')
        self.assertEqual(itemValidated.adapted().getOfficeManager()['email'], 'pmmanager@plonemeeting.org')

        self.assertEqual(itemDirectlyValidated.adapted().getOfficeManager(), '')

        self.assertEqual(itemReturned.adapted().getOfficeManager()['fullname'], 'M. PMManager')
        self.assertEqual(itemReturned.adapted().getOfficeManager()['phone'], '0497/696969')
        self.assertEqual(itemReturned.adapted().getOfficeManager()['email'], 'pmmanager@plonemeeting.org')

        self.assertEqual(itemReturnedTwice.adapted().getOfficeManager()['fullname'], 'M. PMManager')
        self.assertEqual(itemReturnedTwice.adapted().getOfficeManager()['phone'], '0497/696969')
        self.assertEqual(itemReturnedTwice.adapted().getOfficeManager()['email'], 'pmmanager@plonemeeting.org')

    def test_ItemSetToAddendum(self):
        """When an item is set to/from 'addendum', it's itemNumber
           is automatically adapted accordingly.  An 'addendum' item
           will use a subnumber."""
        self.setMeetingConfig(self.meetingConfig2.getId())
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        meeting = self.create('Meeting', date=DateTime())
        self.presentItem(item)
        self.freezeMeeting(meeting)

        # not possible to set item to 'addendum' as it is the only item in the meeting
        # and subcall to "change item number" breaks and listType is not changed
        view = item.restrictedTraverse('@@change-item-listtype')
        view('addendum')
        self.assertEqual(item.getListType(), 'normal')
        item2 = self.create('MeetingItem')
        self.presentItem(item2)
        # first item of the meeting may not be set to 'addendum'
        self.assertEqual(item.getItemNumber(), 100)
        view('addendum')
        self.assertEqual(item.getListType(), 'normal')

        # set second item to 'addendum'
        view = item2.restrictedTraverse('@@change-item-listtype')
        view('addendum')
        # now it is addendum and itemNumber as been set to a subnumber
        self.assertEqual(item2.getListType(), 'addendum')
        self.assertEqual(item2.getItemNumber(), 101)
        # back to 'normal', itemNumber is set back to an integer
        view('normal')
        self.assertEqual(item2.getItemNumber(), 200)

    def test_SentenceAppendedToCouncilItemDecisionEndWhenPresented(self):
        """When a council item is presented, it's decisionEnd field is adapted,
           a particular sentence is added at the end of the field."""
        cfg2 = self.meetingConfig2
        cfg2Id = cfg2.getId()
        self.changeUser('pmManager')
        self.setMeetingConfig(cfg2Id)
        self.create('Meeting', date=DateTime('2015/11/11'))
        FIRST_SENTENCE = '<p>A first sentence.</p>'
        item = self.create('MeetingItem')
        item.setDecisionEnd(FIRST_SENTENCE)
        self.assertEqual(item.getDecisionEnd(), FIRST_SENTENCE)
        # present item, special sentence will be appended
        self.presentItem(item)
        self.assertEqual(item.getDecisionEnd(),
                         FIRST_SENTENCE + COUNCILITEM_DECISIONEND_SENTENCE)
        # not appended twice, create an item that already ends with sentence
        # more over add an extra empty <p></p> at the end
        item2 = self.create('MeetingItem')
        item2.setDecisionEnd(FIRST_SENTENCE + COUNCILITEM_DECISIONEND_SENTENCE + '<p>&nbsp;</p>')
        self.assertEqual(item2.getDecisionEnd(),
                         FIRST_SENTENCE + COUNCILITEM_DECISIONEND_SENTENCE + '<p>&nbsp;</p>')
        self.presentItem(item2)
        self.assertEqual(item2.getDecisionEnd(),
                         FIRST_SENTENCE + COUNCILITEM_DECISIONEND_SENTENCE + '<p>&nbsp;</p>')

    def test_PrintFDStats(self):
        self.changeUser('admin')
        # add finance groups
        self._createFinanceGroups()
        # configure customAdvisers for 'meeting-config-college'
        _configureCollegeCustomAdvisers(self.portal)
        # define relevant users for finance groups
        self._setupFinanceGroups()

        # Create item 1 with an advice asked to df-contrale.
        self.changeUser('pmManager')
        item1 = self.create('MeetingItem', title='Item1 with advice')

        financial_group_uids = self.tool.financialGroupUids()
        item1.setFinanceAdvice(financial_group_uids[0])
        self.proposeItem(item1)
        self.do(item1, 'proposeToFinance')
        self.changeUser('pmFinController')
        # Set completeness to complete.
        changeCompleteness = item1.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_complete')
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Add a negative advice.
        self.changeUser('pmFinManager')
        advice1 = createContentInContainer(item1,
                                           'meetingadvicefinances',
                                           **{'advice_group': financial_group_uids[0],
                                              'advice_type': 'negative_finance',
                                              'advice_comment': RichTextValue(u'My bad comment finance')})
        self.changeUser('pmFinController')
        self.do(advice1, 'proposeToFinancialReviewer')

        self.changeUser('pmFinReviewer')
        self.do(advice1, 'proposeToFinancialManager')

        # Sign the advice which is sent back to director.
        self.changeUser('pmFinManager')
        self.do(advice1, 'signFinancialAdvice')

        # Propose to finance for the second time
        self.changeUser('pmManager')
        self.do(item1, 'proposeToFinance')
        self.changeUser('pmFinController')
        # Set the completeness to incomplete with a comment.
        changeCompleteness = item1.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_incomplete')
        self.request['comment'] = 'You are not complete'
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Send the item back to internal reviewer due to his incompleteness.
        self.changeUser('pmManager')
        self.do(item1,
                'backToProposedToInternalReviewer',
                comment="Go back to the abyss"
                )
        self.do(item1, 'proposeToDirector')
        self.do(item1, 'proposeToFinance')
        self.changeUser('pmFinController')
        # Let assume that the item is now complete. So set the completeness.
        changeCompleteness = item1.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_complete')
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Give a positive advice
        advice1.advice_type = 'positive_finance'
        # Erase the comment
        advice1.advice_comment = RichTextValue('')
        notify(ObjectModifiedEvent(advice1))

        self.changeUser('pmFinController')
        self.do(advice1, 'proposeToFinancialReviewer')

        self.changeUser('pmFinReviewer')
        self.do(advice1, 'proposeToFinancialManager')

        # Sign the advice so the item is validated.
        self.changeUser('pmFinManager')
        self.do(advice1, 'signFinancialAdvice')

        # Setup needed because we will now try with an advice from
        # df-comptabilita-c-et-audit-financier. Since the finance users don't
        # have basically the right to handle that sort of advice, we give them
        # the right here.
        # add pmFinController, pmFinReviewer and pmFinManager to advisers and to their respective finance group
        self._addPrincipalToGroup('pmFinController', '%s_advisers' % financial_group_uids[1])
        self._addPrincipalToGroup('pmFinReviewer', '%s_advisers' % financial_group_uids[1])
        self._addPrincipalToGroup('pmFinManager', '%s_advisers' % financial_group_uids[1])
        self._addPrincipalToGroup('pmFinController', '%s_financialcontrollers' % financial_group_uids[1])
        self._addPrincipalToGroup('pmFinReviewer', '%s_financialreviewers' % financial_group_uids[1])
        self._addPrincipalToGroup('pmFinManager', '%s_financialmanagers' % financial_group_uids[1])

        # Create the second item with advice.
        self.changeUser('pmManager')
        item2 = self.create('MeetingItem', title='Item2 with advice')
        item2.setFinanceAdvice(financial_group_uids[1])
        self.proposeItem(item2)
        self.do(item2, 'proposeToFinance')
        self.changeUser('pmFinController')
        # The item is complete.
        changeCompleteness = item2.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_complete')
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Give positive advice.
        self.changeUser('pmFinManager')
        advice2 = createContentInContainer(item2,
                                           'meetingadvicefinances',
                                           **{'advice_group': financial_group_uids[1],
                                              'advice_type': 'positive_finance'})

        self.changeUser('pmFinController')
        self.do(advice2, 'proposeToFinancialReviewer')

        self.changeUser('pmFinReviewer')
        self.do(advice2, 'proposeToFinancialManager')

        # Sign the advice, item is now validated.
        self.changeUser('pmFinManager')
        self.do(advice2, 'signFinancialAdvice')

        # Present this item to a meeting.
        self.changeUser('pmManager')
        meeting = self.create('Meeting', date='2019/09/19')
        # Delete recurring items.
        self.deleteAsManager(meeting.getItems()[0].UID())
        self.deleteAsManager(meeting.getItems()[0].UID())
        self.presentItem(item2)

        # Create the third item with advice which gonna be timed out..
        self.changeUser('pmManager')
        item3 = self.create('MeetingItem', title='Item3 with advice timed out')
        item3.setFinanceAdvice(financial_group_uids[1])
        self.proposeItem(item3)
        self.do(item3, 'proposeToFinance')
        self.changeUser('pmFinController')
        # The item is complete.
        changeCompleteness = item3.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_complete')
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Give negative advice.
        self.changeUser('pmFinManager')
        advice3 = createContentInContainer(item3,
                                           'meetingadvicefinances',
                                           **{'advice_group': financial_group_uids[1],
                                              'advice_type': 'negative_finance'})

        self.changeUser('pmFinController')
        self.do(advice3, 'proposeToFinancialReviewer')

        self.changeUser('pmFinReviewer')
        self.do(advice3, 'proposeToFinancialManager')

        # Sign the advice so the item is returned to director.
        self.changeUser('pmFinManager')
        self.do(advice3, 'signFinancialAdvice')

        # Propose to finance a second time.
        self.changeUser('pmManager')
        self.do(item3, 'proposeToFinance')
        self.changeUser('pmFinController')
        # Item is still complete.
        changeCompleteness = item3.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_complete')
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Now, finance will forget this item and make it expire.
        item3.adviceIndex[financial_group_uids[1]]['delay_started_on'] = datetime(2016, 1, 1)
        item3.updateLocalRoles()

        # Create the fourth item without advice, but timed out too.
        self.changeUser('pmManager')
        item4 = self.create('MeetingItem', title='Item4 timed out without advice')
        item4.setFinanceAdvice(financial_group_uids[0])
        self.proposeItem(item4)
        self.do(item4, 'proposeToFinance')
        self.changeUser('pmFinController')
        # The item is complete.
        changeCompleteness = item4.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_complete')
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Now, finance will forget this item and make it expire.
        item4.adviceIndex[financial_group_uids[0]]['delay_started_on'] = datetime(2016, 1, 1)
        item4.updateLocalRoles()

        # Create the fifth item with a bad advice and then remove financial impact.
        self.changeUser('pmManager')
        item5 = self.create('MeetingItem', title='Item5 with advice')

        financial_group_uids = self.tool.financialGroupUids()
        item5.setFinanceAdvice(financial_group_uids[0])
        self.proposeItem(item5)
        self.do(item5, 'proposeToFinance')
        self.changeUser('pmFinController')
        # Set completeness to complete.
        changeCompleteness = item5.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_complete')
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Add a negative advice.
        self.changeUser('pmFinManager')
        advice5 = createContentInContainer(item5,
                                           'meetingadvicefinances',
                                           **{'advice_group': financial_group_uids[0],
                                              'advice_type': 'negative_finance',
                                              'advice_comment': RichTextValue(u'Bad comment finance')})
        self.changeUser('pmFinController')
        self.do(advice5, 'proposeToFinancialReviewer')

        self.changeUser('pmFinReviewer')
        self.do(advice5, 'proposeToFinancialManager')

        # Sign the advice which is sent back to director.
        self.changeUser('pmFinManager')
        self.do(advice5, 'signFinancialAdvice')

        # Remove the financial impact.
        item5.setFinanceAdvice('_none_')

        # Create the sixth item with positive advice with remarks.
        self.changeUser('pmManager')
        item6 = self.create('MeetingItem', title='Item6 with positive advice with remarks')
        item6.setFinanceAdvice(financial_group_uids[1])
        self.proposeItem(item6)
        self.do(item6, 'proposeToFinance')
        self.changeUser('pmFinController')
        # The item is complete.
        changeCompleteness = item6.restrictedTraverse('@@change-item-completeness')
        self.request.set('new_completeness_value', 'completeness_complete')
        self.request.form['form.submitted'] = True
        changeCompleteness()

        # Give positive advice.
        self.changeUser('pmFinManager')
        advice6 = createContentInContainer(item6,
                                           'meetingadvicefinances',
                                           **{'advice_group': financial_group_uids[1],
                                              'advice_type': 'positive_with_remarks_finance',
                                              'advice_comment': RichTextValue(u'A remark')})

        self.changeUser('pmFinController')
        self.do(advice6, 'proposeToFinancialReviewer')

        self.changeUser('pmFinReviewer')
        self.do(advice6, 'proposeToFinancialManager')

        # Sign the advice, item is now validated.
        self.changeUser('pmFinManager')
        self.do(advice6, 'signFinancialAdvice')

        # Needed to make believe that the finance advice are checked in the
        # dashboard.
        self.changeUser('pmCreator1')
        item1.REQUEST.set('facetedQuery',
                          '{"c7":["delay_real_group_id__unique_id_002",\
                                  "delay_real_group_id__unique_id_003",\
                                  "delay_real_group_id__unique_id_004",\
                                  "delay_real_group_id__unique_id_005",\
                                  "delay_real_group_id__unique_id_006",\
                                  "delay_real_group_id__unique_id_007"]}')
        # Get a folder which is needed to call the view on it.
        folder = self.tool.getPloneMeetingFolder('meeting-config-college', 'pmCreator1').searches_items
        view = folder.restrictedTraverse('document_generation_helper_view')
        catalog = api.portal.get_tool('portal_catalog')
        results = view.printFDStats(catalog(portal_type='MeetingItemCollege', sort_on='id'))

        self.assertEqual(results[0]['title'], "Item1 with advice")
        self.assertEqual(results[0]['meeting_date'], "")
        self.assertEqual(results[0]['group'], "Developers")
        self.assertEqual(results[0]['end_advice'], "OUI")
        self.assertEqual(results[0]['comments'], "")
        self.assertEqual(results[0]['adviser'], u'DF - Contr\xf4le')
        self.assertEqual(results[0]['advice_type'], "Avis finance favorable")

        self.assertEqual(results[1]['title'], "Item1 with advice")
        self.assertEqual(results[1]['meeting_date'], "")
        self.assertEqual(results[1]['group'], "Developers")
        self.assertEqual(results[1]['end_advice'], "")
        self.assertEqual(results[1]['comments'], "Go back to the abyssYou are not complete")
        self.assertEqual(results[1]['adviser'], u'DF - Contr\xf4le')
        self.assertEqual(results[1]['advice_type'], 'Renvoy\xc3\xa9 au validateur interne pour incompl\xc3\xa9tude')

        self.assertEqual(results[2]['title'], "Item1 with advice")
        self.assertEqual(results[2]['meeting_date'], "")
        self.assertEqual(results[2]['group'], "Developers")
        self.assertEqual(results[2]['end_advice'], "NON")
        self.assertEqual(results[2]['comments'], "My bad comment finance")
        self.assertEqual(results[2]['adviser'], u'DF - Contr\xf4le')
        self.assertEqual(results[2]['advice_type'], 'Avis finance d\xc3\xa9favorable')

        self.assertEqual(results[3]['title'], "Item1 with advice")
        self.assertEqual(results[3]['meeting_date'], "")
        self.assertEqual(results[3]['group'], "Developers")
        self.assertEqual(results[3]['end_advice'], "")
        self.assertEqual(results[3]['comments'], "")
        self.assertEqual(results[3]['adviser'], u'DF - Contr\xf4le')
        self.assertEqual(results[3]['advice_type'], 'Compl\xc3\xa9tude')

        self.assertEqual(results[4]['title'], "Item2 with advice")
        self.assertEqual(results[4]['meeting_date'], "19/09/2019")
        self.assertEqual(results[4]['group'], "Developers")
        self.assertEqual(results[4]['end_advice'], "OUI")
        self.assertEqual(results[4]['comments'], "")
        self.assertEqual(results[4]['adviser'], u'DF - Comptabilit\xe9 et Audit financier')
        self.assertEqual(results[4]['advice_type'], "Avis finance favorable")

        self.assertEqual(results[5]['title'], "Item2 with advice")
        self.assertEqual(results[5]['meeting_date'], "19/09/2019")
        self.assertEqual(results[5]['group'], "Developers")
        self.assertEqual(results[5]['end_advice'], "")
        self.assertEqual(results[5]['comments'], "")
        self.assertEqual(results[5]['adviser'], u'DF - Comptabilit\xe9 et Audit financier')
        self.assertEqual(results[5]['advice_type'], 'Compl\xc3\xa9tude')

        self.assertEqual(results[6]['title'], "Item3 with advice timed out")
        self.assertEqual(results[6]['meeting_date'], "")
        self.assertEqual(results[6]['group'], "Developers")
        self.assertEqual(results[6]['end_advice'], "OUI")
        self.assertEqual(results[6]['comments'], "")
        self.assertEqual(results[6]['adviser'], u'DF - Comptabilit\xe9 et Audit financier')
        self.assertEqual(results[6]['advice_type'], 'Avis finance expir\xc3\xa9')

        self.assertEqual(results[7]['title'], "Item3 with advice timed out")
        self.assertEqual(results[7]['meeting_date'], "")
        self.assertEqual(results[7]['group'], "Developers")
        self.assertEqual(results[7]['end_advice'], "NON")
        self.assertEqual(results[7]['comments'], "")
        self.assertEqual(results[7]['adviser'], u'DF - Comptabilit\xe9 et Audit financier')
        self.assertEqual(results[7]['advice_type'], 'Avis finance d\xc3\xa9favorable')

        self.assertEqual(results[8]['title'], "Item3 with advice timed out")
        self.assertEqual(results[8]['meeting_date'], "")
        self.assertEqual(results[8]['group'], "Developers")
        self.assertEqual(results[8]['end_advice'], "")
        self.assertEqual(results[8]['comments'], "")
        self.assertEqual(results[8]['adviser'], u'DF - Comptabilit\xe9 et Audit financier')
        self.assertEqual(results[8]['advice_type'], 'Compl\xc3\xa9tude')

        self.assertEqual(results[9]['title'], "Item4 timed out without advice")
        self.assertEqual(results[9]['meeting_date'], "")
        self.assertEqual(results[9]['group'], "Developers")
        self.assertEqual(results[9]['end_advice'], "")
        self.assertEqual(results[9]['comments'], "")
        self.assertEqual(results[9]['adviser'], u'DF - Contr\xf4le')
        self.assertEqual(results[9]['advice_type'], 'Avis finance expir\xc3\xa9')

        self.assertEqual(results[10]['title'], "Item4 timed out without advice")
        self.assertEqual(results[10]['meeting_date'], "")
        self.assertEqual(results[10]['group'], "Developers")
        self.assertEqual(results[10]['end_advice'], "")
        self.assertEqual(results[10]['comments'], "")
        self.assertEqual(results[10]['adviser'], u'DF - Contr\xf4le')
        self.assertEqual(results[10]['advice_type'], 'Compl\xc3\xa9tude')

        self.assertEqual(results[11]['title'], "Item5 with advice")
        self.assertEqual(results[11]['meeting_date'], "")
        self.assertEqual(results[11]['group'], "Developers")
        self.assertEqual(results[11]['end_advice'], "OUI")
        self.assertEqual(results[11]['comments'], "Bad comment finance")
        self.assertEqual(results[11]['adviser'], u'DF - Contr\xf4le')
        self.assertEqual(results[11]['advice_type'], 'Avis finance d\xc3\xa9favorable')

        self.assertEqual(results[12]['title'], "Item5 with advice")
        self.assertEqual(results[12]['meeting_date'], "")
        self.assertEqual(results[12]['group'], "Developers")
        self.assertEqual(results[12]['end_advice'], "")
        self.assertEqual(results[12]['comments'], "")
        self.assertEqual(results[12]['adviser'], u'DF - Contr\xf4le')
        self.assertEqual(results[12]['advice_type'], 'Compl\xc3\xa9tude')

        self.assertEqual(results[13]['title'], "Item6 with positive advice with remarks")
        self.assertEqual(results[13]['meeting_date'], "")
        self.assertEqual(results[13]['group'], "Developers")
        self.assertEqual(results[13]['end_advice'], "OUI")
        self.assertEqual(results[13]['comments'], "A remark")
        self.assertEqual(results[13]['adviser'], u'DF - Comptabilit\xe9 et Audit financier')
        self.assertEqual(results[13]['advice_type'], 'Avis finance favorable avec remarques')

        self.assertEqual(results[14]['title'], "Item6 with positive advice with remarks")
        self.assertEqual(results[14]['meeting_date'], "")
        self.assertEqual(results[14]['group'], "Developers")
        self.assertEqual(results[14]['end_advice'], "")
        self.assertEqual(results[14]['comments'], "")
        self.assertEqual(results[14]['adviser'], u'DF - Comptabilit\xe9 et Audit financier')
        self.assertEqual(results[14]['advice_type'], 'Compl\xc3\xa9tude')

    def test_ShowOtherMeetingConfigsClonableToEmergency(self):
        """Condition method to restrict use of field
          MeetingItem.otherMeetingConfigsClonableToEmergency to MeetingManagers.
          Or if it was checked by a MeetingManager, then it appears to normal user,
          so if the normal user uncheck 'clone to', emergency is unchecked as well."""
        cfg = self.meetingConfig
        self.changeUser('siteadmin')
        if 'otherMeetingConfigsClonableToEmergency' not in cfg.getUsedItemAttributes():
            cfg.setUsedItemAttributes(cfg.getUsedItemAttributes() +
                                      ('otherMeetingConfigsClonableToEmergency', ))
        # as notmal user, not viewable
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        item.setOtherMeetingConfigsClonableTo((self.meetingConfig2.getId(), ))
        self.assertFalse(item.adapted().showOtherMeetingConfigsClonableToEmergency())
        # viewable as Manager
        self.changeUser('pmManager')
        self.assertTrue(item.adapted().showOtherMeetingConfigsClonableToEmergency())
        # if set, it will be viewable by common editor
        item.setOtherMeetingConfigsClonableToEmergency((self.meetingConfig2.getId(), ))
        self.changeUser('pmCreator1')
        self.assertTrue(item.adapted().showOtherMeetingConfigsClonableToEmergency())

    def test_ItemTakenOverByFinancesAdviser(self):
        """When item is proposed_to_finance, item is taken over by finances adviser.
           There was a bug with ToolPloneMeeting.get_plone_groups_for_user cachekey
           that is why we call it in this test."""
        self.changeUser('admin')
        cfg = self.meetingConfig
        cfg.setUsedAdviceTypes(('asked_again', ) + cfg.getUsedAdviceTypes())
        # add finance groups
        self._createFinanceGroups()
        # configure customAdvisers for 'meeting-config-college'
        _configureCollegeCustomAdvisers(self.portal)
        # define relevant users for finance groups
        self._setupFinanceGroups()

        # create item with asked finances advice
        self.changeUser('pmCreator1')
        self.tool.get_plone_groups_for_user()
        item = self.create('MeetingItem')
        financial_group_uids = self.tool.financialGroupUids()
        item.setFinanceAdvice(financial_group_uids[0])
        # send item to finances
        self.proposeItem(item)
        self.changeUser('pmReviewer1')
        self.tool.get_plone_groups_for_user()
        self.do(item, 'proposeToFinance')
        # finances take item over and send item back to director
        self.changeUser('pmFinController')
        self.tool.get_plone_groups_for_user()
        view = item.restrictedTraverse('@@toggle_item_taken_over_by')
        view.toggle(takenOverByFrom=item.getTakenOverBy())
        self.assertEqual(item.getTakenOverBy(), 'pmFinController')
        self.do(item, 'backToProposedToInternalReviewer')
        self.assertEqual(item.getTakenOverBy(), '')
        # login as director and send item back to finances
        self.changeUser('pmReviewer1')
        self.do(item, 'proposeToDirector')
        self.do(item, 'proposeToFinance')
        self.assertEqual(item.getTakenOverBy(), 'pmFinController')

    def test_ListArchivingRefsRestrictToGroups(self):
        """MeetingItem.archivingRefs vocabulary, available values may be restricted
           depending on current user groups."""
        self.changeUser('siteadmin')
        cfg = self.meetingConfig
        cfg.setArchivingRefs((
            {'active': '1',
             'restrict_to_groups': [self.vendors_uid],
             'row_id': '1',
             'code': '1',
             'label': "1"},
            {'active': '1',
             'restrict_to_groups': [],
             'row_id': '2',
             'code': '2',
             'label': '2'},))
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem')
        self.assertEqual(self.request.getURL(), 'http://nohost')
        self.assertFalse('1' in item.listArchivingRefs())
        self.assertTrue('2' in item.listArchivingRefs())
        # view is optimized to only return stored value
        self.request['URL'] = item.absolute_url() + ('/meetingitem_view')
        self.assertFalse(item.listArchivingRefs())
        item.setArchivingRef('1')
        self.assertEqual(item.listArchivingRefs().keys(), ['1'])
        item.setArchivingRef('2')
        self.assertEqual(item.listArchivingRefs().keys(), ['2'])

    def test_TreasuryCopyGroup(self):
        """TREASURY_GROUP_ID 'incopy' suffix is set in copy of items
           having finances advice when at least validated."""
        cfg = self.meetingConfig
        cfg.setUseCopies(True)
        self.changeUser('admin')
        self._createFinanceGroups()
        _configureCollegeCustomAdvisers(self.portal)
        self.changeUser('pmManager')
        item = self.create('MeetingItem')
        # bypass finances advice
        item.setEmergency('emergency_asked')
        # ask finance advice
        financial_group_uids = self.tool.financialGroupUids()
        item.setFinanceAdvice(financial_group_uids[0])
        item._update_after_edit()
        self.assertTrue(financial_group_uids[0] in item.adviceIndex)
        # no copyGroups
        self.assertEqual(item.getAllCopyGroups(), ())
        self.validateItem(item)
        self.assertEqual(item.getAllCopyGroups(),
                         ('auto__%s_incopy' % org_id_to_uid(TREASURY_GROUP_ID), ))

    def test_Index_category_id(self):
        """ """
        cfg = self.meetingConfig
        cfg.setUseGroupsAsCategories(False)
        self.changeUser('pmCreator1')
        item = self.create('MeetingItem', category='research')
        indexable_wrapper = IndexableObjectWrapper(item, self.catalog)
        self.assertEqual(indexable_wrapper.category_id, 'research')
