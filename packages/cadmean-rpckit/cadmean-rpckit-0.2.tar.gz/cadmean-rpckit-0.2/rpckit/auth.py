class JwtAuthorizationTicket:

    def __init__(self, accessToken, refreshToken):
        self.access_token = accessToken
        self.refresh_token = refreshToken


class JwtAuthorizationTicketHolder:

    def set_ticket(self, ticket):
        pass

    def get_ticket(self):
        pass


class TransientJwtAuthorizationTicketHolder(JwtAuthorizationTicketHolder):

    def __init__(self):
        self.ticket = None

    def set_ticket(self, ticket):
        self.ticket = ticket

    def get_ticket(self):
        return self.ticket
