

class BaseStatus:

    status_text = ''

    def get_status(self):
        """
        Return a string status for the given status event,
        used to display in an app row.
        """
        raise NotImplementedError


class BatterPercentStatus(BaseStatus):

    status_text = 'Battery Persentage'

    def get_status(self):
        return '100%'