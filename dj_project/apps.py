from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
    MENU_OPEN_FIRST_CHILD=True
    menu = (
        ParentItem('Authentication Users & Groups', children=[
            ChildItem("Users", 'auth.user'),
            ChildItem('User groups', 'auth.group'),
        ], icon='fa fa-users'),

        ParentItem('User Details', children=[
            ChildItem(model='login_signup.appuser'),
            ChildItem(model='login_signup.usercrossfollower'),
            ChildItem(model='login_signup.userxblockeduser'),
        ], icon='fa fa-address-card'),

        ParentItem('Audio & Sticker', children=[
            ChildItem(model='coins_and_gifts.audiocategories'),
            ChildItem(model='coins_and_gifts.audiomanagement'),
            ChildItem(model='coins_and_gifts.stickermanagement'),
        ], icon='fa fa-music'),

        ParentItem('Gift', children=[
            ChildItem(model='coins_and_gifts.giftmanagement'),
            ChildItem(model='coins_and_gifts.gifttransactions'),
        ], icon='fa fa-gift'),

        ParentItem('Coins & Refer', children=[
            ChildItem(model='coins_and_gifts.coinmanagement'),
            ChildItem(model='coins_and_gifts.cointransactions'),
            ChildItem(model='coins_and_gifts.coinredeemtransactions'),
            ChildItem(model='coins_and_gifts.userrefer'),
        ], icon='fa fa-inr'),

        ParentItem('Effects & Filters', children=[
            ChildItem(model='effects_and_filters.effectsandfilters'),
        ], icon='fa fa-magic'),

        ParentItem('Star & Channels', children=[
            ChildItem(model='star_and_channels.starmanagement'),
            ChildItem(model='star_and_channels.stars'),
            ChildItem(model='star_and_channels.channellist'),
            ChildItem(model='star_and_channels.channelxuser'),
        ], icon='fa fa-star'),

        ParentItem('Video', children=[
            ChildItem(model='video.mediatable'),
            ChildItem(model='video.mediaxlikexviews'),
            ChildItem(model='video.comments'),
            ChildItem(model='video.commentlikes'),
        ], icon='fa fa-youtube-play'),

        ParentItem('Reported User & Content', children=[
            ChildItem(model='reported.userreporthistory'),
            ChildItem(model='reported.reporttypes'),
            ChildItem(model='reported.postreporthistory'),
        ], icon='fa fa-thumbs-down'),

        ParentItem('Mails & Notifications', children=[
            ChildItem(model='notification_and_mails.notificationtemplates'),
            ChildItem(model='notification_and_mails.notificationhistory'),
            ChildItem(model='notification_and_mails.emailtemplates'),
            ChildItem(model='notification_and_mails.emailhistory'),
        ], icon='fa fa-envelope'),

        ParentItem('Policies & Guidlines', children=[
            ChildItem(model='notification_and_mails.termandconditionandpolicy'),
            ChildItem("How to earn coins", 'coins_and_gifts.headingandpoints'),
            ChildItem(model='video.tutorialvideo'),
        ], icon='fa fa-file-text'),
    )
