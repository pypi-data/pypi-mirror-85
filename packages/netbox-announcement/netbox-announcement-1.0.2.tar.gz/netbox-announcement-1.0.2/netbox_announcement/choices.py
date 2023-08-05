from utilities.choices import ChoiceSet

# 
# Announcement
# 


class AnnouncementTypeChoices(ChoiceSet):
    TYPE_COMPANY = 'company'
    TYPE_NETWORK = 'network'
    TYPE_SERVER = 'server'
    
    CHOICES = (
        (TYPE_COMPANY, 'Company'),
        (TYPE_NETWORK, 'Network'),
        (TYPE_SERVER, 'Server')
    )

class AnnouncementServerTypeChoices(ChoiceSet):
    SERVER_TYPE_DEVICE = 'device'
    SERVER_TYPE_VM = 'vm'
    
    CHOICES = (
        (SERVER_TYPE_DEVICE, 'Device'),
        (SERVER_TYPE_VM, 'VM'),
    )
      
    
class AnnouncementMailedChoices(ChoiceSet):
    MAILED_YES = True
    MAILED_NO = False

    CHOICES = (
        (MAILED_YES, 'true'),
        (MAILED_NO, 'false')
    )




