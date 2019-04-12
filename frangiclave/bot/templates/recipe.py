from frangiclave.bot.templates.base import URL_FORMAT, make_section, DIVIDER
from frangiclave.compendium.recipe import Recipe


def make_recipe(recipe: Recipe):
    return [
        make_section('*Recipe: {}*'.format(URL_FORMAT.format('recipe', recipe.recipe_id))),
        DIVIDER,
        make_section(
            f'*_Label:_* {recipe.label}\n'
            f'*_Start Description:_* {recipe.start_description}\n'
            f'*_Description:_* {recipe.description}'
        )
    ]
