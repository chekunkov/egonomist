name "egonomist"
run_list(
    "recipe[build-essential]",
	"recipe[python]",
	"recipe[opencv]"
)
default_attributes()
