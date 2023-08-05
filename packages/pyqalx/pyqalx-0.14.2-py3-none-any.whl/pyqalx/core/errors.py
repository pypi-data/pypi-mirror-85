"""
pyqalx.core.errors defines QalxError exception and a load of children.

If pyqalx is going raise an error you know about then use one of these or
create a new one.
"""


class QalxError(Exception):
    """Base qalx error. Take responsibility!"""


class QalxAuthError(QalxError):
    """
    qalx did not find a way to authenticate or the authentication didn't work
    """


class QalxNoGUIDError(QalxError):
    """A QalxEntity without a guid is like a dog without a bone."""


class QalxNoInfoError(QalxError):
    """A QalxEntity without info is like a dog without a bone."""


class QalxReturnedMultipleError(QalxError):
    """There should only be one thing. But qalx sent more than one."""


class QalxConfigProfileNotFound(QalxError):
    """The profile wasn't in the file or the file wasn't properly formed."""


class QalxConfigFileNotFound(QalxError):
    """
    There should be a file in the users `home` directory (either a .bots or
    .qalx)
    """


class QalxQueueError(QalxError):
    """There wasn't the correct information to connect to the remote queue."""


class QalxBotInitialisationFailed(QalxError):
    """The bot initialisation function returned something falsey."""


class QalxEntityTypeNotFound(QalxError):
    """We couldn't find the entity type you were looking for."""


class QalxEntityNotFound(QalxError):
    """We couldn't find the entity you were looking for."""


class QalxMultipleEntityReturned(QalxError):
    """We found more than one entity, but you just wanted the one hey?"""


class QalxConfigError(QalxError):
    """Something about an attempted load of config didn't work"""


class QalxAPIResponseError(QalxError):
    """There was a problem with some kind of API request."""


class QalxEntityUnchanged(QalxError):
    """
    Saved something which hadn't actually been changed when we thought it had.
    """


class QalxInvalidSession(QalxError):
    """
    The qalx_session argument passed to an adapter isn't a valid QalxSession
    instance
    """


class QalxNoEntity(QalxError):
    """
    A user tried to access the `entity` attribute on QalxAdapter when they
    hadn't set an entity
    """


class QalxIncorrectEntityType(QalxError):
    """
    The entity on the QalxAdapter is of a different type to the type of adapter
    """


class QalxFileError(QalxError):
    """
    There is something wrong with the file details passed to the QalxAdapter
    """


class QalxAlreadyRegistered(QalxError):
    """The entity is already registered with the session"""


class QalxCannotUnregister(QalxError):
    """The entity cannot be unregistered"""


class QalxRegistrationClassNotFound(QalxError):
    """The registration class for registering a custom class was not found"""


class QalxInvalidBlueprintError(QalxError):
    """The blueprint is not valid."""


class QalxInvalidTagError(QalxError):
    """The user does not have access to write to the specific tags"""


class QalxStepFunctionNotDefined(QalxError):
    """A specific Bot step function has not been defined by the user"""


class QalxFactoryError(QalxError):
    """Generic error with a Qalx factory"""


class QalxFactoryValidationError(QalxFactoryError):
    """Error when validating a factory"""


class QalxFactoryPackError(QalxFactoryError):
    """Error when packing a factory"""


class QalxFactoryBuildError(QalxFactoryError):
    """Error when building a factory"""


class QalxFactoryDemolishError(QalxFactoryError):
    """Error when demolishing a factory"""
