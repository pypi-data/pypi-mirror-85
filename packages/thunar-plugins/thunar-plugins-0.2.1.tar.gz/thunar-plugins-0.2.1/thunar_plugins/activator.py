import thunar_plugins

locals().update(
    {
        x.__name__: x
        for x in thunar_plugins.get_available_plugins(
            also_blacklisted=False
        ).values()
    }
)
