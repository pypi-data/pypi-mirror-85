"""Recipe module of official Python client for Driverless AI."""

import re
from typing import Any
from typing import List

from driverlessai import _core
from driverlessai import _utils


class ModelRecipe:
    """Interact with a model recipe on the Driverless AI server.

    Attributes:
        name (str): recipe name
        is_custom (bool): ``True`` if the recipe is custom

    Examples::

        # Get list of all custom models
        [m for m in dai.recipes.models.list() if m.is_custom]

        # Get list of names of all models
        [m.name for m in dai.recipes.models.list()]
    """

    def __init__(self, info: Any) -> None:
        self.name = info.name
        self.is_custom = info.is_custom

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self!s}"

    def __str__(self) -> str:
        return self.name


class ModelRecipes:
    """Interact with model recipes on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> List["ModelRecipe"]:
        """Return list of model recipe objects.

        Examples::

            dai.recipes.models.list()
        """
        return [ModelRecipe(m) for m in self._client._backend.list_model_estimators()]


class RecipeJob(_utils.ServerJob):
    """Monitor creation of a custom recipe on the Driverless AI server.

    Attributes:
        key: unique ID of job
    """

    def __init__(self, client: "_core.Client", key: str) -> None:
        super().__init__(client=client, key=key)

    def _update(self) -> None:
        self._info: Any = self._client._backend.get_custom_recipe_job(self.key)

    def result(self, silent: bool = False) -> "RecipeJob":
        """Wait for job to complete, then return self.

        Args:
            silent: if True, don't display status updates
        """
        self._wait(silent)
        return self

    def status(self, verbose: int = 0) -> str:
        """Return job status string.

        Args:
            verbose:
                - 0: short description
                - 1: short description with progress percentage
                - 2: detailed description with progress percentage
        """
        status = self._status()
        if verbose == 1:
            return f"{status.message} {self._info.progress:.2%}"
        if verbose == 2:
            if status == _utils.JobStatus.FAILED:
                message = " - " + self._info.error
            else:
                message = ""  # message for recipes is partially nonsense atm
            return f"{status.message} {self._info.progress:.2%}{message}"
        return status.message


class Recipes:
    """Create and interact with recipes on the Driverless AI server.

    Attributes:
        models (ModelRecipes): see model recipes
        scorers (ScorerRecipes): see scorer recipes
        transformers (TransformerRecipes): see transformer recipes
    """

    def __init__(self, client: "_core.Client") -> None:
        self._client = client
        self.models = ModelRecipes(client)
        self.scorers = ScorerRecipes(client)
        self.transformers = TransformerRecipes(client)

    def create(self, recipe: str) -> None:
        """Create a recipe on the Driverless AI server.

        Args:
            recipe: path to recipe or url for recipe

        Examples::

            dai.recipes.create(
                recipe='https://github.com/h2oai/driverlessai-recipes/blob/master/scorers/regression/explained_variance.py'
            )
        """
        self.create_async(recipe).result()
        return

    def create_async(self, recipe: str) -> RecipeJob:
        """Launch creation of a recipe on the Driverless AI server.

        Args:
            recipe: path to recipe or url for recipe

        Examples::

            dai.recipes.create_async(
                recipe='https://github.com/h2oai/driverlessai-recipes/blob/master/scorers/regression/explained_variance.py'
            )
        """
        if re.match("^http[s]?://", recipe):
            key = self._client._backend.create_custom_recipe_from_url(recipe)
        else:
            key = self._client._backend._perform_recipe_upload(recipe)
        return RecipeJob(self._client, key)


class ScorerRecipe:
    """Interact with a scorer recipe on the Driverless AI server.

    Attributes:
        name (str): recipe name
        description (str): recipe description
        for_binomial (bool): ``True`` if scorer works for binomial models
        for_multiclass (bool): ``True`` if scorer works for multiclass models
        for_regression (bool): ``True`` if scorer works for regression models
        is_custom (bool): ``True`` if the recipe is custom

    Examples::

        # Retrieve a list of binomial scorers
        [s for s in dai.recipes.scorers.list() if s.for_binomial]

        # Retrieve a list of multiclass scorers
        [s for s in dai.recipes.scorers.list() if s.for_multiclass]

        # Retrieve a list of regression scorers
        [s for s in dai.recipes.scorers.list() if s.for_regression]

        # Get list of all custom scorers
        [s for s in dai.recipes.scorers.list() if s.is_custom]

        # Get list of names of all scorers
        [s.name for s in dai.recipes.scorers.list()]

        # Get list of descriptions for all scorers
        [s.description for s in dai.recipes.scorers.list()]
    """

    def __init__(self, info: Any) -> None:
        self.name = info.name
        self.description = info.description
        self.for_binomial = info.for_binomial
        self.for_multiclass = info.for_multiclass
        self.for_regression = info.for_regression
        self.is_custom = info.is_custom

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self!s}"

    def __str__(self) -> str:
        return self.name


class ScorerRecipes:
    """Interact with scorer recipes on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> List["ScorerRecipe"]:
        """Return list of scorer recipe objects.

        Examples::

            dai.recipes.scorers.list()
        """
        return [ScorerRecipe(s) for s in self._client._backend.list_scorers()]


class TransformerRecipe:
    """Interact with a transformer recipe on the Driverless AI server.

    Attributes:
        name (str): recipe name
        is_custom (bool): ``True`` if the recipe is custom

    Examples::

        # Get list of all custom transformers
        [m for m in dai.recipes.transformers.list() if m.is_custom]

        # Get list of names of all transformers
        [m.name for m in dai.recipes.transformers.list()]
    """

    def __init__(self, info: Any) -> None:
        self.name = info.name
        self.is_custom = info.is_custom

    def __repr__(self) -> str:
        return f"<class '{self.__class__.__name__}'> {self!s}"

    def __str__(self) -> str:
        return self.name


class TransformerRecipes:
    """Interact with transformer recipes on the Driverless AI server."""

    def __init__(self, client: "_core.Client") -> None:
        self._client = client

    def list(self) -> List["TransformerRecipe"]:
        """Return list of transformer recipe objects.

        Examples::

            dai.recipes.transformers.list()
        """
        return [TransformerRecipe(t) for t in self._client._backend.list_transformers()]
