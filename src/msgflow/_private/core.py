from abc import ABC, abstractmethod
from typing import Any, Dict

class Core:
    """ 
    Core is a set of methods that are common among some classes in msgFlow.
    
    This class provides basic functionality for state management, allowing instances
    to be serialized and deserialized. It is intended to be inherited by other classes
    that require these common features.
    """
    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)


class BaseClient(ABC, Core):
    """
    BaseClient is an abstract base class that defines the interface and common behavior
    for client classes in the msgFlow system.

    This class inherits from `Core` to leverage its state management capabilities and
    extends it with additional functionality specific to clients. It requires subclasses
    to implement certain methods, ensuring a consistent interface across different client
    implementations.

    Subclasses must implement the `_initialize_client` and `__call__` methods, which are
    essential for client initialization and operation, respectively. Additionally, this
    class provides methods for serialization and deserialization, allowing client instances
    to be easily saved and restored.

    Attributes:
        to_remove ([optional[list[str]]): A list of attribute keys to be removed during serialization.
        msgflow_type (str): A string identifying the type of the client in the msgFlow system.
        provider (optional[str]): The provider associated with the client, if applicable.
        instance_type (optional[callable]): A method or callable that returns additional
            instance-specific data to be included during serialization.
    """

    @abstractmethod
    def __call__(self):
        """
        Execute the client's main functionality. This method must be implemented by subclasses.

        This method defines the primary behavior of the client and is called when the instance
        is invoked as a function.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    def serialize(self) -> Dict[str, Any]:
        """
        Serialize the client instance into a dictionary.

        This method prepares the client's state for serialization by removing unnecessary
        attributes and including additional metadata such as the client type and provider.

        Returns:
            Dict[str, Any]: A dictionary containing the serialized state of the client,
            including metadata and the client's internal state.
        """
        state =  self.__getstate__()
        if hasattr(self, "to_remove"):
            for key in self.to_remove:
                state.pop(key, None)
        data = {"msgflow_type": self.msgflow_type}
        if hasattr(self, "provider"):
            data["provider"] = self.provider
        if hasattr(self, "instance_type"):
            instance_type = self.instance_type()
            data.update(instance_type)
        data["state"] = state
        return data     

    @classmethod
    def from_serialized(cls, state: Dict[str, Any]):
        """
        Deserialize a client instance from a dictionary.

        This method creates a new instance of the client and restores its state from the
        provided dictionary. It also ensures that the client is properly initialized
        after deserialization.

        Args:
            state (Dict[str, Any]): A dictionary containing the serialized state of the client.

        Returns:
            BaseClient: A new instance of the client with its state restored.
        """
        instance = cls()
        instance.__setstate__(state)
        instance._initialize_client()
        return instance