name "egonomist"
run_list(
    "recipe[build-essential]",
	"recipe[python]",
	"recipe[opencv]",
	"recipe[erlang]",
	"recipe[rabbitmq]"
)
default_attributes()
