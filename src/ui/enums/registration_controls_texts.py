from enum import Enum


class RegistrationControlsTexts(Enum):
    COUNTRY_EMPTY = 'Please specify your country / region of residence'
    EMAIL_EMPTY = 'Please enter your email address'
    EMAIL_VALIDATION = 'Enter a valid email address'
    PASSWORD_LENGTH = 'Use from 8 to 15 characters'
    PASSWORD_LETTERS_CASE = 'Use both uppercase and lowercase letters'
    PASSWORD_COMPLEXITY = 'Use a combination of numbers and English letters'
    INVALID_PARTNER_CODE = ('Partner code is invalid. Click '
                            '“Continue” to register without a partner code.')
    NOT_US_RESIDENT = ('For regulatory reasons, we do not accept citizens '
                       'or residents of the United States')
