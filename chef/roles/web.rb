name "egonomist"
run_list(
    "recipe[apt]",
    "recipe[build-essential]",
	"recipe[python]",
	"recipe[opencv]",
	"recipe[erlang]",
	"recipe[rabbitmq]",
	"recipe[egonomist]"
)
default_attributes()
