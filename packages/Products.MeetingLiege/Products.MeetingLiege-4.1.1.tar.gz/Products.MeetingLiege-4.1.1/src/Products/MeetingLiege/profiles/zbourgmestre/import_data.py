# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.MeetingLiege.config import BOURGMESTRE_GROUP_ID
from Products.MeetingLiege.config import GENERAL_MANAGER_GROUP_ID
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import UserDescriptor


today = DateTime().strftime('%Y/%m/%d')

# File types -------------------------------------------------------------------
annexe = ItemAnnexTypeDescriptor('annexe', 'Annexe', u'attach.png')
annexeDecision = ItemAnnexTypeDescriptor('annexeDecision', 'Annexe à la décision',
                                         u'attach.png', relatedTo='item_decision')
annexeAvis = AnnexTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                 u'attach.png', relatedTo='advice')
annexeSeance = AnnexTypeDescriptor('annexe', 'Annexe',
                                   u'attach.png', relatedTo='meeting')

# No Categories -------------------------------------------------------------------
categories = []

# No Pod templates ----------------------------------------------------------------

bourgmestreTemplates = []

# Users and groups -------------------------------------------------------------
generalManager = UserDescriptor(
    'generalManager', [], email="general_manager@plonemeeting.org", fullname='M. GeneralManager')
bourgmestreManager = UserDescriptor(
    'bourgmestreManager', [], email="bourgmestre_manager@plonemeeting.org",
    fullname='M. Bourgmestre Manager')
bourgmestreReviewer = UserDescriptor(
    'bourgmestreReviewer', [], email="bourgmestre_reviewer@plonemeeting.org",
    fullname='M. Bourgmestre Reviewer')
general_manager_group = OrgDescriptor(GENERAL_MANAGER_GROUP_ID, u'General Managers', u'GMs')
general_manager_group.reviewers.append(generalManager)
bourgmestre_group = OrgDescriptor(BOURGMESTRE_GROUP_ID, u'Bourgmestre', u'BG')
bourgmestre_group.creators.append(bourgmestreManager)
bourgmestre_group.reviewers.append(bourgmestreReviewer)
orgs = [general_manager_group, bourgmestre_group]

# Meeting configurations -------------------------------------------------------
# Bourgmestre
bourgmestreMeeting = MeetingConfigDescriptor(
    'meeting-config-bourgmestre', 'Bourgmestre',
    'Bourgmestre')
bourgmestreMeeting.meetingManagers = ['pmManager']
bourgmestreMeeting.assembly = 'A compléter...'
bourgmestreMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Vraiment Présent',
     'function': u'Le Directeur général',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Charles Exemple',
     'function': u'Le Bourgmestre',
     'date_from': '',
     'date_to': '',
     },
]
bourgmestreMeeting.places = ''
bourgmestreMeeting.categories = categories
bourgmestreMeeting.shortName = 'Bourgmestre'
bourgmestreMeeting.annexTypes = [annexe, annexeDecision, annexeAvis, annexeSeance]
bourgmestreMeeting.itemAnnexConfidentialVisibleFor = (
    'configgroup_budgetimpacteditors',
    'reader_advices',
    'reader_copy_groups',
    'reader_groupsincharge',
    'suffix_proposing_group_prereviewers',
    'suffix_proposing_group_internalreviewers',
    'suffix_proposing_group_observers',
    'suffix_proposing_group_reviewers',
    'suffix_proposing_group_creators',
    'suffix_proposing_group_administrativereviewers')
bourgmestreMeeting.usedItemAttributes = ['observations', ]
bourgmestreMeeting.usedMeetingAttributes = ['signatures', 'assembly', 'observations', ]
bourgmestreMeeting.recordMeetingHistoryStates = []
bourgmestreMeeting.xhtmlTransformFields = ()
bourgmestreMeeting.xhtmlTransformTypes = ()
bourgmestreMeeting.hideCssClassesTo = ('power_observers', 'restricted_power_observers')
bourgmestreMeeting.itemWorkflow = 'meetingitembourgmestre_workflow'
bourgmestreMeeting.meetingWorkflow = 'meetingbourgmestre_workflow'
bourgmestreMeeting.itemConditionsInterface = \
    'Products.MeetingLiege.interfaces.IMeetingItemBourgmestreWorkflowConditions'
bourgmestreMeeting.itemActionsInterface = \
    'Products.MeetingLiege.interfaces.IMeetingItemBourgmestreWorkflowActions'
bourgmestreMeeting.meetingConditionsInterface = \
    'Products.MeetingLiege.interfaces.IMeetingBourgmestreWorkflowConditions'
bourgmestreMeeting.meetingActionsInterface = \
    'Products.MeetingLiege.interfaces.IMeetingBourgmestreWorkflowActions'
bourgmestreMeeting.transitionsToConfirm = ['MeetingItem.delay', ]
bourgmestreMeeting.meetingTopicStates = ('created', )
bourgmestreMeeting.decisionTopicStates = ('closed', )
bourgmestreMeeting.enforceAdviceMandatoriness = False
bourgmestreMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                                 'reverse': '0'}, )
bourgmestreMeeting.recordItemHistoryStates = []
bourgmestreMeeting.maxShownMeetings = 5
bourgmestreMeeting.maxDaysDecisions = 60
bourgmestreMeeting.meetingAppDefaultView = 'searchmyitems'
bourgmestreMeeting.useAdvices = True
bourgmestreMeeting.itemAdviceStates = ('validated',)
bourgmestreMeeting.itemAdviceEditStates = ('validated',)
bourgmestreMeeting.keepAccessToItemWhenAdviceIsGiven = True
bourgmestreMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
bourgmestreMeeting.enableAdviceInvalidation = False
bourgmestreMeeting.itemAdviceInvalidateStates = []
bourgmestreMeeting.customAdvisers = []
bourgmestreMeeting.powerObservers = (
    {'item_access_on': '',
     'item_states': ['accepted',
                     'accepted_but_modified',
                     'delayed',
                     'itemfrozen',
                     'refused',
                     'validated'],
     'label': 'Super observateurs',
     'meeting_access_on': '',
     'meeting_states': ('created', ),
     'row_id': 'powerobservers'},
    {'item_access_on': '',
     'item_states': ['accepted',
                     'accepted_but_modified',
                     'delayed',
                     'itemfrozen',
                     'refused',
                     'returned_to_proposing_group',
                     'marked_not_applicable',
                     'validated'],
     'label': 'Super observateurs restreints',
     'meeting_access_on': '',
     'meeting_states': (),
     'row_id': 'restrictedpowerobservers'},
    # police administrative
    {'item_access_on': 'python:item.getProposingGroup() in [pm_utils.org_id_to_uid("bpa-arraata-c-s")]',
     'item_states': ['accepted',
                     'accepted_but_modified'],
     'label': 'Super observateurs Police administrative',
     'meeting_access_on': '',
     'meeting_states': (),
     'row_id': 'adminpolicepowerobservers'},
    # Juristes Urbanisme
    {'item_access_on': 'python:item.getProposingGroup() in ' \
        '[pm_utils.org_id_to_uid("urba-gestion-administrative"), ' \
        'pm_utils.org_id_to_uid("urba-service-de-lurbanisme"), ' \
        'pm_utils.org_id_to_uid("bpa-permis-environnement")]',
     'item_states': ['accepted',
                     'accepted_but_modified'],
     'label': 'Super observateurs Juristes Urbanisme',
     'meeting_access_on': '',
     'meeting_states': (),
     'row_id': 'jururbapowerobservers'},
    # Juristes Sécurité publique
    {'item_access_on': 'python:item.getProposingGroup() in [pm_utils.org_id_to_uid("bpa-sa-c-curita-c-publique")]',
     'item_states': ['accepted',
                     'accepted_but_modified'],
     'label': 'Super observateurs Juristes Sécurité publique',
     'meeting_access_on': '',
     'meeting_states': (),
     'row_id': 'jursecpubpowerobservers'},
)
bourgmestreMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'marked_not_applicable']
bourgmestreMeeting.workflowAdaptations = []
bourgmestreMeeting.transitionsForPresentingAnItem = (
    u'proposeToAdministrativeReviewer', u'proposeToInternalReviewer', u'proposeToDirector',
    u'proposeToGeneralManager', 'proposeToCabinetManager', u'proposeToCabinetReviewer', u'validate', u'present')
bourgmestreMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le bourgmestre décide de reporter le point.</p>"},))
bourgmestreMeeting.onMeetingTransitionItemActionToExecute = (
    {'meeting_transition': 'close',
     'item_action': 'accept',
     'tal_expression': ''}, )
bourgmestreMeeting.meetingPowerObserversStates = ('closed', 'created', )
bourgmestreMeeting.powerAdvisersGroups = ()
bourgmestreMeeting.itemBudgetInfosStates = ()
bourgmestreMeeting.enableLabels = True
bourgmestreMeeting.useCopies = True
bourgmestreMeeting.hideItemHistoryCommentsToUsersOutsideProposingGroup = True
bourgmestreMeeting.selectableCopyGroups = []
bourgmestreMeeting.podTemplates = bourgmestreTemplates
bourgmestreMeeting.meetingConfigsToCloneTo = []
bourgmestreMeeting.recurringItems = []
bourgmestreMeeting.itemTemplates = []

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(bourgmestreMeeting, ),
                                 orgs=orgs)
data.forceAddUsersAndGroups = True
# ------------------------------------------------------------------------------
