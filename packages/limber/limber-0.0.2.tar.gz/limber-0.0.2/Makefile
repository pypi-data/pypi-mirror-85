
test-cli:
	python limber/cli/cli.py --gcp-keyfile "test key file" --gcp-project "test project"
test:
	python limber
deploy:
	terraform apply
deploy-to-pypi:
	python -m twine upload --config-file .pypirc dist/*